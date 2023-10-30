from datetime import timedelta, datetime
from typing import Optional, Any, Dict
from uuid import uuid4

from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _
from django.conf import settings as dj_settings

from jwtberry import settings
from jwtberry.exceptions import TokenError
from jwtberry.helper import aware_utcnow, datetime_from_epoch, datetime_to_epoch

from jwtberry.blackberry.models import JwtBerry, BlackBerry


class Token:

    token_type: str
    lifetime: timedelta
    _token_core: Optional["TokenCore"] = None

    def __init__(
        self,
        token: Optional["Token"] = None,
        verify: bool = True,
    ):
        self.token = token
        self.current_time = aware_utcnow()

        if token is None:
            self.payload = {
                settings.TOKEN_TYPE_CLAIM: self.token_type,
            }
            self.set_exp(from_time=self.current_time, lifetime=self.lifetime)
            self.set_iat(at_time=self.current_time)
            self.set_jti()
        else:
            try:
                self.payload = self.token_core.decode(token, verify=verify)
            except Exception:
                raise ValueError("Token is invalid")

            if verify:
                self.verify()

    def __getitem__(self, key: str):
        return self.payload[key]

    def __setitem__(self, key: str, value: Any):
        self.payload[key] = value

    def __delitem__(self, key: str):
        del self.payload[key]

    def __contains__(self, key: str):
        return key in self.payload

    def __str__(self):
        return self.token_core.encode(self.payload)

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.payload}>"

    def get(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        return self.payload.get(key, default)

    def verify(self):
        self.verify_exp()

        if settings.TOKEN_TYPE_CLAIM:
            self.verify_type()

        if settings.JTI_CLAIM and settings.JTI_CLAIM not in self.payload:
            raise ValueError("Token has no jti claim")

    def verify_type(self):
        if self.get(settings.TOKEN_TYPE_CLAIM) != self.token_type:
            raise ValueError("Token type is invalid")

    def verify_exp(self, current_time: Optional[datetime] = None):
        current_time = current_time or self.current_time

        if self.get("exp") is None:
            raise ValueError("Token has no expiration")

        claim_time = datetime_from_epoch(self.get("exp"))
        lee_way = self.token_core.get_leeway()
        if claim_time < current_time - lee_way:
            raise ValueError("Token is expired")

    @property
    def token_core(self) -> "TokenCore":
        if self._token_core is None:
            self._token_core = import_string('jwtberry.core.token_core')
        return self._token_core

    def set_exp(
        self,
        from_time: Optional[datetime] = None,
        lifetime: Optional[timedelta] = None,
    ):
        from_time = from_time or self.current_time
        lifetime = lifetime or self.lifetime

        self["exp"] = datetime_to_epoch(from_time + lifetime)

    def set_iat(self, at_time: Optional[datetime] = None):
        at_time = at_time or self.current_time
        self["iat"] = datetime_to_epoch(at_time)

    def set_jti(self):
        self[settings.JTI_CLAIM] = uuid4().hex

    @classmethod
    def create(cls, user) -> "Token":
        token = cls()

        user_id = getattr(user, settings.USER_ID_FIELD)
        if not isinstance(user_id, int):
            user_id = str(user_id)

        token[settings.USER_ID_CLAIM] = user_id
        return token


class BlacklistMixin:
    ...
    payload: Dict[str, Any]

    if "jwtberry.blackberry" in dj_settings.INSTALLED_APPS:

        def verify(self, *args, **kwargs) -> None:
            self.check_blacklist()

            super().verify(*args, **kwargs)  # type: ignore

        def check_blacklist(self) -> None:
            """
            Checks if this token is present in the token blacklist.  Raises
            `TokenError` if so.
            """
            jti = self.payload[settings.JTI_CLAIM]

            if BlackBerry.objects.filter(token__jti=jti).exists():
                raise TokenError(_("Token is blacklisted"))

        def blacklist(self) -> BlackBerry:
            """
            Ensures this token is included in the outstanding token list and
            adds it to the blacklist.
            """
            jti = self.payload[settings.JTI_CLAIM]
            exp = self.payload["exp"]

            # Ensure outstanding token exists with given jti
            token, _ = JwtBerry.objects.get_or_create(
                jti=jti,
                defaults={
                    "token": str(self),
                    "expires_at": datetime_from_epoch(exp),
                },
            )

            return BlackBerry.objects.get_or_create(token=token)

        @classmethod
        def create(cls, user) -> Token:
            """
            Adds this token to the outstanding token list.
            """
            token = super().create(user)  # type: ignore

            jti = token[settings.JTI_CLAIM]
            exp = token["exp"]

            JwtBerry.objects.create(
                user=user,
                jti=jti,
                refresh_token=str(token),
                created_at=token.current_time,
                expires_at=datetime_from_epoch(exp),
            )

            return token


class AccessToken(Token):
    token_type = "access"
    lifetime = settings.ACCESS_TOKEN_LIFETIME


class RefreshToken(BlacklistMixin, Token):
    token_type = "refresh"
    lifetime = settings.REFRESH_TOKEN_LIFETIME
    no_copy_claims = (
        settings.TOKEN_TYPE_CLAIM,
        "exp",
        settings.JTI_CLAIM,
        "jti"
    )
    access_token_class = AccessToken

    @property
    def access_token(self) -> AccessToken:
        access = self.access_token_class()

        access.set_exp(from_time=self.current_time)

        for claim, value in self.payload.items():
            if claim not in self.no_copy_claims:
                access[claim] = value

        return access

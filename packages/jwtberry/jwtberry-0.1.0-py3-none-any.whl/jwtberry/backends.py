from typing import Optional, Set, TypeVar

from asgiref.sync import sync_to_async
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from jwtberry import settings
from jwtberry.exceptions import InvalidToken, JwtAuthFailed
from jwtberry.models import JwtUser
from jwtberry.tokens import Token


User = TypeVar("User", AbstractBaseUser, JwtUser)


class JwtAuthBackend:
    user_model = get_user_model()

    AUTH_HEADER_TYPE_BYTES: Set[bytes] = {
        h.encode('utf-8') for h in settings.AUTH_HEADER_TYPES
    }

    def authenticate(self, request=None, **kwargs):
        if request is None or hasattr(request, "__jwtberry__"):
            return None

        # if hasattr(request, "user") and request.user.is_authenticated:
        #     return request.user

        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token)

    async def authenticate_async(self, request=None, **kwargs):
        return await sync_to_async(self.authenticate)(request, **kwargs)

    @staticmethod
    def get_header(request) -> Optional[bytes]:
        header = request.headers.get(settings.AUTH_HEADER_NAME)
        if isinstance(header, str):
            header = header.encode("utf-8")
        return header

    def get_raw_token(self, header: bytes) -> Optional[bytes]:
        parts = header.split()
        if len(parts) == 0:
            return None

        if parts[0] not in self.AUTH_HEADER_TYPE_BYTES:
            return None

        if len(parts) != 2:
            raise JwtAuthFailed({
                "detail": _("Invalid Authorization header. Credentials string should not contain spaces."),
                "code": "invalid_authorization_header",
            })

        return parts[1]

    def get_validated_token(self, raw_token: bytes) -> Token:
        messages = []
        for TokenClass in (import_string(tm) for tm in settings.AUTH_TOKEN_CLASSES):
            try:
                return TokenClass(raw_token, verify=False)
            except ValueError as e:
                messages.append({
                    "token_class": TokenClass.__name__,
                    "token_type": TokenClass.token_type,
                    "message": str(e),
                })

        raise InvalidToken({
            "detail": _("Token is invalid or expired"),
            "messages": messages,
        })

    def get_user(self, validated_token: Token):
        if not isinstance(validated_token, Token):
            return None

        try:
            user_id = validated_token[settings.USER_ID_CLAIM]
        except KeyError:
            raise InvalidToken({
                "detail": _("Token contained no recognizable user identification"),
                "code": "invalid_user_id_claim",
            })

        try:
            user = self.user_model.objects.get(**{settings.USER_ID_FIELD: user_id})
        except self.user_model.DoesNotExist:
            raise InvalidToken({
                "detail": _("User not found"),
                "code": "user_not_found",
            })

        if not user.is_active:
            raise InvalidToken({
                "detail": _("User is inactive"),
                "code": "user_inactive",
            })
        return user


def default_user_authentication_rule(user: User) -> bool:
    return user is not None and user.is_active

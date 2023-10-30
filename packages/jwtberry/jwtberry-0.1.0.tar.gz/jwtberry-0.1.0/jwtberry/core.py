import json
from datetime import timedelta
from typing import Optional, Union, Type, Any, Dict

from django.utils.translation import gettext_lazy as _

import jwt
from jwt import (
    PyJWKClient,
    PyJWKClientError,
    InvalidTokenError,
    InvalidAlgorithmError,
    algorithms,
)

from jwtberry import settings
from jwtberry.exceptions import TokenCoreError
from jwtberry.helper import format_lazy
from jwtberry.tokens import Token


class TokenCore:

    def __init__(
            self,
            algorithm: settings.Algorithm,
            signing_key: Optional[str] = None,
            verifying_key: str = '',
            audience: Optional[str] = None,
            issuer: Optional[str] = None,
            jwk_url: Optional[str] = None,
            leeway: Union[int, float, timedelta] = None,
            json_encoder: Optional[Type[json.JSONEncoder]] = None,
    ):
        self._validate_algorithm(algorithm)

        self.algorithm = algorithm
        self.signing_key = signing_key
        self.verifying_key = verifying_key
        self.audience = audience
        self.issuer = issuer

        self.jwk_client = PyJWKClient(jwk_url) if jwk_url else None
        self.leeway = leeway
        self.json_encoder = json_encoder

    @staticmethod
    def _validate_algorithm(algorithm: settings.Algorithm):
        if algorithm not in settings.Algorithm:
            raise TokenCoreError(format_lazy(_("Algorithm '{}' is not supported"), algorithm))

        if algorithm in algorithms.requires_cryptography and not algorithms.has_crypto:
            raise TokenCoreError(
                format_lazy(
                    _("Algorithm '{}' requires cryptography package"), algorithm
                )
            )

    def encode(self, payload: Dict[str, Any]) -> str:
        """Encode a payload into a JWT string"""

        jwt_payload = payload.copy()
        if self.audience is not None:
            jwt_payload["aud"] = self.audience

        if self.issuer is not None:
            jwt_payload["iss"] = self.issuer

        token = jwt.encode(
            jwt_payload,
            self.signing_key,
            algorithm=self.algorithm.value,
            json_encoder=self.json_encoder,
        )
        if isinstance(token, bytes):
            return token.decode("utf-8")
        return token

    def decode(self, token: Token, verify: bool = True) -> Dict[str, Any]:
        """Decode a JWT string into a payload dict"""

        try:
            return jwt.decode(
                token,
                self.get_verifying_key(token),
                algorithms=[self.algorithm.value],
                audience=self.audience,
                issuer=self.issuer,
                leeway=self.get_leeway(),
                options={
                    "verify_signature": verify,
                    "verify_aud": self.audience is not None,
                },
            )
        except InvalidAlgorithmError as exc:
            raise TokenCoreError(
                format_lazy(_("Algorithm '{}' is not supported"), self.algorithm)
            ) from exc
        except InvalidTokenError as exc:
            raise TokenCoreError(_("Token is invalid or expired")) from exc

    def get_verifying_key(self, token):
        if self.algorithm.value.startswith("HS"):
            return self.signing_key

        if self.jwk_client:
            try:
                return self.jwk_client.get_signing_key_from_jwt(token).key
            except PyJWKClientError as exc:
                raise TokenCoreError(_("Unable to load JWK keys")) from exc
        return self.verifying_key

    def get_leeway(self):
        if self.leeway is None:
            return timedelta(seconds=0)
        if isinstance(self.leeway, (int, float)):
            return timedelta(seconds=self.leeway)
        if isinstance(self.leeway, timedelta):
            return self.leeway

        raise TokenCoreError(
            format_lazy(
                _("Unsupported leeway type '{}'. Expected int, float or timedelta"),
                type(self.leeway),
            )
        )


token_core = TokenCore(
    algorithm=settings.ALGORITHM,
    signing_key=settings.SIGNING_KEY,
    verifying_key=settings.VERIFYING_KEY,
    audience=settings.AUDIENCE,
    issuer=settings.ISSUER,
    jwk_url=settings.JWK_URL,
    leeway=settings.LEEWAY,
    json_encoder=settings.JSON_ENCODER,
)

from typing import Any, Dict, Optional, Union

from django.utils.translation import gettext_lazy as _


class TokenError(Exception):
    ...


class TokenCoreError(TokenError):
    ...


class JwtAuthFailed(Exception):
    """
    Base class for all JWT Auth exceptions.
    """
    default_detail = _("JWT Auth Failed")
    default_code = "jwt_auth_failed"

    def __init__(
        self,
        detail: Union[str, Dict[str, Any], None] = None,
        code: Optional[str] = None,
    ) -> None:
        self._data = {
            "detail": self.default_detail,
            "code": code or self.default_code,
        }

        if isinstance(detail, dict):
            self._data.update(detail)
        elif isinstance(detail, str):
            self._data["detail"] = detail

        super().__init__(self._data)

    @property
    def data(self) -> Dict[str, Any]:
        return self._data

    def __str__(self) -> str:
        return f'{self._data["detail"]} ({self._data["code"]})'


class InvalidToken(JwtAuthFailed):
    """
    Raised when an invalid token is received.
    """
    default_detail = _("Invalid token")
    default_code = "invalid_token"

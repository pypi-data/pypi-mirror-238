from datetime import timedelta
import enum
from typing import Tuple, Optional

from django.conf import settings


class Algorithm(enum.Enum):
    HS256 = "HS256"
    HS384 = "HS384"
    HS512 = "HS512"
    RS256 = "RS256"
    RS384 = "RS384"
    RS512 = "RS512"
    ES256 = "ES256"
    ES384 = "ES384"
    ES512 = "ES512"


ACCESS_TOKEN_LIFETIME: timedelta = timedelta(minutes=5)
REFRESH_TOKEN_LIFETIME: timedelta = timedelta(days=1)
UPDATE_LAST_LOGIN: bool = False
ALGORITHM: Algorithm = Algorithm.HS256
SIGNING_KEY: str = settings.SECRET_KEY
VERIFYING_KEY: str = ''
AUDIENCE: Optional[str] = None
ISSUER: Optional[str] = None
JSON_ENCODER: Optional[str] = None
JWK_URL: Optional[str] = None
LEEWAY: timedelta = timedelta(seconds=0)
AUTH_HEADER_TYPES: Tuple[str] = ('Bearer',)
AUTH_HEADER_NAME: str = "Authorization"
USER_ID_FIELD: str = 'id'
USER_ID_CLAIM: str = 'user_id'
USER_AUTHENTICATION_RULE: str = 'jwtberry.backends.default_user_authentication_rule'
AUTH_TOKEN_CLASSES: Tuple[str] = ('jwtberry.tokens.AccessToken',)
TOKEN_TYPE_CLAIM: str = 'token_type'
JTI_CLAIM: str = 'jti'
# TOKEN_USER_CLASS: str = "rest_framework_simplejwt.models.TokenUser"

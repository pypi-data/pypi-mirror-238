from typing import Any

import strawberry
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.utils.module_loading import import_string
from strawberry.types import Info

from jwtberry import settings
from jwtberry.auth import authenticate
from jwtberry.tokens import RefreshToken
from jwtberry.types import JwtAuthError, JwtTokenType


@strawberry.mutation
async def auth_token(info: Info, email: str, password: str) -> Any:
    auth_kwargs = {
        get_user_model().USERNAME_FIELD: email,
        'password': password,
    }

    try:
        auth_kwargs['request'] = info.context.request
    except AttributeError:
        pass

    user = await authenticate(**auth_kwargs)

    auth_rule = import_string(settings.USER_AUTHENTICATION_RULE)
    if not auth_rule(user):
        return JwtAuthError(
            code='auth_error',
            message='Invalid Credentials or inactive user',
        )

    @sync_to_async
    def create_token():
        return RefreshToken.create(user)

    refresh = await create_token()

    data = JwtTokenType(
        access=str(refresh.access_token),
        refresh=str(refresh),
    )

    if settings.UPDATE_LAST_LOGIN:
        update_last_login(None, user)

    return data


@strawberry.mutation
async def refresh_token(info: Info, refresh: str) -> Any:
    ...

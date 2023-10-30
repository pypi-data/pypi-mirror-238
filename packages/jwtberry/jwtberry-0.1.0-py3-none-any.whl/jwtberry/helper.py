from calendar import timegm
from datetime import datetime, timezone
from typing import Callable, Any, Set

from django.conf import settings
from django.http import HttpRequest
from django.utils.functional import lazy
from django.utils.timezone import is_naive, make_aware
from graphql import GraphQLResolveInfo
from strawberry.django.context import StrawberryDjangoContext
from strawberry.types import Info, ExecutionContext
from jwtberry.settings import AUTH_HEADER_TYPES, AUTH_HEADER_NAME


def make_utc(dt: datetime) -> datetime:
    if settings.USE_TZ and is_naive(dt):
        return make_aware(dt, timezone=timezone.utc)

    return dt


def aware_utcnow() -> datetime:
    return make_utc(datetime.utcnow())


def datetime_to_epoch(dt: datetime) -> int:
    return timegm(dt.utctimetuple())


def datetime_from_epoch(ts: float) -> datetime:
    return make_utc(datetime.utcfromtimestamp(ts))


def format_lazy(s: str, *args, **kwargs) -> str:
    return s.format(*args, **kwargs)


format_lazy: Callable = lazy(format_lazy, str)


AUTH_HEADER_TYPE_BYTES: Set[bytes] = {
    h.encode('utf-8') for h in AUTH_HEADER_TYPES
}


def get_http_authorization(request: HttpRequest) -> str | None:
    header = request.headers.get(AUTH_HEADER_NAME)
    if isinstance(header, str):
        header = header.encode("utf-8")

    if header is None:
        return None

    auth = header.split()

    if len(auth) != 2 or auth[0] not in AUTH_HEADER_TYPE_BYTES:
        return None
    return auth[1].decode("utf-8")

from functools import cached_property

from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from strawberry.django.context import StrawberryDjangoContext

from jwtberry.helper import get_http_authorization
from django.contrib.auth import authenticate


class JwtContext(StrawberryDjangoContext):

    @cached_property
    def user(self) -> User | None:
        if not self.request:
            return None

        return authenticate(request=self.request)


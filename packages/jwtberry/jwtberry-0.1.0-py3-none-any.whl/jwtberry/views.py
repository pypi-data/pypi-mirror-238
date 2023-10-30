from typing import Any

from django.http import HttpResponse, HttpRequest
from strawberry.django.views import GraphQLView, AsyncGraphQLView

from jwtberry.context import JwtContext


class JwtGraphQLView(GraphQLView):
    """
        This is not implemented yet, please use JwtAsyncGraphQLView
    """
    def get_context(self, request: HttpRequest, response: HttpResponse) -> Any:
        ...
        # return JwtContext(request=request, response=response)


class JwtAsyncGraphQLView(AsyncGraphQLView):

    async def get_context(self, request: HttpRequest, response: HttpResponse) -> Any:
        return JwtContext(request=request, response=response)



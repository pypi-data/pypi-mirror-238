import asyncio
from typing import Any

from asgiref.sync import sync_to_async
from strawberry import BasePermission
from strawberry.types import Info


class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    # This method can also be sync!
    async def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
        @sync_to_async
        def check():
            return info.context.user and info.context.user.is_authenticated

        return await check()

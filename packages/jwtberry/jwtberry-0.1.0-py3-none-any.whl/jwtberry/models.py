from typing import Union, Optional, List, Any

from django.contrib.auth import models as auth_models
from django.db.models.manager import EmptyManager
from django.utils.functional import cached_property

from jwtberry import settings


class JwtUser:

    is_active: bool = True

    _groups = EmptyManager(auth_models.Group)
    _user_permissions = EmptyManager(auth_models.Permission)

    def __init__(self, token: "Token"):
        self.token = token

    def __str__(self):
        return str(self.token)

    def __repr__(self):
        return repr(self.token)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, JwtUser):
            return NotImplemented

        return self.id == other.id

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(self.id)

    def __getattr__(self, attr: str) -> Optional[Any]:
        return self.token.get(attr, None)

    @cached_property
    def id(self) -> Union[int, str]:
        return self.token[settings.USER_ID_CLAIM]

    @cached_property
    def pk(self) -> Union[int, str]:
        return self.id

    @cached_property
    def username(self) -> str:
        return self.token.get("username", "")

    @cached_property
    def is_staff(self) -> bool:
        return self.token.get("is_staff", False)

    @cached_property
    def is_superuser(self) -> bool:
        return self.token.get("is_superuser", False)

    @property
    def is_anonymous(self) -> bool:
        return False

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def get_username(self) -> str:
        return self.username

    @property
    def groups(self) -> auth_models.Group:
        return self._groups

    @property
    def user_permissions(self) -> auth_models.Permission:
        return self._user_permissions

    def get_group_permissions(self, obj: Optional[object] = None) -> set:
        return set()

    def get_all_permissions(self, obj: Optional[object] = None) -> set:
        return set()

    def has_perm(self, perm: str, obj: Optional[object] = None) -> bool:
        return False

    def has_perms(self, perm_list: List[str], obj: Optional[object] = None) -> bool:
        return False

    def has_module_perms(self, module: str) -> bool:
        return False

    def save(self) -> None:
        raise NotImplementedError("Token users have no DB representation")

    def delete(self) -> None:
        raise NotImplementedError("Token users have no DB representation")

    def set_password(self, raw_password: str) -> None:
        raise NotImplementedError("Token users have no DB representation")

    def check_password(self, raw_password: str) -> None:
        raise NotImplementedError("Token users have no DB representation")

from typing import Annotated, Union

import strawberry


@strawberry.type
class JwtTokenType:
    access: str
    refresh: str


@strawberry.type
class JwtAuthError:
    code: str
    message: str


JwtAuthResponse = Annotated[
    Union[JwtTokenType, JwtAuthError],
    strawberry.union("JwtAuthResponse", types=[JwtTokenType, JwtAuthError]),
]

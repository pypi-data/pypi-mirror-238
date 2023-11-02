# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Literal
from typing import Union

import pydantic

from headless.types import IClient
from headless.types import IRequest
from headless.types import IResponse


__all__: list[str] = [
    'AccessTokenRequest',
    'AuthorizationCodeTokenRequest',
    'BaseTokenRequest',
    'RefreshTokenRequest',
]


class BaseTokenRequest(pydantic.BaseModel):
    pass


class AuthorizationCodeTokenRequest(BaseTokenRequest):
    grant_type: Literal['authorization_code'] = pydantic.Field(
        default=...,
        description="This value **must** be `authorization_code`."
    )

    code: str = pydantic.Field(
        default=...,
        description="The authorization code received from the authorization server"
    )

    redirect_uri: str | None = pydantic.Field(
        default=None,
        description=(
            "This parameter is **required** if the `redirect_uri` parameter was "
            "included in the authorization request and their values **must** be identical."
        )
    )

    client_id: str | None = pydantic.Field(
        default=None,
        description=(
            "This parameter is **required** if the client is not authenticating with "
            "the authorization server."
        )
    )


class RefreshTokenRequest(BaseTokenRequest):
    grant_type: Literal['refresh_token'] = pydantic.Field(
        default=...,
        description="This value **must** be `refresh_token`."
    )

    refresh_token: str = pydantic.Field(
        default=...,
        description="The refresh token that was issued to the client."
    )

    scope: str | None = pydantic.Field(
        default=None,
        description=(
            "The space-delimited scope of the access request. The requested "
            "scope **must not** include any scope not originally granted by "
            "the resource owner, and if omitted is treated as equal to the "
            "scope originally granted by the resource owner."
        )
    )


class AccessTokenRequest(pydantic.BaseModel):
    __root__: Union[
        AuthorizationCodeTokenRequest,
        RefreshTokenRequest
    ]

    async def send(
        self,
        client: IClient[IRequest[Any], IResponse[Any, Any]],
        url: str
    ) -> IResponse[Any, Any]:
        return await client.get(url=url, json=self.dict(exclude_none=True))
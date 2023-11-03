# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from headless.types import ICredential
from headless.types import IRequest

from .types import BearerTokenCredential
from .types import TokenResponse
from .openauthorizationclient import OpenAuthorizationClient


class ClientCredential(ICredential):
    __module__: str = 'headless.ext.oidc'
    oauth: OpenAuthorizationClient
    credential: BearerTokenCredential | None
    resource: str | None = None

    def __init__(
        self,
        client: OpenAuthorizationClient,
        resource: str | None = None
    ) -> None:
        self.credential = None
        self.oauth = client
        self.resource = resource

    async def add_to_request(self, request: IRequest[Any]) -> None:
        if self.credential is None:
            await self.obtain(request)
        assert self.credential is not None
        return await self.credential.add_to_request(request)
    
    async def obtain(self, request: IRequest[Any]) -> None:
        response = await self.oauth.token(
            grant_type='client_credentials'
        )
        self.credential = response.credential

    async def on_token_obtained(
        self,
        request: IRequest[Any],
        response: TokenResponse
    ) -> None:
        pass
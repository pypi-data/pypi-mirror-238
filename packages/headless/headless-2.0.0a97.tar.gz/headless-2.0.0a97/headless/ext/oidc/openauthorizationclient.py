# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from headless.core import httpx
from .clientsecretcredential import ClientSecretCredential
from .server import Server as Provider
from .types import AccessTokenRequest
from .types import ClientSecret
from .types import TokenResponse


class OpenAuthorizationClient(httpx.Client):
    provider: Provider[Any]

    def __init__(
        self,
        url: str,
        credential: ClientSecret | None = None,
        issuer: str | None = None,
        token_endpoint: str | None = None
    ):
        assert credential is not None
        self.provider = Provider(
            issuer=issuer or url,
            token_endpoint=token_endpoint
        )
        super().__init__(
            base_url=url,
            credential=ClientSecretCredential(
                server=self.provider,
                client_id=credential.client_id,
                client_secret=credential.client_secret,
                mode=credential.mode
            )
        )

    async def token(
        self,
        grant_type: str
    ) -> TokenResponse:
        """Obtain a token from the authorization server using the specified
        `grant_type`.
        """
        return await self.provider.token(
            client=self,
            request=AccessTokenRequest.parse_obj({'grant_type': grant_type})
        )
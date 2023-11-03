# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from headless.core import httpx
from headless.ext.oidc import ClientCredential
from headless.ext.oidc import OpenAuthorizationClient
from headless.ext.oidc.types import ClientSecret


class FedexClient(httpx.Client):
    provider: OpenAuthorizationClient

    def __init__(
        self,
        *,
        url: str,
        client_id: str,
        client_secret: str
    ):
        self.oauth = OpenAuthorizationClient(
            url=url,
            credential=ClientSecret(client_id, client_secret, mode='client_secret_post'),
            token_endpoint=f'{url}/oauth/token'
        )
        super().__init__(
            base_url=url,
            credential=ClientCredential(client=self.oauth)
        )
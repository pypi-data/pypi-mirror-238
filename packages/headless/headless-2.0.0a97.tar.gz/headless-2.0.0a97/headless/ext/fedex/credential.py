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

from headless.types import ICredential
from headless.types import IRequest
from headless.ext.oidc import Provider


class FedexCredential(ICredential):
    __module__: str = 'headless.ext.oidc.types'
    provider: Provider
    mode: str = 'client_secret_post'

    def __init__(
        self,
        provider: Provider[Any],
        client_id: str,
        client_secret: str,
    ):
        self.provider = provider

    async def add_to_request(self, request: IRequest[Any]) -> None:
        pass
# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

import ckms.types
import pydantic

from headless.types import IClient
from headless.types import IRequest
from headless.types import IResponse


class JSONWebKeySet(ckms.types.JSONWebKeySet):

    @classmethod
    async def discover(
        cls,
        client: IClient[IRequest[Any], IResponse[Any, Any]],
        url: str
    ) -> 'JSONWebKeySet':
        response = await client.get(url=url)
        if response.status_code >= 400:
            client.logger.warning("Unable to discover JWKS from URL (url: %s)", url)
            return cls()
        try:
            return cls.parse_obj(await response.json())
        except pydantic.ValidationError:
            client.logger.warning("Invalid JWKS format (url: %s)", url)
            return cls()

# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import NoReturn

import fastapi
from headless.ext.oidc.types import Error

from ..types import IClient
from ..types import IAuthorizationServer
from .currentauthorizationserver import CurrentAuthorizationServer


__all__: list[str] = ['CurrentClient']


def on_client_unknown() -> NoReturn:
    raise Error(
        error='invalid_request',
        error_description=(
            "Could not determine the client from the request "
            "parameters."
        )
    )


def CurrentClient(required: bool) -> Any:

    async def get(
        request: fastapi.Request,
        oauth2: IAuthorizationServer[Any] = CurrentAuthorizationServer
    ) -> IClient:
        client_id: str | None
        is_request = request.url.path == request.url_for('oauth2.authorize').path
        if is_request:
            client_id = request.query_params.get('client_id')
        else:
            raise NotImplementedError("Can not get client for current endpoint.")
        if client_id is None:
            on_client_unknown()
        client = await oauth2.get_client(client_id)
        if client is None:
            on_client_unknown()
        return client

    return fastapi.Depends(get)
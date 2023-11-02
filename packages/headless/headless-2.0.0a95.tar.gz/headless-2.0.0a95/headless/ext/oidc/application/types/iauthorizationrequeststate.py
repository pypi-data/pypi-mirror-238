# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Awaitable
from typing import Callable
from typing import Protocol
from typing import TypeVar

import fastapi
import starlette.datastructures
from headless.ext.oidc import types

from .iauthorizationserver import IAuthorizationServer
from .iclient import IClient
from .irequestsubject import IRequestSubject
from .iresourceowner import IResourceOwner
from .resourceownerkey import ResourceOwnerKey

T = TypeVar('T')


class IAuthorizationRequestState(Protocol):

    @property
    def resource_owner(self) -> ResourceOwnerKey:
        ...

    @classmethod
    async def new(
        cls: type[T],
        client_id: str,
        sub: str,
        params: types.AuthorizationRequestParameters,
        allocate_id: Callable[..., Awaitable[str]] | None = None
    ) -> T: ...

    async def get_redirect_url(self, *, server: IAuthorizationServer[Any], issuer: str, client: IClient, **params: str) -> str: ...
    def authenticate(self, client: IClient, subject: IRequestSubject) -> bool: ...
    def get_authorize_url(self, request: fastapi.Request) -> starlette.datastructures.URL: ...
    def get_request_id(self) -> str: ...
    def get_request_uri(self) -> str: ...
    def consent_required(self, owner: IResourceOwner) -> set[str]: ...
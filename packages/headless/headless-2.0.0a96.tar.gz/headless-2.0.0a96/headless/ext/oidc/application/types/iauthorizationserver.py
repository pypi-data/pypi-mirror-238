# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# type: ignore
from typing import Any
from typing import Generic
from typing import Protocol
from typing import TypeAlias
from typing import TypeVar
from typing import TYPE_CHECKING

import fastapi
from headless.ext.oidc.types import AuthorizationRequest
from headless.ext.oidc.types import AuthorizationRequestParameters
from headless.ext.oidc.types import RequestURI

if TYPE_CHECKING:
    from .authorizationrequest import AuthorizationRequest
    from .iauthorizationrequeststate import IAuthorizationRequestState
from .iclient import IClient
from .iobjectidentifier import IObjectIdentifier
from .iresourceowner import IResourceOwner
from .irequestsubject import IRequestSubject


Object = TypeVar('Object')
ResourceOwner = TypeVar('ResourceOwner')


class IAuthorizationServer(Generic[ResourceOwner], Protocol):
    ObjectType: TypeAlias = Object

    #async def decode_authorization_request(
    #    self,
    #    dto: AuthorizationRequest
    #) -> None:
    #    """Decode an authorization request into a datastructure holding the
    #    parameters.

    #    If the request is provided through query parameters, do nothing
    #    and return the parameters.

    #    If the request is a reference (using the ``request_uri`` query
    #    parameter), lookup the persisted request object.

    #    If the request is a request object, decrypt the JWE if the object is
    #    encrypted, and verify the signature using the preregistered public
    #    keys from the client.

    #    Return an instance of :class:`~cbra.ext.oidc.types.AuthorizationRequestParameters` 
    #    """
    #    ...

    def get_issuer(self) -> str | None: ...

    async def authorize(
        self,
        request: fastapi.Request,
        subject: IRequestSubject,
        authz: AuthorizationRequest,
    ) -> str:
        """Handle an authorization request and return a string to which the
        user-agent must be redirected.
        """
        raise NotImplementedError

    async def begin_authorization(
        self,
        *,
        client: IClient,
        subject: IRequestSubject,
        params: AuthorizationRequestParameters
    ) -> 'IAuthorizationRequestState':
        ...

    async def assign_ppid(self, client: IClient, subject: IRequestSubject) -> str: ...
    async def render_template(self, template_name: str, ctx: dict[str, Any] | None = None) -> str: ...
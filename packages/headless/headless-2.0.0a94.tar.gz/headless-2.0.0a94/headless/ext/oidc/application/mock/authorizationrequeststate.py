# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import secrets
from typing import Any
from typing import Awaitable
from typing import Callable

import fastapi
import pydantic
import starlette.datastructures
from headless.ext.oidc import types

from ..types import AuthorizationRequestLifecycle
from ..types import IAuthorizationServer
from ..types import IClient
from ..types import IRequestSubject
from ..types import IResourceOwner
from ..types import ResourceOwnerKey


class AuthorizationRequestState(pydantic.BaseModel):
    code: str
    client_id: str
    id: str
    lifecycle: AuthorizationRequestLifecycle
    params: types.AuthorizationRequestParameters
    scope: set[str] = set()
    sub: str | None

    @property
    def resource_owner(self) -> ResourceOwnerKey:
        assert self.sub is not None
        return ResourceOwnerKey(self.client_id, self.sub)

    @classmethod
    async def new(
        cls,
        client_id: str,
        sub: str,
        params: types.AuthorizationRequestParameters,
        allocate_id: Callable[..., Awaitable[str]] | None = None
    ):
        assert client_id == params.client_id
        return cls(
            client_id=client_id,
            code=secrets.token_urlsafe(48),
            id=(await allocate_id()) if allocate_id else secrets.token_urlsafe(48),
            lifecycle=AuthorizationRequestLifecycle.pending,
            params=params,
            sub=sub
        )

    def authenticate(self, client: IClient, subject: IRequestSubject) -> bool:
        if self.sub is None:
            self.sub = subject.identifier()
        return all([
            client.id == self.client_id,
            subject.identifier() == self.sub
        ])

    def consent_required(self, owner: IResourceOwner) -> set[str]:
        """Return a set holding the scope for which the resource owner must
        grant consent.
        """
        return owner.must_consent(self.params.scope) | self.scope

    def get_authorize_url(self, request: fastapi.Request) -> starlette.datastructures.URL:
        return request.url_for('oauth2.authorize')\
            .remove_query_params(list(request.query_params.keys()))\
            .replace_query_params(
                client_id=self.client_id,
                request_uri=f'urn:ietf:params:oauth:request_uri:{self.id}'
            )

    async def get_redirect_url(
        self,
        *,
        server: IAuthorizationServer[Any],
        issuer: str,
        client: IClient,
        **params: str
    ) -> str:
        if self.params.response_mode != types.ResponseMode.query:
            raise NotImplementedError
        assert self.params.redirect_uri is not None
        params.update({
            'code': self.code,
            'iss': issuer,
        })
        if self.params.state:
            params['state'] = self.params.state
        return self.params.redirect_uri.redirect(False, **params)

    def get_request_id(self) -> str:
        return self.id
    
    def get_request_uri(self) -> str:
        return f'urn:ietf:params:oauth:request_uri:{self.id}'
# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import dataclasses
import logging
import secrets
import urllib.parse
from typing import Any

import fastapi
from headless.ext.oidc.types import AuthorizationRequestParameters
from headless.ext.oidc.types import GrantType
from headless.ext.oidc.types import InvalidRequest
from headless.ext.oidc.types import InvalidScope
from headless.ext.oidc.types import RedirectURI
from headless.ext.oidc.types import ResponseMode
from headless.ext.oidc.types import ResponseType
from headless.ext.oidc.types import UnauthorizedClient
from headless.ext.oidc.types import UnsupportedResponseType

from ..types import AuthorizationRequest
from ..types import IAuthorizationRequestState
from ..types import IClient
from ..types import IAuthorizationServer
from ..types import IRequestSubject
from ..types import IResourceOwner
from ..types import IServerStorage
from ..types import ResourceOwnerKey
from .authorizationrequeststate import AuthorizationRequestState
from .resourceowner import ResourceOwner
from .mockstorage import MockStorage
from .services import TemplateService
    

@dataclasses.dataclass
class MockClient:
    id: str
    grant_types: list[GrantType]
    redirect_uris: list[RedirectURI]
    requires_state: bool
    response_modes: list[ResponseMode]
    response_types: list[ResponseType]
    sector_identifier_uri: str | None
    scope: set[str]

    def allows_redirect(self, uri: RedirectURI) -> bool:
        """Return a boolean indicating if the given redirect URI `uri` is
        allowed by the client.
        """
        return uri in self.redirect_uris

    def allows_scope(self, scope: set[str]) -> bool:
        """Return a boolean indicating if the client allows the given
        scope.
        """
        return scope <= self.scope

    def default_redirect(self) -> RedirectURI:
        """Return the default redirection URI configured by the client."""
        if not self.redirect_uris:
            raise InvalidRequest("The redirect_uri parameter was missing and the client did not specify a default.")
        return self.redirect_uris[0]

    def get_sector_identifier(self) -> str:
        """Return the sector identifier for this client."""
        # If the Client has not provided a value for sector_identifier_uri
        # in Dynamic Client Registration [OpenID.Registration], the Sector
        # Identifier used for pairwise identifier calculation is the host
        # component of the registered redirect_uri. If there are multiple
        # hostnames in the registered redirect_uris, the Client MUST
        # register a sector_identifier_uri .... When a sector_identifier_uri
        # is provided, the host component of that URL is used as the Sector
        # Identifier for the pairwise identifier calculation. The value of
        # the sector_identifier_uri MUST be a URL using the https scheme
        # that points to a JSON file containing an array of redirect_uri
        # values. The values of the registered redirect_uris MUST be
        # included in the elements of the array.
        #
        # OpenID Connect Core 1.0 incorporating errata set 1
        if self.sector_identifier_uri:
            sector_identifier = urllib.parse.urlparse(self.sector_identifier_uri).netloc
        else:
            hosts = {urllib.parse.urlparse(x).netloc for x in self.redirect_uris}
            assert hosts, self.redirect_uris
            if len(hosts) > 1:
                raise NotImplementedError
            sector_identifier = hosts.pop()
        return sector_identifier

    async def validate_request(
        self,
        params: AuthorizationRequestParameters
    ) -> None:
        """Validates the parameters of an authorization request according to
        the OAuth 2.x and OpenID Connect specifications.
        """
        if "authorization_code" not in self.grant_types:
            raise UnauthorizedClient("The client does not allow requesting an authorization code using this method.")
        if not params.redirect_uri:
            params.redirect_uri = self.default_redirect()
        if not self.allows_redirect(params.redirect_uri):
            raise InvalidRequest("The client does not allow redirection to the given URL.")
        if params.response_type not in self.response_types:
            raise UnsupportedResponseType("The client does not allow the requested response type.")
        if not self.allows_scope(params.scope):
            raise InvalidScope("The client does not allow the requested scope.")
        if params.response_mode is None:
            params.response_mode = ResponseMode.default(params.response_type)
        if params.response_mode not in self.response_modes:
            raise InvalidRequest("The client does not allow the requested response mode.")
        if self.requires_state and not params.state:
            raise InvalidRequest("The client requires the use of the state parameter.")

        # If there are multiple hostnames in the registered redirect_uris,
        # the Client MUST register a sector_identifier_uri
        #
        # OpenID Connect Core 1.0 incorporating errata set 1
        hosts = {urllib.parse.urlparse(x).netloc for x in self.redirect_uris}
        if len(hosts) > 1 and not self.sector_identifier_uri:
            raise InvalidRequest(
                "The client specifies multiple redirect_uris but no "
                "sector_identifier_uri was provided."
            )

        if self.sector_identifier_uri:
            if False:
                raise InvalidRequest(
                    "The response from the sector identifier URI did not contain a valid "
                    "JSON document."
                )
            redirect_uris: set[str] = set()
            if str(params.redirect_uri) not in redirect_uris:
                raise InvalidRequest("The sector does not allow redirection to the given URL.")



class MockAuthorizationServer(IAuthorizationServer[ResourceOwner]):
    logger: logging.Logger = logging.getLogger('uvicorn')
    storage: IServerStorage = MockStorage(
        clients=[
            MockClient(
                id='default',
                grant_types=["authorization_code"],
                redirect_uris=[RedirectURI('http://127.0.0.1:8000/oauth/v2/callback')],
                requires_state=True,
                response_modes=[ResponseMode.query],
                response_types=["code"],
                scope={"foo"},
                sector_identifier_uri=None
            )
        ]
    )
    owners: dict[ResourceOwnerKey, ResourceOwner] = {}
    pairwise_identifiers: dict[tuple[str, str], str] = {}
    requests: dict[str, AuthorizationRequestState] = {}

    def __init__(
        self,
        templates: TemplateService = fastapi.Depends(TemplateService)
    ) -> None:
        self.templates = templates

    def get_issuer(self) -> str | None:
        return None

    async def assign_ppid(self, client: IClient, subject: IRequestSubject) -> str:
        k = (client.get_sector_identifier(), subject.identifier())
        if k not in self.pairwise_identifiers:
            self.pairwise_identifiers[k] = ppid = secrets.token_hex(16)
            self.logger.info(
                "Assigned pairwise subject identifier (sector: %s, client: %s, sub: %s, ppid: %s)",
                k[0], client.id, k[1], ppid
            )
        return self.pairwise_identifiers[k]

    async def authorize(
        self,
        request: fastapi.Request,
        subject: IRequestSubject,
        authz: AuthorizationRequest
    ) -> str:
        """Handle an authorization request with the given parameters."""
        client = await self.storage.get(authz.client_id)
        if client is None:
            raise InvalidRequest("The client specified by the client_id parameter does not exist.")

        # Validate the request parameters and reconstruct (possible) existing
        # authorization request state. If the request is a reference but does not
        # exist, this is a fatal error.
        state = await self.storage.get(authz.key)
        if authz.is_reference() and state is None:
            assert authz.request_uri is not None
            self.logger.info(
                "Subject attempted to authorize a non-existing request (client: %s, sub: %s, request: %s)",
                client.id, subject.identifier(), authz.request_uri
            )
            raise InvalidRequest("This request is expired, does not exist, or is already granted.")

        if state is None:
            state = await self.begin_authorization(
                client=client,
                subject=subject,
                params=await authz.get_params(self, client)
            )
            self.logger.info(
                "Created authorization request (client: %s, sub: %s, request: %s)",
                client.id, subject.identifier(), state.get_request_id()
            )

        # Authenticate the state i.e. the request was made for this client,
        # by this subject. This is redundant for new requests, but always
        # check anyway. If authentication fails, this is a fatal error.
        if not state.authenticate(client, subject):
            self.logger.warning(
                "Unauthorized subject tried to grant authorization request "
                "(client: %s, sub: %s, request: %s)",
                client.id, subject.identifier(), state.get_request_uri()
            )
            raise InvalidRequest("Unable to process your request.")

        # Retrieve the ResourceOwner entity for this client. If it does not
        # exist, create one in pristine state (i.e. no scopes granted). Run
        # policies regarding the session state (e.g. two-factor present, has
        # certain properties). Check if the resource owner consents to the
        # requested scope, and redirect to the consent interface if required.
        owner = await self.storage.get(state.resource_owner)
        if owner is None:
            owner = await self.register_subject(client, subject)
        #missing_scope = state.consent_required(owner)
        #if missing_scope:
        #    raise NotImplementedError(state.get_authorize_url(request))

        return await state.get_redirect_url(server=self, issuer='foo', client=client)

    async def begin_authorization(
        self,
        *,
        client: IClient,
        subject: IRequestSubject,
        params: AuthorizationRequestParameters
    ) -> IAuthorizationRequestState:
        await client.validate_request(params)
        request = await AuthorizationRequestState.new(client.id, subject.identifier(), params)
        await self.storage.persist(request)
        return request

    async def register_subject(self, client: IClient, subject: IRequestSubject) -> IResourceOwner:
        owner = ResourceOwner(
            client_id=client.id,
            consented_scope=set(),
            sub=subject.identifier(),
            ppid=await self.assign_ppid(client, subject)
        )
        await self.storage.persist(owner)
        self.logger.info(
            "Registered subject for client (client: %s, sub: %s).",
            client.id, subject.identifier()
        )
        return owner
    
    async def render_template(
        self,
        template_name: str,
        ctx: dict[str, Any] | None = None
    ) -> str:
        try:
            return await self.templates.render_template(template_name, ctx or {})
        except LookupError:
            return ""
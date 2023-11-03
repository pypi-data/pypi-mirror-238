# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import cast
from typing import Any
from typing import Generic
from typing import TypeVar

import pydantic
from headless.ext.oauth2.models import ServerMetadata
from headless.types import IClient
from headless.types import IRequest
from headless.types import IResponse
from .types import AccessTokenRequest
from .types import Error
from .types import JSONWebKeySet
from .types import ProtocolError
from .types import TokenResponse


T = TypeVar('T', bound=TokenResponse)


class Server(Generic[T]):
    """Provides an interface to an OAuth 2.x/OpenID Connect authorization
    server. May be autodiscovered using the Metadata Endpoint, or manually
    configured. When configuring manually, at least the `token_endpoint`
    parameter must be provided.
    """
    __module__: str = 'headless.ext.oidc'
    keys: JSONWebKeySet
    metadata_class: type[ServerMetadata] = ServerMetadata
    token_response_class: type[T] = cast(type[T], TokenResponse)

    def __init__(
        self,
        issuer: str,
        autodiscover: bool = True,
        token_endpoint: str | None = None,
        metadata_endpoint: str | None = None,
        discovery_urls: list[str] = [
            '/.well-known/oauth-authorization-server',
            '/.well-known/openid-configuration'
        ],
        metadata_class: type[ServerMetadata] = ServerMetadata
    ) -> None:
        self.discovery_urls = tuple(discovery_urls)
        self.metadata_class = metadata_class
        self.autodiscover = autodiscover and not bool(token_endpoint)
        self.issuer = issuer
        self.keys = JSONWebKeySet()
        self.metadata = self.metadata_class.parse_obj({
            'issuer': issuer,
            'token_endpoint': token_endpoint
        })
        self.metadata_endpoint = metadata_endpoint

    def is_protected(self, endpoint: str) -> bool:
        """Return a boolean indicating if the endpoint is protected and the client
        must provide credentials.
        """
        return endpoint in {
            self.metadata.introspection_endpoint,
            self.metadata.pushed_authorization_request_endpoint,
            self.metadata.revocation_endpoint,
            self.metadata.token_endpoint,
        }

    async def discover(self, client: IClient[IRequest[Any], IResponse[Any, Any]]) -> None:
        """Inspect the metadata endpoint of the configured issuer to discover
        endpoints and server capabilities.
        """
        if not self.autodiscover:
            return
        urls: list[str] = [f'{self.issuer}/{url}' for url in self.discovery_urls]
        metadata = None
        for url in urls:
            if metadata is not None:
                break
            metadata = await self.metadata_class.discover(client, url)
        if metadata is not None:
            self.metadata = metadata

        # Every authorization server is assumed to provide at least a
        # token endpoint. At this point, this is either autodiscovered
        # was passed as an argument to the constructor.
        if not self.metadata.token_endpoint:
            client.logger.critical(
                "Unable to discover server %s and manual configuration missing.",
                self.issuer
            )

        # If the server points to a JWKS, we can use it to verify the responses
        # and to encrypt data we sent.
        if self.metadata.jwks_uri:
            self.keys = await JSONWebKeySet.discover(client, self.metadata.jwks_uri)

    async def token(
        self,
        client: IClient[Any, Any],
        request: AccessTokenRequest
    ) -> T:
        assert self.metadata.token_endpoint is not None
        response = await request.send(
            client=client,
            url=self.metadata.token_endpoint,
            credential=client.credential
        )
        try:
            dto = await response.json()
        except ValueError:
            client.logger.critical(
                "Unable to decode token endpoint response as JSON "
                "(issuer: %s, endpoint: %s)",
                self.issuer, self.metadata.token_endpoint
            )
            raise ProtocolError
        
        if not isinstance(dto, dict):
            client.logger.critical(
                "Invalid JSON response from token endpoint "
                "(issuer: %s, endpoint: %s)",
                self.issuer, self.metadata.token_endpoint
            )
            raise ProtocolError
        dto = cast(dict[str, str], dto)
        
        # At this point, dto contains either an error or a valid token
        # response.
        try:
            if 'error' in dto:
                raise Error(**dto)
        except TypeError:
            client.logger.critical(
                "Invalid JSON response from token endpoint "
                "(issuer: %s, endpoint: %s)",
                self.issuer, self.metadata.token_endpoint
            )
            raise ProtocolError

        # If parsing fails here, then the server also returned an
        # invalid response, but we don't catch it so that the output
        # of the pydantic error is shown in the logs.
        try:
            return self.token_response_class.parse_obj(await response.json())
        except pydantic.ValidationError:
            # If the response code is 200 but the JSON datastructue could not
            # be parsed, the server violates the protocol.
            client.logger.critical(
                "Invalid response from token endpoint (issuer: %s, endpoint: %s)",
                self.issuer, self.metadata.token_endpoint
            )
            raise ProtocolError
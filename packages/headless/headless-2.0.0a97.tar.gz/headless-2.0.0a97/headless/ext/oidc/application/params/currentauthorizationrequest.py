# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import fastapi
import pydantic
from headless.ext.oidc.types import InvalidRequest
from headless.ext.oidc.types import LazyException
from headless.ext.oidc.types import ResponseType
from headless.ext.oidc.types import ResponseMode

from ..types import AuthorizationRequest


__all__: list[str] = ['CurrentAuthorizationRequest']


def get(
    client_id: str | None = fastapi.Query(
        default=None,
        title="Client ID",
        description="Identifies the client that is requesting an access token."
    ),
    redirect_uri: str | None = fastapi.Query(
        default=None,
        title="Redirect URI",
        description=(
            "The client redirection endpoint. This URI **must** be priorly "
            "whitelisted for the client specified by `client_id`. If the "
            "client has multiple allowed redirect URIs and did not "
            "configure a default, then this parameter is **required**."
        )
    ),
    request_jwt: str | None = fastapi.Query(
        default=None,
        alias='request',
        title="Request",
        description=(
            "A JSON Web Token (JWT) whose JWT Claims Set holds the "
            "JSON-encoded OAuth 2.0 authorization request parameters. "
            "Must not be used in combination with the `request_uri` "
            "parameter, and all other parameters except `client_id` "
            "must be absent.\n\n"
            "Confidential and credentialed clients must first sign "
            "the claims using their private key, and then encrypt the "
            "result with the public keys that are provided by the "
            "authorization server through the `jwks_uri` specified "
            "in its metadata."
        )
    ),
    request_uri: str | None = fastapi.Query(
        default=None,
        title="Request URI",
        description=(
            "References a Pushed Authorization Request (PAR) or a remote "
            "object containing the authorization request.\n\n"
            "If the authorization request was pushed to this authorization "
            "server, then the format of the `request_uri` parameter is "
            "`urn:ietf:params:oauth:request_uri:<reference-value>`. "
            "Otherwise, it is an URI using the `https` scheme. If the "
            "`request_uri` parameter is a remote object, then the external "
            "domain must have been priorly whitelisted by the client."
        )
    ),
    response_type: str | None = fastapi.Query(
        default=None,
        title="Response type",
        description="Specifies the response type."
    ),
    response_mode: str | None = fastapi.Query(
        default=None,
        title="Response mode",
        description=(
            "Informs the authorization server of the mechanism to be used "
            "for returning authorization response parameters."
        )
    ),
    scope: str | None = fastapi.Query(
        default=None,
        title="Scope",
        description=(
            "The space-delimited scope that is requested by the client."
        )
    ),
    request_state: str | None = fastapi.Query(
        default=None,
        alias='state',
        title="State",
        description=(
            "An opaque value used by the client to maintain state between the "
            "request and callback.  The authorization server includes this "
            "value when redirecting the user-agent back to the client."
        )
    )
):
    if client_id is None:
        return LazyException(InvalidRequest("The client_id parameter is mandatory."))
    try:
        return AuthorizationRequest.parse_obj({
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'request': request_jwt,
            'request_uri': request_uri,
            'response_mode': response_mode,
            'response_type': response_type,
            'scope': scope,
            'state': request_state
        })
    except pydantic.ValidationError as exc:
        deferred = None
        for error in exc.errors():
            _, param = error['loc']
            if error.get('type') in {'value_error.const', 'type_error.enum'}:
                deferred = InvalidRequest(f'Invalid value provided for parameter {param}')
        if deferred is None:
            raise
        return LazyException(deferred)
    except Exception as exc:
        return LazyException(exc)


CurrentAuthorizationRequest = fastapi.Depends(get)
# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import inspect
import logging
from collections import OrderedDict
from typing import Any
from typing import Callable

import fastapi
from fastapi import APIRouter
from headless.ext.oidc.types import AccessTokenRequest
from headless.ext.oidc.types import GrantType
from headless.ext.oidc.types import FatalError

from .params import CurrentAuthorizationRequest
from .params import CurrentSubject
from .types import AuthorizationRequest
from .types import IAuthorizationServer
from .types import IRequestSubject


__all__: list[str] = [
    'OpenAuthorizationApplication',
]


class OpenAuthorizationApplication(APIRouter):
    grant_types_supported: set[str] = set()
    logger: logging.Logger = logging.getLogger('uvicorn')
    oauth2: IAuthorizationServer[Any]

    def __init__(
        self,
        *,
        app: fastapi.FastAPI,
        server: type[IAuthorizationServer[Any]],
        subjects: Any,
        # https://www.rfc-editor.org/rfc/rfc8414.html#section-2.1
        grant_types_supported: set[GrantType] = {"authorization_code", "implicit"},
        token_handler: bool = False
    ):
        super().__init__()
        self.app = app
        self.grant_types_supported = set(grant_types_supported)
        self.oauth2 = fastapi.Depends(server)
        if token_handler:
            # If this application is a token handler, then there are no grant types
            # to support.
            self.grant_types_supported = set()

        if self.grant_types_supported:
            self.add_api_route(
                path='/token',
                endpoint=self.token,
                name='oauth2.token',
                summary="Token endpoint",
                    tags=['OAuth 2.x/OpenID Connect']
            )
            if bool({"authorization_code", "implicit"} & self.grant_types_supported):
                self.add_api_route(
                    path='/authorize',
                    endpoint=self.inject_signature(
                        callable=self.authorize,
                        oauth2=self.oauth2,
                        subject=CurrentSubject(subjects=subjects, required=True)
                    ),
                    name='oauth2.authorize',
                    summary="Authorization endpoint",
                    status_code=302,
                    response_class=fastapi.responses.RedirectResponse,
                    response_description="Redirect to the client redirection endpoint.",
                    response_model=None,
                    responses={
                        422: {
                            'description': (
                                "Unrecoverable error that is not allowed to redirect"
                            )
                        }
                    },
                    tags=['OAuth 2.x/OpenID Connect']
                )

    async def authorize(
        self,
        request: fastapi.Request,
        oauth2: IAuthorizationServer[Any] = NotImplemented,
        subject: IRequestSubject = NotImplemented,
        authz: AuthorizationRequest = CurrentAuthorizationRequest
    ) -> str | fastapi.responses.HTMLResponse:
        assert oauth2 != NotImplemented
        assert subject != NotImplemented
        try:
            return await oauth2.authorize(request, subject, authz)
        except FatalError as exc:
            return fastapi.responses.HTMLResponse(
                content=await oauth2.render_template('oauth/error.html.j2', {
                    'error': exc,
                    'page_title': "Access denied: autorization error",
                    'subject': subject
                }),
                headers={
                    'X-OAuth-Error': exc.error
                },
                status_code=400,
            )

    def inject_signature(
        self,
        callable: Callable[..., Any],
        **kwargs: Any
    ) -> Callable[..., Any]:
        sig = inspect.signature(callable)
        params = OrderedDict(sig.parameters.items())
        for name, default in kwargs.items():
            if name not in params:
                raise ValueError(f"No such argument: {name}")
            params[name] = inspect.Parameter(
                kind=params[name].kind,
                name=params[name].name,
                default=default,
                annotation=params[name].annotation
            )

        async def f(*args: Any, **kwargs: Any) -> Any:
            return await callable(*args, **kwargs)
        f.__signature__ = sig.replace(parameters=list(params.values())) # type: ignore
        return f

    async def token(
        self,
        dto: AccessTokenRequest
    ):
        pass
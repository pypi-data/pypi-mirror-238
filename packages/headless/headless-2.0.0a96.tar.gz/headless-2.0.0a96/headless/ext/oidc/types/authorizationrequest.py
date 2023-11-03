# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import re
from typing import Any
from typing import Union

import pydantic

from .fatalerror import InvalidRequest
from .parameters import ResponseType
from .redirecturi import RedirectURI
from .requesturi import RequestURI
from .responsemode import ResponseMode


__all__: list[str] = [
    'AuthorizationRequest',
    'AuthorizationRequestParameters',
]



ERRORS: dict[int, str] = {
    10000: "The request and request_uri parameters are mutually exclusive.",
    10001: "The request_uri parameter must be a valid URN.",
}


class BaseAuthorizationRequest(pydantic.BaseModel):
    client_id: str


class AuthorizationRequestParameters(BaseAuthorizationRequest):
    redirect_uri: RedirectURI | None
    response_mode: ResponseMode | None
    response_type: ResponseType
    scope: set[str]
    state: str | None = None

    @pydantic.validator('scope', pre=True)
    def validate_scope(cls, scope: str | set[str] | None) -> set[str]:
        if isinstance(scope, str):
            scope = {str.strip(x) for x in re.split(r'\s+', scope)}
        scope = scope or set()
        return set(filter(bool, scope))


class AuthorizationRequestReference(BaseAuthorizationRequest):
    request_uri: RequestURI


class AuthorizationRequestObject(BaseAuthorizationRequest):
    request: str


class AuthorizationRequest(pydantic.BaseModel):
    __root__: Union[
        AuthorizationRequestParameters,
        AuthorizationRequestReference,
        AuthorizationRequestObject
    ]

    @property
    def request_uri(self) -> RequestURI:
        assert isinstance(self.__root__, AuthorizationRequestReference)
        return self.__root__.request_uri
    
    @pydantic.root_validator(pre=True)
    def preprocess(
        cls,
        values: dict[str, Any]
    ) -> dict[str, Any]:
        params: dict[str, Any] | None = values.get('__root__')
        if params:
            # request and request_uri are mutually exclusive.
            if params.get('request') and params.get('request_uri'):
                raise InvalidRequest(
                    "The request and request_uri parameters are mutually "
                    "exclusive."
                )
            
            is_complete = not any([params.get('request'), params.get('request_uri')])
            if is_complete and not params.get('response_type'):
                raise InvalidRequest("The response_type parameter is required.")
        return values
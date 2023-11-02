# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from headless.ext.oidc import types

from .authorizationrequeststatekey import AuthorizationRequestStateKey
from .iauthorizationserver import IAuthorizationServer
from .clientkey import ClientKey
from .iclient import IClient


class AuthorizationRequest(types.AuthorizationRequest):

    @property
    def client_id(self) -> ClientKey:
        return ClientKey(self.__root__.client_id)

    @property
    def key(self) -> AuthorizationRequestStateKey | types.NullIdentifier:
        if isinstance(self.__root__, types.AuthorizationRequestReference)\
        and self.__root__.request_uri.id is not None:
            return AuthorizationRequestStateKey(self.__root__.request_uri.id)

        return types.NullIdentifier()

    def is_new(self) -> bool:
        return isinstance(self.__root__,
            (types.AuthorizationRequestParameters, types.AuthorizationRequestObject)
        )
    
    def is_reference(self) -> bool:
        return isinstance(self.__root__, types.AuthorizationRequestReference)

    async def get_params(
        self,
        oauth2: IAuthorizationServer[Any],
        client: IClient
    ) -> types.AuthorizationRequestParameters:
        if not isinstance(self.__root__, types.AuthorizationRequestParameters):
            raise NotImplementedError(type(self.__root__).__name__)
        
        return self.__root__
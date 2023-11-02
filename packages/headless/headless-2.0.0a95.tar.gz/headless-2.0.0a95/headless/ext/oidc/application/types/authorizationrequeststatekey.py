# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from headless.ext.oidc.types import IObjectIdentifier

from .iauthorizationrequeststate import IAuthorizationRequestState


class AuthorizationRequestStateKey(IObjectIdentifier[str, IAuthorizationRequestState]):
    __id: str

    def __init__(self, request_id: str) -> None:
        self.__id = request_id

    def cast(self) -> str:
        return str(self.__id)
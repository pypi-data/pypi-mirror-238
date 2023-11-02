# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Protocol

from headless.ext.oidc.types import AuthorizationRequestParameters
from headless.ext.oidc.types import RedirectURI

from .basevalidator import BaseValidator
from .resourceidentifier import ResourceIdentifier


class IClient(Protocol):
    id: str

    def allows_redirect(self, uri: RedirectURI) -> bool: ...
    def allows_scope(self, scope: set[str]) -> bool: ...
    def default_redirect(self) -> RedirectURI: ...
    def get_sector_identifier(self) -> str: ...
    async def validate_request(self, params: AuthorizationRequestParameters) -> None: ...


class ClientIdentifier(ResourceIdentifier[IClient], BaseValidator[str]):


    @classmethod
    def __modify_schema__(
        cls,
        field_schema: dict[str, Any]
    ) -> None:
        field_schema.update( # pragma: no cover
            title='Client identifier',
            type='string',
        )

    def __init__(self, client_id: str) -> None:
        self.client_id = client_id

    def __str__(self) -> str:
        return self.client_id
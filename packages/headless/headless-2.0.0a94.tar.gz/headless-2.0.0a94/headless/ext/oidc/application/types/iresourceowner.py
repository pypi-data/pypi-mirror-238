# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Protocol
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .resourceownerkey import ResourceOwnerKey


class IResourceOwner(Protocol):

    @property
    def key(self) -> 'ResourceOwnerKey':
        ...

    def consents(self) -> set[str]: ...
    def must_consent(self, scope: set[str]) -> set[str]: ...
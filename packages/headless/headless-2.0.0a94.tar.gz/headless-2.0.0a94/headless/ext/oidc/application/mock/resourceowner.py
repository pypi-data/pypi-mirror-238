# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import dataclasses

from ..types import ResourceOwnerKey


@dataclasses.dataclass
class ResourceOwner:
    client_id: str
    sub: str
    ppid: str
    consented_scope: set[str]

    @property
    def key(self) -> ResourceOwnerKey:
        return ResourceOwnerKey(self.client_id, self.sub)

    def consents(self) -> set[str]:
        return {x for x in self.consented_scope}
    
    def must_consent(self, scope: set[str]) -> set[str]:
        return scope - self.consents()

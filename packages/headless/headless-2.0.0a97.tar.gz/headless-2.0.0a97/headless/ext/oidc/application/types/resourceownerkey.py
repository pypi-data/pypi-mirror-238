# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from .iresourceowner import IResourceOwner
from .iobjectidentifier import IObjectIdentifier


class ResourceOwnerKey(IObjectIdentifier[str, IResourceOwner]):
    client_id: str
    sub: str

    def __init__(self, client_id: str, sub: str) -> None:
        self.client_id = client_id
        self.sub = sub

    def cast(self) -> str:
        return f'{self.client_id}/{self.sub}'
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
from typing import TypeVar

from headless.ext.oidc.types import IObjectIdentifier


T = TypeVar('T')


class IServerStorage(Protocol):

    async def get(self, key: IObjectIdentifier[Any, T]) -> T | None: ...
    async def persist(self, object: Any) -> None: ...
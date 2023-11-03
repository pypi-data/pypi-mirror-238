# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import functools
from typing import Any
from typing import TypeVar

from headless.ext.oidc.types import IObjectIdentifier
from headless.ext.oidc.types import NullIdentifier

from ..types import AuthorizationRequestStateKey
from ..types import ClientKey
from ..types import IClient
from ..types import IResourceOwner
from ..types import ResourceOwnerKey
from .authorizationrequeststate import AuthorizationRequestState
from .resourceowner import ResourceOwner


T = TypeVar('T')


class MockStorage:
    objects: dict[IObjectIdentifier[Any, Any] | str, Any]
    requests: dict[str, AuthorizationRequestState] = {}

    def __init__(
        self,
        clients: list[IClient]
    ):
        self.objects = {}
        self.objects.update({x.id: x for x in clients})

    @functools.singledispatchmethod
    async def _get(self, key: IObjectIdentifier[Any, T]) -> T | None:
        raise NotImplementedError(
            f"Unable to lookup object using {type(key).__name__}"
        )
    
    @_get.register
    async def null(self, key: NullIdentifier) -> None:
        return None

    @_get.register
    async def _get_authorization_request(
        self,
        key: AuthorizationRequestStateKey
    ) -> Any | None:
        return await self.get_authorization_request(key)

    @_get.register
    async def _get_client(
        self,
        key: ClientKey
    ) -> Any | None:
        return await self.get_client(key)

    @_get.register
    async def _get_resource_owner(
        self,
        key: ResourceOwnerKey
    ) -> Any | None:
        return await self.get_resource_owner(key)

    async def get(self, key: IObjectIdentifier[Any, T]) -> T | None:
        return await self._get(key)

    async def get_authorization_request(
        self,
        key: AuthorizationRequestStateKey
    ) -> AuthorizationRequestState | None:
        return self.requests.get(key.cast())

    async def get_client(
        self,
        key: ClientKey
    ) -> IClient | None:
        return self.objects.get(key.cast())

    async def get_resource_owner(
        self,
        key: ResourceOwnerKey
    ) -> IResourceOwner | None:
        return self.objects.get(key.cast())

    async def persist(self, object: Any) -> None:
        return await self._persist(object)

    @functools.singledispatchmethod
    async def _persist(self, object: Any) -> None:
       raise NotImplementedError(f"Unsupported object: {type(object).__name__}")
    
    @_persist.register
    async def _persist_authorization_request_state(
        self,
        obj: AuthorizationRequestState
    ):
        return await self.persist_authorization_request_state(obj)
    
    @_persist.register
    async def persist_authorization_request_state(
        self,
        obj: AuthorizationRequestState
    ) -> None:
        self.objects[obj.id] = obj
    
    @_persist.register
    async def _persist_resource_owner(
        self,
        obj: ResourceOwner
    ):
        return await self.persist_resource_owner(obj)
    
    @_persist.register
    async def persist_resource_owner(
        self,
        obj: ResourceOwner
    ) -> None:
        self.objects[obj.key.cast()] = obj
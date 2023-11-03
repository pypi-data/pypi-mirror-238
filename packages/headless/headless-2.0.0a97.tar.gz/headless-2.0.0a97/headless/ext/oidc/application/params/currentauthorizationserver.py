# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

import fastapi

from ..types import IAuthorizationServer
from ..types import Request


__all__: list[str] = ['CurrentAuthorizationServer']


def get(request: Request) -> IAuthorizationServer[Any]:
    return request.oauth2


CurrentAuthorizationServer: IAuthorizationServer[Any] = fastapi.Depends(get)
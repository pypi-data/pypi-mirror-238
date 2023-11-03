# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import fastapi

from ..types import IAuthorizationServer
from .currentauthorizationserver import CurrentAuthorizationServer


__all__: list[str] = ['Issuer']




def get(
    request: fastapi.Request,
    oauth2: IAuthorizationServer = CurrentAuthorizationServer,
) -> str:
    return oauth2.get_issuer() or f'{request.url.scheme}://{request.url.netloc}'
    

Issuer: str = fastapi.Depends(get)
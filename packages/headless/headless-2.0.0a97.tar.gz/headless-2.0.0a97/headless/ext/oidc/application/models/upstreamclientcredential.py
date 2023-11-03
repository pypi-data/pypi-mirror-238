# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Literal
from typing import Union

import pydantic


class RawClientSecret(pydantic.BaseModel):
    kind: Literal['client_secret']
    client_secret: str



class ReferencedClientSecret(pydantic.BaseModel):
    kind: Literal['client_secret']
    ref: str


class UpstreamClientCredential(pydantic.BaseModel):
    __root__: Union[
        RawClientSecret,
        ReferencedClientSecret
    ]

    async def get(self) -> RawClientSecret:
        raise NotImplementedError
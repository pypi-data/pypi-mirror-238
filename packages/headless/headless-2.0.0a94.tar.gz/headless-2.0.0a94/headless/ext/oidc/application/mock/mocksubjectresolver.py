# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import dataclasses
from typing import Annotated

import fastapi
from canonical import ResourceName
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBasic
from fastapi.security import HTTPBasicCredentials

from ..types import IRequestSubject


security = HTTPBasic()


class MockSubjectResolver:
    credentials: HTTPBasicCredentials
    username: str = 'username'
    password: str = 'password'

    def __init__(
        self,
        credentials: Annotated[HTTPBasicCredentials, fastapi.Depends(security)]
    ):
        self.credentials = credentials

    async def current(self) -> IRequestSubject | None:
        if self.credentials.username != self.username\
        or self.credentials.password != self.password:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Basic"},
            )
        return MockSubject(username=self.username)


@dataclasses.dataclass
class MockSubject:
    username: str

    @property
    def resource_name(self) -> ResourceName:
        return ResourceName(f'//localhost/subjects/{self.username}')
    
    def identifier(self) -> str:
        return self.username
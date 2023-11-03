# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import dataclasses
from typing import Literal


@dataclasses.dataclass
class ClientSecret:
    client_id: str
    client_secret: str
    mode: Literal['client_secret_basic', 'client_secret_post', 'client_secret_jwt'] | None
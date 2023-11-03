# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.


class Error(Exception):
    __module__: str = 'headless.ext.oidc.types'
    error: str
    error_description: str | None = None
    error_url: str | None = None

    @classmethod
    def invalid_request(cls, description: str):
        return cls(error='invalid_request', error_description=description)

    def __init__(
        self,
        *,
        error: str,
        error_description: str | None,
        error_url: str | None = None
    ):
        self.error = error
        self.error_description = error_description
        self.error_url = error_url

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        return f"Error('{self.error}', '{self.error_description or 'None'}')"
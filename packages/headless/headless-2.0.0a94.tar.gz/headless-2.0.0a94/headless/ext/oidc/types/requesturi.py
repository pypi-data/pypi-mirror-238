# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import urllib.parse
from typing import Any
from typing import Callable
from typing import Generator
from typing import TypeVar

from pydantic.validators import str_validator

from .fatalerror import InvalidRequest


T = TypeVar('T', bound='RequestURI')


class RequestURI(str):
    __module__: str = 'headless.ext.oidc.types'
    _parsed: urllib.parse.ParseResult
    _request_id: str | None

    @property
    def id(self) -> str | None:
        return self._request_id

    @classmethod
    def __modify_schema__(
        cls,
        field_schema: dict[str, Any]
    ) -> None:
        field_schema.update( # pragma: no cover
            title='Request URI',
            type='string',
            format='uri'
        )

    @classmethod
    def __get_validators__(cls: type[T]) -> Generator[Callable[..., str | T], None, None]:
        yield str_validator
        yield cls.validate

    @classmethod
    def validate(cls: type[T], v: str) -> T:
        if len(v) > 2048:
            raise InvalidRequest('Provided value is too long to be a URI.')
        p = urllib.parse.urlparse(v)
        if p.scheme in {'http', 'https'} and not p.netloc:
            raise InvalidRequest('Provided value is not a valid URI.')
        if not p.scheme:
            raise InvalidRequest(f"The request_uri parameter must be a valid URN.")
        if p.scheme not in {'urn', 'https'}:
            raise InvalidRequest(f'The request_uri parameter uses an unknown scheme.')
        return cls(urllib.parse.urlunparse(p))

    def __new__(cls, object: str):
        instance = super().__new__(cls, object)
        instance._parsed = urllib.parse.urlparse(object)
        instance._request_id = None
        if instance._parsed.scheme == 'urn':
            instance._request_id = str.rsplit(instance, ':', 1)[-1]
        return instance
    
    def is_external(self) -> bool:
        return self._parsed.scheme in {'http', 'https'}

    def __repr__(self) -> str: # pragma: no cover
        return f'RequestURI({self})'
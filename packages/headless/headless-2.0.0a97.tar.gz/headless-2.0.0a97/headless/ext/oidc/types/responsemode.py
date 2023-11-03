# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""Declares :class:`ResponseType`."""
import enum

from .fatalerror import InvalidRequest
from .parameters import ResponseType


RESPONSE_TYPE_DEFAULTS: dict[str, str] = {
    'code'  : 'query',
    'token' : 'fragment'
}


class ResponseMode(str, enum.Enum):
    form_post = 'form_post'
    form_post_jwt = 'form_post.jwt'
    fragment = 'fragment'
    fragment_jwt = 'fragment.jwt'
    jwt = 'jwt'
    none = 'none'
    query = 'query'
    query_jwt = 'query.jwt'

    @classmethod
    def default(cls, response_type: ResponseType) -> 'ResponseMode':
        if response_type not in RESPONSE_TYPE_DEFAULTS:
            raise InvalidRequest(f"No default response mode known for {response_type}.")
        return ResponseMode(RESPONSE_TYPE_DEFAULTS[response_type])
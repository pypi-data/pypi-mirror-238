# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from .error import Error


class FatalError(Error):
    """An implementation of :class:`~headless.ext.oicd.types.Error` that
    represent an exception that fatally exits the authorization flow.
    """
    __module__: str = 'headless.ext.oidc.types'


class InvalidScope(FatalError):
    __module__: str = 'headless.ext.oidc.types'

    def __init__(self, description: str, url: str | None = None):
        super().__init__(
            error='invalid_scope',
            error_description=description,
            error_url=url
        )


class InvalidRequest(FatalError):
    __module__: str = 'headless.ext.oidc.types'

    def __init__(self, description: str, url: str | None = None):
        super().__init__(
            error='invalid_request',
            error_description=description,
            error_url=url
        )


class UnauthorizedClient(FatalError):
    __module__: str = 'headless.ext.oidc.types'

    def __init__(self, description: str, url: str | None = None):
        super().__init__(
            error='unauthorized_client',
            error_description=description,
            error_url=url
        )


class UnsupportedResponseType(FatalError):
    __module__: str = 'headless.ext.oidc.types'

    def __init__(self, description: str, url: str | None = None):
        super().__init__(
            error='unsupported_response_type',
            error_description=description,
            error_url=url
        )
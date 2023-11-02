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

from ..types import ISubjectResolver
from ..utils import set_signature_defaults


__all__: list[str] = ['CurrentSubject']


def CurrentSubject(
    *,
    subjects: type[ISubjectResolver],
    required: bool
) -> Any:

    async def get(subjects: ISubjectResolver):
        subject = await subjects.current()
        if subject is None and required:
            raise NotImplementedError
        return subject

    get = set_signature_defaults(get, {
        'subjects': fastapi.Depends(subjects)
    })
    return fastapi.Depends(get, use_cache=True)
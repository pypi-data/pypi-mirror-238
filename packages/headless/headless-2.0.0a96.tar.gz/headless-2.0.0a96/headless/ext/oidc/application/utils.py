# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import inspect
from collections import OrderedDict
from typing import Any
from typing import Callable


def set_signature_defaults(
    callable: Callable[..., Any],
    defaults: dict[str, Any]
) -> Callable[..., Any]:
    sig = inspect.signature(callable)
    params = OrderedDict(sig.parameters.items())
    for name, default in defaults.items():
        if name not in params:
            raise ValueError(f"No such argument: {name}")
        params[name] = inspect.Parameter(
            kind=params[name].kind,
            name=params[name].name,
            default=default,
            annotation=params[name].annotation
        )

    async def f(*args: Any, **kwargs: Any) -> Any:
        return await callable(*args, **kwargs)
    f.__signature__ = sig.replace(parameters=list(params.values())) # type: ignore
    return f
from typing import Any, Dict, Optional

import cachetools
from typing_extensions import get_type_hints


@cachetools.cached(key=lambda obj, include_extras=False, *_, **__: (obj, include_extras), cache=dict())
def cached_get_type_hints(obj: type, include_extras: bool = False, globalns: Optional[Dict[str, Any]] = None):
    return get_type_hints(obj, include_extras=include_extras, globalns=globalns)

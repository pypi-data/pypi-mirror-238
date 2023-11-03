from . import locations
from . import systems
from . import files

def enable_cache() -> None:

    from . import cache
    cache.Cache.use_cache = True


def disable_cache() -> None:

    from . import cache
    cache.Cache.use_cache = False

def clear_cache(metadata_only:bool = False) -> None:

    from . import cache
    cache.Cache.clear(metadata_only)
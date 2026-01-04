import json

from api.cache.memory import MemoryCacheAdapter

cache_store = MemoryCacheAdapter()

CACHE_KEY_PREFIX_USER_LAST_ENTRY = "user_last_entry"
CACHE_KEY_PREFIX_USER_ENTRY_COUNT = "user_entry_count"


def cache_entry_as_user_last_entry(user_id: int, subject: str, message: str):
    cache_payload = json.dumps({
        "subject": subject,
        "message": message,
    })
    cache_store.put(f"{CACHE_KEY_PREFIX_USER_LAST_ENTRY}:{user_id}", cache_payload)


def get_user_last_entry_from_cache(user_id: int) -> dict[str, str] | None:
    result = cache_store.get(f"{CACHE_KEY_PREFIX_USER_LAST_ENTRY}:{user_id}")
    if result is None:
        return None

    return json.loads(result)

def increment_user_entry_count_on_cache(user_id: int):
    cache_store.increment(f"{CACHE_KEY_PREFIX_USER_ENTRY_COUNT}:{user_id}")


def get_user_entry_count_from_cache(user_id: int) -> int | None:
    return cache_store.get(f"{CACHE_KEY_PREFIX_USER_ENTRY_COUNT}:{user_id}")

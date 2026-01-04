from typing import Any
from threading import Lock


# Redis can be used instead of in memory cache.
class MemoryCacheAdapter:
    # TODO add a method to retrieve cache data for multiple keys.

    def __init__(self):
        self.storage: dict[str, Any] = {}
        self._lock = Lock()

    def put(self, key: str, value: Any):
        with self._lock:
            self.storage[key] = value

    def increment(self, key: str, delta: int = 1):
        with self._lock:
            if key in self.storage:
                value = self.storage[key]
                self.storage[key] = value + delta
            else:
                self.storage[key] = delta

    def get(self, key: str) -> Any | None:
        with self._lock:
            return self.storage.get(key)

    def flush(self):
        self.storage.clear()

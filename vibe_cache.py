import json
from pathlib import Path
import threading


class VibeQueryCache:
    def __init__(self, path: str):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.lock = threading.Lock()
        if self.path.exists():
            with open(self.path, "r", encoding="utf-8") as f:
                self.cache = json.load(f)
        else:
            self.cache = {}

    def _make_key(self, media_id: str, title: str, model_name: str) -> str:
        return f"{media_id}::{title}::{model_name}"

    def get(self, media_id: str, title: str, model_name: str):
        key = self._make_key(media_id, title, model_name)
        return self.cache.get(key)

    def set(self, media_id: str, title: str , model_name: str, queries: list):
        key = self._make_key(media_id, title, model_name)
        with self.lock:  # Thread-safe update
            self.cache[key] = queries
            print(f"Caching {key}")
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self.cache, f, indent=2)
import collections.abc
from typing import Optional


class BaseLoader:
    EXTENSIONS = ()

    def load(self, filename: str, encoding: Optional[str] = None) -> None:
        raise NotImplementedError

    def get_key(self, d, k, v):
        val = d.get(k, {})
        if val is None and v:
            return {}
        return val

    def update(self, d, u):
        if not u:
            return d
        for k, v in u.items():
            if isinstance(v, collections.abc.Mapping):
                d[k] = self.update(self.get_key(d, k, v), v)
            else:
                d[k] = v
        return d

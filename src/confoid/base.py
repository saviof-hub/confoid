from __future__ import annotations

from typing import Any, Dict


class Settings(dict):
    def __contains__(self, k: str) -> bool:
        try:
            return dict.__contains__(self, k) or hasattr(self, k)
        except Exception:
            return False

    def __getattr__(self, k: str) -> Any:
        try:
            # Throws exception if not in prototype chain
            return object.__getattribute__(self, k)
        except AttributeError:
            try:
                return self[k]
            except KeyError:
                raise AttributeError(k)

    def __setattr__(self, k: str, v: Any) -> None:
        try:
            # Throws exception if not in prototype chain
            object.__getattribute__(self, k)
        except AttributeError:
            try:
                self[k] = v
            except Exception:
                raise AttributeError(k)
        else:
            object.__setattr__(self, k, v)

    def __delattr__(self, k: str) -> None:
        try:
            # Throws exception if not in prototype chain
            object.__getattribute__(self, k)
        except AttributeError:
            try:
                del self[k]
            except KeyError:
                raise AttributeError(k)
        else:
            object.__delattr__(self, k)

    def as_dict(self) -> Dict[str, Any]:
        return settings_to_dict(self)

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> Settings:
        return dict_to_settings(d)


def dict_to_settings(x: Dict[str, Any]) -> Settings:
    if isinstance(x, dict):
        return Settings((k, dict_to_settings(v)) for k, v in dict.items(x))
    elif isinstance(x, (list, tuple)):
        return type(x)(dict_to_settings(v) for v in x)
    else:
        return x


def settings_to_dict(x: Settings) -> Dict[str, Any]:
    if isinstance(x, dict):
        return dict((k, settings_to_dict(v)) for k, v in dict.items(x))
    elif isinstance(x, (list, tuple)):
        return type(x)(settings_to_dict(v) for v in x)
    else:
        return x

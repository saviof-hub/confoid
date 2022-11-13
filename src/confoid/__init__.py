from __future__ import annotations

import os
from typing import Dict, List, Optional, Union

from . import exceptions, loaders
from .base import Settings
from .constants import ENV_VARS
from .validator import Validator, ValidatorList

CONFIGS: Dict[str, Settings] = {}


class Resolver:
    def __init__(self, prefix: str, **kwargs) -> None:
        self.prefix = prefix
        self.kwargs = kwargs
        self.base_dir = ""
        self.current_env = "local"
        self.files: Optional[Union[str, List[str]]] = None
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.resolve()
        self.expand()

    @staticmethod
    def to_full_path(base_dir: str, path: str) -> str:
        return os.path.join(base_dir, path)

    def setattr_from_env(
        self, key, env: str, default: Optional[str] = ""
    ) -> Union[str, None]:
        _value = os.getenv(f"{self.prefix}_{env}")
        if _value:
            setattr(self, key, _value)
        if not getattr(
            self, key, None
        ):  # value is still None then set fallback (default) value
            setattr(self, key, default)
        return os.getenv(f"{self.prefix}_{env}", default)

    def resolve(self) -> Resolver:
        for key, value in ENV_VARS.items():
            self.setattr_from_env(key, value[0], default=value[1])
        return self

    def expand(self) -> Resolver:
        if not self.files:
            return self

        files = self.files
        if isinstance(files, str):
            files = [files]
        files = [self.to_full_path(self.base_dir, x) for x in files]
        valid_files = []
        for _file in files:
            if not os.path.exists(_file):
                print(f"{_file}: does not exists.. skipping")
            else:
                valid_files.append(_file)
        if not valid_files:
            error = f"No valid files found, checked {files}"
            raise exceptions.ResolveError(error)

        if len(valid_files) == 1 and self.current_env:
            name, ext = os.path.splitext(valid_files[0])
            env_file = f"{name}.{self.current_env}.{ext[1:]}"
            if os.path.exists(env_file):
                valid_files.append(env_file)
        self.files = valid_files
        return self

    def validate(self) -> Resolver:
        for key, _ in self.kwargs.items():
            _value = getattr(self, key)
            if _value is None:
                env_var = f"{self.prefix}_{ENV_VARS[key][0]}"
                error = f"No {key} provided to config also checked env: {env_var}"
                raise exceptions.ResolveError(error)
        return self


def Config(
    prefix: str,
    files: Optional[Union[str, List[str]]] = None,
    base_dir: Optional[str] = "",
    current_env: Optional[str] = "local",
    validators: Optional[List[Validator]] = [],
    reload: bool = False,
    env_default_value: Optional[str] = "N/A",
) -> Union[bool, Settings]:  # noqa

    if not reload and prefix in CONFIGS:
        return CONFIGS[prefix]

    resolver = Resolver(
        prefix, base_dir=base_dir, current_env=current_env, files=files
    ).validate()

    print(f"{prefix}: Setting environment: {resolver.current_env}")
    print(f"{prefix}: Using config files: {resolver.files}")

    data = loaders.settings_loader(resolver.files, env_default_value=env_default_value)
    settings = Settings.from_dict(data)
    settings.current_env = resolver.current_env
    ValidatorList(settings, validators).validate()
    CONFIGS[prefix] = settings

    return settings

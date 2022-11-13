import os
import re
from typing import List, Optional

import yaml
from confoid import constants
from confoid.loaders.base import BaseLoader

from typing import Dict

default_sep = ":"
default_value = "N/A"
raise_if_na = False

default_sep = default_sep or ""
default_sep_pattern = r"(" + default_sep + "[^}]+)?" if default_sep else ""
pattern = re.compile(
    r".*?\$\{([^}{" + default_sep + r"]+)" + default_sep_pattern + r"\}.*?"
)


class ENV(dict):
    """Env class."""

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        for key, value in kwargs.items():
            if not os.getenv(key):
                os.environ[key] = value

    def to_dict(self):
        return self.kwargs


class YAMLLoader(BaseLoader):
    EXTENSIONS = constants.YAML_EXTENSIONS

    def __init__(self, env_default_value=None) -> None:
        self.loader = yaml.SafeLoader
        self.encoding = "utf-8"
        self.tag = "!ENV"
        self.loader.add_constructor("!Environment", self.env_constructor)
        self.loader.add_implicit_resolver(self.tag, pattern, None)
        self.loader.add_constructor(self.tag, self.constructor_env_variables)

        if env_default_value is not None:
            global default_value
            default_value = env_default_value

    @classmethod
    def loader(cls, filenames: List[str], env_default_value=None) -> Dict[str, str]:
        data = {}
        loader = cls(env_default_value=env_default_value)
        for filename in filenames:
            _data = loader.load(filename)
            data = loader.update(data, _data)
        return data

    def load(self, filename: str, encoding: Optional[str] = None):
        settings = {}
        with open(filename, encoding=encoding or self.encoding) as conf_data:
            settings = yaml.load(conf_data, Loader=self.loader)  # nosec
        return settings

    @staticmethod
    def env_constructor(loader: yaml.SafeLoader, node: yaml.nodes.MappingNode) -> ENV:
        """Construct an env node."""
        return ENV(**loader.construct_mapping(node)).to_dict()

    @staticmethod
    def clean_value(value):
        if value.startswith(('"', "'")):
            value = value[1:]

        if value.endswith(('"', "'")):
            value = value[:-1]
        return value

    @staticmethod
    def get_env_fallback(g, key, default_value):
        curr_default_value = default_value
        found = False
        for each in g:
            if default_sep in each:
                _, curr_default_value = each.split(default_sep, 1)
                if curr_default_value:
                    curr_default_value = YAMLLoader.clean_value(curr_default_value)
                    found = True
                    break
        if not found and raise_if_na:
            raise ValueError(f"Could not find default value for {key}")
        return curr_default_value

    @staticmethod
    def constructor_env_variables(loader, node):
        value = loader.construct_scalar(node)
        match = pattern.findall(value)  # to find all env variables in line
        if not match:
            return value

        full_value = value
        for g in match:
            curr_default_value = default_value
            env_var_name = g
            env_var_name_with_default = g
            if default_sep and isinstance(g, tuple) and len(g) > 1:
                env_var_name = g[0]
                env_var_name_with_default = "".join(g)
                curr_default_value = YAMLLoader.get_env_fallback(
                    g, env_var_name, curr_default_value
                )
            full_value = full_value.replace(
                f"${{{env_var_name_with_default}}}",
                os.environ.get(env_var_name, curr_default_value),
            )
        return full_value

import os
from typing import List, Optional, Union

from confoid.exceptions import MixedFileTypes

from .base import BaseLoader
from .yaml_loader import YAMLLoader


def settings_loader(
    filenames=Union[str, List[str]], env_default_value=None
) -> Optional[BaseLoader]:
    exts = list(set([os.path.splitext(filename)[-1] for filename in filenames]))
    if not len(exts) == 1:  # all discovered files should have same extension
        raise MixedFileTypes("Settings files cannot contained mixed filetypes")

    exts = exts[0]
    if exts in YAMLLoader.EXTENSIONS:
        return YAMLLoader.loader(filenames, env_default_value=env_default_value)
    return None

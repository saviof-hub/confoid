import pytest
from confoid import exceptions, loaders
from confoid.loaders import base


def test_base_load():
    _base = base.BaseLoader()
    with pytest.raises(NotImplementedError):
        _base.load("test")


def test_settings_loader_errors():
    data = loaders.settings_loader(["test"])
    assert data is None

    with pytest.raises(exceptions.MixedFileTypes):
        loaders.settings_loader(["test.yml", "test.toml"])

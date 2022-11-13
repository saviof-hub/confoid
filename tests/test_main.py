import pytest
from confoid import Settings


@pytest.mark.parametrize(
    "basedir, filename", [
        ("test", "test.yml"),
        ("new", "old.yml")
    ]
)
def test_resolver_fullpath(resolver, basedir, filename):
    path = resolver.to_full_path(basedir, filename)
    assert path == f"{basedir}/{filename}"


def test_config(config, load_yaml):
    base_dir = "tests/config/yml"
    base_config_name = "base.application"

    settings = config(base_dir, base_config_name, env_default_value="")
    assert isinstance(settings, Settings)

    expected = load_yaml(f"{base_dir}/{base_config_name}.result.yml")

    assert settings.get("default") == expected.get("default")
    assert settings.default.redis.password == expected["default"]["redis"]["password"]


def test_config_env_var(config, monkeypatch):
    new_password = 'testenv'
    monkeypatch.setenv('TEST_SERVICE_DEFAULT_PASSWORD', new_password)

    settings = config("tests/config/yml", "base.application")
    assert isinstance(settings, Settings)
    assert settings.default.redis.password == new_password

def test_config_env_var_default_value(config):
    new_password = 'testenv'
    settings = config("tests/config/yml", "base.application", env_default_value=new_password)
    assert isinstance(settings, Settings)
    assert settings.default.random == new_password

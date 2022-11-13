import pytest
import yaml
from confoid import Config, Resolver


@pytest.fixture
def resolver():
    return Resolver("test")

@pytest.fixture
def config():
    def get_config(base_dir, config, current_env="testing", validators=[], env_default_value=None):
        return Config(
            files=f"{config}.yml",
            prefix="TEST_SERVICE",
            base_dir=base_dir,
            current_env=current_env,
            validators=validators,
            reload=True,
            env_default_value=env_default_value
        )
    return get_config

@pytest.fixture
def load_yaml():
    def load_yaml(filename):
        with open(filename, 'r') as file:
            return yaml.safe_load(file)
    return load_yaml

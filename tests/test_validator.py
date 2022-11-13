import pytest
from confoid import Settings, Validator, exceptions


def test_validator(config):
    settings = config(
        "tests/config/yml", "base.application",
        validators=[
            Validator("default", must_exist=True, env=["development"])
        ])

    assert isinstance(settings, Settings)


def test_validator_errors(config):
    with pytest.raises(exceptions.ValidationError):
        config(
            "tests/config/yml", "base.application",
            validators=[
                Validator("defaults", must_exist=True, env="development")
            ])


def test_validator_single(config):
    settings = config(
        "tests/config/yml", "base.application",
        validators=Validator("defaults", must_exist=True, env="development"))
    assert isinstance(settings, Settings)

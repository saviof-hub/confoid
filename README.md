# Confoid

Configuration Management for Python.


[![image](https://img.shields.io/pypi/v/confoid.svg)](https://pypi.org/project/confoid/)
[![image](https://img.shields.io/pypi/pyversions/confoid.svg)](https://pypi.org/project/confoid/)
[![GitHub license](https://img.shields.io/github/license/saviof-hub/confoid.svg)](https://github.com/saviof-hub/confoid/blob/main/LICENSE)

[![GitHub Actions (Python package)](https://github.com/artbycrunk/hyper-prompt/workflows/Tests/badge.svg)](https://github.com/artbycrunk/hyper-prompt)

[![Average time to resolve an issue](https://isitmaintained.com/badge/resolution/saviof-hub/confoid.svg)](https://isitmaintained.com/project/saviof-hub/confoid "Average time to resolve an issue")
[![Percentage of issues still open](https://isitmaintained.com/badge/open/saviof-hub/confoid.svg)](https://isitmaintained.com/project/saviof-hub/confoid "Percentage of issues still open")


## Install

```bash
$ pip install confoid
```

## Loading a single config file

```py
import confoid

new_settings = confoid.Config("application.yml")
```

## Loading multiple  config file

Multiple files can be provided in `order` and will merge with the previous configuration.

```py
import confoid

config_files = ["application.yml", "application.development.yml"]

new_settings = confoid.Config(
    config_files, 
    base_dir="config",
)
```

## Autoload based on provided environment

```py
import confoid

new_settings = confoid.Config("application.yml", current_env="development")
# this will load application.yml and application.{current_env}.yml
```

## Reading the settings

```py
settings.username == "admin"  # dot notation with multi nesting support
settings['password'] == "secret123"  # dict like access
settings.get("nonexisting", "default value")  # Default values just like a dict
settings.databases.name == "mydb"  # Nested key traversing
```

## Config merging

application.yml
```yml
default:
  prefix:
    otp: "user-otp"
    auth: "auth-tokens"
  type: inmemory
  redis:
    url: 
```

application.development.yml
```yml
default:
  type: redis
  redis:
    url: redis://saviof.com
    encoding: "utf8"
```

Will resolve to the following final config

```yml
default:
  prefix:
    otp: "user-otp"
    auth: "auth-tokens"
  type: redis
  redis:
    url: redis://saviof.com
    encoding: "utf8"
```

## Config environment vars

All fields can use environment variables with a fallback default value
```yml
password: ${TEST_SERVICE_DEFAULT_PASSWORD:test}
```

## Validators can be added for pre checks on loaded config
```python
from confoid import Validator

config_files = ["application.yml", "application.development.yml"]

new_settings = confoid.Config(
    config_files, 
    base_dir="config",
    validators=[
        Validator("default", "default.redis.password", must_exist=True)
        Validator("otp.length", gte=6, lte=20)
        Validator("default.type", values=["inmemory", "redis"])
    ]
)
```

from __future__ import annotations

from types import MappingProxyType
from typing import Any, Callable, Optional, Sequence, Union

from . import exceptions


class Empty:
    def __str__(self) -> str:
        return "EMPTY"


empty = Empty()


class Validator:
    default_messages = MappingProxyType(
        {
            "must_exist_true": "{name} is required in env {env}",
            "must_exist_false": "{name} cannot exists in env {env}",
            "condition": "{name} invalid for {function}({value}) in env {env}",
            "operations": (
                "{name} must {operation} {op_value} " "but it is {value} in env {env}"
            ),
            "combined": "combined validators failed {errors}",
        }
    )

    def __init__(
        self,
        *names: str,
        must_exist: Optional[bool] = None,
        required: Optional[bool] = None,  # alias for `must_exist`
        condition: Optional[Callable[[Any], bool]] = None,
        when: Optional[Validator] = None,
        env: Optional[Union[str, Sequence[str]]] = None,
        # messages: Optional[Dict[str, str]] = None,
        default: Optional[Union[Any, Callable[[Any, Validator], Any]]] = empty,
        description: Optional[str] = None,
        **operations: Any,
    ) -> None:
        self.messages = dict(self.default_messages)
        # if messages:
        #     self.messages.update(messages)

        self.names = names
        self.must_exist = must_exist if must_exist is not None else required
        self.condition = condition
        self.when = when
        self.operations = operations
        self.default = default
        self.description = description
        self.envs: Optional[Sequence[str]] = None

        if isinstance(env, str):
            self.envs = [env]
        elif isinstance(env, (list, tuple)):
            self.envs = env

    def validate(
        self,
        settings: Any,
        env: Optional[str] = None,
    ) -> None:
        print("self.must_exist", self.names, self.must_exist)
        env = env or settings.current_env
        for name in self.names:

            value = settings.get(name)

            if self.must_exist is True and value is None:
                raise exceptions.ValidationError(
                    self.messages["must_exist_true"].format(name=name, env=env)
                )


class ValidatorList(list):
    def __init__(
        self,
        settings: Any,
        validators: Optional[Sequence[Validator]] = None,
        *args: Validator,
        **kwargs: Any,
    ) -> None:
        if isinstance(validators, (list, tuple)):
            args = list(args) + list(validators)
        super(ValidatorList, self).__init__(args, **kwargs)  # type: ignore
        self.settings = settings

    def validate(
        self,
    ) -> None:
        for validator in self:
            validator.validate(self.settings)

import re

from fastapi_exception import MissingError, throw_validation_with_exception
from pydantic_core import core_schema

from fastapi_validation.custom_errors.value_error import InvalidValueError

PASSWORD_REGEX = r'^(?=.*[A-Z])(?=.*\d)\S{6,}$'


class PasswordValidation:
    @classmethod
    def __get_pydanctic_json_schema__(cls, field_schema):
        field_schema.update(
            pattern=PASSWORD_REGEX,
            examples=['Secret@1234'],
        )

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source,
        _handler,
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(cls._validate, core_schema.str_schema())

    @classmethod
    def _validate(cls, value):
        if not isinstance(value, str) or not value:
            throw_validation_with_exception(MissingError(('body', 'password')))

        if not re.search(PASSWORD_REGEX, value):
            throw_validation_with_exception(InvalidValueError('password', ('body', 'password')))

        return value

    def __repr__(self):
        return f'PasswordValidation({super().__repr__()})'

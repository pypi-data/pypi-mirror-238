from inspect import isfunction
from typing import Any, Optional

from fastapi_global_variable import GlobalVariable
from sqlalchemy import text

from ..types.custom_condition_type import CustomCondition
from .base_exist_validator import BaseExistValidator


class SqlExists(BaseExistValidator):
    def __init__(
        self,
        table,
        column: Any,
        case_insensitive: bool = False,
        customs: Optional[list[CustomCondition]] = [],
    ):
        self.table = table
        self.column = column
        self.case_insensitive = case_insensitive
        self.customs = customs

    def validate(self, *criterion):
        return GlobalVariable.get_or_fail('run_with_global_session')(
            lambda session: session.query(self.table).with_entities(self.table.id).filter(*criterion).first()
        )

    def init_criterion(self, value: Any):
        if self.case_insensitive:
            return {text(f'"{self.table}".{self.column} ILIKE :value').bindparams(value=value)}

        return {text(f'"{self.table}".{self.column} = :value').bindparams(value=value)}

    def build_custom_criterion(self, criterion, values: dict[str, Any]):
        for custom in self.customs:
            custom['exclude'] = False if 'exclude' not in custom else custom.get('exclude')
            custom_column = custom['column']
            custom_value = custom.get('value')(values) if isfunction(custom.get('value')) else custom.get('value')

            sub_criterion = set()
            if custom['exclude']:
                if not custom_value or custom_value is None:
                    sub_criterion.add(text(f'"{self.table}.{custom_column} IS NOT NULL'))
                else:
                    sub_criterion.add(
                        text(f'"{self.table}".{custom_column} != :custom_value').bindparams(custom_value=custom_value)
                    )
            else:
                if not custom_value or custom_value is None:
                    sub_criterion.add(text(f'"{self.table}".{custom_column} IS NULL'))
                else:
                    sub_criterion.add(
                        text(f'"{self.table}".{custom_column} = :custom_value').bindparams(custom_value=custom_value)
                    )

            criterion.add(*sub_criterion)

from abc import abstractmethod
from typing import Any

from fastapi_validation.types.custom_condition_type import CustomCondition


class BaseExistValidator:
    @abstractmethod
    def validate(self, *criterion):
        pass

    @abstractmethod
    def init_criterion(self, case_insensitive: bool, table_name: str, column: str, value: Any):
        pass

    @abstractmethod
    def build_custom_criterion(
        self, criterion, table_name: str, values: dict[str, Any], customs: list[CustomCondition] = []
    ):
        pass

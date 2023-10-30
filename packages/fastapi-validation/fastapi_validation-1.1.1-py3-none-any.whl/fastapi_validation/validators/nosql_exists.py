import re
from inspect import isfunction
from typing import Any, Optional

from beanie.odm.queries.find import FindOne

from ..models.projection_model import ProjectionModel
from ..types.custom_condition_type import CustomCondition
from .base_exist_validator import BaseExistValidator


class NosqlExists(BaseExistValidator):
    def __init__(
        self,
        document: Any,
        property: Any,
        case_insensitive: bool = False,
        customs: Optional[list[CustomCondition]] = [],
    ):
        self.document = document
        self.property = property
        self.case_insensitive = case_insensitive
        self.customs = customs

    def validate(self, *criterion):
        return FindOne(self.document).find_one(*criterion, projection_model=ProjectionModel)

    def init_criterion(self, value: Any):
        if self.case_insensitive:
            pattern = re.compile(f".*{re.escape(value)}.*", re.IGNORECASE)
            return {self.property: {'$regex': pattern}}

        return {self.property: value}

    def build_custom_criterion(self, criterion, values: dict[str, Any]):
        for custom in self.customs:
            custom['exclude'] = False if 'exclude' not in custom else custom.get('exclude')
            custom_column = custom['column']
            custom_value = custom.get('value')(values) if isfunction(custom.get('value')) else custom.get('value')

            sub_criterion = {}
            if custom['exclude']:
                if not custom_value or custom_value is None:
                    sub_criterion.update({custom_column: {'$ne': None}})
                else:
                    sub_criterion.update({custom_column: {'$ne': custom_value}})
            else:
                if not custom_value or custom_value is None:
                    sub_criterion.update({custom_column: {'$eq': None}})
                else:
                    sub_criterion.update({custom_column: {'$ne': custom_value}})

            criterion.add(*sub_criterion)

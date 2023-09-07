from typing import Type, TypeVar

from requests import Response

import ext_allure as allure

from pydantic import BaseModel, root_validator, ValidationError
T = TypeVar('T')


class DataClass(BaseModel):
    def as_dict(self):
        return self.dict(by_alias=True, exclude_unset=True, exclude_none=False, exclude=None)

    @root_validator(pre=True)
    def make_unset(cls, values):
        new_values = {key: value for (key, value) in values.items() if value is not None}
        return new_values

    class Config:
        allow_population_by_field_name = True



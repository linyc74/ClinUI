from abc import ABC
from typing import Type
from .schema import Schema


class AbstractModel(ABC):

    schema: Type[Schema]

    def __init__(self, schema: Type[Schema]):
        self.schema = schema

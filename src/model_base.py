from abc import ABC
from .schema import Schema


class AbstractModel(ABC):

    schema: Schema

    def __init__(self, schema: Schema):
        self.schema = schema

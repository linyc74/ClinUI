from typing import Dict, Any
from .schema import BaseModel
from .model_utils import CastDatatypes


class ProcessAttributesVghtpeLuad(BaseModel):

    def main(self, attributes: Dict[str, Any]) -> Dict[str, Any]:

        attributes = CastDatatypes(self.schema).main(attributes)

        return attributes


class ProcessAttributesVghtpeHnscc(BaseModel):

    def main(self, attributes: Dict[str, Any]) -> Dict[str, Any]:

        attributes = CastDatatypes(self.schema).main(attributes)

        return attributes

import pandas as pd
from typing import Dict, Any
from .schema import BaseModel


class CastDatatypes(BaseModel):

    def main(self, attributes: Dict[str, Any]) -> Dict[str, Any]:

        for key, val in attributes.items():

            if val == '':
                attributes[key] = pd.NA
            elif self.schema.COLUMN_ATTRIBUTES[key]['type'] == 'int':
                attributes[key] = int(val)
            elif self.schema.COLUMN_ATTRIBUTES[key]['type'] == 'float':
                attributes[key] = float(val)
            elif self.schema.COLUMN_ATTRIBUTES[key]['type'] == 'date':
                attributes[key] = pd.to_datetime(val).strftime('%Y-%m-%d')  # format it as str
            elif self.schema.COLUMN_ATTRIBUTES[key]['type'] == 'date_list':
                attributes[key] = format_date_list(val)
            elif self.schema.COLUMN_ATTRIBUTES[key]['type'] == 'bool':
                attributes[key] = True if val.upper() == 'TRUE' else False
            # assume other types are all str

        return attributes


def format_date_list(val: str) -> str:
    """
    '2020;2020-02;2020-03-01' --> '2020-01-01 ; 2020-02-01 ; 2020-03-01'
    """
    sep = ';'
    dates = []
    for x in val.split(sep):
        xx = x.strip()
        if not xx == '':
            dates.append(pd.to_datetime(xx).strftime('%Y-%m-%d'))
    return f' {sep} '.join(dates)

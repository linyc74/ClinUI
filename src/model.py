import pandas as pd
from os.path import basename
from typing import Tuple, List, Optional, Dict, Any
from .schema import USER_INPUT_COLUMNS


class Model:

    dataframe: pd.DataFrame  # this is the main clinical data table

    def __init__(self):
        self.reset_dataframe()

    def reset_dataframe(self):
        self.dataframe = pd.DataFrame(columns=USER_INPUT_COLUMNS)

    def read_sequencing_table(self, file: str) -> Tuple[bool, str]:
        df = pd.read_excel(file) if file.endswith('.xlsx') else pd.read_csv(file)

        for c in USER_INPUT_COLUMNS:
            if c not in df.columns:
                return False, f'Column "{c}" not found in "{basename(file)}"'

        self.dataframe = df[USER_INPUT_COLUMNS]
        return True, ''

    def save_sequencing_table(self, file: str):
        if file.endswith('.xlsx'):
            self.dataframe.to_excel(file, index=False)
        else:
            self.dataframe.to_csv(file, index=False)

    def get_dataframe(self) -> pd.DataFrame:
        return self.dataframe.copy()

    def sort_dataframe(self, by: str, ascending: bool):
        self.dataframe = self.dataframe.sort_values(
            by=by,
            ascending=ascending,
            kind='mergesort'  # deterministic, keep the original order when tied
        ).reset_index(
            drop=True
        )

    def drop(self, rows: Optional[List[int]] = None, columns: Optional[List[str]] = None):
        self.dataframe = self.dataframe.drop(
            index=rows,
            columns=columns
        ).reset_index(
            drop=True
        )

    def get_row(self, row: int) -> Dict[str, Any]:
        return self.dataframe.loc[row, ].to_dict()

    def update_row(self, row: int, attributes: Dict[str, str]):
        for key, val in attributes.items():
            self.dataframe.loc[row, key] = val

    def append_row(self, attributes: Dict[str, str]):
        self.dataframe = append(self.dataframe, pd.Series(attributes))


def append(df: pd.DataFrame, s: pd.Series) -> pd.DataFrame:
    return pd.concat([df, pd.DataFrame([s])], ignore_index=True)

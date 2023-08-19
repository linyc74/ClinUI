import pandas as pd
from os.path import basename
from typing import Tuple, List, Optional, Dict, Any, Union
from .schema import USER_INPUT_COLUMNS, SAMPLE_ID, LAB_ID, LAB_SAMPLE_ID


class Model:

    dataframe: pd.DataFrame  # this is the main clinical data table

    def __init__(self):
        self.reset_dataframe()

    def reset_dataframe(self):
        self.dataframe = pd.DataFrame(columns=USER_INPUT_COLUMNS)

    def read_clinical_data_table(self, file: str) -> Tuple[bool, str]:
        df = read(file)

        success, message = check_columns(
            df=df,
            columns=USER_INPUT_COLUMNS,
            file=file)

        if not success:
            return False, message

        self.dataframe = df[USER_INPUT_COLUMNS]
        return True, ''

    def import_sequencing_table(self, file: str) -> Tuple[bool, str]:
        seq_df = read(file)

        success, message = check_columns(
            df=seq_df,
            columns=['ID', 'Lab', 'Lab Sample ID'],
            file=file)

        if not success:
            return False, message

        self.dataframe = AddNewRowsFromSequencingTable().main(
            dataframe=self.dataframe,
            seq_df=seq_df)

        return True, ''

    def save_clinical_data_table(self, file: str):
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


class AddNewRowsFromSequencingTable:

    dataframe: pd.DataFrame
    seq_df: pd.DataFrame

    def main(
            self,
            dataframe: pd.DataFrame,
            seq_df: pd.DataFrame) -> pd.DataFrame:

        self.dataframe = dataframe.copy()
        self.seq_df = seq_df

        for i, row in self.seq_df.iterrows():

            sequencing_id = row['ID']
            if sequencing_id in self.dataframe[SAMPLE_ID].values:
                continue

            new_row = {
                SAMPLE_ID: sequencing_id,
                LAB_ID: row['Lab'],
                LAB_SAMPLE_ID: row['Lab Sample ID'],
            }

            self.dataframe = append(self.dataframe, new_row)

        return self.dataframe


def read(file: str) -> pd.DataFrame:
    return pd.read_excel(file) if file.endswith('.xlsx') else pd.read_csv(file)


def check_columns(df: pd.DataFrame, columns: List[str], file: str) -> Tuple[bool, str]:
    for c in columns:
        if c not in df.columns:
            return False, f'Column "{c}" not found in "{basename(file)}"'
    return True, ''


def append(df: pd.DataFrame, s: Union[dict, pd.Series]) -> pd.DataFrame:
    if type(s) is dict:
        s = pd.Series(s)
    return pd.concat([df, pd.DataFrame([s])], ignore_index=True)

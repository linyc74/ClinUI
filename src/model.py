import os
import pandas as pd
from os.path import basename
from typing import List, Optional, Dict, Any, Union, Tuple, Type
from .cbio_ingest import cBioIngest
from .model_nycu import ProcessAttributesNycuOscc
from .schema import BaseModel, Schema, NycuOsccSchema


class Model(BaseModel):

    dataframe: pd.DataFrame  # this is the main clinical data table

    def __init__(self, schema: Type[Schema]):
        super().__init__(schema=schema)
        self.reset_dataframe()

    def reset_dataframe(self):
        self.dataframe = pd.DataFrame(columns=self.schema.DISPLAY_COLUMNS)

    def import_clinical_data_table(self, file: str):
        self.dataframe = ImportClinicalDataTable(self.schema).main(
            clinical_data_df=self.dataframe,
            file=file)

        # When the whole column is NaN, it becomes float64, convert it back to object
        self.dataframe = self.dataframe.astype(object)

    def import_sequencing_table(self, file: str):
        self.dataframe = ImportSequencingTable(self.schema).main(
            clinical_data_df=self.dataframe,
            file=file)

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

    def drop(
            self,
            rows: Optional[List[int]] = None,
            columns: Optional[List[str]] = None):
        self.dataframe = self.dataframe.drop(
            index=rows,
            columns=columns
        ).reset_index(
            drop=True
        )

    def get_row(self, row: int) -> Dict[str, str]:
        """
        Everything going out of model should be string to avoid complex type issues
        """
        ret = self.dataframe.loc[row, ].to_dict()

        for key, val in ret.items():
            if pd.isna(val):
                ret[key] = ''  # NaN to ''

        ret = {k: str(v) for k, v in ret.items()}

        return ret

    def update_row(self, row: int, attributes: Dict[str, str]):
        """
        Everyting comes in model should be string
        Data type conversion is done in the model
        """
        attributes = self.__process(attributes=attributes)
        for key, val in attributes.items():
            self.dataframe.at[row, key] = val  # use .at to accept a list (iterable) as a single value

    def append_row(self, attributes: Dict[str, str]):
        """
        Everyting comes in model should be string
        Data type conversion is done in the model
        """
        attributes = self.__process(attributes=attributes)
        self.dataframe = append(self.dataframe, pd.Series(attributes))

    def __process(self, attributes: Dict[str, str]) -> Dict[str, Any]:
        if self.schema is NycuOsccSchema:
            attributes = ProcessAttributesNycuOscc().main(attributes=attributes)
        attributes = CastDatatypes(self.schema).main(attributes=attributes)
        return attributes

    def find(
            self,
            text: str,
            start: Optional[Tuple[int, str]]) \
            -> Optional[Tuple[int, str]]:

        if start is None:
            start_irow = 0
            start_icol = 0
        else:
            start_irow = start[0]
            start_icol = self.dataframe.columns.to_list().index(start[1])

        nrows, ncols = self.dataframe.shape

        for r in range(nrows):
            for c in range(ncols):
                if r <= start_irow and c <= start_icol:
                    continue
                if text.lower() in str(self.dataframe.iloc[r, c]).lower():
                    return r, self.dataframe.columns[c]

    def export_cbioportal_study(
            self,
            maf_dir: str,
            study_info_dict: Dict[str, str],
            tags_dict: Dict[str, str],
            outdir: str):

        ExportCbioportalStudy(self.schema).main(
            clinical_data_df=self.dataframe,
            maf_dir=maf_dir,
            study_info_dict=study_info_dict,
            tags_dict=tags_dict,
            outdir=outdir)


class ImportClinicalDataTable(BaseModel):

    clinical_data_df: pd.DataFrame
    file: str

    def main(
            self,
            clinical_data_df: pd.DataFrame,
            file: str) -> pd.DataFrame:

        self.clinical_data_df = clinical_data_df.copy()
        self.file = file

        df = ReadTable(self.schema).main(
            file=file,
            columns=self.schema.DISPLAY_COLUMNS)

        id_column = self.clinical_data_df.columns[0]

        for i, row in df.iterrows():

            already_exists = row[id_column] in self.clinical_data_df[id_column].values
            if already_exists:
                continue

            self.clinical_data_df = append(self.clinical_data_df, row)

        return self.clinical_data_df


class ImportSequencingTable(BaseModel):

    SAMPLE_ID = NycuOsccSchema.SAMPLE_ID
    LAB_ID = NycuOsccSchema.LAB_ID
    LAB_SAMPLE_ID = NycuOsccSchema.LAB_SAMPLE_ID

    clinical_data_df: pd.DataFrame
    file: str

    seq_df: pd.DataFrame

    def main(
            self,
            clinical_data_df: pd.DataFrame,
            file: str) -> pd.DataFrame:

        self.clinical_data_df = clinical_data_df.copy()
        self.file = file

        self.set_seq_df()
        self.append_new_rows()

        return self.clinical_data_df

    def set_seq_df(self):
        self.seq_df = ReadTable(self.schema).main(
            file=self.file,
            columns=['ID', 'Lab', 'Lab Sample ID']
        )

    def append_new_rows(self):
        for i, row in self.seq_df.iterrows():

            sequencing_id = row['ID']
            already_exists = sequencing_id in self.clinical_data_df[self.SAMPLE_ID].values
            if already_exists:
                continue

            new_row = {
                self.SAMPLE_ID: sequencing_id,
                self.LAB_ID: row['Lab'],
                self.LAB_SAMPLE_ID: row['Lab Sample ID'],
            }

            self.clinical_data_df = append(self.clinical_data_df, new_row)


class ReadTable(BaseModel):

    file: str
    columns: List[str]

    df: pd.DataFrame

    def main(
            self,
            file: str,
            columns: List[str]) -> pd.DataFrame:

        self.file = file
        self.columns = columns

        self.read_file()
        self.assert_columns()
        self.df = self.df[self.columns]

        return self.df

    def read_file(self):
        if self.file.endswith('.xlsx'):
            self.df = pd.read_excel(
                self.file,
                na_values=['', 'NaN'],  # these values are considered as NaN
                keep_default_na=False,  # don't convert 'None' or other default NA values to NaN
                dtype=str  # read everything as string, let other functions handle the conversion
            )
        else:  # assume csv
            self.df = pd.read_csv(
                self.file,
                na_values=['', 'NaN'],
                keep_default_na=False,
                dtype=str
            )

    def assert_columns(self):
        for c in self.columns:
            assert c in self.df.columns, f'Column "{c}" not found in "{basename(self.file)}"'


class ExportCbioportalStudy(BaseModel):

    clinical_data_df: pd.DataFrame
    maf_dir: str
    study_info_dict: Dict[str, str]
    tags_dict: Dict[str, str]
    outdir: str

    def main(
            self,
            clinical_data_df: pd.DataFrame,
            maf_dir: str,
            study_info_dict: Dict[str, str],
            tags_dict: Dict[str, str],
            outdir: str):

        self.clinical_data_df = clinical_data_df
        self.maf_dir = maf_dir
        self.study_info_dict = study_info_dict
        self.tags_dict = tags_dict
        self.outdir = outdir

        self.make_outdir()
        self.run_cbio_ingest()

    def make_outdir(self):
        os.makedirs(self.outdir, exist_ok=True)

    def run_cbio_ingest(self):
        cBioIngest(self.schema).main(
            clinical_data_df=self.clinical_data_df,
            maf_dir=self.maf_dir,
            study_info_dict=self.study_info_dict,
            tags_dict=self.tags_dict,
            outdir=self.outdir)


def append(
        df: pd.DataFrame,
        s: Union[dict, pd.Series]) -> pd.DataFrame:

    if type(s) is dict:
        s = pd.Series(s)

    if df.empty:
        return pd.DataFrame([s])  # no need to concat, just return the Series as a DataFrame

    return pd.concat([df, pd.DataFrame([s])], ignore_index=True)


class CastDatatypes(BaseModel):

    def main(self, attributes: Dict[str, str]) -> Dict[str, Any]:

        ret: Dict[str, Any] = attributes.copy()

        for key, val in ret.items():

            if val == '':
                ret[key] = pd.NA
            elif self.schema.COLUMN_ATTRIBUTES[key]['type'] == 'int':
                ret[key] = int(val)
            elif self.schema.COLUMN_ATTRIBUTES[key]['type'] == 'float':
                ret[key] = float(val)
            elif self.schema.COLUMN_ATTRIBUTES[key]['type'] == 'date':
                ret[key] = pd.to_datetime(val).strftime('%Y-%m-%d')  # format it as str
            elif self.schema.COLUMN_ATTRIBUTES[key]['type'] == 'date_list':
                ret[key] = format_date_list(val)
            elif self.schema.COLUMN_ATTRIBUTES[key]['type'] == 'bool':
                ret[key] = True if val.upper() == 'TRUE' else False
            # assume other types are all str

        return ret


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

import os
import shutil

import pandas as pd
from os.path import basename
from typing import Tuple, List, Optional, Dict, Any, Union
from .template import Settings
from .cbio_ingest import cBioIngest
from .schema import USER_INPUT_COLUMNS, SAMPLE_ID, LAB_ID, LAB_SAMPLE_ID, STUDY_IDENTIFIER_KEY


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

        self.dataframe = ImportSequencingTableIntoClinicalDataTable().main(
            clinical_data_df=self.dataframe,
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

    def export_cbioportal_study(
            self,
            maf_dir: str,
            study_info_dict: Dict[str, str],
            tags_dict: Dict[str, str],
            dstdir: str) -> Tuple[bool, str]:

        success, msg = ExportCbioportalStudy().main(
            clinical_data_df=self.dataframe,
            maf_dir=maf_dir,
            study_info_dict=study_info_dict,
            tags_dict=tags_dict,
            dstdir=dstdir)

        return success, msg


class ImportSequencingTableIntoClinicalDataTable:

    clinical_data_df: pd.DataFrame
    seq_df: pd.DataFrame

    def main(
            self,
            clinical_data_df: pd.DataFrame,
            seq_df: pd.DataFrame) -> pd.DataFrame:

        self.clinical_data_df = clinical_data_df.copy()
        self.seq_df = seq_df

        for i, row in self.seq_df.iterrows():

            sequencing_id = row['ID']
            already_exists = sequencing_id in self.clinical_data_df[SAMPLE_ID].values
            if already_exists:
                continue

            new_row = {
                SAMPLE_ID: sequencing_id,
                LAB_ID: row['Lab'],
                LAB_SAMPLE_ID: row['Lab Sample ID'],
            }

            self.clinical_data_df = append(self.clinical_data_df, new_row)

        return self.clinical_data_df


class ExportCbioportalStudy:

    clinical_data_df: pd.DataFrame
    maf_dir: str
    study_info_dict: Dict[str, str]
    tags_dict: Dict[str, str]
    dstdir: str

    settings: Settings

    def main(
            self,
            clinical_data_df: pd.DataFrame,
            maf_dir: str,
            study_info_dict: Dict[str, str],
            tags_dict: Dict[str, str],
            dstdir: str) -> Tuple[bool, str]:

        self.clinical_data_df = clinical_data_df
        self.maf_dir = maf_dir
        self.study_info_dict = study_info_dict
        self.tags_dict = tags_dict
        self.dstdir = dstdir

        self.set_settings()
        success, msg = self.run_cbio_ingest()

        return success, msg

    def set_settings(self):
        study_id = self.study_info_dict[STUDY_IDENTIFIER_KEY]
        outdir = f'{self.dstdir}/{study_id}'
        os.makedirs(outdir, exist_ok=True)
        self.settings = Settings(
            workdir='.',
            outdir=outdir,
            threads=1,
            debug=False,
            mock=False)

    def run_cbio_ingest(self) -> Tuple[bool, str]:
        try:
            cBioIngest(self.settings).main(
                clinical_data_df=self.clinical_data_df,
                maf_dir=self.maf_dir,
                study_info_dict=self.study_info_dict,
                tags_dict=self.tags_dict)
            return True, 'Export cBioPortal study complete'
        except Exception as e:
            shutil.rmtree(self.settings.outdir)
            return False, str(e)


def read(file: str) -> pd.DataFrame:
    return pd.read_excel(file) if file.endswith('.xlsx') else pd.read_csv(file)


def check_columns(
        df: pd.DataFrame,
        columns: List[str], file: str) -> Tuple[bool, str]:
    for c in columns:
        if c not in df.columns:
            return False, f'Column "{c}" not found in "{basename(file)}"'
    return True, ''


def append(
        df: pd.DataFrame,
        s: Union[dict, pd.Series]) -> pd.DataFrame:
    if type(s) is dict:
        s = pd.Series(s)
    return pd.concat([df, pd.DataFrame([s])], ignore_index=True)

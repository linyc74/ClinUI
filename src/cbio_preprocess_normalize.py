import numpy as np
import pandas as pd
from typing import Tuple, Union
from .model_base import AbstractModel


class PreprocessNormalize(AbstractModel):

    df: pd.DataFrame
    study_id: str

    patient_df: pd.DataFrame
    sample_df: pd.DataFrame

    def main(self, clinical_data_df: pd.DataFrame, study_id: str) -> Tuple[pd.DataFrame, pd.DataFrame]:

        self.df = clinical_data_df
        self.study_id = study_id

        self.drop_identifiable_information()
        self.normalize_patient_sample_data()

        return self.patient_df, self.sample_df

    def drop_identifiable_information(self):
        self.df = self.df.drop(columns=self.schema.CBIO_DROP_COLUMNS)

    def normalize_patient_sample_data(self):
        self.patient_df, self.sample_df = NormalizePatientSampleData(self.schema).main(
            df=self.df,
            study_id=self.study_id)


def delta_t(
        start: Union[pd.Timestamp, str, type(np.NAN)],
        end: Union[pd.Timestamp, str, type(np.NAN)]) -> pd.Timedelta:

    if type(start) is str:
        start = pd.to_datetime(start)
    elif pd.isna(start):
        start = pd.NaT

    if type(end) is str:
        end = pd.to_datetime(end)
    elif pd.isna(end):
        end = pd.NaT

    return end - start


class NormalizePatientSampleData(AbstractModel):

    df: pd.DataFrame
    study_id: str

    patient_df: pd.DataFrame
    sample_df: pd.DataFrame

    def main(self, df: pd.DataFrame, study_id: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
        self.df = df
        self.study_id = study_id

        self.rename_and_add_columns()
        self.extract_patient_data()
        self.extract_sample_data()

        return self.patient_df, self.sample_df

    def rename_and_add_columns(self):
        self.df = self.df.rename(columns={self.df.columns[0]: 'Sample ID'})  # cBioPortal requires it to be 'Sample ID'

        self.df['Study ID'] = self.study_id
        self.df['Patient ID'] = self.df['Sample ID']

        columns = self.df.columns.to_list()
        reordered = columns[-2:] + columns[:-2]  # move the last two columns 'Study ID' and 'Patient ID' to the front
        self.df = self.df[reordered]

    def extract_patient_data(self):
        columns = ['Patient ID'] + self.schema.CBIO_PATIENT_LEVEL_COLUMNS
        df = self.df[columns].copy()
        self.patient_df = df

    def extract_sample_data(self):
        columns = [
            c for c in self.df.columns if c not in self.schema.CBIO_PATIENT_LEVEL_COLUMNS
        ]
        self.sample_df = self.df[columns].copy()

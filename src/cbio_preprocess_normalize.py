import numpy as np
import pandas as pd
from typing import Tuple, Union
from .schema import *
from .template import Processor


class PreprocessNormalize(Processor):

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
        self.df = DropIdentifiableInformation(self.settings).main(self.df)

    def normalize_patient_sample_data(self):
        self.patient_df, self.sample_df = NormalizePatientSampleData(self.settings).main(
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


class DropIdentifiableInformation(Processor):

    DROP_COLUMNS = [
        LAB_SAMPLE_ID,
        BIRTH_DATE,
        CLINICAL_DIAGNOSIS_DATE,
        PATHOLOGICAL_DIAGNOSIS_DATE,
        INITIAL_TREATMENT_COMPLETION_DATE,
        LAST_FOLLOW_UP_DATE,
        EXPIRE_DATE,
        RECUR_DATE_AFTER_INITIAL_TREATMENT,
    ]

    def main(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.drop(columns=self.DROP_COLUMNS)


class NormalizePatientSampleData(Processor):

    PATIENT_LEVEL_COLUMNS = [
        SEX,
        PATIENT_WEIGHT,
        PATIENT_HEIGHT,
        ETHNICITY_CATEGORY,
        ALCOHOL_CONSUMPTION,
        ALCOHOL_CONSUMPTION_FREQUENCY,
        ALCOHOL_CONSUMPTION_DURATION,
        ALCOHOL_CONSUMPTION_QUIT,
        BETEL_NUT_CHEWING,
        BETEL_NUT_CHEWING_FREQUENCY,
        BETEL_NUT_CHEWING_DURATION,
        BETEL_NUT_CHEWING_QUIT,
        CIGARETTE_SMOKING,
        CIGARETTE_SMOKING_FREQUENCY,
        CIGARETTE_SMOKING_DURATION,
        CIGARETTE_SMOKING_QUIT,
        CAUSE_OF_DEATH,
        DISEASE_FREE_SURVIVAL_MONTHS,
        DISEASE_FREE_SURVIVAL_STATUS,
        DISEASE_SPECIFIC_SURVIVAL_MONTHS,
        DISEASE_SPECIFIC_SURVIVAL_STATUS,
        OVERALL_SURVIVAL_MONTHS,
        OVERALL_SURVIVAL_STATUS,
    ]

    df: pd.DataFrame
    study_id: str

    patient_df: pd.DataFrame
    sample_df: pd.DataFrame

    def main(self, df: pd.DataFrame, study_id: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
        self.df = df
        self.study_id = study_id

        self.extract_patient_data()
        self.extract_sample_data()

        return self.patient_df, self.sample_df

    def extract_patient_data(self):
        columns = [SAMPLE_ID] + self.PATIENT_LEVEL_COLUMNS
        df = self.df[columns].copy()
        df = df.rename(
            columns={SAMPLE_ID: PATIENT_ID}
        )
        self.patient_df = df

    def extract_sample_data(self):
        columns = [
            c for c in self.df.columns if c not in self.PATIENT_LEVEL_COLUMNS
        ]

        df = self.df[columns].copy()

        df[STUDY_ID] = self.study_id  # add study id column
        df[PATIENT_ID] = df[SAMPLE_ID]  # add patient id column

        # re-order columns
        columns = df.columns.to_list()
        reordered = columns[-2:] + columns[:-2]
        df = df[reordered]

        self.sample_df = df

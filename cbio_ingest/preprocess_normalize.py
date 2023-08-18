import pandas as pd
from typing import Tuple, Hashable
from .schema import *
from .template import Processor


CANCER = 'Cancer'
OTHER_DISEASE = 'Other Disease'


class PreprocessNormalize(Processor):

    xlsx: str

    df: pd.DataFrame
    patient_df: pd.DataFrame
    sample_df: pd.DataFrame

    def main(self, xlsx: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
        self.xlsx = xlsx

        self.df = pd.read_excel(self.xlsx)

        self.check_input_columns()
        self.calculate_survival()
        self.drop_identifiable_information()
        self.normalize_patient_sample_data()

        return self.patient_df, self.sample_df

    def check_input_columns(self):
        CheckInputColumns(self.settings).main(self.df)

    def calculate_survival(self):
        self.df = CalculateSurvival(self.settings).main(self.df)

    def drop_identifiable_information(self):
        self.df = DropIdentifiableInformation(self.settings).main(self.df)

    def normalize_patient_sample_data(self):
        self.patient_df, self.sample_df = NormalizePatientSampleData(self.settings).main(self.df)


class CheckInputColumns(Processor):

    INPUT_COLUMNS = [
        'Study ID',
        'Lab Sample ID',
        'Sample ID',
        'Sex',
        'Patient Weight (Kg)',
        'Patient Height (cm)',
        'Ethnicity Category',
        'Birth Date',
        'Clinical Diagnosis Date',
        'Pathological Diagnosis Date',
        'Cancer Type',
        'Cancer Type Detailed',
        'Sample Type',
        'Oncotree Code',
        'Somatic status',
        'Center',
        'Tumor Disease Anatomic Site',
        'ICD-O-3 Site Code',
        'Alcohol Consumption',
        'Alcohol Consumption Frequency (Days Per Week)',
        'Alcohol Consumption Duration (Years)',
        'Alcohol Consumption Quit (Years)',
        'Betel Nut Chewing',
        'Betel Nut Chewing Frequency (Pieces Per Day)',
        'Betel Nut Chewing Duration (Years)',
        'Betel Nut Chewing Quit (Years)',
        'Cigarette Smoking',
        'Cigarette Smoking Frequency (Packs Per Day)',
        'Cigarette Smoking Duration (Years)',
        'Cigarette Smoking Quit (Years)',
        'Histologic Grade',
        'Surgery',
        'Neoadjuvant/Induction Chemotherapy',
        'Neoadjuvant/Induction Chemotherapy Drug',
        'Adjuvant Chemotherapy',
        'Adjuvant Chemotherapy Drug',
        'Palliative Chemotherapy',
        'Palliative Chemotherapy Drug',
        'Adjuvant Targeted Therapy',
        'Adjuvant Targeted Therapy Drug',
        'Palliative Targeted Therapy',
        'Palliative Targeted Therapy Drug',
        'Immunotherapy',
        'Immunotherapy Drug',
        'Radiation Therapy',
        'Radiation Therapy Dose (cGY)',
        'IHC Anti-PDL1 mAb 22C3 TPS (%)',
        'IHC Anti-PDL1 mAb 22C3 CPS (%)',
        'IHC Anti-PDL1 mAb 28-8 TPS (%)',
        'IHC Anti-PDL1 mAb 28-8 CPS (%)',
        'Lymph Node Level I',
        'Lymph Node Level Ia',
        'Lymph Node Level Ib',
        'Lymph Node Level II',
        'Lymph Node Level IIa',
        'Lymph Node Level IIb',
        'Lymph Node Level III',
        'Lymph Node Level IV',
        'Lymph Node Level V',
        'Lymphovascular Invasion (LVI)',
        'Perineural Invasion (PNI)',
        'Clinical Overt Extranodal Extension',
        'Pathological Extranodal Extension (ENE)',
        'Depth of Invasion (mm)',
        'Tumor Margin',
        'Clinical TNM (cTNM)',
        'Pathological TNM (pTNM)',
        'Postneoadjuvant Clinical TNM (ycTNM)',
        'Postneoadjuvant Pathological TNM (ypTNM)',
        'Neoplasm Disease Stage American Joint Committee on Cancer Code',
        'ICD-10 Classification',
        'Subtype',
        'Initial Treatment Completion Date',
        'Last Follow-up Date',
        'Recur Date after Initial Treatment',
        'Expire Date',
        'Cause of Death',
    ]

    df: pd.DataFrame

    def main(self, df: pd.DataFrame):
        self.df = df

        for c in self.INPUT_COLUMNS:
            assert c in self.df.columns, f'Column "{c}" not in the clinical data Excel file'


class CalculateSurvival(Processor):

    df: pd.DataFrame

    def main(self, df: pd.DataFrame) -> pd.DataFrame:
        self.df = df

        for i, row in self.df.iterrows():
            self.calculate_diagnosis_age(i, row)
            self.check_cause_of_death(i, row)
            self.calculate_disease_free_survival(i, row)
            self.calculate_disease_specific_survival(i, row)
            self.calculate_overall_survival(i, row)

        self.convert_time_units()

        return self.df

    def calculate_diagnosis_age(self, i: Hashable, row: pd.Series):
        self.df.loc[i, DIAGNOSIS_AGE] = row[CLINICAL_DIAGNOSIS_DATE] - row[BIRTH_DATE]

    def check_cause_of_death(self, i: Hashable, row: pd.Series):
        has_expire_date = pd.notna(row[EXPIRE_DATE])

        if has_expire_date:
            if row[CAUSE_OF_DEATH].title() not in [CANCER, OTHER_DISEASE]:
                print(
                    f'WARNING! Sample ID "{row[SAMPLE_ID]}": "{row[CAUSE_OF_DEATH]}" is not a valid cause of death, default to "{OTHER_DISEASE}"')
                self.df.loc[i, CAUSE_OF_DEATH] = OTHER_DISEASE

    def calculate_disease_free_survival(self, i: Hashable, row: pd.Series):
        recurred = pd.notna(row[RECUR_DATE_AFTER_INITIAL_TREATMENT])
        alive = pd.isna(row[EXPIRE_DATE])

        t0 = row[INITIAL_TREATMENT_COMPLETION_DATE]

        if recurred:
            duration = row[RECUR_DATE_AFTER_INITIAL_TREATMENT] - t0
            status = '1:Recurred/Progressed'
        else:
            if alive:
                duration = row[LAST_FOLLOW_UP_DATE] - t0
                status = '0:DiseaseFree'
            else:  # dead
                duration = row[EXPIRE_DATE] - t0
                if row[CAUSE_OF_DEATH].capitalize() == CANCER:
                    status = '1:Recurred/Progressed'
                else:
                    status = '0:DiseaseFree'

        self.df.loc[i, DISEASE_FREE_SURVIVAL_MONTHS] = duration
        self.df.loc[i, DISEASE_FREE_SURVIVAL_STATUS] = status

    def calculate_disease_specific_survival(self, i: Hashable, row: pd.Series):
        alive = pd.isna(row[EXPIRE_DATE])
        t0 = row[INITIAL_TREATMENT_COMPLETION_DATE]

        if alive:
            duration = row[LAST_FOLLOW_UP_DATE] - t0
            status = '0:ALIVE OR DEAD TUMOR FREE'
        else:
            duration = row[EXPIRE_DATE] - t0
            if row[CAUSE_OF_DEATH].capitalize() == CANCER:
                status = '1:DEAD WITH TUMOR'
            else:
                status = '0:ALIVE OR DEAD TUMOR FREE'

        self.df.loc[i, DISEASE_SPECIFIC_SURVIVAL_MONTHS] = duration
        self.df.loc[i, DISEASE_SPECIFIC_SURVIVAL_STATUS] = status

    def calculate_overall_survival(self, i: Hashable, row: pd.Series):
        if pd.notna(row[EXPIRE_DATE]):
            duration = row[EXPIRE_DATE] - row[INITIAL_TREATMENT_COMPLETION_DATE]
            status = '1:DECEASED'
        else:
            duration = row[LAST_FOLLOW_UP_DATE] - row[INITIAL_TREATMENT_COMPLETION_DATE]
            status = '0:LIVING'

        self.df.loc[i, OVERALL_SURVIVAL_MONTHS] = duration
        self.df.loc[i, OVERALL_SURVIVAL_STATUS] = status

    def convert_time_units(self):
        self.df[DIAGNOSIS_AGE] = self.df[DIAGNOSIS_AGE] / pd.Timedelta(days=365)

        for c in [
            DISEASE_FREE_SURVIVAL_MONTHS,
            DISEASE_SPECIFIC_SURVIVAL_MONTHS,
            OVERALL_SURVIVAL_MONTHS
        ]:
            self.df[c] = self.df[c] / pd.Timedelta(days=30)


class DropIdentifiableInformation(Processor):

    DROP_COLUMNS = [
        'Lab Sample ID',
        BIRTH_DATE,
        CLINICAL_DIAGNOSIS_DATE,
        'Pathological Diagnosis Date',
        'Initial Treatment Completion Date',
        'Last Follow-up Date',
        'Expire Date',
        'Recur Date after Initial Treatment',
    ]

    def main(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.drop(columns=self.DROP_COLUMNS)


class NormalizePatientSampleData(Processor):

    PATIENT_LEVEL_COLUMNS = [
        'Sex',
        'Patient Weight (Kg)',
        'Patient Height (cm)',
        'Ethnicity Category',
        'Alcohol Consumption',
        'Alcohol Consumption Frequency (Days Per Week)',
        'Alcohol Consumption Duration (Years)',
        'Alcohol Consumption Quit (Years)',
        'Betel Nut Chewing',
        'Betel Nut Chewing Frequency (Pieces Per Day)',
        'Betel Nut Chewing Duration (Years)',
        'Betel Nut Chewing Quit (Years)',
        'Cigarette Smoking',
        'Cigarette Smoking Frequency (Packs Per Day)',
        'Cigarette Smoking Duration (Years)',
        'Cigarette Smoking Quit (Years)',
        CAUSE_OF_DEATH,
        DISEASE_FREE_SURVIVAL_MONTHS,
        DISEASE_FREE_SURVIVAL_STATUS,
        DISEASE_SPECIFIC_SURVIVAL_MONTHS,
        DISEASE_SPECIFIC_SURVIVAL_STATUS,
        OVERALL_SURVIVAL_MONTHS,
        OVERALL_SURVIVAL_STATUS,
    ]

    df: pd.DataFrame

    patient_df: pd.DataFrame
    sample_df: pd.DataFrame

    def main(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        self.df = df

        self.extract_patient_data()
        self.extract_sample_data()

        return self.patient_df, self.sample_df

    def extract_patient_data(self):
        columns = [SAMPLE_ID] + self.PATIENT_LEVEL_COLUMNS
        df = self.df[columns]
        df = df.rename(
            columns={SAMPLE_ID: PATIENT_ID}
        )
        self.patient_df = df

    def extract_sample_data(self):
        columns = [
            c for c in self.df.columns if c not in self.PATIENT_LEVEL_COLUMNS
        ]
        df = self.df[columns]

        df[PATIENT_ID] = df[SAMPLE_ID]  # add patient id column

        # re-order patient id column
        columns = df.columns.to_list()
        patient_id_column = columns.pop()
        columns.insert(1, patient_id_column)
        df = df[columns]

        self.sample_df = df

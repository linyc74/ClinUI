import os
import numpy as np
import pandas as pd
from os.path import basename
from typing import List, Optional, Dict, Any, Union
from .schema import *
from .template import Settings
from .cbio_ingest import cBioIngest


class Model:

    dataframe: pd.DataFrame  # this is the main clinical data table

    def __init__(self):
        self.reset_dataframe()

    def reset_dataframe(self):
        self.dataframe = pd.DataFrame(columns=DISPLAY_COLUMNS)

    def read_clinical_data_table(self, file: str):
        self.dataframe = ReadTable().main(file=file, columns=DISPLAY_COLUMNS)

    def import_sequencing_table(self, file: str):
        seq_df = ReadTable().main(
            file=file,
            columns=['ID', 'Lab', 'Lab Sample ID']
        )
        self.dataframe = MergeSeqDfIntoClinicalDataDf().main(
            clinical_data_df=self.dataframe,
            seq_df=seq_df
        )

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
        attributes = ProcessAttributes().main(attributes)
        for key, val in attributes.items():
            self.dataframe.loc[row, key] = val

    def append_row(self, attributes: Dict[str, str]):
        attributes = ProcessAttributes().main(attributes)
        self.dataframe = append(self.dataframe, pd.Series(attributes))

    def export_cbioportal_study(
            self,
            maf_dir: str,
            study_info_dict: Dict[str, str],
            tags_dict: Dict[str, str],
            dstdir: str):

        ExportCbioportalStudy().main(
            clinical_data_df=self.dataframe,
            maf_dir=maf_dir,
            study_info_dict=study_info_dict,
            tags_dict=tags_dict,
            dstdir=dstdir)


class ReadTable:

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
        self.convert_datetime_columns()

        return self.df

    def read_file(self):
        self.df = pd.read_excel(self.file) if self.file.endswith('.xlsx') else pd.read_csv(self.file)

    def assert_columns(self):
        for c in self.columns:
            assert c in self.df.columns, f'Column "{c}" not found in "{basename(self.file)}"'

    def convert_datetime_columns(self):
        for c in self.df.columns:
            type_ = COLUMN_ATTRIBUTES.get(c, {}).get('type', None)
            if type_ == 'datetime':
                self.df[c] = pd.to_datetime(self.df[c])


class MergeSeqDfIntoClinicalDataDf:

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


class ProcessAttributes:

    def main(self, attributes: Dict[str, Any]) -> Dict[str, Any]:
        attributes = CalculateSurvival().main(attributes)
        attributes = CalculateICD().main(attributes)
        attributes = CalculateTotalLymphNodes().main(attributes)
        attributes = CalculateStage().main(attributes)
        attributes = CastDatatypes().main(attributes)
        return attributes


class CalculateSurvival:

    attributes: Dict[str, Any]

    def main(self, attributes: Dict[str, Any]) -> Dict[str, Any]:
        self.attributes = attributes.copy()

        self.diagnosis_age()
        self.check_cause_of_death()
        self.disease_free_survival()
        self.disease_specific_survival()
        self.overall_survival()

        return self.attributes

    def diagnosis_age(self):
        self.attributes[CLINICAL_DIAGNOSIS_AGE] = delta_t(
            start=self.attributes[BIRTH_DATE],
            end=self.attributes[CLINICAL_DIAGNOSIS_DATE]) / pd.Timedelta(days=365)

    def check_cause_of_death(self):
        has_expire_date = self.attributes[EXPIRE_DATE] != ''

        if has_expire_date:
            cause = self.attributes[CAUSE_OF_DEATH]
            assert cause in COLUMN_ATTRIBUTES[CAUSE_OF_DEATH]['options'], f'"{cause}" is not a valid cause of death'

    def disease_free_survival(self):
        attr = self.attributes

        recurred = attr[RECUR_DATE_AFTER_INITIAL_TREATMENT] != ''
        alive = attr[EXPIRE_DATE] == ''

        t0 = attr[INITIAL_TREATMENT_COMPLETION_DATE]

        if recurred:
            duration = delta_t(start=t0, end=attr[RECUR_DATE_AFTER_INITIAL_TREATMENT])
            status = '1:Recurred/Progressed'
        else:
            if alive:
                duration = delta_t(start=t0, end=attr[LAST_FOLLOW_UP_DATE])
                status = '0:DiseaseFree'
            else:  # died
                duration = delta_t(start=t0, end=attr[EXPIRE_DATE])
                if attr[CAUSE_OF_DEATH].upper() == 'CANCER':
                    status = '1:Recurred/Progressed'
                else:
                    status = '0:DiseaseFree'

        self.attributes[DISEASE_FREE_SURVIVAL_MONTHS] = duration / pd.Timedelta(days=30)
        self.attributes[DISEASE_FREE_SURVIVAL_STATUS] = status

    def disease_specific_survival(self):
        attr = self.attributes

        alive = attr[EXPIRE_DATE] == ''
        t0 = attr[INITIAL_TREATMENT_COMPLETION_DATE]

        if alive:
            duration = delta_t(start=t0, end=attr[LAST_FOLLOW_UP_DATE])
            status = '0:ALIVE OR DEAD TUMOR FREE'
        else:
            duration = delta_t(start=t0, end=attr[EXPIRE_DATE])
            if attr[CAUSE_OF_DEATH].upper() == 'CANCER':
                status = '1:DEAD WITH TUMOR'
            else:
                status = '0:ALIVE OR DEAD TUMOR FREE'

        self.attributes[DISEASE_SPECIFIC_SURVIVAL_MONTHS] = duration / pd.Timedelta(days=30)
        self.attributes[DISEASE_SPECIFIC_SURVIVAL_STATUS] = status

    def overall_survival(self):
        attr = self.attributes

        alive = attr[EXPIRE_DATE] == ''
        t0 = attr[INITIAL_TREATMENT_COMPLETION_DATE]

        if alive:
            duration = delta_t(start=t0, end=attr[LAST_FOLLOW_UP_DATE])
            status = '0:LIVING'
        else:
            duration = delta_t(start=t0, end=attr[EXPIRE_DATE])
            status = '1:DECEASED'

        self.attributes[OVERALL_SURVIVAL_MONTHS] = duration / pd.Timedelta(days=30)
        self.attributes[OVERALL_SURVIVAL_STATUS] = status


class CalculateICD:

    # https://training.seer.cancer.gov/head-neck/abstract-code-stage/codes.html (2023 edition)
    ANATOMIC_SITE_TO_ICD_O_3_SITE_CODE = {
        # Lip
        'External upper lip': 'C00.0',
        'External lower lip': 'C00.1',
        'External lip': 'C00.2',
        'Mucosa of upper lip': 'C00.3',
        'Mucosa of lower lip': 'C00.4',
        'Mucosa of lip': 'C00.5',
        'Commissure of lip': 'C00.6',
        'Overlapping lesion of lip': 'C00.8',
        'Lip': 'C00.9',

        # Base of tongue
        'Base of tongue': 'C01.9',

        # Other and unspecified parts of tongue
        'Dorsal surface of tongue': 'C02.0',
        'Border of tongue': 'C02.1',
        'Ventral surface of tongue': 'C02.2',
        'Anterior 2/3 of tongue': 'C02.3',
        'Lingual tonsil': 'C02.4',
        'Overlapping lesion of tongue': 'C02.8',
        'Tongue': 'C02.9',

        # Gum
        'Upper gum': 'C03.0',
        'Lower gum': 'C03.1',
        'Gum': 'C03.9',

        # Floor of mouth
        'Anterior floor of mouth': 'C04.0',
        'Lateral floor of mouth': 'C04.1',
        'Overlapping lesion of floor of mouth': 'C04.8',
        'Floor of mouth': 'C04.9',

        # Palate
        'Hard palate': 'C05.0',
        'Soft palate': 'C05.1',
        'Uvula': 'C05.2',
        'Overlapping lesion of palate': 'C05.8',
        'Palate': 'C05.9',

        # Other and unspecified parts of mouth
        'Cheek mucosa': 'C06.0',
        'Vestibule of mouth': 'C06.1',
        'Retromolar area': 'C06.2',
        'Overlapping lesion of other and unspecified parts of mouth': 'C06.8',
        'Mouth': 'C06.9',

        # Parotid gland
        'Parotid gland': 'C07.9',

        # Other and unspecified major salivary gland
        'Submandibular gland': 'C08.0',
        'Sublingual gland': 'C08.1',
        'Overlapping lesion of major salivary glands': 'C08.8',
        'Major salivary gland': 'C08.9',

        # Custom
        'Retromolar Triangle': 'C06.2',
        'Right Tongue': 'C02.9',
        'Left Tongue': 'C02.9',
        'Cross Midline (CM) Tongue': 'C02.9',
        'Left Upper Gingiva': 'C03.0',
        'Left Lower Gingiva': 'C03.1',
        'Right Upper Gingiva': 'C03.0',
        'Right Lower Gingiva': 'C03.1',
        'Cross Midline (CM) Left Upper Gingiva': 'C03.0',
        'Cross Midline (CM) Right Lower Gingiva': 'C03.1',
        'Cross Midline (CM) Gingiva': 'C03.9',
        'Left Palate': 'C05.9',
        'Right Palate': 'C05.9',
        'Cross Midline (CM) Palate': 'C05.9',
        'Upper Lip': 'C00.9',
        'Lower Lip': 'C00.9',
        'External Upper Lip': 'C00.0',
        'External Lower Lip': 'C00.1',
        'Upper Lip Inner Aspect': 'C00.3',
        'Lower Lip Inner Aspect': 'C00.4',
        'Cross Midline (CM) Lip': 'C00.9',
        'Left Buccal Mucosa': 'C06.0',
        'Right Buccal Mucosa': 'C06.0',
    }

    # https://www.icd10data.com/ICD10CM/Codes (2023 edition)
    # I manually checked ICD-10 and found it to be identical to ICD-O-3,
    #   although the wordings of ICD-10 and ICD-O-3 are slightly different
    # Here I use the description from ICD-O-3
    # Note that "C08.8" is not present in ICD-10 (maybe they just forgot to add it?)
    ANATOMIC_SITE_TO_ICD_10_CLASSIFICATION = {
        # Lip
        'External upper lip': 'C00.0',
        'External lower lip': 'C00.1',
        'External lip': 'C00.2',
        'Mucosa of upper lip': 'C00.3',
        'Mucosa of lower lip': 'C00.4',
        'Mucosa of lip': 'C00.5',
        'Commissure of lip': 'C00.6',
        'Overlapping lesion of lip': 'C00.8',
        'Lip': 'C00.9',

        # Base of tongue
        'Base of tongue': 'C01.9',

        # Other and unspecified parts of tongue
        'Dorsal surface of tongue': 'C02.0',
        'Border of tongue': 'C02.1',
        'Ventral surface of tongue': 'C02.2',
        'Anterior 2/3 of tongue': 'C02.3',
        'Lingual tonsil': 'C02.4',
        'Overlapping lesion of tongue': 'C02.8',
        'Tongue': 'C02.9',

        # Gum
        'Upper gum': 'C03.0',
        'Lower gum': 'C03.1',
        'Gum': 'C03.9',

        # Floor of mouth
        'Anterior floor of mouth': 'C04.0',
        'Lateral floor of mouth': 'C04.1',
        'Overlapping lesion of floor of mouth': 'C04.8',
        'Floor of mouth': 'C04.9',

        # Palate
        'Hard palate': 'C05.0',
        'Soft palate': 'C05.1',
        'Uvula': 'C05.2',
        'Overlapping lesion of palate': 'C05.8',
        'Palate': 'C05.9',

        # Other and unspecified parts of mouth
        'Cheek mucosa': 'C06.0',
        'Vestibule of mouth': 'C06.1',
        'Retromolar area': 'C06.2',
        'Overlapping lesion of other and unspecified parts of mouth': 'C06.8',
        'Mouth': 'C06.9',

        # Parotid gland
        'Parotid gland': 'C07.9',

        # Other and unspecified major salivary gland
        'Submandibular gland': 'C08.0',
        'Sublingual gland': 'C08.1',
        'Major salivary gland': 'C08.9',

        # Custom
        'Retromolar Triangle': 'C06.2',
        'Right Tongue': 'C02.9',
        'Left Tongue': 'C02.9',
        'Cross Midline (CM) Tongue': 'C02.9',
        'Left Upper Gingiva': 'C03.0',
        'Left Lower Gingiva': 'C03.1',
        'Right Upper Gingiva': 'C03.0',
        'Right Lower Gingiva': 'C03.1',
        'Cross Midline (CM) Left Upper Gingiva': 'C03.0',
        'Cross Midline (CM) Right Lower Gingiva': 'C03.1',
        'Cross Midline (CM) Gingiva': 'C03.9',
        'Left Palate': 'C05.9',
        'Right Palate': 'C05.9',
        'Cross Midline (CM) Palate': 'C05.9',
        'Upper Lip': 'C00.9',
        'Lower Lip': 'C00.9',
        'External Upper Lip': 'C00.0',
        'External Lower Lip': 'C00.1',
        'Upper Lip Inner Aspect': 'C00.3',
        'Lower Lip Inner Aspect': 'C00.4',
        'Cross Midline (CM) Lip': 'C00.9',
        'Left Buccal Mucosa': 'C06.0',
        'Right Buccal Mucosa': 'C06.0',
    }

    attributes: Dict[str, Any]

    def main(self, attributes: Dict[str, Any]) -> Dict[str, Any]:
        self.attributes = attributes.copy()
        self.add_icd_o_3()
        self.add_icd_10()
        return self.attributes

    def add_icd_o_3(self):
        site = self.attributes[TUMOR_DISEASE_ANATOMIC_SITE]
        icd_o_3 = self.ANATOMIC_SITE_TO_ICD_O_3_SITE_CODE.get(site, None)
        if icd_o_3 is not None:
            self.attributes[ICD_O_3_SITE_CODE] = icd_o_3

    def add_icd_10(self):
        site = self.attributes[TUMOR_DISEASE_ANATOMIC_SITE]
        icd_10 = self.ANATOMIC_SITE_TO_ICD_10_CLASSIFICATION.get(site, None)
        if icd_10 is not None:
            self.attributes[ICD_10_CLASSIFICATION] = icd_10


class CalculateTotalLymphNodes:

    attributes: Dict[str, Any]

    def main(self, attributes: Dict[str, Any]) -> Dict[str, Any]:
        self.attributes = attributes.copy()
        if self.attributes[TOTAL_LYMPH_NODE] == '':
            self.attributes[TOTAL_LYMPH_NODE] = '0/0'
        return self.attributes


class CalculateStage:

    attributes: Dict[str, Any]

    def main(self, attributes: Dict[str, Any]) -> Dict[str, Any]:
        self.attributes = attributes.copy()
        self.attributes[NEOPLASM_DISEASE_STAGE_AMERICAN_JOINT_COMMITTEE_ON_CANCER_CODE] = 'Stage X'
        return self.attributes


class CastDatatypes:

    def main(self, attributes: Dict[str, Any]) -> Dict[str, Any]:
        for key, val in attributes.items():
            if val == '':
                attributes[key] = pd.NA
            elif COLUMN_ATTRIBUTES[key]['type'] == 'int':
                attributes[key] = int(val)
            elif COLUMN_ATTRIBUTES[key]['type'] == 'float':
                attributes[key] = float(val)
            elif COLUMN_ATTRIBUTES[key]['type'] == 'datetime':
                attributes[key] = pd.to_datetime(val)
            elif COLUMN_ATTRIBUTES[key]['type'] == 'boolean':
                attributes[key] = True if val.upper() == 'TRUE' else False
        return attributes


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
            dstdir: str):

        self.clinical_data_df = clinical_data_df
        self.maf_dir = maf_dir
        self.study_info_dict = study_info_dict
        self.tags_dict = tags_dict
        self.dstdir = dstdir

        self.set_settings()
        self.run_cbio_ingest()

    def set_settings(self):
        os.makedirs(self.dstdir, exist_ok=True)
        self.settings = Settings(
            workdir='.',
            outdir=self.dstdir,
            threads=1,
            debug=False,
            mock=False)

    def run_cbio_ingest(self):
        cBioIngest(self.settings).main(
            clinical_data_df=self.clinical_data_df,
            maf_dir=self.maf_dir,
            study_info_dict=self.study_info_dict,
            tags_dict=self.tags_dict)


def append(
        df: pd.DataFrame,
        s: Union[dict, pd.Series]) -> pd.DataFrame:
    if type(s) is dict:
        s = pd.Series(s)
    return pd.concat([df, pd.DataFrame([s])], ignore_index=True)


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

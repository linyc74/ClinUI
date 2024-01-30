import os
import numpy as np
import pandas as pd
from os.path import basename
from typing import List, Optional, Dict, Any, Union, Tuple
from .columns import *
from .schema import DATA_SCHEMA_DICT, Schema
from .template import Settings
from .cbio_ingest import cBioIngest


class Model:

    schema: Schema
    dataframe: pd.DataFrame  # this is the main clinical data table

    def __init__(self, schema: str):
        self.schema = DATA_SCHEMA_DICT[schema]
        self.reset_dataframe()

    def reset_dataframe(self):
        self.dataframe = pd.DataFrame(columns=self.schema.DISPLAY_COLUMNS)

    def read_clinical_data_table(self, file: str):
        self.dataframe = ReadTable(self.schema).main(
            file=file,
            columns=self.schema.DISPLAY_COLUMNS)

    def import_sequencing_table(self, file: str):
        seq_df = ReadTable(self.schema).main(
            file=file,
            columns=['ID', 'Lab', 'Lab Sample ID']
        )
        self.dataframe = MergeSeqDfIntoClinicalDataDf(self.schema).main(
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
        attributes = ProcessAttributes(self.schema).main(attributes)
        for key, val in attributes.items():
            self.dataframe.loc[row, key] = val

    def append_row(self, attributes: Dict[str, str]):
        attributes = ProcessAttributes(self.schema).main(attributes)
        self.dataframe = append(self.dataframe, pd.Series(attributes))

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
            dstdir: str):

        ExportCbioportalStudy().main(
            clinical_data_df=self.dataframe,
            maf_dir=maf_dir,
            study_info_dict=study_info_dict,
            tags_dict=tags_dict,
            dstdir=dstdir)


class ModelTool:

    schema: Schema

    def __init__(self, schema: Schema):
        self.schema = schema


class ReadTable(ModelTool):

    file: str
    columns: List[str]

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

    df: pd.DataFrame

    def read_file(self):
        self.df = pd.read_excel(self.file) if self.file.endswith('.xlsx') else pd.read_csv(self.file)

    def assert_columns(self):
        for c in self.columns:
            assert c in self.df.columns, f'Column "{c}" not found in "{basename(self.file)}"'

    def convert_datetime_columns(self):
        for c in self.df.columns:
            type_ = self.schema.COLUMN_ATTRIBUTES.get(c, {}).get('type', None)
            if type_ == 'datetime':
                self.df[c] = pd.to_datetime(self.df[c])


class MergeSeqDfIntoClinicalDataDf(ModelTool):

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


#


class ProcessAttributes(ModelTool):

    def main(self, attributes: Dict[str, Any]) -> Dict[str, Any]:
        attributes = CalculateDiagnosisAge(self.schema).main(attributes)
        attributes = CalculateSurvival(self.schema).main(attributes)
        attributes = CalculateICD(self.schema).main(attributes)
        attributes = CalculateTotalLymphNodes(self.schema).main(attributes)
        attributes = CalculateStage(self.schema).main(attributes)
        attributes = CastDatatypes(self.schema).main(attributes)
        return attributes


class Calculate(ModelTool):

    REQUIRED_KEYS: List[str]

    attributes: Dict[str, Any]

    def has_required_keys(self) -> bool:
        for key in self.REQUIRED_KEYS:
            if key not in self.schema.DISPLAY_COLUMNS:
                return False
        return True


class CalculateDiagnosisAge(Calculate):

    REQUIRED_KEYS = [
        BIRTH_DATE,
        CLINICAL_DIAGNOSIS_DATE,
        CLINICAL_DIAGNOSIS_AGE,
    ]

    def main(self,attributes: Dict[str, Any]) -> Dict[str, Any]:

        self.attributes = attributes.copy()

        if not self.has_required_keys():
            return self.attributes

        self.diagnosis_age()

        return self.attributes

    def diagnosis_age(self):
        self.attributes[CLINICAL_DIAGNOSIS_AGE] = delta_t(
            start=self.attributes[BIRTH_DATE],
            end=self.attributes[CLINICAL_DIAGNOSIS_DATE]) / pd.Timedelta(days=365)


class CalculateSurvival(Calculate):

    REQUIRED_KEYS = [
        INITIAL_TREATMENT_COMPLETION_DATE,
        LAST_FOLLOW_UP_DATE,
        RECUR_DATE_AFTER_INITIAL_TREATMENT,
        EXPIRE_DATE,
        CAUSE_OF_DEATH,
        DISEASE_FREE_SURVIVAL_MONTHS,
        DISEASE_FREE_SURVIVAL_STATUS,
        DISEASE_SPECIFIC_SURVIVAL_MONTHS,
        DISEASE_SPECIFIC_SURVIVAL_STATUS,
        OVERALL_SURVIVAL_MONTHS,
        OVERALL_SURVIVAL_STATUS,
    ]

    def main(
            self,
            attributes: Dict[str, Any]) -> Dict[str, Any]:

        self.attributes = attributes.copy()

        if not self.has_required_keys():
            return self.attributes

        self.check_cause_of_death()
        self.disease_free_survival()
        self.disease_specific_survival()
        self.overall_survival()

        return self.attributes

    def check_cause_of_death(self):
        has_expire_date = self.attributes[EXPIRE_DATE] != ''

        if has_expire_date:
            cause = self.attributes[CAUSE_OF_DEATH]
            assert cause in self.schema.COLUMN_ATTRIBUTES[CAUSE_OF_DEATH]['options'], f'"{cause}" is not a valid cause of death'

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


class CalculateICD(Calculate):

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

    REQUIRED_KEYS = [
        TUMOR_DISEASE_ANATOMIC_SITE,
        ICD_O_3_SITE_CODE,
        ICD_10_CLASSIFICATION
    ]

    attributes: Dict[str, Any]

    def main(self, attributes: Dict[str, Any]) -> Dict[str, Any]:

        self.attributes = attributes.copy()

        if not self.has_required_keys():
            return self.attributes

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


class CalculateStage(Calculate):
    """
    https://www.cancer.org/cancer/types/oral-cavity-and-oropharyngeal-cancer/detection-diagnosis-staging/staging.html
    """

    REQUIRED_KEYS = [
        CLINICAL_TNM,
        NEOPLASM_DISEASE_STAGE_AMERICAN_JOINT_COMMITTEE_ON_CANCER_CODE,
    ]

    attributes: Dict[str, Any]

    t: str
    n: str
    m: str
    stage: str

    def main(self, attributes: Dict[str, Any]) -> Dict[str, Any]:
        self.attributes = attributes.copy()

        if not self.has_required_keys():
            return self.attributes

        self.set_tnm()
        self.set_stage()
        self.attributes[NEOPLASM_DISEASE_STAGE_AMERICAN_JOINT_COMMITTEE_ON_CANCER_CODE] = self.stage

        return self.attributes

    def set_tnm(self):
        tnm = self.attributes[CLINICAL_TNM]
        self.t = tnm.split('T')[1].split('N')[0]
        self.n = tnm.split('N')[1].split('M')[0]
        self.m = tnm.split('M')[1]

    def set_stage(self):
        t, n, m = self.t, self.n, self.m
        if m == '1':
            self.stage = 'Stage IVC'
        elif t == '4b' and m == '0':
            self.stage = 'Stage IVB'
        elif n == '3' and m == '0':
            self.stage = 'Stage IVB'
        elif t in ['1', '2', '3', '4a'] and n == '2' and m == '0':
            self.stage = 'Stage IVA'
        elif t == '4a' and n in ['0', '1'] and m == '0':
            self.stage = 'Stage IVA'
        elif t in ['1', '2', '3'] and n == '1' and m == '0':
            self.stage = 'Stage III'
        elif t == '3' and n == '0' and m == '0':
            self.stage = 'Stage III'
        elif t == '2' and n == '0' and m == '0':
            self.stage = 'Stage II'
        elif t == '1' and n == '0' and m == '0':
            self.stage = 'Stage I'
        elif t == 'is' and n == '0' and m == '0':
            self.stage = 'Stage 0'
        else:
            raise ValueError(f'Invalid "{CLINICAL_TNM}": "{self.attributes[CLINICAL_TNM]}" for finding AJCC stage')


class CalculateTotalLymphNodes(Calculate):

    REQUIRED_KEYS = [
        LYMPH_NODE_LEVEL_I,
        LYMPH_NODE_LEVEL_IA,
        LYMPH_NODE_LEVEL_IB,
        LYMPH_NODE_LEVEL_II,
        LYMPH_NODE_LEVEL_IIA,
        LYMPH_NODE_LEVEL_IIB,
        LYMPH_NODE_LEVEL_III,
        LYMPH_NODE_LEVEL_IV,
        LYMPH_NODE_LEVEL_V,
        LYMPH_NODE_RIGHT,
        LYMPH_NODE_LEFT,
        TOTAL_LYMPH_NODE,
    ]

    attributes: Dict[str, Any]

    numerator: int
    denominator: int

    def main(self, attributes: Dict[str, Any]) -> Dict[str, Any]:
        self.attributes = attributes.copy()

        if not self.has_required_keys():
            return self.attributes

        self.numerator, self.denominator = 0, 0
        self.add_level_1()
        self.add_level_2()
        self.add_level_3()
        self.add_level_4()
        self.add_level_5()
        self.add_right_left()
        self.attributes[TOTAL_LYMPH_NODE] = f'{self.numerator}/{self.denominator}'

        return self.attributes

    def add_level_1(self):
        level_1 = self.attributes.get(LYMPH_NODE_LEVEL_I, '')
        level_1a = self.attributes.get(LYMPH_NODE_LEVEL_IA, '')
        level_1b = self.attributes.get(LYMPH_NODE_LEVEL_IB, '')

        if level_1 != '':
            a, b = level_1.split('/')
            self.numerator += int(a)
            self.denominator += int(b)
            return  # no need to check level 1a and 1b

        if level_1a != '':
            a, b = level_1a.split('/')
            self.numerator += int(a)
            self.denominator += int(b)
        if level_1b != '':
            a, b = level_1b.split('/')
            self.numerator += int(a)
            self.denominator += int(b)

    def add_level_2(self):
        level_2 = self.attributes.get(LYMPH_NODE_LEVEL_II, '')
        level_2a = self.attributes.get(LYMPH_NODE_LEVEL_IIA, '')
        level_2b = self.attributes.get(LYMPH_NODE_LEVEL_IIB, '')

        if level_2 != '':
            a, b = level_2.split('/')
            self.numerator += int(a)
            self.denominator += int(b)
            return  # no need to check level 2a and 2b

        if level_2a != '':
            a, b = level_2a.split('/')
            self.numerator += int(a)
            self.denominator += int(b)
        if level_2b != '':
            a, b = level_2b.split('/')
            self.numerator += int(a)
            self.denominator += int(b)

    def add_level_3(self):
        level_3 = self.attributes.get(LYMPH_NODE_LEVEL_III, '')
        if level_3 != '':
            a, b = level_3.split('/')
            self.numerator += int(a)
            self.denominator += int(b)

    def add_level_4(self):
        level_4 = self.attributes.get(LYMPH_NODE_LEVEL_IV, '')
        if level_4 != '':
            a, b = level_4.split('/')
            self.numerator += int(a)
            self.denominator += int(b)

    def add_level_5(self):
        level_5 = self.attributes.get(LYMPH_NODE_LEVEL_V, '')
        if level_5 != '':
            a, b = level_5.split('/')
            self.numerator += int(a)
            self.denominator += int(b)

    def add_right_left(self):
        if self.numerator + self.denominator > 0:
            return  # no need to check right and left

        right = self.attributes.get(LYMPH_NODE_RIGHT, '')
        left = self.attributes.get(LYMPH_NODE_LEFT, '')
        if right != '':
            a, b = right.split('/')
            self.numerator += int(a)
            self.denominator += int(b)
        if left != '':
            a, b = left.split('/')
            self.numerator += int(a)
            self.denominator += int(b)


class CastDatatypes(Calculate):

    def main(self, attributes: Dict[str, Any]) -> Dict[str, Any]:

        for key, val in attributes.items():

            if val == '':
                attributes[key] = pd.NA
            elif self.schema.COLUMN_ATTRIBUTES[key]['type'] == 'int':
                attributes[key] = int(val)
            elif self.schema.COLUMN_ATTRIBUTES[key]['type'] == 'float':
                attributes[key] = float(val)
            elif self.schema.COLUMN_ATTRIBUTES[key]['type'] == 'datetime':
                attributes[key] = pd.to_datetime(val)
            elif self.schema.COLUMN_ATTRIBUTES[key]['type'] == 'boolean':
                attributes[key] = True if val.upper() == 'TRUE' else False

        return attributes


#


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

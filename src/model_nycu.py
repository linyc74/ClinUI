"""
This module is statically coupled with NycuOsccSchema
Thus there is no need to dynamically pass in the self.schema object
"""
import numpy as np
import pandas as pd
from typing import Dict, Any, Union, List
from .schema import NycuOsccSchema


S = NycuOsccSchema


class CalculateNycuOscc:

    def main(self, attributes: Dict[str, str]) -> Dict[str, Any]:

        attributes = CalculateDiagnosisAge().main(attributes)
        attributes = CalculateSurvival().main(attributes)
        attributes = CalculateICD().main(attributes)
        attributes = CalculateLymphNodes().main(attributes)
        attributes = CalculateStage().main(attributes)

        return attributes


class Calculate:

    REQUIRED_KEYS: List[str]
    attributes: Dict[str, Any]

    def main(self, attributes: Dict[str, Any]) -> Dict[str, Any]:
        self.attributes = attributes.copy()

        if not self.has_required_keys():
            return self.attributes

        self.calculate()

        return self.attributes

    def has_required_keys(self) -> bool:
        for key in self.REQUIRED_KEYS:
            if key not in self.attributes:
                return False
        return True

    def calculate(self):
        raise NotImplementedError


class CalculateDiagnosisAge(Calculate):

    REQUIRED_KEYS = [
        S.BIRTH_DATE,
        S.CLINICAL_DIAGNOSIS_DATE,
    ]

    def calculate(self):
        self.attributes[S.CLINICAL_DIAGNOSIS_AGE] = delta_t(
            start=self.attributes[S.BIRTH_DATE],
            end=self.attributes[S.CLINICAL_DIAGNOSIS_DATE]) / pd.Timedelta(days=365)


class CalculateSurvival(Calculate):

    REQUIRED_KEYS = [
        S.INITIAL_TREATMENT_COMPLETION_DATE,
        S.LAST_FOLLOW_UP_DATE,
        S.RECUR_DATE_AFTER_INITIAL_TREATMENT,
        S.EXPIRE_DATE,
        S.CAUSE_OF_DEATH,
    ]

    alive: bool

    def calculate(self):
        self.set_alive()
        self.check_cause_of_death()
        self.disease_free_survival()
        self.disease_specific_survival()
        self.overall_survival()

    def set_alive(self):
        expire_date = self.attributes[S.EXPIRE_DATE]
        self.alive = pd.isna(expire_date) or expire_date == ''

    def check_cause_of_death(self):
        if not self.alive:
            cause = self.attributes[S.CAUSE_OF_DEATH]
            assert cause in S.COLUMN_ATTRIBUTES[S.CAUSE_OF_DEATH]['options'], f'"{cause}" is not a valid cause of death'

    def disease_free_survival(self):
        attr = self.attributes

        recurred = attr[S.RECUR_DATE_AFTER_INITIAL_TREATMENT] != ''

        t0 = attr[S.INITIAL_TREATMENT_COMPLETION_DATE]

        if recurred:
            duration = delta_t(start=t0, end=attr[S.RECUR_DATE_AFTER_INITIAL_TREATMENT])
            status = '1:Recurred/Progressed'
        else:
            if self.alive:
                duration = delta_t(start=t0, end=attr[S.LAST_FOLLOW_UP_DATE])
                status = '0:DiseaseFree'
            else:  # died
                duration = delta_t(start=t0, end=attr[S.EXPIRE_DATE])
                if attr[S.CAUSE_OF_DEATH].upper() == 'CANCER':
                    status = '1:Recurred/Progressed'
                else:
                    status = '0:DiseaseFree'

        self.attributes[S.DISEASE_FREE_SURVIVAL_MONTHS] = '' if pd.isna(duration) else duration / pd.Timedelta(days=30)
        self.attributes[S.DISEASE_FREE_SURVIVAL_STATUS] = '' if pd.isna(duration) else status

    def disease_specific_survival(self):
        attr = self.attributes

        t0 = attr[S.INITIAL_TREATMENT_COMPLETION_DATE]

        if self.alive:
            duration = delta_t(start=t0, end=attr[S.LAST_FOLLOW_UP_DATE])
            status = '0:ALIVE OR DEAD TUMOR FREE'
        else:
            duration = delta_t(start=t0, end=attr[S.EXPIRE_DATE])
            if attr[S.CAUSE_OF_DEATH].upper() == 'CANCER':
                status = '1:DEAD WITH TUMOR'
            else:
                status = '0:ALIVE OR DEAD TUMOR FREE'

        self.attributes[S.DISEASE_SPECIFIC_SURVIVAL_MONTHS] = '' if pd.isna(duration) else duration / pd.Timedelta(days=30)
        self.attributes[S.DISEASE_SPECIFIC_SURVIVAL_STATUS] = '' if pd.isna(duration) else status

    def overall_survival(self):
        attr = self.attributes

        t0 = attr[S.INITIAL_TREATMENT_COMPLETION_DATE]

        if self.alive:
            duration = delta_t(start=t0, end=attr[S.LAST_FOLLOW_UP_DATE])
            status = '0:LIVING'
        else:
            duration = delta_t(start=t0, end=attr[S.EXPIRE_DATE])
            status = '1:DECEASED'

        self.attributes[S.OVERALL_SURVIVAL_MONTHS] = '' if pd.isna(duration) else duration / pd.Timedelta(days=30)
        self.attributes[S.OVERALL_SURVIVAL_STATUS] = '' if pd.isna(duration) else status


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
    # I manually checked ICD-10 and found it to be identical to ICD-O-3, although the wordings of ICD-10 and ICD-O-3 are slightly different
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
        S.TUMOR_DISEASE_ANATOMIC_SITE,
    ]

    def calculate(self):
        self.add_icd_o_3()
        self.add_icd_10()

    def add_icd_o_3(self):
        site = self.attributes[S.TUMOR_DISEASE_ANATOMIC_SITE]
        icd_o_3 = self.ANATOMIC_SITE_TO_ICD_O_3_SITE_CODE.get(site, '')
        self.attributes[S.ICD_O_3_SITE_CODE] = icd_o_3

    def add_icd_10(self):
        site = self.attributes[S.TUMOR_DISEASE_ANATOMIC_SITE]
        icd_10 = self.ANATOMIC_SITE_TO_ICD_10_CLASSIFICATION.get(site, '')
        self.attributes[S.ICD_10_CLASSIFICATION] = icd_10


class CalculateStage(Calculate):
    """
    https://www.cancer.org/cancer/types/oral-cavity-and-oropharyngeal-cancer/detection-diagnosis-staging/staging.html
    """

    REQUIRED_KEYS = [
        S.CLINICAL_TNM,
    ]

    t: str
    n: str
    m: str

    def calculate(self):
        self.set_tnm()
        self.calculate_stage()

    def set_tnm(self):
        try:
            tnm = self.attributes[S.CLINICAL_TNM]
            self.t = tnm.split('T')[1].split('N')[0]
            self.n = tnm.split('N')[1].split('M')[0]
            self.m = tnm.split('M')[1]
        except Exception as e:
            print(e)
            self.t, self.n, self.m = '', '', ''

    def calculate_stage(self):
        t, n, m = self.t, self.n, self.m
        if m == '1':
            stage = 'Stage IVC'
        elif t == '4b' and m == '0':
            stage = 'Stage IVB'
        elif n in ['3', '3a', '3b'] and m == '0':
            stage = 'Stage IVB'
        elif t in ['1', '2', '3', '4a'] and n in ['2', '2a', '2b', '2c'] and m == '0':
            stage = 'Stage IVA'
        elif t == '4a' and n in ['0', '1'] and m == '0':
            stage = 'Stage IVA'
        elif t in ['1', '2', '3'] and n == '1' and m == '0':
            stage = 'Stage III'
        elif t == '3' and n == '0' and m == '0':
            stage = 'Stage III'
        elif t == '2' and n == '0' and m == '0':
            stage = 'Stage II'
        elif t == '1' and n == '0' and m == '0':
            stage = 'Stage I'
        elif t == 'is' and n == '0' and m == '0':
            stage = 'Stage 0'
        else:
            print(f'WARNING! Invalid "{S.CLINICAL_TNM}": "{self.attributes[S.CLINICAL_TNM]}" for finding AJCC stage')
            stage = ''

        self.attributes[S.NEOPLASM_DISEASE_STAGE_AMERICAN_JOINT_COMMITTEE_ON_CANCER_CODE] = stage


class CalculateLymphNodes(Calculate):

    REQUIRED_KEYS = []  # all lymph node records are optional

    total_m: int
    total_n: int

    def calculate(self):
        self.total_m, self.total_n = 0, 0
        self.add_level_1a_1b()
        self.add_level_2a_2b()
        self.add_all_levels()
        self.add_right_left()
        self.attributes[S.TOTAL_LYMPH_NODE] = f'{self.total_m}/{self.total_n}'

    def add_level_1a_1b(self):
        level_1a = self.attributes.get(S.LYMPH_NODE_LEVEL_IA, '')
        level_1b = self.attributes.get(S.LYMPH_NODE_LEVEL_IB, '')

        if level_1a == '' and level_1b == '':
            return

        level_1_m, level_1_n = 0, 0

        if level_1a != '':
            m, n = level_1a.split('/')
            level_1_m += int(m)
            level_1_n += int(n)

        if level_1b != '':
            m, n = level_1b.split('/')
            level_1_m += int(m)
            level_1_n += int(n)

        self.attributes[S.LYMPH_NODE_LEVEL_I] = f'{level_1_m}/{level_1_n}'

    def add_level_2a_2b(self):
        level_2a = self.attributes.get(S.LYMPH_NODE_LEVEL_IIA, '')
        level_2b = self.attributes.get(S.LYMPH_NODE_LEVEL_IIB, '')

        if level_2a == '' and level_2b == '':
            return

        level_2_m, level_2_n = 0, 0

        if level_2a != '':
            m, n = level_2a.split('/')
            level_2_m += int(m)
            level_2_n += int(n)
        if level_2b != '':
            m, n = level_2b.split('/')
            level_2_m += int(m)
            level_2_n += int(n)

        self.attributes[S.LYMPH_NODE_LEVEL_II] = f'{level_2_m}/{level_2_n}'

    def add_all_levels(self):
        level_1 = self.attributes.get(S.LYMPH_NODE_LEVEL_I, '')
        if level_1 != '':
            a, b = level_1.split('/')
            self.total_m += int(a)
            self.total_n += int(b)

        level_2 = self.attributes.get(S.LYMPH_NODE_LEVEL_II, '')
        if level_2 != '':
            a, b = level_2.split('/')
            self.total_m += int(a)
            self.total_n += int(b)

        level_3 = self.attributes.get(S.LYMPH_NODE_LEVEL_III, '')
        if level_3 != '':
            a, b = level_3.split('/')
            self.total_m += int(a)
            self.total_n += int(b)

        level_4 = self.attributes.get(S.LYMPH_NODE_LEVEL_IV, '')
        if level_4 != '':
            a, b = level_4.split('/')
            self.total_m += int(a)
            self.total_n += int(b)

        level_5 = self.attributes.get(S.LYMPH_NODE_LEVEL_V, '')
        if level_5 != '':
            a, b = level_5.split('/')
            self.total_m += int(a)
            self.total_n += int(b)

    def add_right_left(self):
        if self.total_m + self.total_n > 0:
            return  # no need to check right and left

        right = self.attributes.get(S.LYMPH_NODE_RIGHT, '')
        left = self.attributes.get(S.LYMPH_NODE_LEFT, '')
        if right != '':
            a, b = right.split('/')
            self.total_m += int(a)
            self.total_n += int(b)
        if left != '':
            a, b = left.split('/')
            self.total_m += int(a)
            self.total_n += int(b)

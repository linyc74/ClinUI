"""
This module is the foundation of all data model-related aspects of the application.
It is the "database" schema on which everything is built.
"""
from abc import ABC
from typing import List, Dict, Any, Type


class Schema:

    NAME: str

    DISPLAY_COLUMNS: List[str]

    AUTOGENERATED_COLUMNS: List[str]

    COLUMN_ATTRIBUTES: Dict[
        str, Dict[
            str, Any
        ]
    ]

    CBIO_DROP_COLUMNS: List[str]

    CBIO_PATIENT_LEVEL_COLUMNS: List[str]

    CBIO_STUDY_INFO_FIELD_TO_OPTIONS: Dict[str, List[str]]


class BaseModel(ABC):

    schema: Type[Schema]

    def __init__(self, schema: Type[Schema]):
        self.schema = schema


class NycuOsccSchema(Schema):

    NAME = 'NYCU OSCC'

    PATIENT_ID = 'Patient ID'
    SAMPLE_ID = 'Sample ID'
    LAB_ID = 'Lab ID'
    LAB_SAMPLE_ID = 'Lab Sample ID'
    MEDICAL_RECORD_ID = 'Medical Record ID'
    PATHOLOGICAL_RECORD_ID = 'Pathological Record ID'
    PATIENT_NAME = 'Patient Name'
    SURGICAL_EXCISION_DATE = 'Surgical Excision Date'
    SEX = 'Sex'
    PATIENT_WEIGHT = 'Patient Weight (Kg)'
    PATIENT_HEIGHT = 'Patient Height (cm)'
    ETHNICITY_CATEGORY = 'Ethnicity Category'
    BIRTH_DATE = 'Birth Date'
    CLINICAL_DIAGNOSIS_DATE = 'Clinical Diagnosis Date'
    PATHOLOGICAL_DIAGNOSIS_DATE = 'Pathological Diagnosis Date'
    CLINICAL_DIAGNOSIS_AGE = 'Clinical Diagnosis Age'
    CANCER_TYPE = 'Cancer Type'
    CANCER_TYPE_DETAILED = 'Cancer Type Detailed'
    SAMPLE_TYPE = 'Sample Type'
    ONCOTREE_CODE = 'Oncotree Code'
    SOMATIC_STATUS = 'Somatic Status'
    CENTER = 'Center'
    TUMOR_DISEASE_ANATOMIC_SITE = 'Tumor Disease Anatomic Site'
    ICD_O_3_SITE_CODE = 'ICD-O-3 Site Code'
    ALCOHOL_CONSUMPTION = 'Alcohol Consumption'
    ALCOHOL_CONSUMPTION_FREQUENCY = 'Alcohol Consumption Frequency (Bottles Per Day)'
    ALCOHOL_CONSUMPTION_DURATION = 'Alcohol Consumption Duration (Years)'
    ALCOHOL_CONSUMPTION_QUIT = 'Alcohol Consumption Quit (Years)'
    BETEL_NUT_CHEWING = 'Betel Nut Chewing'
    BETEL_NUT_CHEWING_FREQUENCY = 'Betel Nut Chewing Frequency (Pieces Per Day)'
    BETEL_NUT_CHEWING_DURATION = 'Betel Nut Chewing Duration (Years)'
    BETEL_NUT_CHEWING_QUIT = 'Betel Nut Chewing Quit (Years)'
    CIGARETTE_SMOKING = 'Cigarette Smoking'
    CIGARETTE_SMOKING_FREQUENCY = 'Cigarette Smoking Frequency (Packs Per Day)'
    CIGARETTE_SMOKING_DURATION = 'Cigarette Smoking Duration (Years)'
    CIGARETTE_SMOKING_QUIT = 'Cigarette Smoking Quit (Years)'
    HISTOLOGIC_GRADE = 'Histologic Grade'
    SURGERY = 'Surgery'
    NEOADJUVANT_INDUCTION_CHEMOTHERAPY = 'Neoadjuvant/Induction Chemotherapy'
    NEOADJUVANT_INDUCTION_CHEMOTHERAPY_DRUG = 'Neoadjuvant/Induction Chemotherapy Drug'
    ADJUVANT_CHEMOTHERAPY = 'Adjuvant Chemotherapy'
    ADJUVANT_CHEMOTHERAPY_DRUG = 'Adjuvant Chemotherapy Drug'
    PALLIATIVE_CHEMOTHERAPY = 'Palliative Chemotherapy'
    PALLIATIVE_CHEMOTHERAPY_DRUG = 'Palliative Chemotherapy Drug'
    ADJUVANT_TARGETED_THERAPY = 'Adjuvant Targeted Therapy'
    ADJUVANT_TARGETED_THERAPY_DRUG = 'Adjuvant Targeted Therapy Drug'
    PALLIATIVE_TARGETED_THERAPY = 'Palliative Targeted Therapy'
    PALLIATIVE_TARGETED_THERAPY_DRUG = 'Palliative Targeted Therapy Drug'
    IMMUNOTHERAPY = 'Immunotherapy'
    IMMUNOTHERAPY_DRUG = 'Immunotherapy Drug'
    RADIATION_THERAPY = 'Radiation Therapy'
    RADIATION_THERAPY_DOSE = 'Radiation Therapy Dose (cGY)'
    IHC_ANTI_PDL1_MAB_22C3_TPS = 'IHC Anti-PDL1 mAb 22C3 TPS (%)'
    IHC_ANTI_PDL1_MAB_22C3_CPS = 'IHC Anti-PDL1 mAb 22C3 CPS (%)'
    IHC_ANTI_PDL1_MAB_28_8_TPS = 'IHC Anti-PDL1 mAb 28-8 TPS (%)'
    IHC_ANTI_PDL1_MAB_28_8_CPS = 'IHC Anti-PDL1 mAb 28-8 CPS (%)'
    LYMPH_NODE_LEVEL_I = 'Lymph Node Level I'
    LYMPH_NODE_LEVEL_IA = 'Lymph Node Level Ia'
    LYMPH_NODE_LEVEL_IB = 'Lymph Node Level Ib'
    LYMPH_NODE_LEVEL_II = 'Lymph Node Level II'
    LYMPH_NODE_LEVEL_IIA = 'Lymph Node Level IIa'
    LYMPH_NODE_LEVEL_IIB = 'Lymph Node Level IIb'
    LYMPH_NODE_LEVEL_III = 'Lymph Node Level III'
    LYMPH_NODE_LEVEL_IV = 'Lymph Node Level IV'
    LYMPH_NODE_LEVEL_V = 'Lymph Node Level V'
    LYMPH_NODE_RIGHT = 'Lymph Node (Right)'
    LYMPH_NODE_LEFT = 'Lymph Node (Left)'
    TOTAL_LYMPH_NODE = 'Total Lymph Node'
    LYMPHOVASCULAR_INVASION_LVI = 'Lymphovascular Invasion (LVI)'
    PERINEURAL_INVASION = 'Perineural Invasion (PNI)'
    CLINICAL_OVERT_EXTRANODAL_EXTENSION = 'Clinical Overt Extranodal Extension'
    PATHOLOGICAL_EXTRANODAL_EXTENSION = 'Pathological Extranodal Extension (ENE)'
    DEPTH_OF_INVASION = 'Depth of Invasion (mm)'
    TUMOR_MARGIN = 'Tumor Margin'
    CLINICAL_TNM = 'Clinical TNM (cTNM)'
    PATHOLOGICAL_TNM = 'Pathological TNM (pTNM)'
    POSTNEOADJUVANT_CLINICAL_TNM = 'Postneoadjuvant Clinical TNM (ycTNM)'
    POSTNEOADJUVANT_PATHOLOGICAL_TNM = 'Postneoadjuvant Pathological TNM (ypTNM)'
    NEOPLASM_DISEASE_STAGE_AMERICAN_JOINT_COMMITTEE_ON_CANCER_CODE = 'Neoplasm Disease Stage American Joint Committee on Cancer Code'
    ICD_10_CLASSIFICATION = 'ICD-10 Classification'
    SUBTYPE = 'Subtype'
    INITIAL_TREATMENT_COMPLETION_DATE = 'Initial Treatment Completion Date'
    LAST_FOLLOW_UP_DATE = 'Last Follow-up Date'
    RECUR_DATE_AFTER_INITIAL_TREATMENT = 'Recur Date after Initial Treatment'
    EXPIRE_DATE = 'Expire Date'
    CAUSE_OF_DEATH = 'Cause of Death'
    DISEASE_FREE_SURVIVAL_MONTHS = 'Disease Free (Months)'
    DISEASE_FREE_SURVIVAL_STATUS = 'Disease Free Status'
    DISEASE_SPECIFIC_SURVIVAL_MONTHS = 'Disease-specific Survival (Months)'
    DISEASE_SPECIFIC_SURVIVAL_STATUS = 'Disease-specific Survival Status'
    OVERALL_SURVIVAL_MONTHS = 'Overall Survival (Months)'
    OVERALL_SURVIVAL_STATUS = 'Overall Survival Status'

    DISPLAY_COLUMNS = [
        SAMPLE_ID,
        MEDICAL_RECORD_ID,
        PATHOLOGICAL_RECORD_ID,
        PATIENT_NAME,
        LAB_ID,
        LAB_SAMPLE_ID,
        SURGICAL_EXCISION_DATE,
        SEX,
        PATIENT_WEIGHT,
        PATIENT_HEIGHT,
        ETHNICITY_CATEGORY,
        BIRTH_DATE,
        CLINICAL_DIAGNOSIS_DATE,
        CLINICAL_DIAGNOSIS_AGE,
        PATHOLOGICAL_DIAGNOSIS_DATE,
        CANCER_TYPE,
        CANCER_TYPE_DETAILED,
        SAMPLE_TYPE,
        ONCOTREE_CODE,
        SOMATIC_STATUS,
        CENTER,
        TUMOR_DISEASE_ANATOMIC_SITE,
        ICD_O_3_SITE_CODE,
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
        HISTOLOGIC_GRADE,
        SURGERY,
        NEOADJUVANT_INDUCTION_CHEMOTHERAPY,
        NEOADJUVANT_INDUCTION_CHEMOTHERAPY_DRUG,
        ADJUVANT_CHEMOTHERAPY,
        ADJUVANT_CHEMOTHERAPY_DRUG,
        PALLIATIVE_CHEMOTHERAPY,
        PALLIATIVE_CHEMOTHERAPY_DRUG,
        ADJUVANT_TARGETED_THERAPY,
        ADJUVANT_TARGETED_THERAPY_DRUG,
        PALLIATIVE_TARGETED_THERAPY,
        PALLIATIVE_TARGETED_THERAPY_DRUG,
        IMMUNOTHERAPY,
        IMMUNOTHERAPY_DRUG,
        RADIATION_THERAPY,
        RADIATION_THERAPY_DOSE,
        IHC_ANTI_PDL1_MAB_22C3_TPS,
        IHC_ANTI_PDL1_MAB_22C3_CPS,
        IHC_ANTI_PDL1_MAB_28_8_TPS,
        IHC_ANTI_PDL1_MAB_28_8_CPS,
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
        LYMPHOVASCULAR_INVASION_LVI,
        PERINEURAL_INVASION,
        CLINICAL_OVERT_EXTRANODAL_EXTENSION,
        PATHOLOGICAL_EXTRANODAL_EXTENSION,
        DEPTH_OF_INVASION,
        TUMOR_MARGIN,
        CLINICAL_TNM,
        PATHOLOGICAL_TNM,
        POSTNEOADJUVANT_CLINICAL_TNM,
        POSTNEOADJUVANT_PATHOLOGICAL_TNM,
        NEOPLASM_DISEASE_STAGE_AMERICAN_JOINT_COMMITTEE_ON_CANCER_CODE,
        ICD_10_CLASSIFICATION,
        SUBTYPE,
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

    AUTOGENERATED_COLUMNS = [
        CLINICAL_DIAGNOSIS_AGE,
        ICD_O_3_SITE_CODE,
        ICD_10_CLASSIFICATION,
        NEOADJUVANT_INDUCTION_CHEMOTHERAPY,
        ADJUVANT_CHEMOTHERAPY,
        PALLIATIVE_CHEMOTHERAPY,
        ADJUVANT_TARGETED_THERAPY,
        PALLIATIVE_TARGETED_THERAPY,
        IMMUNOTHERAPY,
        NEOPLASM_DISEASE_STAGE_AMERICAN_JOINT_COMMITTEE_ON_CANCER_CODE,
        DISEASE_FREE_SURVIVAL_MONTHS,
        DISEASE_FREE_SURVIVAL_STATUS,
        DISEASE_SPECIFIC_SURVIVAL_MONTHS,
        DISEASE_SPECIFIC_SURVIVAL_STATUS,
        OVERALL_SURVIVAL_MONTHS,
        OVERALL_SURVIVAL_STATUS,
    ]

    COLUMN_ATTRIBUTES = {
        SAMPLE_ID: {
            'type': 'str',
            'options': ['000-00000-0000-E-X00-00'],
        },
        MEDICAL_RECORD_ID: {
            'type': 'str',
        },
        PATHOLOGICAL_RECORD_ID: {
            'type': 'str',
        },
        PATIENT_NAME: {
            'type': 'str',
        },
        LAB_ID: {
            'type': 'str',
            'options': ['XXX_LAB'],
        },
        LAB_SAMPLE_ID: {
            'type': 'str',
            'options': ['VGH_001_T', 'NYCUH_001_T'],
        },
        PATIENT_ID: {
            'type': 'str',
            'options': ['000-00000'],
        },
        SURGICAL_EXCISION_DATE: {
            'type': 'date',
            'options': ['2020-01-01'],
        },
        SEX: {
            'type': 'str',
            'options': ['Male', 'Female'],
        },
        PATIENT_WEIGHT: {
            'type': 'float',
            'options': [0.0],
        },
        PATIENT_HEIGHT: {
            'type': 'float',
            'options': [0.0],
        },
        ETHNICITY_CATEGORY: {
            'type': 'str',
            'options': ['Han', 'Aboriginal'],
        },
        BIRTH_DATE: {
            'type': 'date',
            'options': ['1900-01-01'],
        },
        CLINICAL_DIAGNOSIS_DATE: {
            'type': 'date',
            'options': ['2020-01-01'],
        },
        PATHOLOGICAL_DIAGNOSIS_DATE: {
            'type': 'date',
            'options': ['2020-01-01'],
        },
        CLINICAL_DIAGNOSIS_AGE: {
            'type': 'float',
        },
        CANCER_TYPE: {
            'type': 'str',
            'options': ['Head and Neck Cancer'],
        },
        CANCER_TYPE_DETAILED: {
            'type': 'str',
            'options': [
                'Head and Neck Squamous Cell Carcinoma',
                'Oral Cavity Squamous Cell Carcinoma',
                'Salivary Carcinoma',
                'Mucoepideroid Carcinoma',
            ],
        },
        SAMPLE_TYPE: {
            'type': 'str',
            'options': ['Primary', 'Precancer', 'Recurrent'],
        },
        ONCOTREE_CODE: {
            'type': 'str',
            'options': ['OCSC', 'OPHSC'],
        },
        SOMATIC_STATUS: {
            'type': 'str',
            'options': ['Matched Adjacent Normal', 'Matched Blood Normal', 'Tumor Only'],
        },
        CENTER: {
            'type': 'str',
            'options': ['Taipei Veterans General Hospital', 'National Yang Ming Chiao Tung University Hospital'],
        },
        TUMOR_DISEASE_ANATOMIC_SITE: {
            'type': 'str',
            'options': [
                'Retromolar Triangle',
                'Right Tongue',
                'Left Tongue',
                'Cross Midline (CM) Tongue',
                'Left Upper Gingiva',
                'Left Lower Gingiva',
                'Right Upper Gingiva',
                'Right Lower Gingiva',
                'Cross Midline (CM) Left Upper Gingiva',
                'Cross Midline (CM) Right Lower Gingiva',
                'Cross Midline (CM) Gingiva',
                'Left Palate',
                'Right Palate',
                'Cross Midline (CM) Palate',
                'Upper Lip',
                'Lower Lip',
                'External Upper Lip',
                'External Lower Lip',
                'Upper Lip Inner Aspect',
                'Lower Lip Inner Aspect',
                'Cross Midline (CM) Lip',
                'Left Buccal Mucosa',
                'Right Buccal Mucosa',
            ],
        },
        ICD_O_3_SITE_CODE: {
            'type': 'str',
        },
        ALCOHOL_CONSUMPTION: {
            'type': 'str',
            'options': ['Current', 'Ex', 'Never', 'Denied'],
        },
        ALCOHOL_CONSUMPTION_FREQUENCY: {
            'type': 'str',
            'options': ['0.0', 'Occasional', 'Social', 'Heavy'],
        },
        ALCOHOL_CONSUMPTION_DURATION: {
            'type': 'float',
            'options': [0.0],
        },
        ALCOHOL_CONSUMPTION_QUIT: {
            'type': 'float',
            'options': [0.0],
        },
        BETEL_NUT_CHEWING: {
            'type': 'str',
            'options': ['Current', 'Ex', 'Never', 'Denied'],
        },
        BETEL_NUT_CHEWING_FREQUENCY: {
            'type': 'str',
            'options': ['0.0', 'Occasional', 'Social', 'Heavy'],
        },
        BETEL_NUT_CHEWING_DURATION: {
            'type': 'float',
            'options': [0.0],
        },
        BETEL_NUT_CHEWING_QUIT: {
            'type': 'float',
            'options': [0.0],
        },
        CIGARETTE_SMOKING: {
            'type': 'str',
            'options': ['Current', 'Ex', 'Never', 'Denied']
        },
        CIGARETTE_SMOKING_FREQUENCY: {
            'type': 'sting',
            'options': ['0.0', 'Occasional', 'Social', 'Heavy'],
        },
        CIGARETTE_SMOKING_DURATION: {
            'type': 'float',
            'options': [0.0],
        },
        CIGARETTE_SMOKING_QUIT: {
            'type': 'float',
            'options': [0.0],
        },
        HISTOLOGIC_GRADE: {
            'type': 'str',
            'options': ['Well Differentiated', 'Moderately Differentiated', 'Poorly Differentiated',
                        'Undifferentated Anaplastic'],
        },
        SURGERY: {
            'type': 'str',
            'options': ['Wide Excision', 'Neck Dissection', 'Wide Excision and Neck Dissection'],
        },
        NEOADJUVANT_INDUCTION_CHEMOTHERAPY: {
            'type': 'bool',
            'options': [False, True],
        },
        NEOADJUVANT_INDUCTION_CHEMOTHERAPY_DRUG: {
            'type': 'str',
            'options': [
                '',
                'None',
                'Cisplatin',
                '5-FU',
                'Docetaxel',
                'Cisplatin, 5-FU',
                'Docetaxel, Cisplatin',
                'Docetaxel, Cisplatin, 5-FU (TPF)',
                'Cisplatin, Mitomycin, 5-FU (PMU)',
            ],
        },
        ADJUVANT_CHEMOTHERAPY: {
            'type': 'bool',
            'options': [False, True],
        },
        ADJUVANT_CHEMOTHERAPY_DRUG: {
            'type': 'str',
            'options': [
                'Cisplatin, Mitomycin, 5-FU (PMU)',
                'Cisplatin, 5-FU, Leucovorin (PFL)',
                'None',
                'Cisplatin',
                '5-FU',
                'Docetaxel',
                'Cisplatin, 5-FU',
                'Cisplatin, Docetaxel',
                'Docetaxel, Cisplatin, 5-FU (TPF)',
            ],
        },
        PALLIATIVE_CHEMOTHERAPY: {
            'type': 'bool',
            'options': [False, True],
        },
        PALLIATIVE_CHEMOTHERAPY_DRUG: {
            'type': 'str',
            'options': [
                '',
                'None',
                'Cisplatin',
                '5-FU',
                'Docetaxel',
                'Cisplatin, 5-FU',
                'Docetaxel, Cisplatin',
                'Docetaxel, Cisplatin, 5-FU (TPF)',
                'Cisplatin, Mitomycin, 5-FU (PMU)',
            ],
        },
        ADJUVANT_TARGETED_THERAPY: {
            'type': 'bool',
            'options': [False, True],
        },
        ADJUVANT_TARGETED_THERAPY_DRUG: {
            'type': 'str',
            'options': [
                '',
                'None',
                'Cetuximab',
                'Cetuximab and Docetaxel',
            ],
        },
        PALLIATIVE_TARGETED_THERAPY: {
            'type': 'bool',
            'options': [False, True],
        },
        PALLIATIVE_TARGETED_THERAPY_DRUG: {
            'type': 'str',
            'options': [
                '',
                'None',
                'Cetuximab',
                'Cetuximab and Docetaxel',
            ],
        },
        IMMUNOTHERAPY: {
            'type': 'bool',
            'options': [False, True],
        },
        IMMUNOTHERAPY_DRUG: {
            'type': 'str',
            'options': [
                '',
                'None',
                'Pembrolizumab',
                'Nivolumab',
            ],
        },
        RADIATION_THERAPY: {
            'type': 'str',
            'options': ['Adjuvant', 'None', 'Definitive', 'Palliative'],
        },
        RADIATION_THERAPY_DOSE: {
            'type': 'float',
            'options': [6600.0, 0.0],
        },
        IHC_ANTI_PDL1_MAB_22C3_TPS: {
            'type': 'str',
            'options': ['> 50%', '< 50%', 'NA'],
        },
        IHC_ANTI_PDL1_MAB_22C3_CPS: {
            'type': 'str',
            'options': ['> 50%', '< 50%', 'NA'],
        },
        IHC_ANTI_PDL1_MAB_28_8_TPS: {
            'type': 'str',
            'options': ['> 50%', '< 50%', 'NA'],
        },
        IHC_ANTI_PDL1_MAB_28_8_CPS: {
            'type': 'str',
            'options': ['> 50%', '< 50%', 'NA'],
        },
        LYMPH_NODE_LEVEL_I: {
            'type': 'str',
            'options': ['0/0', ''],
        },
        LYMPH_NODE_LEVEL_IA: {
            'type': 'str',
            'options': ['0/0', ''],
        },
        LYMPH_NODE_LEVEL_IB: {
            'type': 'str',
            'options': ['0/0', ''],
        },
        LYMPH_NODE_LEVEL_II: {
            'type': 'str',
            'options': ['0/0', ''],
        },
        LYMPH_NODE_LEVEL_IIA: {
            'type': 'str',
            'options': ['0/0', ''],
        },
        LYMPH_NODE_LEVEL_IIB: {
            'type': 'str',
            'options': ['0/0', ''],
        },
        LYMPH_NODE_LEVEL_III: {
            'type': 'str',
            'options': ['0/0', ''],
        },
        LYMPH_NODE_LEVEL_IV: {
            'type': 'str',
            'options': ['0/0', ''],
        },
        LYMPH_NODE_LEVEL_V: {
            'type': 'str',
            'options': ['0/0', ''],
        },
        LYMPH_NODE_RIGHT: {
            'type': 'str',
            'options': ['0/0', ''],
        },
        LYMPH_NODE_LEFT: {
            'type': 'str',
            'options': ['0/0', ''],
        },
        TOTAL_LYMPH_NODE: {
            'type': 'str',
            'options': ['0/0', ''],
        },
        LYMPHOVASCULAR_INVASION_LVI: {
            'type': 'str',
            'options': ['Negative', 'Positive', 'Suspicious'],
        },
        PERINEURAL_INVASION: {
            'type': 'str',
            'options':  ['Negative', 'Positive', 'Extensive'],
        },
        CLINICAL_OVERT_EXTRANODAL_EXTENSION: {
            'type': 'str',
            'options': ['Negative', 'Positive'],
        },
        PATHOLOGICAL_EXTRANODAL_EXTENSION: {
            'type': 'str',
            'options': ['Negative', 'Micro', 'Macro'],
        },
        DEPTH_OF_INVASION: {
            'type': 'float',
            'options': [0.0],
        },
        TUMOR_MARGIN: {
            'type': 'str',
            'options': ['Negative', 'Close', 'Positive', '1 mm', '2 mm', '3 mm', '4 mm'],
        },
        CLINICAL_TNM: {
            'type': 'str',
            'options': [
                'T1N0M0',
                'TisN0M0',
                'T2N0M0',
                'T3N0M0',
                'T1N1M0',
                'T2N1M0',
                'T3N1M0',
                'T4aN0M0',
                'T4aN1M0',
                'T1N2M0',
                'T2N2M0',
                'T3N2M0',
                'T4aN2M0',
                'T1N3M0',
                'T2N3M0',
                'T3N3M0',
                'T4aN3M0',
                'T4bN0M0',
                'T4bN1M0',
                'T4bN2M0',
                'T4bN3M0',
                'T4bN3M1',
            ],
        },
        PATHOLOGICAL_TNM: {
            'type': 'str',
            'options': [
                'T1N0M0',
                'TisN0M0',
                'T2N0M0',
                'T3N0M0',
                'T1N1M0',
                'T2N1M0',
                'T3N1M0',
                'T4aN0M0',
                'T4aN1M0',
                'T1N2M0',
                'T2N2M0',
                'T3N2M0',
                'T4aN2M0',
                'T1N3M0',
                'T2N3M0',
                'T3N3M0',
                'T4aN3M0',
                'T4bN0M0',
                'T4bN1M0',
                'T4bN2M0',
                'T4bN3M0',
                'T4bN3M1',
            ],
        },
        POSTNEOADJUVANT_CLINICAL_TNM: {
            'type': 'str',
            'options': [
                '',
                'T1N0M0',
                'TisN0M0',
                'T2N0M0',
                'T3N0M0',
                'T1N1M0',
                'T2N1M0',
                'T3N1M0',
                'T4aN0M0',
                'T4aN1M0',
                'T1N2M0',
                'T2N2M0',
                'T3N2M0',
                'T4aN2M0',
                'T1N3M0',
                'T2N3M0',
                'T3N3M0',
                'T4aN3M0',
                'T4bN0M0',
                'T4bN1M0',
                'T4bN2M0',
                'T4bN3M0',
                'T4bN3M1',
            ],
        },
        POSTNEOADJUVANT_PATHOLOGICAL_TNM: {
            'type': 'str',
            'options': [
                '',
                'T1N0M0',
                'TisN0M0',
                'T2N0M0',
                'T3N0M0',
                'T1N1M0',
                'T2N1M0',
                'T3N1M0',
                'T4aN0M0',
                'T4aN1M0',
                'T1N2M0',
                'T2N2M0',
                'T3N2M0',
                'T4aN2M0',
                'T1N3M0',
                'T2N3M0',
                'T3N3M0',
                'T4aN3M0',
                'T4bN0M0',
                'T4bN1M0',
                'T4bN2M0',
                'T4bN3M0',
                'T4bN3M1',
            ],
        },
        NEOPLASM_DISEASE_STAGE_AMERICAN_JOINT_COMMITTEE_ON_CANCER_CODE: {
            'type': 'str',
            'options': ['Stage I', 'Stage II', 'Stage III', 'Stage IVA', 'Stage IVB', 'Stage IVC'],
        },
        ICD_10_CLASSIFICATION: {
            'type': 'str',
        },
        SUBTYPE: {
            'type': 'str',
            'options': ['HNSC HPV-', 'HNSC HPV+', ''],
        },
        INITIAL_TREATMENT_COMPLETION_DATE: {
            'type': 'date',
            'options': ['2020-01-01'],
        },
        LAST_FOLLOW_UP_DATE: {
            'type': 'date',
            'options': ['2020-01-01'],
        },
        RECUR_DATE_AFTER_INITIAL_TREATMENT: {
            'type': 'date',
            'options': ['', '2020-01-01'],
        },
        EXPIRE_DATE: {
            'type': 'date',
            'options': ['', '2020-01-01'],
        },
        CAUSE_OF_DEATH: {
            'type': 'str',
            'options': ['', 'Cancer', 'Other Disease', 'Other Cancer', 'Uncertain'],
        },
        DISEASE_FREE_SURVIVAL_MONTHS: {
            'type': 'float',
        },
        DISEASE_FREE_SURVIVAL_STATUS: {
            'type': 'str',
            'options': ['0:DiseaseFree', '1:Recurred/Progressed'],
        },
        DISEASE_SPECIFIC_SURVIVAL_MONTHS: {
            'type': 'float',
        },
        DISEASE_SPECIFIC_SURVIVAL_STATUS: {
            'type': 'str',
            'options': ['0:ALIVE OR DEAD TUMOR FREE', '1:DEAD WITH TUMOR'],
        },
        OVERALL_SURVIVAL_MONTHS: {
            'type': 'float',
        },
        OVERALL_SURVIVAL_STATUS: {
            'type': 'str',
            'options': ['0:LIVING', '1:DECEASED'],
        },
    }

    CBIO_DROP_COLUMNS = [
        MEDICAL_RECORD_ID,
        PATHOLOGICAL_RECORD_ID,
        PATIENT_NAME,
        LAB_SAMPLE_ID,
        BIRTH_DATE,
        CLINICAL_DIAGNOSIS_DATE,
        PATHOLOGICAL_DIAGNOSIS_DATE,
        INITIAL_TREATMENT_COMPLETION_DATE,
        LAST_FOLLOW_UP_DATE,
        EXPIRE_DATE,
        RECUR_DATE_AFTER_INITIAL_TREATMENT,
    ]

    CBIO_PATIENT_LEVEL_COLUMNS = [
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

    CBIO_STUDY_INFO_FIELD_TO_OPTIONS = {
        'type_of_cancer': ['hnsc'],
        'cancer_study_identifier': ['hnsc_nycu_2024'],
        'name': ['Head and Neck Squamous Cell Carcinomas (NYCU, 2024)'],
        'description': ['Whole exome sequencing of oral squamous cell carcinoma (OSCC) tumor/normal pairs'],
        'groups': ['PUBLIC'],
        'reference_genome': ['hg38'],
        'source_data': ['yy_mmdd_dataset'],
    }


class VghtpeLuadSchema(Schema):

    NAME = 'VGHTPE LUAD'

    SERIAL_NO = 'Serial No'
    GENDER = 'Gender'
    AGE = 'AGE'
    SMOKING_YN = 'Smoking_YN'
    FAMILY_HISTORY_YN = 'Family_History_YN'
    NEODJUVANT_THERAPY_YN = 'Neodjuvant_therapy_YN'
    ADJUVANT_THERAPY_YN = 'Adjuvant_therapy_YN'
    LAST_F_U_DATE = 'Last f/u date'
    DFS = 'DFS'
    DEATH_Y1N0 = 'Death Y1N0'
    DEATH_DATE = 'Death date'
    OS = 'OS'
    HISTOLOGIC_TYPE = 'Histologic type'
    SUBTYPE_FOR_INVASIVE_NONMUCINOUS_ADENOCARCINOMA = 'Subtype for invasive nonmucinous adenocarcinoma'
    HISTOLOGIC_GRADE = 'Histologic Grade'
    SPREAD_THROUGH_AIR_SPACES_STAS = 'Spread Through Air Spaces (STAS)'
    VISCERAL_PLEURA_INVASION = 'Visceral Pleura Invasion'
    LYMPHOVASCULAR_INVASION = 'Lymphovascular Invasion'
    PRIMARY_TUMOR_PT = 'Primary Tumor (pT)'
    REGIONAL_LYMPH_NODES_PN = 'Regional Lymph Nodes (pN)'
    DISTANT_METASTASIS_PM = 'Distant Metastasis (pM)'

    DISPLAY_COLUMNS = [
        SERIAL_NO,
        GENDER,
        AGE,
        SMOKING_YN,
        FAMILY_HISTORY_YN,
        NEODJUVANT_THERAPY_YN,
        ADJUVANT_THERAPY_YN,
        LAST_F_U_DATE,
        DFS,
        DEATH_Y1N0,
        DEATH_DATE,
        OS,
        HISTOLOGIC_TYPE,
        SUBTYPE_FOR_INVASIVE_NONMUCINOUS_ADENOCARCINOMA,
        HISTOLOGIC_GRADE,
        SPREAD_THROUGH_AIR_SPACES_STAS,
        VISCERAL_PLEURA_INVASION,
        LYMPHOVASCULAR_INVASION,
        PRIMARY_TUMOR_PT,
        REGIONAL_LYMPH_NODES_PN,
        DISTANT_METASTASIS_PM,
    ]

    AUTOGENERATED_COLUMNS = []

    COLUMN_ATTRIBUTES = {
        SERIAL_NO: {
            'type': 'str',
            'options': ['C0000'],
        },
        GENDER: {
            'type': 'str',
            'options': ['F', 'M'],
        },
        AGE: {
            'type': 'int',
        },
        SMOKING_YN: {
            'type': 'str',
            'options': ['0', '1', 'NA'],
        },
        FAMILY_HISTORY_YN: {
            'type': 'str',
            'options': ['0', '1', 'NA'],
        },
        NEODJUVANT_THERAPY_YN: {
            'type': 'str',
            'options': ['0', '1', 'NA'],
        },
        ADJUVANT_THERAPY_YN: {
            'type': 'str',
            'options': ['0', '1', 'NA'],
        },
        LAST_F_U_DATE: {
            'type': 'date',
            'options': ['', '2020-01-01'],
        },
        DFS: {
            'type': 'float',
        },
        DEATH_Y1N0: {
            'type': 'str',
            'options': ['0', '1', 'NA'],
        },
        DEATH_DATE: {
            'type': 'date',
            'options': ['', '2020-01-01'],
        },
        OS: {
            'type': 'float',
        },
        HISTOLOGIC_TYPE: {
            'type': 'str',
            'options': [
                'Minimally invasive adenocarcinoma, nonmucinous',
                'Invasive adenocarcinoma, nonmucinous',
                'Invasive squamous cell carcinoma, non-keratinizing',
                'Invasive squamous cell carcinoma, keratinizing',
                'Adenosquamous carcinoma'
            ],
        },
        SUBTYPE_FOR_INVASIVE_NONMUCINOUS_ADENOCARCINOMA: {
            'type': 'str',
            'options': ['NA', 'Acinar', 'Micropapillary', 'Lepidic', 'Solid', 'Papillary'],
        },
        HISTOLOGIC_GRADE: {
            'type': 'str',
            'options': [
                'G1: Well differentiated',
                'G2: Moderately differentiated',
                'G3: Poorly differentiated',
                'Not applicable'
            ],
        },
        SPREAD_THROUGH_AIR_SPACES_STAS: {
            'type': 'str',
            'options': ['Not identified', 'Present'],
        },
        VISCERAL_PLEURA_INVASION: {
            'type': 'str',
            'options': ['Not identified', 'Present (PL1)', 'Present (PL2)'],
        },
        LYMPHOVASCULAR_INVASION: {
            'type': 'str',
            'options': ['Not identified', 'Present'],
        },
        PRIMARY_TUMOR_PT: {
            'type': 'str',
            'options': ['pT1mi', 'pT1a', 'pT1b', 'pT2a', 'pT2b', 'pT3'],
        },
        REGIONAL_LYMPH_NODES_PN: {
            'type': 'str',
            'options': ['pN0', 'pN1', 'pN2', 'pNX'],
        },
        DISTANT_METASTASIS_PM: {
            'type': 'str',
            'options': ['No distant metastasis in specimen examined'],
        },
    }

    CBIO_DROP_COLUMNS = [
        LAST_F_U_DATE,
        DEATH_DATE,
    ]

    CBIO_PATIENT_LEVEL_COLUMNS = [
        GENDER,
        AGE,
        SMOKING_YN,
        FAMILY_HISTORY_YN,
        NEODJUVANT_THERAPY_YN,
        ADJUVANT_THERAPY_YN,
        DFS,
        DEATH_Y1N0,
        OS,
    ]

    CBIO_STUDY_INFO_FIELD_TO_OPTIONS = {
        'type_of_cancer': ['luad'],
        'cancer_study_identifier': ['luad_vghtpe_2024'],
        'name': ['Lung Adenocarcinoma (VGHTPE, 2024)'],
        'description': ['Whole exome sequencing of LUAD tumor/normal pairs'],
        'groups': ['PUBLIC'],
        'reference_genome': ['hg38'],
        'source_data': ['dataset'],
    }


class VghtpeHnsccSchema(Schema):

    NAME = 'VGHTPE HNSCC'

    STUDY_NUM = 'Study_num'
    T = 'T'
    N = 'N'
    M = 'M'
    STAGE = 'stage'
    RECURRENCE = 'recurrence'
    PATHOLOGICAL_DIAGNOSIS_DATE_VGHTPE_HNSCC = 'pathological_diagnosis_date'
    ENE = 'ENE'
    PNI = 'PNI'
    LVI = 'LVI'
    T_EMBOLI = 'T Emboli'
    WPOI = 'WPOI'

    DISPLAY_COLUMNS = [
        STUDY_NUM,
        T,
        N,
        M,
        STAGE,
        RECURRENCE,
        PATHOLOGICAL_DIAGNOSIS_DATE_VGHTPE_HNSCC,
        ENE,
        PNI,
        LVI,
        T_EMBOLI,
        WPOI,
    ]

    AUTOGENERATED_COLUMNS = []

    COLUMN_ATTRIBUTES = {
        STUDY_NUM: {
            'type': 'str',
            'options': ['H0000']
        },
        T: {
            'type': 'str',
            'options': ['1', '1a', '1b', '2', '3', '3a', '4', '4a', '4b', 'is', 'NA']
        },
        N: {
            'type': 'str',
            'options': ['0', '1', '2', '2a', '2b', '2c', '3', '3a', '3b', 'NA']
        },
        M: {
            'type': 'str',
            'options': ['0', '1', 'NA']
        },
        STAGE: {
            'type': 'str',
            'options': ['0', 'I', 'IA', 'IB', 'II', 'IIB', 'III', 'IIIB', 'IVA', 'IVB', 'IVC', 'NA']
        },
        RECURRENCE: {
            'type': 'str',
            'options': ['0', '1', 'NA']
        },
        PATHOLOGICAL_DIAGNOSIS_DATE_VGHTPE_HNSCC: {
            'type': 'str',
            'options': ['2020-01-01']
        },
        ENE: {
            'type': 'str',
            'options': ['0', '1', 'NA', 'PNOS']
        },
        PNI: {
            'type': 'str',
            'options': ['0', '1', 'NA']
        },
        LVI: {
            'type': 'str',
            'options': ['0', '1', 'NA']
        },
        T_EMBOLI: {
            'type': 'str',
            'options': ['0', '1', 'NA']
        },
        WPOI: {
            'type': 'str',
            'options': ['0', '1', 'NA']
        },
    }

    CBIO_DROP_COLUMNS = [
        PATHOLOGICAL_DIAGNOSIS_DATE_VGHTPE_HNSCC,
    ]

    CBIO_PATIENT_LEVEL_COLUMNS = []

    CBIO_STUDY_INFO_FIELD_TO_OPTIONS = {
        'type_of_cancer': ['hnsc'],
        'cancer_study_identifier': ['hnsc_vghtpe_2024'],
        'name': ['Head and Neck Squamous Cell Carcinoma (VGHTPE, 2024)'],
        'description': ['Whole exome sequencing of HNSCC tumor/normal pairs'],
        'groups': ['PUBLIC'],
        'reference_genome': ['hg38'],
        'source_data': ['dataset'],
    }


DATA_SCHEMA_DICT = {
    NycuOsccSchema.NAME: NycuOsccSchema,
    VghtpeLuadSchema.NAME: VghtpeLuadSchema,
    VghtpeHnsccSchema.NAME: VghtpeHnsccSchema,
}

STUDY_IDENTIFIER_KEY = 'cancer_study_identifier'
DESCRIPTION_KEY = 'description'


STUDY_ID = 'Study ID'
PATIENT_ID = 'Patient ID'
SAMPLE_ID = 'Sample ID'
LAB_ID = 'Lab ID'
LAB_SAMPLE_ID = 'Lab Sample ID'
SEX = 'Sex'
PATIENT_WEIGHT = 'Patient Weight (Kg)'
PATIENT_HEIGHT = 'Patient Height (cm)'
ETHNICITY_CATEGORY = 'Ethnicity Category'
BIRTH_DATE = 'Birth Date'
CLINICAL_DIAGNOSIS_DATE = 'Clinical Diagnosis Date'
PATHOLOGICAL_DIAGNOSIS_DATE = 'Pathological Diagnosis Date'
DIAGNOSIS_AGE = 'Diagnosis Age'
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
LYMPHOVASCULAR_INVASION = 'Lymphovascular Invasion (LVI)'
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


USER_INPUT_COLUMNS = [
    STUDY_ID,
    SAMPLE_ID,
    LAB_ID,
    LAB_SAMPLE_ID,
    SEX,
    PATIENT_WEIGHT,
    PATIENT_HEIGHT,
    ETHNICITY_CATEGORY,
    BIRTH_DATE,
    CLINICAL_DIAGNOSIS_DATE,
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
    LYMPHOVASCULAR_INVASION,
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
]
PATIENT_LEVEL_COLUMNS = [
    PATIENT_ID,
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


SCHEMA = {
    STUDY_ID: {
        'nullable': False,
        'type': 'string',
    },
    SAMPLE_ID: {
        'nullable': False,
        'type': 'string',
    },
    LAB_SAMPLE_ID: {
        'nullable': False,
        'type': 'string',
    },
    PATIENT_ID: {
        'nullable': False,
        'type': 'string',
    },
    SEX: {
        'nullable': True,
        'type': 'string',
        'options': ['Male', 'Female'],
    },
    PATIENT_WEIGHT: {
        'nullable': True,
        'type': 'float',
    },
    ETHNICITY_CATEGORY: {
        'nullable': True,
        'type': 'string',
        'options': ['Han', 'Aboriginal'],
    },
    BIRTH_DATE: {
        'nullable': True,
        'type': 'date',
    },
    CLINICAL_DIAGNOSIS_DATE: {
        'nullable': True,
        'type': 'date',
    },
    PATHOLOGICAL_DIAGNOSIS_DATE: {
        'nullable': True,
        'type': 'date',
    },
    DIAGNOSIS_AGE: {
        'nullable': True,
        'type': 'float',
    },
    CANCER_TYPE: {
        'nullable': True,
        'type': 'string',
        'options': ['Head and Neck Cancer'],
    },
    CANCER_TYPE_DETAILED: {
        'nullable': True,
        'type': 'string',
        'options': ['Oral Cavity Squamous Cell Carcinoma', 'Head and Neck Squamous Cell Carcinoma'],
    },
    SAMPLE_TYPE: {
        'nullable': True,
        'type': 'string',
        'options': ['Primary', 'Precancer', 'Recurrent'],
    },
    ONCOTREE_CODE: {
        'nullable': True,
        'type': 'string',
        'options': ['OCSC', 'OPHSC'],
    },
    SOMATIC_STATUS: {
        'nullable': True,
        'type': 'string',
        'options': ['Matched Adjacent Normal', 'Matched Blood Normal', 'Tumor Only'],
    },
    CENTER: {
        'nullable': True,
        'type': 'string',
        'options': ['Taipei Veterans General Hospital', 'National Yang Ming Chiao Tung University Hospital'],
    },
    TUMOR_DISEASE_ANATOMIC_SITE: {
        'nullable': True,
        'type': 'string',
    },
    ICD_O_3_SITE_CODE: {
        'nullable': True,
        'type': 'string',
    },
    ALCOHOL_CONSUMPTION: {
        'nullable': True,
        'type': 'string',
        'options': ['Current', 'Ex', 'Never'],
    },
    ALCOHOL_CONSUMPTION_FREQUENCY: {
        'nullable': True,
        'type': 'float',
    },
    ALCOHOL_CONSUMPTION_DURATION: {

        'nullable': True,
        'type': 'float',
    },
    ALCOHOL_CONSUMPTION_QUIT: {
        'nullable': True,
        'type': 'float',
    },
    BETEL_NUT_CHEWING: {
        'nullable': True,
        'type': 'string',
        'options': ['Current', 'Ex', 'Never'],
    },
    BETEL_NUT_CHEWING_FREQUENCY: {
        'nullable': True,
        'type': 'float',
    },
    BETEL_NUT_CHEWING_DURATION: {
        'nullable': True,
        'type': 'float',
    },
    BETEL_NUT_CHEWING_QUIT: {
        'nullable': True,
        'type': 'float',
    },
    CIGARETTE_SMOKING: {
        'nullable': True,
        'type': 'string',
        'options': ['Current', 'Ex', 'Never']
    },
    CIGARETTE_SMOKING_FREQUENCY: {
        'nullable': True,
        'type': 'float',
    },
    CIGARETTE_SMOKING_DURATION: {
        'nullable': True,
        'type': 'float',
    },
    CIGARETTE_SMOKING_QUIT: {
        'nullable': True,
        'type': 'float',
    },
    HISTOLOGIC_GRADE: {
        'nullable': True,
        'type': 'string',
        'options': ['Well Differentiated', 'Moderately Differentiated', 'Poorly Differentiated', 'Undifferentated Anaplastic'],
    },
    SURGERY: {
        'nullable': True,
        'type': 'string',
        'options': ['Wide Excision', 'Neck Dissection', 'Wide Excision and Neck Dissection'],
    },
    NEOADJUVANT_INDUCTION_CHEMOTHERAPY: {
        'nullable': True,
        'type': 'boolean',
        'options': [True, False],
    },
    NEOADJUVANT_INDUCTION_CHEMOTHERAPY_DRUG: {
        'nullable': True,
        'type': 'string',
    },
    ADJUVANT_CHEMOTHERAPY: {
        'nullable': True,
        'type': 'boolean',
        'options': [True, False],
    },
    ADJUVANT_CHEMOTHERAPY_DRUG: {
        'nullable': True,
        'type': 'string',
    },
    PALLIATIVE_CHEMOTHERAPY: {
        'nullable': True,
        'type': 'boolean',
        'options': [True, False],
    },
    PALLIATIVE_CHEMOTHERAPY_DRUG: {
        'nullable': True,
        'type': 'string',
    },
    ADJUVANT_TARGETED_THERAPY: {
        'nullable': True,
        'type': 'boolean',
        'options': [True, False],
    },
    ADJUVANT_TARGETED_THERAPY_DRUG: {
        'nullable': True,
        'type': 'string',
    },
    PALLIATIVE_TARGETED_THERAPY: {
        'nullable': True,
        'type': 'boolean',
        'options': [True, False],
    },
    PALLIATIVE_TARGETED_THERAPY_DRUG: {
        'nullable': True,
        'type': 'string',
    },
    IMMUNOTHERAPY: {
        'nullable': True,
        'type': 'boolean',
        'options': [True, False],
    },
    IMMUNOTHERAPY_DRUG: {
        'nullable': True,
        'type': 'string',
        'options': ['Pembrolizumab', 'Nivolumab'],
    },
    RADIATION_THERAPY: {
        'nullable': True,
        'type': 'string',
        'options': ['Definitive', 'Adjuvant', 'Palliative'],
    },
    RADIATION_THERAPY_DOSE: {
        'nullable': True,
        'type': 'float',
    },
    IHC_ANTI_PDL1_MAB_22C3_TPS: {
        'nullable': True,
        'type': 'string',
        'options': ['> 50%', '< 50%'],
    },
    IHC_ANTI_PDL1_MAB_22C3_CPS: {
        'nullable': True,
        'type': 'string',
        'options': ['> 50%', '< 50%'],
    },
    IHC_ANTI_PDL1_MAB_28_8_TPS: {
        'nullable': True,
        'type': 'string',
        'options': ['> 50%', '< 50%'],
    },
    IHC_ANTI_PDL1_MAB_28_8_CPS: {
        'nullable': True,
        'type': 'string',
        'options': ['> 50%', '< 50%'],
    },
    LYMPH_NODE_LEVEL_I: {
        'nullable': True,
        'type': 'string',
    },
    LYMPH_NODE_LEVEL_IA: {
        'nullable': True,
        'type': 'string',
    },
    LYMPH_NODE_LEVEL_IB: {
        'nullable': True,
        'type': 'string',
    },
    LYMPH_NODE_LEVEL_II: {
        'nullable': True,
        'type': 'string',
    },
    LYMPH_NODE_LEVEL_IIA: {
        'nullable': True,
        'type': 'string',
    },
    LYMPH_NODE_LEVEL_IIB: {
        'nullable': True,
        'type': 'string',
    },
    LYMPH_NODE_LEVEL_III: {
        'nullable': True,
        'type': 'string',
    },
    LYMPH_NODE_LEVEL_IV: {
        'nullable': True,
        'type': 'string',
    },
    LYMPH_NODE_LEVEL_V: {
        'nullable': True,
        'type': 'string',
    },
    LYMPHOVASCULAR_INVASION: {
        'nullable': True,
        'type': 'boolean',
        'options': [True, False],
    },
    PERINEURAL_INVASION: {
        'nullable': True,
        'type': 'string',
        'options': ['Negative', 'Positive', 'Extensive'],
    },
    CLINICAL_OVERT_EXTRANODAL_EXTENSION: {
        'nullable': True,
        'type': 'boolean',
        'options': [True, False],
    },
    PATHOLOGICAL_EXTRANODAL_EXTENSION: {
        'nullable': True,
        'type': 'string',
        'options': ['Negative', 'Micro', 'Macro'],
    },
    DEPTH_OF_INVASION: {
        'nullable': True,
        'type': 'float',
    },
    TUMOR_MARGIN: {
        'nullable': True,
        'type': 'string',
        'options': ['Negative', 'Close', 'Positive'],
    },
    CLINICAL_TNM: {
        'nullable': True,
        'type': 'string',
    },
    PATHOLOGICAL_TNM: {
        'nullable': True,
        'type': 'string',
    },
    POSTNEOADJUVANT_CLINICAL_TNM: {
        'nullable': True,
        'type': 'string',
    },
    POSTNEOADJUVANT_PATHOLOGICAL_TNM: {
        'nullable': True,
        'type': 'string',
    },
    NEOPLASM_DISEASE_STAGE_AMERICAN_JOINT_COMMITTEE_ON_CANCER_CODE: {
        'nullable': True,
        'type': 'string',
        'options': ['Stage I', 'Stage II', 'Stage III', 'Stage IVA', 'Stage IVB', 'Stage IVC'],
    },
    ICD_10_CLASSIFICATION: {
        'nullable': True,
        'type': 'string',
        'options': ['C02.1', 'C03.0', 'C03.1', 'C06.0', 'K13.6', 'K13.29'],
    },
    SUBTYPE: {
        'nullable': True,
        'type': 'string',
        'options': ['HNSC HPV+', 'HNSC HPV-'],
    },
    INITIAL_TREATMENT_COMPLETION_DATE: {
        'nullable': True,
        'type': 'date',
    },
    LAST_FOLLOW_UP_DATE: {
        'nullable': True,
        'type': 'date',
    },
    RECUR_DATE_AFTER_INITIAL_TREATMENT: {
        'nullable': True,
        'type': 'date',
    },
    EXPIRE_DATE: {
        'nullable': True,
        'type': 'date',
    },
    CAUSE_OF_DEATH: {
        'nullable': True,
        'type': 'string',
        'options': ['Cancer', 'Other Disease'],
    },
    DISEASE_FREE_SURVIVAL_MONTHS: {
        'nullable': True,
        'type': 'float',
    },
    DISEASE_FREE_SURVIVAL_STATUS: {
        'nullable': True,
        'options': ['0:DiseaseFree', '1:Recurred/Progressed'],
    },
    DISEASE_SPECIFIC_SURVIVAL_MONTHS: {
        'nullable': True,
        'type': 'float',
    },
    DISEASE_SPECIFIC_SURVIVAL_STATUS: {
        'nullable': True,
        'type': 'string',
        'options': ['0:ALIVE OR DEAD TUMOR FREE', '1:DEAD WITH TUMOR'],
    },
    OVERALL_SURVIVAL_MONTHS: {
        'nullable': True,
        'type': 'float',
    },
    OVERALL_SURVIVAL_STATUS: {
        'nullable': True,
        'type': 'string',
        'options': ['0:LIVING', '1:DECEASED'],
    },
}

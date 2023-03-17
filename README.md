# cBio Ingest

**Data ingestion for cBioPortal**

## Usage

```bash
git clone https://github.com/linyc74/cbio_ingest.git

python cbio_ingest \
  -i ./study-info.xlsx \
  -c ./clinical-data.xlsx \
  -m ./maf-folder \
  -o ./hnsc_nycu_2022
```

## Schema

Columns in the `clinical-data.xlsx`:

- `Study ID`
- `Lab Sample ID`
- `Sample ID`
- `Sex`
- `Patient Weight (Kg)`
- `Patient Height (cm)`
- `Ethnicity Category`
- `Birth Date`
- `Clinical Diagnosis Date`
- `Pathological Diagnosis Date`
- `Cancer Type`
- `Cancer Type Detailed`
- `Sample Type`
- `Oncotree Code`
- `Somatic status`
- `Center`
- `Tumor Disease Anatomic Site`
- `ICD-O-3 Site Code`
- `Alcohol Consumption`
- `Alcohol Consumption Frequency (Days Per Week)`
- `Alcohol Consumption Duration (Years)`
- `Alcohol Consumption Quit (Years)`
- `Betel Nut Chewing`
- `Betel Nut Chewing Frequency (Pieces Per Day)`
- `Betel Nut Chewing Duration (Years)`
- `Betel Nut Chewing Quit (Years)`
- `Cigarette Smoking`
- `Cigarette Smoking Frequency (Packs Per Day)`
- `Cigarette Smoking Duration (Years)`
- `Cigarette Smoking Quit (Years)`
- `Histologic Grade`
- `Surgery`
- `Neoadjuvant/Induction Chemotherapy`
- `Neoadjuvant/Induction Chemotherapy Drug`
- `Adjuvant Chemotherapy`
- `Adjuvant Chemotherapy Drug`
- `Palliative Chemotherapy`
- `Palliative Chemotherapy Drug`
- `Adjuvant Targeted Therapy`
- `Adjuvant Targeted Therapy Drug`
- `Palliative Targeted Therapy`
- `Palliative Targeted Therapy Drug`
- `Immunotherapy`
- `Immunotherapy Drug`
- `Radiation Therapy`
- `Radiation Therapy Dose (cGY)`
- `IHC Anti-PDL1 mAb 22C3 TPS (%)`
- `IHC Anti-PDL1 mAb 22C3 CPS (%)`
- `IHC Anti-PDL1 mAb 28-8 TPS (%)`
- `IHC Anti-PDL1 mAb 28-8 CPS (%)`
- `Lymph Node Level I`
- `Lymph Node Level Ia`
- `Lymph Node Level Ib`
- `Lymph Node Level II`
- `Lymph Node Level IIa`
- `Lymph Node Level IIb`
- `Lymph Node Level III`
- `Lymph Node Level IV`
- `Lymph Node Level V`
- `Lymphovascular Invasion (LVI)`
- `Perineural Invasion (PNI)`
- `Clinical Overt Extranodal Extension`
- `Pathological Extranodal Extension (ENE)`
- `Depth of Invasion (mm)`
- `Tumor Margin`
- `Clinical TNM (cTNM)`
- `Pathological TNM (pTNM)`
- `Postneoadjuvant Clinical TNM (ycTNM)`
- `Postneoadjuvant Pathological TNM (ypTNM)`
- `Neoplasm Disease Stage American Joint Committee on Cancer Code`
- `ICD-10 Classification`
- `Subtype`
- `Initial Treatment Completion Date`
- `Last Follow-up Date`
- `Recur Date after Initial Treatment`
- `Expire Date`
- `Cause of Death`

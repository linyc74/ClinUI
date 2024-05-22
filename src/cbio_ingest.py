import json
import os.path
import pandas as pd
from typing import Dict, List, Optional
from .schema import BaseModel
from .cbio_constant import STUDY_IDENTIFIER_KEY, SAMPLE_ID
from .cbio_write_clinical_data import WriteClinicalData
from .cbio_write_mutation_data import WriteMutationData
from .cbio_preprocess_normalize import PreprocessNormalize


class cBioIngest(BaseModel):

    clinical_data_df: pd.DataFrame
    maf_dir: str
    study_info_dict: Dict[str, str]
    tags_dict: Optional[Dict[str, str]]
    outdir: str

    patient_df: pd.DataFrame
    sample_df: pd.DataFrame

    def main(
            self,
            clinical_data_df: pd.DataFrame,
            maf_dir: str,
            study_info_dict: Dict[str, str],
            tags_dict: Optional[Dict[str, str]],
            outdir: str):

        self.clinical_data_df = clinical_data_df
        self.maf_dir = maf_dir
        self.study_info_dict = study_info_dict
        self.tags_dict = tags_dict
        self.outdir = outdir

        self.write_study_info()
        self.preprocess_normalize()
        self.write_clinical_data()
        self.write_mutation_data()
        self.create_case_lists()

    def write_study_info(self):
        WriteStudyInfo(self.schema).main(
            study_info_dict=self.study_info_dict,
            tags_dict=self.tags_dict,
            outdir=self.outdir)

    def preprocess_normalize(self):
        self.patient_df, self.sample_df = PreprocessNormalize(self.schema).main(
            clinical_data_df=self.clinical_data_df,
            study_id=self.study_info_dict[STUDY_IDENTIFIER_KEY]
        )

    def write_clinical_data(self):
        WriteClinicalData(self.schema).main(
            study_info_dict=self.study_info_dict,
            patient_df=self.patient_df,
            sample_df=self.sample_df,
            outdir=self.outdir)

    def write_mutation_data(self):
        WriteMutationData(self.schema).main(
            maf_dir=self.maf_dir,
            study_info_dict=self.study_info_dict,
            sample_df=self.sample_df,
            outdir=self.outdir)

    def create_case_lists(self):
        CreateCaseLists(self.schema).main(
            study_info_dict=self.study_info_dict,
            sample_df=self.sample_df,
            outdir=self.outdir)


class WriteStudyInfo(BaseModel):

    META_STUDY_TXT_FILENAME = 'meta_study.txt'
    TAGS_JSON_FILENAME = 'tags.json'

    study_info_dict: Dict[str, str]
    tags_dict: Optional[Dict[str, str]]
    outdir: str

    def main(
            self,
            study_info_dict: Dict[str, str],
            tags_dict: Optional[Dict[str, str]],
            outdir: str):

        self.study_info_dict = study_info_dict
        self.tags_dict = tags_dict
        self.outdir = outdir

        self.write_meta_study_txt()
        self.write_tags_json()

    def write_meta_study_txt(self):
        with open(f'{self.outdir}/{self.META_STUDY_TXT_FILENAME}', 'w') as fh:
            for key, val in self.study_info_dict.items():
                fh.write(f'{key}: {val}\n')
            if self.tags_dict is not None:
                fh.write(f'tags_file: {self.TAGS_JSON_FILENAME}\n')

    def write_tags_json(self):
        if self.tags_dict is None:
            return
        with open(f'{self.outdir}/{self.TAGS_JSON_FILENAME}', 'w') as fh:
            json.dump(self.tags_dict, fh, indent=4)


class CreateCaseLists(BaseModel):

    CASE_DIRNAME = 'case_lists'
    ALL_TXT = 'cases_all.txt'
    SEQUENCED_TXT = 'cases_sequenced.txt'

    study_info_dict: Dict[str, str]
    sample_df: pd.DataFrame
    outdir: str

    case_dir: str
    sample_ids: List[str]

    def main(
            self,
            study_info_dict: Dict[str, str],
            sample_df: pd.DataFrame,
            outdir: str):

        self.study_info_dict = study_info_dict
        self.sample_df = sample_df
        self.outdir = outdir

        self.make_case_dir()
        self.set_sample_ids()
        self.write_all_txt()
        self.write_sequenced_txt()

    def make_case_dir(self):
        self.case_dir = f'{self.outdir}/{self.CASE_DIRNAME}'
        os.makedirs(self.case_dir, exist_ok=True)

    def set_sample_ids(self):
        self.sample_ids = self.sample_df[SAMPLE_ID].tolist()

    def write_all_txt(self):
        ids = '\t'.join(self.sample_ids)

        study_id = self.study_info_dict[STUDY_IDENTIFIER_KEY]
        text = f'''\
cancer_study_identifier: {study_id}
stable_id: {study_id}_all
case_list_name: All samples
case_list_description: All samples ({len(self.sample_ids)} samples)
case_list_category: all_cases_in_study
case_list_ids: {ids}'''

        with open(f'{self.case_dir}/{self.ALL_TXT}', 'w') as fh:
            fh.write(text)

    def write_sequenced_txt(self):
        ids = '\t'.join(self.sample_ids)

        study_id = self.study_info_dict[STUDY_IDENTIFIER_KEY]
        text = f'''\
cancer_study_identifier: {study_id}
stable_id: {study_id}_sequenced
case_list_name: Samples with mutation data
case_list_description: Samples with mutation data ({len(self.sample_ids)} samples)
case_list_category: all_cases_with_mutation_data
case_list_ids: {ids}'''

        with open(f'{self.case_dir}/{self.SEQUENCED_TXT}', 'w') as fh:
            fh.write(text)

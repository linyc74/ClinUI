import json
import os.path
import pandas as pd
from typing import Dict, List, Optional
from .template import Processor
from .write_clinical_data import WriteClinicalData
from .write_mutation_data import WriteMutationData
from .constant import STUDY_IDENTIFIER_KEY, SAMPLE_ID
from .preprocess_normalize import PreprocessNormalize


class cBioIngest(Processor):

    study_info_xlsx: str
    clinical_data_xlsx: str
    maf_dir: str
    tags_json: Optional[str]

    study_info_dict: Dict[str, str]
    patient_df: pd.DataFrame
    sample_df: pd.DataFrame

    def main(
            self,
            study_info_xlsx: str,
            clinical_data_xlsx: str,
            maf_dir: str,
            tags_json: Optional[str]):

        self.study_info_xlsx = study_info_xlsx
        self.clinical_data_xlsx = clinical_data_xlsx
        self.maf_dir = maf_dir
        self.tags_json = tags_json

        self.read_study_info()
        self.preprocess_normalize()
        self.write_clinical_data()
        self.write_mutation_data()
        self.create_case_lists()

    def read_study_info(self):
        self.study_info_dict = ReadStudyInfo(self.settings).main(
            xlsx=self.study_info_xlsx,
            tags_json=self.tags_json)

    def preprocess_normalize(self):
        self.patient_df, self.sample_df = PreprocessNormalize(self.settings).main(
            xlsx=self.clinical_data_xlsx)

    def write_clinical_data(self):
        WriteClinicalData(self.settings).main(
            study_info_dict=self.study_info_dict,
            patient_df=self.patient_df,
            sample_df=self.sample_df)

    def write_mutation_data(self):
        WriteMutationData(self.settings).main(
            maf_dir=self.maf_dir,
            study_info_dict=self.study_info_dict,
            sample_df=self.sample_df)

    def create_case_lists(self):
        CreateCaseLists(self.settings).main(
            study_info_dict=self.study_info_dict,
            sample_df=self.sample_df)


class ReadStudyInfo(Processor):

    FNAME = 'meta_study.txt'
    TAGS_JSON_FNAME = 'tags.json'

    xlsx: str
    tags_json: Optional[str]

    info_dict: Dict[str, str]

    def main(self, xlsx: str, tags_json: Optional[str]) -> Dict[str, str]:
        self.xlsx = xlsx
        self.tags_json = tags_json

        self.logger.info(f'Study info: {self.xlsx}')
        self.set_info_dict()
        self.write_txt()
        self.write_tags_json()

        return self.info_dict

    def set_info_dict(self):
        df = pd.read_excel(self.xlsx, header=None, index_col=0)
        column = df[1]

        self.info_dict = {
            key.lower().replace(' ', '_').rstrip(':'): val
            for key, val in column.to_dict().items()
        }

        if self.tags_json is not None:
            self.info_dict['tags_file'] = self.TAGS_JSON_FNAME

    def write_txt(self):
        with open(f'{self.outdir}/{self.FNAME}', 'w') as fh:
            for key, val in self.info_dict.items():
                fh.write(f'{key}: {val}\n')

    def write_tags_json(self):
        if self.tags_json is None:
            return
        o = json.loads(self.tags_json)
        with open(f'{self.outdir}/{self.TAGS_JSON_FNAME}', 'w') as fh:
            json.dump(o, fh, indent=4)


class CreateCaseLists(Processor):

    CASE_DIRNAME = 'case_lists'
    ALL_TXT = 'cases_all.txt'
    SEQUENCED_TXT = 'cases_sequenced.txt'

    study_info_dict: Dict[str, str]
    sample_df: pd.DataFrame

    case_dir: str
    sample_ids: List[str]

    def main(
            self,
            study_info_dict: Dict[str, str],
            sample_df: pd.DataFrame):

        self.study_info_dict = study_info_dict
        self.sample_df = sample_df

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

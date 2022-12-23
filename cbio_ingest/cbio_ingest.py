import json
import os.path
import pandas as pd
from typing import Dict, List, Optional
from .template import Processor
from .mutation_data import IngestMafs
from .constant import STUDY_IDENTIFIER_KEY
from .clinical_data import IngestPatientTable, IngestSampleTable


class cBioIngest(Processor):

    study_info_xlsx: str
    patient_table_xlsx: str
    sample_table_xlsx: str
    maf_dir: str
    tags_json: Optional[str]

    study_info_dict: Dict[str, str]
    sample_ids: List[str]

    def main(
            self,
            study_info_xlsx: str,
            patient_table_xlsx: str,
            sample_table_xlsx: str,
            maf_dir: str,
            tags_json: Optional[str]):

        self.study_info_xlsx = study_info_xlsx
        self.patient_table_xlsx = patient_table_xlsx
        self.sample_table_xlsx = sample_table_xlsx
        self.maf_dir = maf_dir
        self.tags_json = tags_json

        self.ingest_study_info()
        self.ingest_patient_table()
        self.ingest_sample_table()
        self.ingest_mafs()
        self.create_case_lists()

    def ingest_study_info(self):
        self.study_info_dict = IngestStudyInfo(self.settings).main(
            xlsx=self.study_info_xlsx,
            tags_json=self.tags_json)

    def ingest_patient_table(self):
        IngestPatientTable(self.settings).main(
            xlsx=self.patient_table_xlsx,
            study_info_dict=self.study_info_dict)

    def ingest_sample_table(self):
        self.sample_ids = IngestSampleTable(self.settings).main(
            xlsx=self.sample_table_xlsx,
            study_info_dict=self.study_info_dict)

    def ingest_mafs(self):
        IngestMafs(self.settings).main(
            maf_dir=self.maf_dir,
            study_info_dict=self.study_info_dict,
            sample_ids=self.sample_ids)

    def create_case_lists(self):
        CreateCaseLists(self.settings).main(
            study_info_dict=self.study_info_dict,
            sample_ids=self.sample_ids)


class IngestStudyInfo(Processor):

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
    sample_ids: List[str]

    case_dir: str

    def main(
            self,
            study_info_dict: Dict[str, str],
            sample_ids: List[str]):

        self.study_info_dict = study_info_dict
        self.sample_ids = sample_ids

        self.make_case_dir()
        self.write_all_txt()
        self.write_sequenced_txt()

    def make_case_dir(self):
        self.case_dir = f'{self.outdir}/{self.CASE_DIRNAME}'
        os.makedirs(self.case_dir, exist_ok=True)

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

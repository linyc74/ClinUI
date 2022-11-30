import json
import os.path
import pandas as pd
from typing import Dict, List, Optional
from .template import Processor


STUDY_IDENTIFIER_KEY = 'cancer_study_identifier'
DESCRIPTION_KEY = 'description'
SAMPLE_ID_COLUMN = 'SAMPLE_ID'


class cBioIngest(Processor):

    study_info_xlsx: str
    sample_table_xlsx: str
    maf_dir: str
    tags_json: Optional[str]

    study_info_dict: Dict[str, str]
    sample_ids: List[str]

    def main(
            self,
            study_info_xlsx: str,
            sample_table_xlsx: str,
            maf_dir: str,
            tags_json: Optional[str]):

        self.study_info_xlsx = study_info_xlsx
        self.sample_table_xlsx = sample_table_xlsx
        self.maf_dir = maf_dir
        self.tags_json = tags_json

        self.ingest_study_info()
        self.ingest_sample_table()
        self.ingest_mafs()
        self.create_case_lists()

    def ingest_study_info(self):
        self.study_info_dict = IngestStudyInfo(self.settings).main(
            xlsx=self.study_info_xlsx,
            tags_json=self.tags_json)

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


class IngestSampleTable(Processor):

    META_FNAME = 'meta_clinical_sample.txt'
    DATA_FNAME = 'data_clinical_sample.txt'

    xlsx: str
    study_info_dict: Dict[str, str]

    df: pd.DataFrame

    def main(
            self,
            xlsx: str,
            study_info_dict: Dict[str, str]) -> List[str]:
        self.xlsx = xlsx
        self.study_info_dict = study_info_dict

        self.logger.info(f'Sample table: {self.xlsx}')

        self.df = pd.read_excel(self.xlsx)

        self.write_meta_file()
        self.write_data_file()

        return self.df[SAMPLE_ID_COLUMN].to_list()

    def write_meta_file(self):
        text = f'''\
cancer_study_identifier: {self.study_info_dict[STUDY_IDENTIFIER_KEY]}
genetic_alteration_type: CLINICAL
datatype: SAMPLE_ATTRIBUTES
data_filename: {self.DATA_FNAME}'''

        with open(f'{self.outdir}/{self.META_FNAME}', 'w') as fh:
            fh.write(text)

    def write_data_file(self):
        rename_dict = {
            c: c.upper().replace(' ', '_')
            for c in self.df.columns
        }
        self.df = self.df.rename(columns=rename_dict)
        self.df.to_csv(f'{self.outdir}/{self.DATA_FNAME}', sep='\t', index=False)


class IngestMafs(Processor):

    META_FNAME = 'meta_mutations_extended.txt'
    DATA_FNAME = 'data_mutations_extended.txt'

    maf_dir: str
    study_info_dict: Dict[str, str]
    sample_ids: List[str]

    mafs: List[str]
    df: pd.DataFrame

    def main(
            self,
            maf_dir: str,
            study_info_dict: Dict[str, str],
            sample_ids: List[str]):

        self.maf_dir = maf_dir
        self.study_info_dict = study_info_dict
        self.sample_ids = sample_ids

        self.write_meta_file()
        self.set_mafs()
        self.read_first_maf()
        self.read_the_rest_mafs()
        self.write_data_file()

    def write_meta_file(self):
        text = f'''\
cancer_study_identifier: {self.study_info_dict[STUDY_IDENTIFIER_KEY]}
genetic_alteration_type: MUTATION_EXTENDED
stable_id: mutations
datatype: MAF
show_profile_in_analysis_tab: true
profile_description: {self.study_info_dict[DESCRIPTION_KEY]}
profile_name: Mutations
data_filename: {self.DATA_FNAME}'''

        with open(f'{self.outdir}/{self.META_FNAME}', 'w') as fh:
            fh.write(text)

    def set_mafs(self):
        self.mafs = [f'{self.maf_dir}/{id_}.maf' for id_ in self.sample_ids]

    def read_first_maf(self):
        self.df = ReadAndProcessMaf(self.settings).main(maf=self.mafs[0])

    def read_the_rest_mafs(self):
        for maf in self.mafs[1:]:
            df = ReadAndProcessMaf(self.settings).main(maf=maf)
            self.df = pd.concat([self.df, df], ignore_index=True)

    def write_data_file(self):
        self.df.to_csv(f'{self.outdir}/{self.DATA_FNAME}', sep='\t', index=False)


class ReadAndProcessMaf(Processor):
    """
    https://docs.cbioportal.org/file-formats/#mutation-data
    """
    COLUMNS = [
        'Hugo_Symbol',
        'Entrez_Gene_Id',
        'Center',
        'NCBI_Build',
        'Chromosome',
        'Start_Position',
        'End_Position',
        'Strand',
        'Variant_Classification',
        'Variant_Type',
        'Reference_Allele',
        'Tumor_Seq_Allele1',
        'Tumor_Seq_Allele2',
        'dbSNP_RS',
        'dbSNP_Val_Status',
        'Tumor_Sample_Barcode',
        'Matched_Norm_Sample_Barcode',
        'Match_Norm_Seq_Allele1',
        'Match_Norm_Seq_Allele2',
        'Tumor_Validation_Allele1',
        'Tumor_Validation_Allele2',
        'Match_Norm_Validation_Allele1',
        'Match_Norm_Validation_Allele2',
        'Match_Norm_Validation_Allele1',
        'Match_Norm_Validation_Allele2',
        'Verification_Status',
        'Validation_Status',
        'Mutation_Status',
        'Sequencing_Phase',
        'Sequence_Source',
        'Validation_Method',
        'Score',
        'BAM_File',
        'Sequencer',
        'HGVSp_Short',
        't_alt_count',
        't_ref_count',
        'n_alt_count',
        'n_ref_count',
    ]
    REQUIRED_COLUMNs = [
        'Hugo_Symbol',
        'NCBI_Build',
        'Chromosome',
        'Variant_Classification',
        'Reference_Allele',
        'Tumor_Seq_Allele2',
        'Tumor_Sample_Barcode',
        'HGVSp_Short',
    ]

    maf: str
    df: pd.DataFrame

    def main(self, maf: str) -> pd.DataFrame:
        self.maf = maf
        self.logger.info(f'Processing {self.maf}')
        self.read_maf()
        self.set_tumor_sample_id()
        return self.df

    def read_maf(self):
        self.df = pd.read_csv(self.maf, sep='\t', skiprows=1, usecols=self.COLUMNS)

    def set_tumor_sample_id(self):
        # The name of the maf file should be the sample id
        filename = os.path.basename(self.maf[:-len('.maf')])
        self.df['Tumor_Sample_Barcode'] = filename


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

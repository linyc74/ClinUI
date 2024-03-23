import os.path
import pandas as pd
from typing import Dict, List
from .model_base import AbstractModel
from .schema import STUDY_IDENTIFIER_KEY


class WriteMutationData(AbstractModel):

    META_FNAME = 'meta_mutations_extended.txt'
    DATA_FNAME = 'data_mutations_extended.txt'

    maf_dir: str
    study_info_dict: Dict[str, str]
    sample_df: pd.DataFrame
    outdir: str

    mafs: List[str]
    df: pd.DataFrame

    def main(
            self,
            maf_dir: str,
            study_info_dict: Dict[str, str],
            sample_df: pd.DataFrame,
            outdir: str):

        self.maf_dir = maf_dir
        self.study_info_dict = study_info_dict
        self.sample_df = sample_df
        self.outdir = outdir

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
profile_description: {self.study_info_dict['description']}
profile_name: Mutations
data_filename: {self.DATA_FNAME}'''

        with open(f'{self.outdir}/{self.META_FNAME}', 'w') as fh:
            fh.write(text)

    def set_mafs(self):
        sample_id_column = self.sample_df.columns[2]  # First 3 columns: 'Study ID', 'Patient ID', 'Sample ID'
        self.mafs = [f'{self.maf_dir}/{id_}.maf' for id_ in self.sample_df[sample_id_column]]

    def read_first_maf(self):
        self.df = ReadAndProcessMaf(self.schema).main(maf=self.mafs[0])

    def read_the_rest_mafs(self):
        for maf in self.mafs[1:]:
            df = ReadAndProcessMaf(self.schema).main(maf=maf)
            self.df = pd.concat([self.df, df], ignore_index=True)

    def write_data_file(self):
        self.df.to_csv(f'{self.outdir}/{self.DATA_FNAME}', sep='\t', index=False)


class ReadAndProcessMaf(AbstractModel):
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
    REQUIRED_COLUMN = [
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
        print(f'Processing {self.maf}', flush=True)
        self.read_maf()
        self.set_tumor_sample_id()
        return self.df

    def read_maf(self):
        self.df = pd.read_csv(self.maf, sep='\t', skiprows=1, usecols=self.COLUMNS)

    def set_tumor_sample_id(self):
        # The name of the maf file should be the sample id
        filename = os.path.basename(self.maf[:-len('.maf')])
        self.df['Tumor_Sample_Barcode'] = filename

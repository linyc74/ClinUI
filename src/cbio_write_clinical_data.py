import pandas as pd
from typing import Dict, List
from .schema import BaseModel
from .cbio_constant import STUDY_IDENTIFIER_KEY, PATIENT_ID


class WriteClinicalData(BaseModel):

    study_info_dict: Dict[str, str]
    patient_df: pd.DataFrame
    sample_df: pd.DataFrame
    outdir: str

    def main(
            self,
            study_info_dict: Dict[str, str],
            patient_df: pd.DataFrame,
            sample_df: pd.DataFrame,
            outdir: str):

        self.study_info_dict = study_info_dict
        self.patient_df = patient_df
        self.sample_df = sample_df
        self.outdir = outdir

        self.remove_empty_columns_from_patient_df()
        self.write_patient_data()
        self.write_sample_data()

    def remove_empty_columns_from_patient_df(self):
        self.patient_df = RemoveEmptyColumns(self.schema).main(self.patient_df)

    def write_patient_data(self):
        # only the "Patient ID" column was left
        columns = self.patient_df.columns.to_list()
        empty_patient_data = columns == [PATIENT_ID]

        if empty_patient_data:
            print('WARNING! Empty patient data, skipping writing patient data file', flush=True)
        else:
            WritePatientData(self.schema).main(
                patient_df=self.patient_df,
                study_info_dict=self.study_info_dict,
                outdir=self.outdir)

    def write_sample_data(self):
        WriteSampleData(self.schema).main(
            sample_df=self.sample_df,
            study_info_dict=self.study_info_dict,
            outdir=self.outdir)


class RemoveEmptyColumns(BaseModel):

    df: pd.DataFrame

    def main(self, df: pd.DataFrame) -> pd.DataFrame:
        self.df = df.copy()
        for column in self.df.columns:
            if all(pd.isna(self.df[column])):
                print(f'Remove empty column for cBioPortal: "{column}"', flush=True)
                self.df.drop(columns=column, inplace=True)
        return self.df


class BaseWriter(BaseModel):

    DATA_FNAME: str

    df: pd.DataFrame
    study_info_dict: Dict[str, str]
    outdir: str

    def write_data_file_1st_2nd_lines(self):
        line = '#' + '\t'.join(self.df.columns) + '\n'
        with open(f'{self.outdir}/{self.DATA_FNAME}', 'w', encoding='UTF-8') as fh:
            for _ in range(2):
                fh.write(line)

    def write_data_file_3rd_line(self):
        datatypes = GetDataTypes(self.schema).main(
            columns=self.df.columns.to_list()
        )

        line = '#' + '\t'.join(datatypes) + '\n'
        with open(f'{self.outdir}/{self.DATA_FNAME}', 'a') as fh:
            fh.write(line)

    def write_data_file_4th_line(self):
        items = ['1' for _ in self.df.columns]
        line = '#' + '\t'.join(items) + '\n'
        with open(f'{self.outdir}/{self.DATA_FNAME}', 'a') as fh:
            fh.write(line)


class WritePatientData(BaseWriter):

    META_FNAME = 'meta_clinical_patient.txt'
    DATA_FNAME = 'data_clinical_patient.txt'

    def main(
            self,
            patient_df: pd.DataFrame,
            study_info_dict: Dict[str, str],
            outdir: str):

        self.df = patient_df
        self.study_info_dict = study_info_dict
        self.outdir = outdir

        self.write_meta_file()
        self.write_data_file_1st_2nd_lines()
        self.write_data_file_3rd_line()
        self.write_data_file_4th_line()
        self.write_data_file()

    def write_meta_file(self):
        text = f'''\
cancer_study_identifier: {self.study_info_dict[STUDY_IDENTIFIER_KEY]}
genetic_alteration_type: CLINICAL
datatype: PATIENT_ATTRIBUTES
data_filename: {self.DATA_FNAME}'''

        with open(f'{self.outdir}/{self.META_FNAME}', 'w') as fh:
            fh.write(text)

    def write_data_file(self):
        self.df = FillInMissingBooleanValues(self.schema).main(self.df)
        self.df = FormatClinicalData(self.schema).main(self.df)
        self.df.to_csv(f'{self.outdir}/{self.DATA_FNAME}', mode='a', sep='\t', index=False)


class WriteSampleData(BaseWriter):

    META_FNAME = 'meta_clinical_sample.txt'
    DATA_FNAME = 'data_clinical_sample.txt'

    def main(
            self,
            sample_df: pd.DataFrame,
            study_info_dict: Dict[str, str],
            outdir: str):

        self.df = sample_df
        self.study_info_dict = study_info_dict
        self.outdir = outdir

        self.write_meta_file()
        self.write_data_file_1st_2nd_lines()
        self.write_data_file_3rd_line()
        self.write_data_file_4th_line()
        self.write_data_file()

    def write_meta_file(self):
        text = f'''\
cancer_study_identifier: {self.study_info_dict[STUDY_IDENTIFIER_KEY]}
genetic_alteration_type: CLINICAL
datatype: SAMPLE_ATTRIBUTES
data_filename: {self.DATA_FNAME}'''

        with open(f'{self.outdir}/{self.META_FNAME}', 'w') as fh:
            fh.write(text)

    def write_data_file(self):
        self.df = FillInMissingBooleanValues(self.schema).main(self.df)
        self.df = FormatClinicalData(self.schema).main(self.df)
        self.df.to_csv(f'{self.outdir}/{self.DATA_FNAME}', mode='a', sep='\t', index=False)


class FillInMissingBooleanValues(BaseModel):

    df: pd.DataFrame

    datatypes: List[str]

    def main(self, df: pd.DataFrame) -> pd.DataFrame:
        self.df = df

        self.set_datatypes()
        self.fillna()

        return self.df

    def set_datatypes(self):
        self.datatypes = GetDataTypes(self.schema).main(columns=self.df.columns.to_list())

    def fillna(self):
        for dtype, column in zip(self.datatypes, self.df.columns):
            if dtype == 'BOOLEAN':
                self.df[column] = self.df[column].fillna(value=False)


class GetDataTypes(BaseModel):

    columns: List[str]

    datatypes: List[str]

    def main(self, columns: List[str]) -> List[str]:
        self.columns = columns

        self.datatypes = []
        for c in self.columns:
            ty = self.schema.COLUMN_ATTRIBUTES.get(c, {}).get('type', 'str')  # default is 'str'

            if ty == 'bool':
                dtype = 'BOOLEAN'
            elif ty == 'int' or ty == 'float':
                dtype = 'NUMBER'
            else:
                dtype = 'STRING'  # default

            self.datatypes.append(dtype)

        return self.datatypes


class FormatClinicalData(BaseModel):

    RENAME_COLUMN_DICT = {
        'DISEASE_FREE_MONTHS': 'DF_MONTHS',
        'DISEASE_FREE_STATUS': 'DF_STATUS',
        'DISEASE_SPECIFIC_SURVIVAL_MONTHS': 'DSS_MONTHS',
        'DISEASE_SPECIFIC_SURVIVAL_STATUS': 'DSS_STATUS',
        'OVERALL_SURVIVAL_MONTHS': 'OS_MONTHS',
        'OVERALL_SURVIVAL_STATUS': 'OS_STATUS',
        'PROGRESSION_FREE_SURVIVAL_MONTHS': 'PFS_MONTHS',
        'PROGRESSION_FREE_SURVIVAL_STATUS': 'PFS_STATUS',
    }

    df: pd.DataFrame

    def main(self, df: pd.DataFrame) -> pd.DataFrame:
        self.df = df

        self.replace_boolean_with_str()
        self.format_columns()
        self.rename_columns()

        return self.df

    def replace_boolean_with_str(self):
        """
        For cBioPortal boolean values need to be written as 'TRUE' and 'FALSE'
        """
        for c in self.df.columns:
            datatype = self.schema.COLUMN_ATTRIBUTES.get(c, {}).get('type', 'str')  # default is 'str'

            # need to check datatype is bool, otherwise what can happen is
            #   1.0 --> 'TRUE', 0.0 --> 'FALSE'
            if datatype == 'bool':
                self.df[c] = self.df[c].replace(to_replace={True: 'TRUE', False: 'FALSE'})

    def format_columns(self):

        def formated(c: str) -> str:
            for x in [' ', '-', ',', '/']:
                c = c.upper().replace(x, '_')
            for x in ['(', ')']:
                c = c.replace(x, '')
            return c

        rename_dict = {c: formated(c) for c in self.df.columns}
        self.df = self.df.rename(columns=rename_dict)

    def rename_columns(self):
        self.df = self.df.rename(columns=self.RENAME_COLUMN_DICT)

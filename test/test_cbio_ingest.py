import pandas as pd
from os.path import exists
from src.cbio_ingest import cBioIngest, WriteStudyInfo
from .setup import TestCase


class TestcBioIngest(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_main(self):
        cBioIngest(self.settings).main(
            study_info_dict={
                'type_of_cancer': 'hnsc',
                'cancer_study_identifier': 'hnsc_nycu_2022',
                'name': 'Head and Neck Squamous Cell Carcinomas (NYCU, 2022)',
                'description': 'Whole exome sequencing of 11 precancer and OSCC tumor/normal pairs',
                'groups': 'PUBLIC',
                'reference_genome': 'hg38',
            },
            clinical_data_df=pd.read_csv(f'{self.indir}/clinical_data.csv'),
            maf_dir=f'{self.indir}/maf_dir',
            tags_dict={'key': 'val'},
        )
        for file in [
            'case_lists/cases_all.txt',
            'case_lists/cases_sequenced.txt',
            'data_clinical_patient.txt',
            'data_clinical_sample.txt',
            'data_mutations_extended.txt',
            'meta_clinical_patient.txt',
            'meta_clinical_sample.txt',
            'meta_mutations_extended.txt',
            'meta_study.txt',
            'tags.json',
        ]:
            with self.subTest(file=file):
                self.assertTrue(exists(f'{self.outdir}/{file}'))


class TestWriteStudyInfo(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_no_tags(self):
        WriteStudyInfo(self.settings).main(
            study_info_dict={
                'type_of_cancer': 'hnsc',
                'cancer_study_identifier': 'hnsc_nycu_2022',
                'name': 'Head and Neck Squamous Cell Carcinomas (NYCU, 2022)',
                'description': 'Whole exome sequencing of 11 precancer and OSCC tumor/normal pairs',
                'groups': 'PUBLIC',
                'reference_genome': 'hg38',
            },
            tags_dict=None,
        )
        expected = f'''\
type_of_cancer: hnsc
cancer_study_identifier: hnsc_nycu_2022
name: Head and Neck Squamous Cell Carcinomas (NYCU, 2022)
description: Whole exome sequencing of 11 precancer and OSCC tumor/normal pairs
groups: PUBLIC
reference_genome: hg38
'''
        with open(f'{self.outdir}/meta_study.txt') as fh:
            actual = fh.read()

        self.assertEqual(expected, actual)

        self.assertTrue(not exists(f'{self.outdir}/tags.json'))

    def test_with_tags(self):
        WriteStudyInfo(self.settings).main(
            study_info_dict={
                'type_of_cancer': 'hnsc',
                'cancer_study_identifier': 'hnsc_nycu_2022',
                'name': 'Head and Neck Squamous Cell Carcinomas (NYCU, 2022)',
                'description': 'Whole exome sequencing of 11 precancer and OSCC tumor/normal pairs',
                'groups': 'PUBLIC',
                'reference_genome': 'hg38',
            },
            tags_dict={'key': 'val'},
        )
        expected = f'''\
type_of_cancer: hnsc
cancer_study_identifier: hnsc_nycu_2022
name: Head and Neck Squamous Cell Carcinomas (NYCU, 2022)
description: Whole exome sequencing of 11 precancer and OSCC tumor/normal pairs
groups: PUBLIC
reference_genome: hg38
tags_file: tags.json
'''
        with open(f'{self.outdir}/meta_study.txt') as fh:
            actual = fh.read()

        self.assertEqual(expected, actual)

        self.assertTrue(exists(f'{self.outdir}/tags.json'))

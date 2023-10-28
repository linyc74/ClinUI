import pandas as pd
from src.write_mutation_data import WriteMutationData
from .setup import TestCase


class TestWriteClinicalData(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_main(self):
        WriteMutationData(self.settings).main(
            maf_dir=f'{self.indir}/maf_dir',
            study_info_dict={
                'type_of_cancer': 'hnsc',
                'cancer_study_identifier': 'hnsc_nycu_2022',
                'name': 'Head and Neck Squamous Cell Carcinomas (NYCU, 2022)',
                'description': 'Whole exome sequencing of 11 precancer and OSCC tumor/normal pairs',
                'groups': 'PUBLIC',
                'reference_genome': 'hg38',
                'tags_file': 'tags.json'
            },
            sample_df=pd.read_csv(f'{self.indir}/sample_df.csv')
        )

import pandas as pd
from src.preprocess_normalize import PreprocessNormalize
from .setup import TestCase


class TestPreprocessNormalize(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_main(self):
        patient_df, sample_df = PreprocessNormalize(self.settings).main(
            clinical_data_df=pd.read_csv(f'{self.indir}/clinical-data.csv')
        )
        self.assertDataFrameEqual(
            pd.read_csv(f'{self.indir}/patient_df.csv'),
            patient_df
        )
        self.assertDataFrameEqual(
            pd.read_csv(f'{self.indir}/sample_df.csv'),
            sample_df
        )

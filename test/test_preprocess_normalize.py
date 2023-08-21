import numpy as np
import pandas as pd
from src.preprocess_normalize import PreprocessNormalize, delta_t
from .setup import TestCase


class TestPreprocessNormalize(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_main(self):
        patient_df, sample_df = PreprocessNormalize(self.settings).main(
            clinical_data_df=pd.read_csv(f'{self.indir}/clinical_data.csv')
        )
        self.assertDataFrameEqual(
            pd.read_csv(f'{self.indir}/patient_df.csv'),
            patient_df
        )
        self.assertDataFrameEqual(
            pd.read_csv(f'{self.indir}/sample_df.csv'),
            sample_df
        )

    def test_delta_t(self):
        actual = delta_t(start='2020/01/01', end='01/01/2021')
        expected = pd.Timedelta(days=366)
        self.assertEqual(expected, actual)

        actual = delta_t(start=pd.Timestamp('2020/01/01'), end=pd.Timestamp('2021/01/01'))
        expected = pd.Timedelta(days=366)
        self.assertEqual(expected, actual)

        actual = delta_t(start='2020/01/01', end=np.nan)
        self.assertTrue(actual is pd.NaT)

        actual = delta_t(start='2020/01/01', end=pd.NaT)
        self.assertTrue(actual is pd.NaT)

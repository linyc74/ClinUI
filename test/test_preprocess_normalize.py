from cbio_ingest.preprocess_normalize import PreprocessNormalize
from .setup import TestCase


class TestPreprocessNormalize(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_main(self):
        patient_df, sample_df = PreprocessNormalize(self.settings).main(
            xlsx=f'{self.indir}/clinical-data.xlsx',
        )
        patient_df.to_csv(f'{self.outdir}/patient_df.csv', index=False)
        sample_df.to_csv(f'{self.outdir}/sample_df.csv', index=False)

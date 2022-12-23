from cbio_ingest.cbio_ingest import cBioIngest
from .setup import TestCase


class TestcBioIngest(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_main(self):
        cBioIngest(self.settings).main(
            study_info_xlsx=f'{self.indir}/study-info.xlsx',
            patient_table_xlsx=f'{self.indir}/patient-table.xlsx',
            sample_table_xlsx=f'{self.indir}/sample-table.xlsx',
            maf_dir=f'{self.indir}/maf-dir',
            tags_json='{"source": "PATH/TO/SOURCE"}'
        )

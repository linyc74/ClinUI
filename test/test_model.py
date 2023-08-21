from src.model import ReadClinicalDataTable
from .setup import TestCase


class TestReadClinicalDataTable(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_main(self):
        actual = ReadClinicalDataTable().main(file=f'{self.indir}/clinical_data.csv')
        self.assertEqual('datetime64[ns]', actual['Birth Date'].dtype)

    def test_assert_error_column(self):
        with self.assertRaises(AssertionError):
            ReadClinicalDataTable().main(file=f'{self.indir}/error_clinical_data.csv')

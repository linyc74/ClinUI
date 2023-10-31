from src.model import Model
from .setup import TestCase


class TestModel(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_read_clinical_data_table(self):
        model = Model()
        model.read_clinical_data_table(file=f'{self.indir}/clinical_data.csv')
        self.assertEqual('datetime64[ns]', model.dataframe['Birth Date'].dtype)

    def test_wrong_clinical_data_table(self):
        model = Model()
        success, message = model.read_clinical_data_table(file=f'{self.indir}/error_clinical_data.csv')
        self.assertFalse(success)
        self.assertTrue(message)

    def test_import_sequencing_table(self):
        model = Model()
        model.read_clinical_data_table(file=f'{self.indir}/clinical_data.csv')
        model.import_sequencing_table(file=f'{self.indir}/sequencing.csv')
        self.assertEqual(12, len(model.dataframe))

    def test_wrong_sequencing_table(self):
        model = Model()
        model.read_clinical_data_table(file=f'{self.indir}/clinical_data.csv')
        success, message = model.import_sequencing_table(file=f'{self.indir}/clinical_data.csv')
        self.assertFalse(success)
        self.assertTrue(message)

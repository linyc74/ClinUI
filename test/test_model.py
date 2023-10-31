from src.model import Model, CalculateSurvival
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


class TestCalculateSurvival(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_main(self):
        attributes = {
            'Birth Date': '1950-01-01',
            'Clinical Diagnosis Date': '2010-12-17',
            'Initial Treatment Completion Date': '2011-07-27',
            'Last Follow-up Date': '2022-08-05',
            'Recur Date after Initial Treatment': '',
            'Expire Date': '2022-08-05',
            'Cause of Death': 'Other Disease'
        }
        attributes = CalculateSurvival().main(attributes=attributes)
        self.assertDictEqual(
            {
                'Birth Date': '1950-01-01',
                'Clinical Diagnosis Date': '2010-12-17',
                'Initial Treatment Completion Date': '2011-07-27',
                'Last Follow-up Date': '2022-08-05',
                'Recur Date after Initial Treatment': '',
                'Expire Date': '2022-08-05',
                'Cause of Death': 'Other Disease',
                'Clinical Diagnosis Age': 61.0,
                'Disease Free (Months)': 134.23333333333332,
                'Disease Free Status': '0:DiseaseFree',
                'Disease-specific Survival (Months)': 134.23333333333332,
                'Disease-specific Survival Status': '0:ALIVE OR DEAD TUMOR FREE',
                'Overall Survival (Months)': 134.23333333333332,
                'Overall Survival Status': '1:DECEASED'
            }, attributes
        )

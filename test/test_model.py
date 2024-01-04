from src.model import Model, CalculateSurvival, CalculateICD, CalculateStage, CalculateTotalLymphNodes
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

    def test_alive_disease_free(self):
        attributes = {
            'Birth Date': '2001-01-01',
            'Clinical Diagnosis Date': '2002-01-01',
            'Initial Treatment Completion Date': '2003-01-01',
            'Last Follow-up Date': '2003-12-27',
            'Recur Date after Initial Treatment': '',
            'Expire Date': '',
            'Cause of Death': ''
        }
        actual = CalculateSurvival().main(attributes=attributes)

        expected = attributes.copy()
        expected.update({
            'Clinical Diagnosis Age': 1.0,
            'Disease Free (Months)': 12.0,
            'Disease Free Status': '0:DiseaseFree',
            'Disease-specific Survival (Months)': 12.0,
            'Disease-specific Survival Status': '0:ALIVE OR DEAD TUMOR FREE',
            'Overall Survival (Months)': 12.0,
            'Overall Survival Status': '0:LIVING',
        })

        self.assertDictEqual(expected, actual)

    def test_alive_recurred(self):
        attributes = {
            'Birth Date': '2001-01-01',
            'Clinical Diagnosis Date': '2002-01-01',
            'Initial Treatment Completion Date': '2003-01-01',
            'Last Follow-up Date': '2004-01-26',
            'Recur Date after Initial Treatment': '2003-12-27',
            'Expire Date': '',
            'Cause of Death': ''
        }
        actual = CalculateSurvival().main(attributes=attributes)

        expected = attributes.copy()
        expected.update({
            'Clinical Diagnosis Age': 1.0,
            'Disease Free (Months)': 12.0,
            'Disease Free Status': '1:Recurred/Progressed',
            'Disease-specific Survival (Months)': 13.0,
            'Disease-specific Survival Status': '0:ALIVE OR DEAD TUMOR FREE',
            'Overall Survival (Months)': 13.0,
            'Overall Survival Status': '0:LIVING',
        })

        self.assertDictEqual(expected, actual)

    def test_recur_and_then_die_of_cancer(self):
        attributes = {
            'Birth Date': '2001-01-01',
            'Clinical Diagnosis Date': '2002-01-01',
            'Initial Treatment Completion Date': '2003-01-01',
            'Last Follow-up Date': '2003-12-27',
            'Recur Date after Initial Treatment': '2003-01-31',
            'Expire Date': '2003-12-27',
            'Cause of Death': 'Cancer'
        }
        actual = CalculateSurvival().main(attributes=attributes)

        expected = attributes.copy()
        expected.update({
            'Clinical Diagnosis Age': 1.0,
            'Disease Free (Months)': 1.0,
            'Disease Free Status': '1:Recurred/Progressed',
            'Disease-specific Survival (Months)': 12.0,
            'Disease-specific Survival Status': '1:DEAD WITH TUMOR',
            'Overall Survival (Months)': 12.0,
            'Overall Survival Status': '1:DECEASED',
        })

        self.assertDictEqual(expected, actual)

    def test_suddenly_die_of_cancer_without_detecting_recurrence(self):
        attributes = {
            'Birth Date': '2001-01-01',
            'Clinical Diagnosis Date': '2002-01-01',
            'Initial Treatment Completion Date': '2003-01-01',
            'Last Follow-up Date': '2003-12-27',
            'Recur Date after Initial Treatment': '',
            'Expire Date': '2003-12-27',
            'Cause of Death': 'Cancer'
        }
        actual = CalculateSurvival().main(attributes=attributes)

        expected = attributes.copy()
        expected.update({
            'Clinical Diagnosis Age': 1.0,
            'Disease Free (Months)': 12.0,
            'Disease Free Status': '1:Recurred/Progressed',
            'Disease-specific Survival (Months)': 12.0,
            'Disease-specific Survival Status': '1:DEAD WITH TUMOR',
            'Overall Survival (Months)': 12.0,
            'Overall Survival Status': '1:DECEASED',
        })

        self.assertDictEqual(expected, actual)

    def test_recur_and_then_die_of_other_disease(self):
        attributes = {
            'Birth Date': '2001-01-01',
            'Clinical Diagnosis Date': '2002-01-01',
            'Initial Treatment Completion Date': '2003-01-01',
            'Last Follow-up Date': '2003-12-27',
            'Recur Date after Initial Treatment': '2003-01-31',
            'Expire Date': '2003-12-27',
            'Cause of Death': 'Other Disease'
        }
        actual = CalculateSurvival().main(attributes=attributes)

        expected = attributes.copy()
        expected.update({
            'Clinical Diagnosis Age': 1.0,
            'Disease Free (Months)': 1.0,
            'Disease Free Status': '1:Recurred/Progressed',
            'Disease-specific Survival (Months)': 12.0,
            'Disease-specific Survival Status': '0:ALIVE OR DEAD TUMOR FREE',
            'Overall Survival (Months)': 12.0,
            'Overall Survival Status': '1:DECEASED',
        })

        self.assertDictEqual(expected, actual)

    def test_no_recurrence_die_of_other_disease(self):
        attributes = {
            'Birth Date': '2001-01-01',
            'Clinical Diagnosis Date': '2002-01-01',
            'Initial Treatment Completion Date': '2003-01-01',
            'Last Follow-up Date': '2003-12-27',
            'Recur Date after Initial Treatment': '',
            'Expire Date': '2003-12-27',
            'Cause of Death': 'Other Disease'
        }
        actual = CalculateSurvival().main(attributes=attributes)

        expected = attributes.copy()
        expected.update({
            'Clinical Diagnosis Age': 1.0,
            'Disease Free (Months)': 12.0,
            'Disease Free Status': '0:DiseaseFree',
            'Disease-specific Survival (Months)': 12.0,
            'Disease-specific Survival Status': '0:ALIVE OR DEAD TUMOR FREE',
            'Overall Survival (Months)': 12.0,
            'Overall Survival Status': '1:DECEASED',
        })

        self.assertDictEqual(expected, actual)


class TestCalculateICD(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_(self):
        attributes = {
            'Tumor Disease Anatomic Site': 'Right Tongue',
        }
        actual = CalculateICD().main(attributes=attributes)

        expected = attributes.copy()
        expected.update({
            'ICD-O-3 Site Code': '',
        })

        self.assertDictEqual(expected, actual)


class TestCalculateStage(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_(self):
        attributes = {
            '': '',
        }
        actual = CalculateStage().main(attributes=attributes)

        expected = attributes.copy()
        expected.update({
            '': '',
        })

        self.assertDictEqual(expected, actual)


class TestCalculateTotalLymphNodes(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_(self):
        attributes = {
            '': '',
        }
        actual = CalculateTotalLymphNodes().main(attributes=attributes)

        expected = attributes.copy()
        expected.update({
            '': '',
        })

        self.assertDictEqual(expected, actual)

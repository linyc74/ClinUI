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

    def test_main(self):
        attributes = {
            'Tumor Disease Anatomic Site': 'External upper lip',
        }
        actual = CalculateICD().main(attributes=attributes)
        expected = {
            'Tumor Disease Anatomic Site': 'External upper lip',
            'ICD-O-3 Site Code': 'C00.0',
            'ICD-10 Classification': 'C00.0',
        }
        self.assertDictEqual(expected, actual)

    def test_not_recognized_site(self):
        attributes = {
            'Tumor Disease Anatomic Site': 'Cat tongue',
        }
        actual = CalculateICD().main(attributes=attributes)
        self.assertDictEqual(attributes, actual)


class TestCalculateStage(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_stage_4c(self):
        attributes = {
            'Clinical TNM (cTNM)': 'T4bN3M1',
        }
        actual = CalculateStage().main(attributes=attributes)
        expected = {
            'Clinical TNM (cTNM)': 'T4bN3M1',
            'Neoplasm Disease Stage American Joint Committee on Cancer Code': 'Stage IVC',
        }
        self.assertDictEqual(expected, actual)

    def test_stage_4b(self):
        attributes = {
            'Clinical TNM (cTNM)': 'T4bN3M0',
        }
        actual = CalculateStage().main(attributes=attributes)
        expected = {
            'Clinical TNM (cTNM)': 'T4bN3M0',
            'Neoplasm Disease Stage American Joint Committee on Cancer Code': 'Stage IVB',
        }
        self.assertDictEqual(expected, actual)

    def test_stage_4a(self):
        attributes = {
            'Clinical TNM (cTNM)': 'T4aN2M0',
        }
        actual = CalculateStage().main(attributes=attributes)
        expected = {
            'Clinical TNM (cTNM)': 'T4aN2M0',
            'Neoplasm Disease Stage American Joint Committee on Cancer Code': 'Stage IVA',
        }
        self.assertDictEqual(expected, actual)

    def test_stage_3(self):
        attributes = {
            'Clinical TNM (cTNM)': 'T2N1M0',
        }
        actual = CalculateStage().main(attributes=attributes)
        expected = {
            'Clinical TNM (cTNM)': 'T2N1M0',
            'Neoplasm Disease Stage American Joint Committee on Cancer Code': 'Stage III',
        }
        self.assertDictEqual(expected, actual)

    def test_stage_2(self):
        attributes = {
            'Clinical TNM (cTNM)': 'T2N0M0',
        }
        actual = CalculateStage().main(attributes=attributes)
        expected = {
            'Clinical TNM (cTNM)': 'T2N0M0',
            'Neoplasm Disease Stage American Joint Committee on Cancer Code': 'Stage II',
        }
        self.assertDictEqual(expected, actual)

    def test_stage_1(self):
        attributes = {
            'Clinical TNM (cTNM)': 'T1N0M0',
        }
        actual = CalculateStage().main(attributes=attributes)
        expected = {
            'Clinical TNM (cTNM)': 'T1N0M0',
            'Neoplasm Disease Stage American Joint Committee on Cancer Code': 'Stage I',
        }
        self.assertDictEqual(expected, actual)

    def test_stage_0(self):
        attributes = {
            'Clinical TNM (cTNM)': 'TisN0M0',
        }
        actual = CalculateStage().main(attributes=attributes)
        expected = {
            'Clinical TNM (cTNM)': 'TisN0M0',
            'Neoplasm Disease Stage American Joint Committee on Cancer Code': 'Stage 0',
        }
        self.assertDictEqual(expected, actual)

    def test_invalid_tnm(self):
        attributes = {
            'Clinical TNM (cTNM)': 'TXN0M0',
        }
        with self.assertRaises(ValueError):
            CalculateStage().main(attributes=attributes)


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

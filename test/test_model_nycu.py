from src.model_nycu import CalculateDiagnosisAge, CalculateSurvival, CalculateICD, CalculateStage, CalculateLymphNodes
from .setup import TestCase


class TestCalculateDiagnosisAge(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_main(self):
        attributes = {
            'Birth Date': '2001-01-01',
            'Clinical Diagnosis Date': '2002-01-01',
        }
        actual = CalculateDiagnosisAge().main(attributes=attributes)

        expected = attributes.copy()
        expected.update({
            'Clinical Diagnosis Age': 1.0,
        })

        self.assertDictEqual(expected, actual)


class TestCalculateSurvival(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_alive_disease_free(self):
        attributes = {
            'Initial Treatment Completion Date': '2003-01-01',
            'Last Follow-up Date': '2003-12-27',
            'Recur Date after Initial Treatment': '',
            'Expire Date': '',
            'Cause of Death': ''
        }
        actual = CalculateSurvival().main(attributes=attributes)

        expected = attributes.copy()
        expected.update({
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
            'Initial Treatment Completion Date': '2003-01-01',
            'Last Follow-up Date': '2004-01-26',
            'Recur Date after Initial Treatment': '2003-12-27',
            'Expire Date': '',
            'Cause of Death': ''
        }
        actual = CalculateSurvival().main(attributes=attributes)

        expected = attributes.copy()
        expected.update({
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
            'Initial Treatment Completion Date': '2003-01-01',
            'Last Follow-up Date': '2003-12-27',
            'Recur Date after Initial Treatment': '2003-01-31',
            'Expire Date': '2003-12-27',
            'Cause of Death': 'Cancer'
        }
        actual = CalculateSurvival().main(attributes=attributes)

        expected = attributes.copy()
        expected.update({
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
            'Initial Treatment Completion Date': '2003-01-01',
            'Last Follow-up Date': '2003-12-27',
            'Recur Date after Initial Treatment': '',
            'Expire Date': '2003-12-27',
            'Cause of Death': 'Cancer'
        }
        actual = CalculateSurvival().main(attributes=attributes)

        expected = attributes.copy()
        expected.update({
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
            'Initial Treatment Completion Date': '2003-01-01',
            'Last Follow-up Date': '2003-12-27',
            'Recur Date after Initial Treatment': '2003-01-31',
            'Expire Date': '2003-12-27',
            'Cause of Death': 'Other Disease'
        }
        actual = CalculateSurvival().main(attributes=attributes)

        expected = attributes.copy()
        expected.update({
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
            'Initial Treatment Completion Date': '2003-01-01',
            'Last Follow-up Date': '2003-12-27',
            'Recur Date after Initial Treatment': '',
            'Expire Date': '2003-12-27',
            'Cause of Death': 'Other Disease'
        }
        actual = CalculateSurvival().main(attributes=attributes)

        expected = attributes.copy()
        expected.update({
            'Disease Free (Months)': 12.0,
            'Disease Free Status': '0:DiseaseFree',
            'Disease-specific Survival (Months)': 12.0,
            'Disease-specific Survival Status': '0:ALIVE OR DEAD TUMOR FREE',
            'Overall Survival (Months)': 12.0,
            'Overall Survival Status': '1:DECEASED',
        })

        self.assertDictEqual(expected, actual)

    def test_empty(self):
        attributes = {
            'Initial Treatment Completion Date': '',
            'Last Follow-up Date': '',
            'Recur Date after Initial Treatment': '',
            'Expire Date': '',
            'Cause of Death': ''
        }
        actual = CalculateSurvival().main(attributes=attributes)
        expected = attributes.copy()
        expected.update({
            'Disease Free (Months)': '',
            'Disease Free Status': '',
            'Disease-specific Survival (Months)': '',
            'Disease-specific Survival Status': '',
            'Overall Survival (Months)': '',
            'Overall Survival Status': '',
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
        expected = {
            'Tumor Disease Anatomic Site': 'Cat tongue',
            'ICD-O-3 Site Code': '',
            'ICD-10 Classification': '',
        }
        self.assertDictEqual(expected, actual)


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

    def test_wrong_format(self):
        attributes = {
            'Clinical TNM (cTNM)': 'XXX',
        }
        actual = CalculateStage().main(attributes=attributes)
        expected = {
            'Clinical TNM (cTNM)': 'XXX',
            'Neoplasm Disease Stage American Joint Committee on Cancer Code': '',
        }
        self.assertDictEqual(expected, actual)


class TestCalculateLymphNodes(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_level_1a_1b(self):
        attributes = {
            'Lymph Node Level Ia': '1/1',
            'Lymph Node Level Ib': '0/1',
        }
        actual = CalculateLymphNodes().main(attributes=attributes)
        expected = attributes.copy()
        expected.update({
            'Lymph Node Level I': '1/2',
            'Lymph Node Level II': '0/0',
            'Total Lymph Node': '1/2',
        })
        self.assertDictEqual(expected, actual)

    def test_level_2a_2b(self):
        attributes = {
            'Lymph Node Level IIa': '1/1',
            'Lymph Node Level IIb': '0/1',
        }
        actual = CalculateLymphNodes().main(attributes=attributes)
        expected = attributes.copy()
        expected.update({
            'Lymph Node Level I': '0/0',
            'Lymph Node Level II': '1/2',
            'Total Lymph Node': '1/2',
        })
        self.assertDictEqual(expected, actual)

    def test_level_3(self):
        attributes = {
            'Lymph Node Level III': '1/2',
        }
        actual = CalculateLymphNodes().main(attributes=attributes)
        expected = attributes.copy()
        expected.update({
            'Lymph Node Level I': '0/0',
            'Lymph Node Level II': '0/0',
            'Total Lymph Node': '1/2',
        })
        self.assertDictEqual(expected, actual)

    def test_level_4(self):
        attributes = {
            'Lymph Node Level IV': '1/2',
        }
        actual = CalculateLymphNodes().main(attributes=attributes)
        expected = attributes.copy()
        expected.update({
            'Lymph Node Level I': '0/0',
            'Lymph Node Level II': '0/0',
            'Total Lymph Node': '1/2',
        })
        self.assertDictEqual(expected, actual)

    def test_level_5(self):
        attributes = {
            'Lymph Node Level V': '1/2',
        }
        actual = CalculateLymphNodes().main(attributes=attributes)
        expected = attributes.copy()
        expected.update({
            'Lymph Node Level I': '0/0',
            'Lymph Node Level II': '0/0',
            'Total Lymph Node': '1/2',
        })
        self.assertDictEqual(expected, actual)

    def test_level_right_left(self):
        attributes = {
            'Lymph Node (Right)': '0/1',
            'Lymph Node (Left)': '1/1',
        }
        actual = CalculateLymphNodes().main(attributes=attributes)
        expected = attributes.copy()
        expected.update({
            'Lymph Node Level I': '0/0',
            'Lymph Node Level II': '0/0',
            'Total Lymph Node': '1/2',
        })
        self.assertDictEqual(expected, actual)

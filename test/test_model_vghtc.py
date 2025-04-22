from src.model_vghtc import CalculateStage
from .setup import TestCase


class TestCalculateStage(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_stage_4c(self):
        attributes = {
            'Pathological TNM (pTNM)': 'T4bN3M1',
        }
        actual = CalculateStage().main(attributes=attributes)
        expected = {
            'Pathological TNM (pTNM)': 'T4bN3M1',
            'AJCC Stage': 'Stage IVC',
        }
        self.assertDictEqual(expected, actual)

    def test_stage_4b(self):
        attributes = {
            'Pathological TNM (pTNM)': 'T4bN3M0',
        }
        actual = CalculateStage().main(attributes=attributes)
        expected = {
            'Pathological TNM (pTNM)': 'T4bN3M0',
            'AJCC Stage': 'Stage IVB',
        }
        self.assertDictEqual(expected, actual)

    def test_stage_4a(self):
        attributes = {
            'Pathological TNM (pTNM)': 'T4aN2M0',
        }
        actual = CalculateStage().main(attributes=attributes)
        expected = {
            'Pathological TNM (pTNM)': 'T4aN2M0',
            'AJCC Stage': 'Stage IVA',
        }
        self.assertDictEqual(expected, actual)

    def test_stage_3(self):
        attributes = {
            'Pathological TNM (pTNM)': 'T2N1M0',
        }
        actual = CalculateStage().main(attributes=attributes)
        expected = {
            'Pathological TNM (pTNM)': 'T2N1M0',
            'AJCC Stage': 'Stage III',
        }
        self.assertDictEqual(expected, actual)

    def test_stage_2(self):
        attributes = {
            'Pathological TNM (pTNM)': 'T2N0M0',
        }
        actual = CalculateStage().main(attributes=attributes)
        expected = {
            'Pathological TNM (pTNM)': 'T2N0M0',
            'AJCC Stage': 'Stage II',
        }
        self.assertDictEqual(expected, actual)

    def test_stage_1(self):
        attributes = {
            'Pathological TNM (pTNM)': 'T1N0M0',
        }
        actual = CalculateStage().main(attributes=attributes)
        expected = {
            'Pathological TNM (pTNM)': 'T1N0M0',
            'AJCC Stage': 'Stage I',
        }
        self.assertDictEqual(expected, actual)

    def test_stage_0(self):
        attributes = {
            'Pathological TNM (pTNM)': 'TisN0M0',
        }
        actual = CalculateStage().main(attributes=attributes)
        expected = {
            'Pathological TNM (pTNM)': 'TisN0M0',
            'AJCC Stage': 'Stage 0',
        }
        self.assertDictEqual(expected, actual)

    def test_missing_annotation(self):
        attributes = {
            'Pathological TNM (pTNM)': 'T2NxMx',
        }
        actual = CalculateStage().main(attributes=attributes)
        expected = {
            'Pathological TNM (pTNM)': 'T2NxMx',
            'AJCC Stage': 'Stage II',
        }
        self.assertDictEqual(expected, actual)

    def test_wrong_format(self):
        attributes = {
            'Pathological TNM (pTNM)': 'XXX',
        }
        actual = CalculateStage().main(attributes=attributes)
        expected = {
            'Pathological TNM (pTNM)': 'XXX',
            'AJCC Stage': '',
        }
        self.assertDictEqual(expected, actual)

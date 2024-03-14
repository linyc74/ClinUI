from src.model import Model
from src.schema import NycuOsccSchema
from .setup import TestCase


class TestModel(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_read_clinical_data_table(self):
        model = Model(NycuOsccSchema)
        model.import_clinical_data_table(file=f'{self.indir}/clinical_data.csv')

    def test_wrong_clinical_data_table(self):
        model = Model(NycuOsccSchema)
        with self.assertRaises(AssertionError):
            model.import_clinical_data_table(file=f'{self.indir}/error_clinical_data.csv')

    def test_import_sequencing_table(self):
        model = Model(NycuOsccSchema)
        model.import_clinical_data_table(file=f'{self.indir}/clinical_data.csv')
        model.import_sequencing_table(file=f'{self.indir}/sequencing.csv')
        self.assertEqual(12, len(model.dataframe))

    def test_wrong_sequencing_table(self):
        model = Model(NycuOsccSchema)
        model.import_clinical_data_table(file=f'{self.indir}/clinical_data.csv')
        with self.assertRaises(AssertionError):
            model.import_sequencing_table(file=f'{self.indir}/error_sequencing.csv')

    def test_find_without_start(self):
        model = Model(NycuOsccSchema)
        model.import_clinical_data_table(file=f'{self.indir}/clinical_data.csv')
        actual = model.find(text='Lin', start=None)
        self.assertTupleEqual((1, 'Lab Sample ID'), actual)

    def test_find_with_start(self):
        model = Model(NycuOsccSchema)
        model.import_clinical_data_table(file=f'{self.indir}/clinical_data.csv')
        actual = model.find(text='Lin', start=(1, 'Sample Collection Date'))
        self.assertTupleEqual((2, 'Lab Sample ID'), actual)

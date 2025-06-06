from src.model import Model
from src.schema import NycuOsccSchema
from .setup import TestCase


class TestModel(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_undo(self):
        model = Model(NycuOsccSchema)
        model.import_clinical_data_table(file=f'{self.indir}/clinical_data.csv')
        model.undo()
        self.assertEqual(0, len(model.dataframe))

    def test_redo(self):
        model = Model(NycuOsccSchema)
        model.import_clinical_data_table(file=f'{self.indir}/clinical_data.csv')
        model.undo()
        model.redo()
        self.assertEqual(11, len(model.dataframe))

    def test_reset_dataframe(self):
        model = Model(NycuOsccSchema)
        model.import_clinical_data_table(file=f'{self.indir}/clinical_data.csv')
        model.reset_dataframe()
        self.assertEqual(0, len(model.dataframe))
        self.assertEqual(2, len(model.undo_cache))

    def test_get_sample(self):
        model = Model(NycuOsccSchema)
        model.import_clinical_data_table(file=f'{self.indir}/clinical_data.csv')

        for row in range(len(model.dataframe)):
            attributes = model.get_sample(row=row)
            for val in attributes.values():
                with self.subTest(row=row, val=val):
                    self.assertTrue(type(val) is str)  # everything out of the model should be string
                    self.assertNotEqual('nan', val)  # 'nan' should be converted to ''

    def test_import_clinical_data_table(self):
        model = Model(NycuOsccSchema)
        model.import_clinical_data_table(file=f'{self.indir}/clinical_data.csv')
        # Do not auto-detect 'NA' as NaN, 'NA' should remain as string
        self.assertEqual('NA', model.dataframe.loc[0, 'Medical Record ID'])
        self.assertEqual(1, len(model.undo_cache))

    def test_import_error_clinical_data_table(self):
        model = Model(NycuOsccSchema)
        model.import_clinical_data_table(file=f'{self.indir}/error_clinical_data.csv')
        self.assertEqual(1, len(model.undo_cache))

    def test_import_sequencing_table(self):
        model = Model(NycuOsccSchema)
        model.import_clinical_data_table(file=f'{self.indir}/clinical_data.csv')
        model.import_sequencing_table(file=f'{self.indir}/sequencing.csv')
        self.assertEqual(12, len(model.dataframe))
        self.assertEqual(2, len(model.undo_cache))

    def test_find_without_start(self):
        model = Model(NycuOsccSchema)
        model.import_clinical_data_table(file=f'{self.indir}/clinical_data.csv')
        actual = model.find(text='Lin', start=None)
        self.assertTupleEqual((1, 'Lab Sample ID'), actual)

    def test_find_with_start(self):
        model = Model(NycuOsccSchema)
        model.import_clinical_data_table(file=f'{self.indir}/clinical_data.csv')
        actual = model.find(text='Lin', start=(1, 'Surgical Excision Date'))
        self.assertTupleEqual((2, 'Lab Sample ID'), actual)

    def test_sort_dataframe(self):
        model = Model(NycuOsccSchema)
        model.import_clinical_data_table(file=f'{self.indir}/clinical_data.csv')
        model.sort_dataframe(by='Surgical Excision Date', ascending=False)
        self.assertEqual('2015-01-06', model.dataframe.loc[0, 'Surgical Excision Date'])
        self.assertEqual(2, len(model.undo_cache))

    def test_drop_column(self):
        model = Model(NycuOsccSchema)
        model.import_clinical_data_table(file=f'{self.indir}/clinical_data.csv')
        model.drop(columns=['Surgical Excision Date'])
        self.assertTrue('Surgical Excision Date' not in model.dataframe.columns)
        self.assertEqual(2, len(model.undo_cache))

    def test_update_sample(self):
        model = Model(NycuOsccSchema)
        model.import_clinical_data_table(file=f'{self.indir}/clinical_data.csv')
        model.update_sample(row=0, attributes={'Medical Record ID': '12345'})
        self.assertEqual('12345', model.dataframe.loc[0, 'Medical Record ID'])
        self.assertEqual(2, len(model.undo_cache))

    def test_append_sample(self):
        model = Model(NycuOsccSchema)
        model.import_clinical_data_table(file=f'{self.indir}/clinical_data.csv')
        model.append_sample(attributes={'Medical Record ID': '12345'})
        self.assertEqual('12345', model.dataframe.loc[11, 'Medical Record ID'])
        self.assertEqual(2, len(model.undo_cache))

    def test_reprocess_table(self):
        model = Model(NycuOsccSchema)
        model.import_clinical_data_table(file=f'{self.indir}/clinical_data.csv')
        model.reprocess_table()
        self.assertEqual(11, len(model.dataframe))
        self.assertEqual(2, len(model.undo_cache))

    def test_track_file_saved(self):
        model = Model(NycuOsccSchema)

        # empty dataframe, no need to save
        self.assertTrue(model.is_file_saved())

        # import a table, not saved
        model.import_clinical_data_table(file=f'{self.indir}/clinical_data.csv')
        self.assertFalse(model.is_file_saved())

        # save the table, saved
        model.save_clinical_data_table(file=f'{self.outdir}/clinical_data.csv')
        self.assertTrue(model.is_file_saved())

        # reprocess the table, not saved
        model.reprocess_table()
        self.assertFalse(model.is_file_saved())

        # undo to the saved state, saved
        model.undo()
        self.assertTrue(model.is_file_saved())

        # redo to the unsaved state, not saved
        model.redo()
        self.assertFalse(model.is_file_saved())

        # save the table, saved
        model.save_clinical_data_table(file=f'{self.outdir}/clinical_data.csv')
        self.assertTrue(model.is_file_saved())

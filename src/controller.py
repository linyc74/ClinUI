import shutil
from typing import Dict, Optional
from .view import View
from .model import Model
from .cbio_constant import STUDY_IDENTIFIER_KEY


class Controller:

    model: Model
    view: View

    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view
        self.__init_actions()
        self.__connect_button_actions()
        self.__connect_short_actions()

    def __init_actions(self):
        self.action_import_clinical_data_table = ActionImportClinicalDataTable(self)
        self.action_import_sequencing_table = ActionImportSequencingTable(self)
        self.action_save_clinical_data_table = ActionSaveClinicalDataTable(self)
        self.action_sort_ascending = ActionSortAscending(self)
        self.action_sort_descending = ActionSortDescending(self)
        self.action_delete_selected_rows = ActionDeleteSelectedRows(self)
        self.action_reset_table = ActionResetTable(self)
        self.action_add_new_sample = ActionAddNewSample(self)
        self.action_edit_sample = ActionEditSample(self)
        self.action_edit_cell = ActionEditCell(self)
        self.action_export_cbioportal_study = ActionExportCbioportalStudy(self)
        self.action_find = ActionFind(self)
        self.action_reprocess_table = ActionReprocessTable(self)
        self.action_undo = ActionUndo(self)
        self.action_redo = ActionRedo(self)
        self.action_control_s = ActionControlS(self)
        self.action_control_f = ActionFind(self)
        self.action_control_z = ActionUndo(self)
        self.action_control_y = ActionRedo(self)

    def __connect_button_actions(self):
        for name in self.view.BUTTON_NAME_TO_LABEL.keys():
            button = getattr(self.view, f'button_{name}')
            method = getattr(self, f'action_{name}', None)
            if method is not None:
                button.clicked.connect(method)
            else:
                print(f'WARNING: Controller method "action_{name}" does not exist for the button "{name}"')

    def __connect_short_actions(self):
        for name in self.view.SHORTCUT_NAME_TO_KEY_SEQUENCE.keys():
            shortcut = getattr(self.view, f'shortcut_{name}')
            method = getattr(self, f'action_{name}', None)
            if method is not None:
                shortcut.activated.connect(method)
            else:
                print(f'WARNING: Controller method "action_{name}" does not exist for the shortcut "{name}"')


class Action:

    model: Model
    view: View

    def __init__(self, controller: Controller):
        self.model = controller.model
        self.view = controller.view


class ActionImportClinicalDataTable(Action):

    def __call__(self):
        file = self.view.file_dialog_open_table()
        if file == '':
            return

        try:
            self.model.import_clinical_data_table(file=file)
            self.view.refresh_table()
        except Exception as e:
            self.view.message_box_error(msg=repr(e))


class ActionImportSequencingTable(Action):

    def __call__(self):
        file = self.view.file_dialog_open_table()
        if file == '':
            return

        try:
            self.model.import_sequencing_table(file=file)
            self.view.refresh_table()
        except Exception as e:
            self.view.message_box_error(msg=repr(e))


class ActionSaveClinicalDataTable(Action):

    def __call__(self):
        file = self.view.file_dialog_save_table(filename='clinical_data_table.csv')
        if file == '':
            return
        self.model.save_clinical_data_table(file=file)
        self.view.refresh_table()


class ActionFind(Action):

    def __call__(self):
        text = self.view.dialog_find()
        if text is None:
            return

        selected_cells = self.view.get_selected_cells()
        start = None if len(selected_cells) == 0 else selected_cells[0]

        found_cell = self.model.find(text=text, start=start)

        if found_cell is None:
            self.view.message_box_info(msg='Couldn\'t find what you were looking for')
            return

        index, column = found_cell
        self.view.select_cell(index=index, column=column)


class ActionSort(Action):

    ASCENDING: bool

    def __call__(self):
        columns = self.view.get_selected_columns()
        if len(columns) == 0:
            self.view.message_box_error(msg='Please select a column')
        elif len(columns) == 1:
            self.model.sort_dataframe(by=columns[0], ascending=self.ASCENDING)
            self.view.refresh_table()
        else:
            self.view.message_box_error(msg='Please select only one column')


class ActionSortAscending(ActionSort):

    ASCENDING = True


class ActionSortDescending(ActionSort):

    ASCENDING = False


class ActionDeleteSelectedRows(Action):

    def __call__(self):
        rows = self.view.get_selected_rows()
        if len(rows) == 0:
            return
        if self.view.message_box_yes_no(msg='Are you sure you want to delete the selected rows?'):
            self.model.drop(rows=rows)
            self.view.refresh_table()


class ActionResetTable(Action):

    def __call__(self):
        if len(self.model.dataframe) == 0:
            return  # nothing to reset

        if self.view.message_box_yes_no(msg='Are you sure you want to reset the table?'):
            self.model.reset_dataframe()
            self.view.refresh_table()


class ActionAddNewSample(Action):

    def __call__(self):
        success = False
        attributes = None
        while not success:
            attributes = self.view.dialog_edit_sample(attributes=attributes)
            if attributes is None:
                break
            try:
                self.model.append_sample(attributes=attributes)
                self.view.refresh_table()
                success = True
            except Exception as e:
                self.view.message_box_error(msg=repr(e))


class ActionEditSample(Action):

    def __call__(self):
        rows = self.view.get_selected_rows()

        if len(rows) == 0:
            self.view.message_box_error(msg='Please select a row')
            return
        elif len(rows) > 1:
            self.view.message_box_error(msg='Please select only one row')
            return

        row = rows[0]  # only one row is selected

        attributes = self.model.get_sample(row=row)

        success = False
        while not success:
            attributes = self.view.dialog_edit_sample(attributes=attributes)
            if attributes is None:
                break
            try:
                self.model.update_sample(row=row, attributes=attributes)
                self.view.refresh_table()
                success = True
            except Exception as e:
                self.view.message_box_error(msg=repr(e))


class ActionEditCell(Action):

    def __call__(self):
        try:
            cells = self.view.get_selected_cells()

            if len(cells) == 0:
                self.view.message_box_error('Please select a cell')
                return
            elif len(cells) > 1:
                self.view.message_box_error('Please select only one cell')
                return

            row, column = cells[0]
            value = self.model.get_value(row=row, column=column)

            new_value = self.view.dialog_edit_cell(value=value)

            if new_value is None:
                return

            self.model.update_cell(row=row, column=column, value=new_value)
            self.view.refresh_table()

        except Exception as e:
            self.view.message_box_error(msg=repr(e))


class ActionExportCbioportalStudy(Action):

    maf_dir: Optional[str]
    outdir: Optional[str]
    project_info_dict: Optional[Dict[str, str]]
    study_info_dict: Dict[str, str]
    tags_dict: Optional[Dict[str, str]]

    def __call__(self):
        self.set_maf_dir()
        if self.maf_dir is None:
            return

        self.set_project_info_dict()
        if self.project_info_dict is None:
            return

        self.set_outdir()
        if self.outdir is None:
            return

        self.set_study_info_dict()
        self.set_tags_dict()
        self.export_cbioportal_study()

    def set_maf_dir(self):
        d = self.view.file_dialog_open_directory(caption='Select MAF directory')
        if d == '':
            self.maf_dir = None
        else:
            self.maf_dir = d

    def set_project_info_dict(self):
        self.project_info_dict = self.view.dialog_project_info()

    def set_outdir(self):
        d = self.view.file_dialog_open_directory(caption='Select Destination Directory')
        study_id = self.project_info_dict[STUDY_IDENTIFIER_KEY]
        if d == '':
            self.outdir = None
        else:
            self.outdir = f'{d}/{study_id}'

    def set_study_info_dict(self):
        self.study_info_dict = self.project_info_dict.copy()
        self.study_info_dict.pop('source_data')

    def set_tags_dict(self):
        s = self.project_info_dict.get('source_data')
        if s == '':
            self.tags_dict = None
        else:
            self.tags_dict = {'source_data': s}

    def export_cbioportal_study(self):
        try:
            self.model.export_cbioportal_study(
                maf_dir=self.maf_dir,
                study_info_dict=self.study_info_dict,
                tags_dict=self.tags_dict,
                outdir=self.outdir)
            self.view.message_box_info(msg='Export cBioPortal study complete')
        except Exception as e:
            shutil.rmtree(self.outdir)
            self.view.message_box_error(msg=repr(e))


class ActionReprocessTable(Action):

    def __call__(self):
        try:
            self.model.reprocess_table()
            self.view.refresh_table()
        except Exception as e:
            self.view.message_box_error(msg=repr(e))


class ActionUndo(Action):

    def __call__(self):
        try:
            self.model.undo()
            self.view.refresh_table()
        except Exception as e:
            self.view.message_box_error(msg=repr(e))


class ActionRedo(Action):

    def __call__(self):
        try:
            self.model.redo()
            self.view.refresh_table()
        except Exception as e:
            self.view.message_box_error(msg=repr(e))


class ActionControlS(Action):

    def __call__(self):
        if self.model.clinical_data_file is None:
            file = self.view.file_dialog_save_table(filename='clinical_data_table.csv')
            if file == '':
                return
        else:
            file = self.model.clinical_data_file
        self.model.save_clinical_data_table(file=file)
        self.view.refresh_table()

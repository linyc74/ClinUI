from typing import Dict, Optional
from .view import View
from .model import Model


class Controller:

    model: Model
    view: View

    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view
        self.__init_actions()
        self.__connect_button_actions()
        self.view.show()

    def __init_actions(self):
        self.action_read_clinical_data_table = ActionReadClinicalDataTable(self)
        self.action_import_sequencing_table = ActionImportSequencingTable(self)
        self.action_save_clinical_data_table = ActionSaveClinicalDataTable(self)
        self.action_sort_ascending = ActionSortAscending(self)
        self.action_sort_descending = ActionSortDescending(self)
        self.action_delete_selected_rows = ActionDeleteSelectedRows(self)
        self.action_reset_table = ActionResetTable(self)
        self.action_add_new_sample = ActionAddNewSample(self)
        self.action_edit_sample = ActionEditSample(self)
        self.action_export_cbioportal_study = ActionExportCbioportalStudy(self)

    def __connect_button_actions(self):
        for name in self.view.BUTTON_NAME_TO_LABEL.keys():
            button = getattr(self.view, f'button_{name}')
            method = getattr(self, f'action_{name}', None)
            if method is not None:
                button.clicked.connect(method)
            else:
                print(f'WARNING: method "action_{name}" does not exist in the Controller')


class Action:

    model: Model
    view: View

    def __init__(self, controller: Controller):
        self.model = controller.model
        self.view = controller.view


class ActionReadClinicalDataTable(Action):

    def __call__(self):
        file = self.view.file_dialog_open_table()
        if file == '':
            return

        try:
            self.model.read_clinical_data_table(file=file)
        except Exception as e:
            self.view.message_box_error(msg=str(e))
            return

        self.view.refresh_table()


class ActionImportSequencingTable(Action):

    def __call__(self):
        file = self.view.file_dialog_open_table()
        if file == '':
            return

        try:
            self.model.import_sequencing_table(file=file)
        except Exception as e:
            self.view.message_box_error(msg=str(e))
            return

        self.view.refresh_table()


class ActionSaveClinicalDataTable(Action):

    def __call__(self):
        file = self.view.file_dialog_save_table(filename='clinical_data_table.csv')
        if file == '':
            return
        self.model.save_clinical_data_table(file=file)


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
        attributes = self.view.dialog_edit_sample()

        if attributes is None:
            return

        success, msg = self.model.append_row(attributes=attributes)
        if not success:
            self.view.message_box_error(msg=msg)

        self.view.refresh_table()


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

        attributes = self.model.get_row(row=row)
        attributes = self.view.dialog_edit_sample(attributes)

        if attributes is None:
            return

        try:
            self.model.update_row(row=row, attributes=attributes)
        except Exception as e:
            self.view.message_box_error(msg=str(e))
            return

        self.view.refresh_table()


class ActionExportCbioportalStudy(Action):

    maf_dir: Optional[str]
    dstdir: Optional[str]
    project_info_dict: Optional[Dict[str, str]]
    study_info_dict: Dict[str, str]
    tags_dict: Optional[Dict[str, str]]

    def __call__(self):
        self.set_maf_dir()
        if self.maf_dir == '':
            return

        self.set_project_info_dict()
        if self.project_info_dict is None:
            return

        self.set_dstdir()
        if self.dstdir == '':
            return

        self.set_study_info_dict()
        self.set_tags_dict()
        self.export_cbioportal_study()

    def set_maf_dir(self):
        self.maf_dir = self.view.file_dialog_open_directory(caption='Select MAF directory')

    def set_project_info_dict(self):
        self.project_info_dict = self.view.dialog_project_info()

    def set_dstdir(self):
        self.dstdir = self.view.file_dialog_open_directory(caption='Select Destination Directory')

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
        success, msg = self.model.export_cbioportal_study(
            maf_dir=self.maf_dir,
            study_info_dict=self.study_info_dict,
            tags_dict=self.tags_dict,
            dstdir=self.dstdir)

        if success:
            self.view.message_box_info(msg=msg)
        else:
            self.view.message_box_error(msg=msg)


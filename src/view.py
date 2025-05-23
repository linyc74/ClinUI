import pandas as pd
from os.path import dirname
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QPushButton, QFileDialog, \
    QMessageBox, QGridLayout, QDialog, QFormLayout, QDialogButtonBox, QComboBox, QScrollArea, QLineEdit, \
    QShortcut
from typing import List, Optional, Any, Dict, Tuple, Type
from .model import Model
from .schema import NycuOsccSchema, VghtcOsccSchema


class Elements:

    BUTTON_NAME_TO_LABEL: Dict[str, str] = {}
    BUTTON_NAME_TO_POSITION: Dict[str, Tuple[int, int]] = {}
    SHORTCUT_NAME_TO_KEY_SEQUENCE: Dict[str, str] = {}


class DefaultElements(Elements):

    BUTTON_NAME_TO_LABEL = {
        'import_clinical_data_table': 'Import Clinical Data Table',
        'save_clinical_data_table': 'Save Clinical Data Table',
        'reprocess_table': 'Reprocess Table',

        'undo': 'Undo',
        'redo': 'Redo',
        'sort_ascending': 'Sort (A to Z)',
        'sort_descending': 'Sort (Z to A)',
        'delete_selected_rows': 'Delete Selected Rows',

        'add_new_sample': 'Add New Sample',
        'edit_sample': 'Edit Sample',
        'export_cbioportal_study': 'Export cBioPortal Study',
    }
    BUTTON_NAME_TO_POSITION = {
        'import_clinical_data_table': (0, 0),
        'save_clinical_data_table': (1, 0),
        'reprocess_table': (4, 0),

        'undo': (0, 1),
        'redo': (1, 1),
        'sort_ascending': (2, 1),
        'sort_descending': (3, 1),
        'delete_selected_rows': (4, 1),

        'add_new_sample': (0, 2),
        'edit_sample': (1, 2),
        'export_cbioportal_study': (4, 2),
    }


class NycuOsccElements(Elements):

    BUTTON_NAME_TO_LABEL = {
        'import_clinical_data_table': 'Import Clinical Data Table',
        'import_sequencing_table': 'Import Sequencing Table',
        'save_clinical_data_table': 'Save Clinical Data Table',
        'reprocess_table': 'Reprocess Table',

        'undo': 'Undo',
        'redo': 'Redo',
        'find': 'Find',
        'sort_ascending': 'Sort (A to Z)',
        'sort_descending': 'Sort (Z to A)',
        'delete_selected_rows': 'Delete Selected Rows',
        'reset_table': 'Reset Table',

        'add_new_sample': 'Add New Sample',
        'edit_sample': 'Edit Sample',
        'edit_cell': 'Edit Cell',
        'export_cbioportal_study': 'Export cBioPortal Study',
    }
    BUTTON_NAME_TO_POSITION = {
        'import_clinical_data_table': (0, 0),
        'import_sequencing_table': (1, 0),
        'save_clinical_data_table': (2, 0),
        'reprocess_table': (6, 0),

        'undo': (0, 1),
        'redo': (1, 1),
        'find': (2, 1),
        'sort_ascending': (3, 1),
        'sort_descending': (4, 1),
        'delete_selected_rows': (5, 1),
        'reset_table': (6, 1),

        'add_new_sample': (0, 2),
        'edit_sample': (1, 2),
        'edit_cell': (2, 2),
        'export_cbioportal_study': (6, 2),
    }
    SHORTCUT_NAME_TO_KEY_SEQUENCE = {
        'control_s': 'Ctrl+S',
        'control_f': 'Ctrl+F',
        'control_z': 'Ctrl+Z',
        'control_y': 'Ctrl+Y',
    }


class VghtcOsccElements(Elements):

    BUTTON_NAME_TO_LABEL = {
        'import_clinical_data_table': 'Import Clinical Data Table',
        'save_clinical_data_table': 'Save Clinical Data Table',
        'reprocess_table': 'Reprocess Table',

        'undo': 'Undo',
        'redo': 'Redo',
        'find': 'Find',
        'sort_ascending': 'Sort (A to Z)',
        'sort_descending': 'Sort (Z to A)',
        'delete_selected_rows': 'Delete Selected Rows',

        'add_new_sample': 'Add New Sample',
        'edit_sample': 'Edit Sample',
    }
    BUTTON_NAME_TO_POSITION = {
        'import_clinical_data_table': (0, 0),
        'save_clinical_data_table': (1, 0),
        'reprocess_table': (5, 0),

        'undo': (0, 1),
        'redo': (1, 1),
        'find': (2, 1),
        'sort_ascending': (3, 1),
        'sort_descending': (4, 1),
        'delete_selected_rows': (5, 1),

        'add_new_sample': (0, 2),
        'edit_sample': (1, 2),
    }


class Table(QTableWidget):

    model: Model

    def __init__(self, model: Model):
        super().__init__()
        self.model = model
        self.refresh_table()

    def refresh_table(self):
        df = self.model.get_dataframe()

        self.setRowCount(len(df.index))
        self.setColumnCount(len(df.columns))

        self.setHorizontalHeaderLabels(df.columns)

        for i in range(len(df.index)):
            for j in range(len(df.columns)):
                value = df.iloc[i, j]
                item = QTableWidgetItem(str_(value))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # makes the item immutable, i.e. user cannot edit it
                self.setItem(i, j, item)

        self.resizeColumnsToContents()

    def get_selected_rows(self) -> List[int]:
        ret = []
        for item in self.selectedItems():
            ith_row = item.row()
            if ith_row not in ret:
                ret.append(ith_row)
        return ret

    def get_selected_columns(self) -> List[str]:
        ret = []
        for item in self.selectedItems():
            ith_col = item.column()
            column = self.horizontalHeaderItem(ith_col).text()
            if column not in ret:
                ret.append(column)
        return ret

    def get_selected_cells(self) -> List[Tuple[int, str]]:
        ret = []
        for item in self.selectedItems():
            ith_row = item.row()
            ith_col = item.column()
            column = self.horizontalHeaderItem(ith_col).text()
            ret.append((ith_row, column))
        return ret

    def select_cell(self, index: int, column: str):
        ith_row = index
        columns = [self.horizontalHeaderItem(i).text() for i in range(self.columnCount())]
        ith_col = columns.index(column)
        self.setCurrentCell(ith_row, ith_col)


class View(QWidget):

    TITLE = 'ClinUI'
    ICON_FILE = 'icon/logo.ico'
    WIDTH, HEIGHT = 1280, 768

    model: Model

    elements: Type[Elements]
    vertical_layout: QVBoxLayout
    table: Table
    button_grid: QGridLayout

    def __init__(self, model: Model):
        super().__init__()
        self.model = model

        self.setWindowTitle(f'{self.TITLE} ({self.model.schema.NAME})')
        self.setWindowIcon(QIcon(self.ICON_FILE))
        self.setWindowIcon(QIcon(f'{dirname(dirname(__file__))}/{self.ICON_FILE}'))
        self.resize(self.WIDTH, self.HEIGHT)

        self.__set_elements()
        self.__init__vertical_layout()
        self.__init__main_table()
        self.__init__buttons()
        self.__init__shortcuts()
        self.__init__methods()
        self.show()

    def __set_elements(self):
        if self.model.schema is NycuOsccSchema:
            self.elements = NycuOsccElements
        elif self.model.schema is VghtcOsccSchema:
            self.elements = VghtcOsccElements
        else:
            self.elements = DefaultElements

    def __init__vertical_layout(self):
        self.vertical_layout = QVBoxLayout()
        self.setLayout(self.vertical_layout)

    def __init__main_table(self):
        self.table = Table(self.model)
        self.vertical_layout.addWidget(self.table)

    def __init__buttons(self):
        self.button_grid = QGridLayout()
        self.vertical_layout.addLayout(self.button_grid)

        for name, label in self.elements.BUTTON_NAME_TO_LABEL.items():
            setattr(self, f'button_{name}', QPushButton(label))
            button = getattr(self, f'button_{name}')
            pos = self.elements.BUTTON_NAME_TO_POSITION[name]
            self.button_grid.addWidget(button, *pos)

    def __init__shortcuts(self):
        for name, key_sequence in self.elements.SHORTCUT_NAME_TO_KEY_SEQUENCE.items():
            shortcut = QShortcut(QKeySequence(key_sequence), self)
            setattr(self, f'shortcut_{name}', shortcut)

    def __init__methods(self):
        self.file_dialog_open_table = FileDialogOpenTable(self)
        self.file_dialog_save_table = FileDialogSaveTable(self)
        self.file_dialog_open_directory = FileDialogOpenDirectory(self)
        self.message_box_info = MessageBoxInfo(self)
        self.message_box_error = MessageBoxError(self)
        self.message_box_yes_no = MessageBoxYesNo(self)
        self.message_box_unsaved_file = MessageBoxUnsavedFile(self)
        self.dialog_edit_sample = DialogEditSample(self)
        self.dialog_project_info = DialogStudyInfo(self)
        self.dialog_find = DialogFind(self)
        self.dialog_edit_cell = DialogEditCell(self)

    def refresh_table(self):
        self.table.refresh_table()

        suffix = ''
        df = self.model.get_dataframe()
        if len(df) > 0:  # only show suffix if there is data
            file = f' - {self.model.clinical_data_file}' if self.model.clinical_data_file is not None else ''
            state = ' (saved)' if self.model.is_file_saved() else ' (unsaved)'
            suffix = file + state

        self.setWindowTitle(f'{self.TITLE} ({self.model.schema.NAME}){suffix}')

    def get_selected_rows(self) -> List[int]:
        return self.table.get_selected_rows()

    def get_selected_columns(self) -> List[str]:
        return self.table.get_selected_columns()

    def get_selected_cells(self) -> List[Tuple[int, str]]:
        return self.table.get_selected_cells()

    def select_cell(self, index: int, column: str):
        self.table.select_cell(index=index, column=column)

    def closeEvent(self, event):
        if not self.model.is_file_saved():
            reply = self.message_box_unsaved_file(msg='You have unsaved changes. Do you want to save them?')
            if reply == QMessageBox.Cancel:
                event.ignore()
            elif reply == QMessageBox.No:
                event.accept()
            elif reply == QMessageBox.Save:
                self.shortcut_control_s.activated.emit()
                event.accept()


#


class FileDialog:

    view: View

    def __init__(self, view: View):
        self.view = view


class FileDialogOpenTable(FileDialog):

    def __call__(self) -> str:
        d = QFileDialog(self.view)
        d.resize(1200, 800)
        d.setWindowTitle('Open')
        d.setNameFilter('All Files (*.*);;CSV files (*.csv);;Excel files (*.xlsx)')
        d.selectNameFilter('CSV files (*.csv)')
        d.setOptions(QFileDialog.DontUseNativeDialog)
        d.setFileMode(QFileDialog.ExistingFile)  # only one existing file can be selected
        d.exec_()
        selected = d.selectedFiles()
        return selected[0] if len(selected) > 0 else ''


class FileDialogSaveTable(FileDialog):

    def __call__(self, filename: str = '') -> str:
        d = QFileDialog(self.view)
        d.resize(1200, 800)
        d.setWindowTitle('Save As')
        d.selectFile(filename)
        d.setNameFilter('All Files (*.*);;CSV files (*.csv);;Excel files (*.xlsx)')
        d.selectNameFilter('CSV files (*.csv)')
        d.setOptions(QFileDialog.DontUseNativeDialog)
        d.setAcceptMode(QFileDialog.AcceptSave)

        ret = ''  # default, no file object selected and accepted
        accepted = d.exec_()
        if accepted:
            files = d.selectedFiles()
            if len(files) > 0:
                ret = files[0]
        return ret


class FileDialogOpenDirectory(FileDialog):

    def __call__(self, caption: str) -> str:
        d = QFileDialog(self.view)
        d.resize(1200, 800)
        d.setWindowTitle(caption)
        d.setOptions(QFileDialog.DontUseNativeDialog)
        d.setFileMode(QFileDialog.DirectoryOnly)  # only one directory can be selected
        d.exec_()
        selected = d.selectedFiles()
        return selected[0] if len(selected) > 0 else ''


#


class MessageBox:

    TITLE: str
    ICON: QMessageBox.Icon

    box: QMessageBox

    def __init__(self, view: View):
        self.box = QMessageBox(parent=view)
        self.box.setWindowTitle(self.TITLE)
        self.box.setIcon(self.ICON)


class MessageBoxInfo(MessageBox):

    TITLE = 'Info'
    ICON = QMessageBox.Information

    def __call__(self, msg: str):
        self.box.setText(msg)
        self.box.exec_()


class MessageBoxError(MessageBox):

    TITLE = 'Error'
    ICON = QMessageBox.Warning

    def __call__(self, msg: str):
        self.box.setText(msg)
        self.box.exec_()


class MessageBoxYesNo(MessageBox):

    TITLE = 'ClinUI'
    ICON = QMessageBox.Question

    def __init__(self, view: View):
        super().__init__(view=view)
        self.box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.box.setDefaultButton(QMessageBox.No)

    def __call__(self, msg: str) -> bool:
        self.box.setText(msg)
        return self.box.exec_() == QMessageBox.Yes


class MessageBoxUnsavedFile(MessageBox):

    TITLE = 'ClinUI'
    ICON = QMessageBox.Warning

    def __init__(self, view: View):
        super().__init__(view=view)
        self.box.setStandardButtons(QMessageBox.Save | QMessageBox.No | QMessageBox.Cancel)
        self.box.setDefaultButton(QMessageBox.Cancel)

    def __call__(self, msg: str) -> int:
        self.box.setText(msg)
        return self.box.exec_()  # QMessageBox.Save, QMessageBox.No, QMessageBox.Cancel are the returned integers


#


class DialogComboBoxes:

    WIDTH: int
    HEIGHT: int

    view: QWidget

    dialog: QDialog
    main_layout: QVBoxLayout
    form_layout: QFormLayout

    field_to_options: Dict[str, List[str]]
    field_to_combo_boxes: Dict[str, QComboBox]

    button_box: QDialogButtonBox

    output_dict: Dict[str, str]

    def __init__(self, view: View):
        self.view = view
        self.init_dialog()
        self.init_layout()
        self.init_field_to_options()
        self.init_field_to_combo_boxes()
        self.init_button_box()

    def init_dialog(self):
        self.dialog = QDialog(parent=self.view)
        self.dialog.setWindowTitle(' ')
        self.dialog.resize(self.WIDTH, self.HEIGHT)

    def init_layout(self):
        """
        This method is adapted from ChatGPT's code
        It's very complicated, and I don't fully understand the construction mechinism
        """
        self.main_layout = QVBoxLayout(self.dialog)

        # Create a ScrollArea
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)  # Important: makes the inner widget resize with the scroll area

        # Create a QWidget for the scroll area content
        scroll_contents = QWidget(scroll)
        self.form_layout = QFormLayout(scroll_contents)

        # Set the scroll area's widget to be the QWidget with all items
        scroll.setWidget(scroll_contents)

        # Add ScrollArea to the main layout
        self.main_layout.addWidget(scroll)

    def init_field_to_options(self):
        raise NotImplementedError

    def init_field_to_combo_boxes(self):
        self.field_to_combo_boxes = {}
        for field, options in self.field_to_options.items():
            combo = QComboBox(parent=self.dialog)
            combo.addItems(options)
            combo.setEditable(True)
            self.field_to_combo_boxes[field] = combo
            self.form_layout.addRow(to_title(field), combo)

    def init_button_box(self):
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, parent=self.dialog)
        self.button_box.accepted.connect(self.dialog.accept)
        self.button_box.rejected.connect(self.dialog.reject)
        self.main_layout.addWidget(self.button_box)

    def set_combo_box_default_text(self):
        for field, options in self.field_to_options.items():
            default = str_(options[0]) if len(options) > 0 else ''
            self.field_to_combo_boxes[field].setCurrentText(default)

    def get_output_dict(self) -> Dict[str, str]:
        return {
            field: combo.currentText()
            for field, combo in self.field_to_combo_boxes.items()
        }


class DialogEditSample(DialogComboBoxes):

    WIDTH, HEIGHT = 600, 800

    def init_field_to_options(self):
        self.field_to_options = {}
        for c in self.view.model.schema.DISPLAY_COLUMNS:
            if c in self.view.model.schema.AUTOGENERATED_COLUMNS:
                continue
            options = self.view.model.schema.COLUMN_ATTRIBUTES[c].get('options', [])
            self.field_to_options[c] = [str(o) for o in options]

    def __call__(
            self,
            attributes: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, str]]:

        if attributes is None:
            self.set_combo_box_default_text()
        else:
            self.set_combo_box_text(attributes=attributes)

        return self.get_output_dict() if self.dialog.exec_() == QDialog.Accepted else None

    def set_combo_box_text(self, attributes: Dict[str, Any]):
        for field, value in attributes.items():
            if field in self.field_to_combo_boxes.keys():
                self.field_to_combo_boxes[field].setCurrentText(str_(value))


class DialogStudyInfo(DialogComboBoxes):

    WIDTH, HEIGHT = 600, 300

    def init_field_to_options(self):
        self.field_to_options = self.view.model.schema.CBIO_STUDY_INFO_FIELD_TO_OPTIONS

    def __call__(self) -> Optional[Dict[str, str]]:
        self.set_combo_box_default_text()
        return self.get_output_dict() if self.dialog.exec_() == QDialog.Accepted else None


#


class DialogLineEdits:

    LINE_TITLES: List[str]
    LINE_DEFAULTS: List[str]

    view: View

    dialog: QDialog
    layout: QFormLayout
    line_edits: List[QLineEdit]
    button_box: QDialogButtonBox

    def __init__(self, view: View):
        self.view = view
        self.__init__dialog()
        self.__init__layout()
        self.__init__line_edits()
        self.__init__button_box()

    def __init__dialog(self):
        self.dialog = QDialog(parent=self.view)
        self.dialog.setWindowTitle(' ')

    def __init__layout(self):
        self.layout = QFormLayout(parent=self.dialog)

    def __init__line_edits(self):
        self.line_edits = []
        for title, default in zip(self.LINE_TITLES, self.LINE_DEFAULTS):
            line_edit = QLineEdit(default, parent=self.dialog)
            self.line_edits.append(line_edit)
            self.layout.addRow(title, line_edit)

    def __init__button_box(self):
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, parent=self.dialog)
        self.button_box.accepted.connect(self.dialog.accept)
        self.button_box.rejected.connect(self.dialog.reject)
        self.layout.addWidget(self.button_box)


class DialogFind(DialogLineEdits):

    LINE_TITLES = [
        'Find:',
    ]
    LINE_DEFAULTS = [
        '',
    ]

    def __call__(self) -> Optional[str]:
        if self.dialog.exec_() == QDialog.Accepted:
            return self.line_edits[0].text()
        else:
            return None


class DialogEditCell(DialogLineEdits):

    LINE_TITLES = [
        'Edit Cell:',
    ]
    LINE_DEFAULTS = [
        '',
    ]

    def __call__(self, value: str) -> Optional[str]:
        self.line_edits[0].setText(value)
        if self.dialog.exec_() == QDialog.Accepted:
            return self.line_edits[0].text()
        else:
            return None


#


def str_(value: Any) -> str:
    """
    Converts to str for GUI display
    """
    return '' if pd.isna(value) else str(value)


def to_title(s: str) -> str:
    """
    'Title of good and evil' -> 'Title of Good and Evil'
    'title_of_good_and_evil' -> 'Title of Good and Evil'
    """
    skip = [
        'of',
        'and',
        'or',
        'on',
        'after',
        'about',
        'mAb',  # monoclonal antibody
    ]

    words = s.replace('_', ' ').split(' ')

    for i, word in enumerate(words):
        if word in skip:
            continue
        words[i] = word[0].upper() + word[1:]  # only capitalize the first letter

    return ' '.join(words)

import os
import pandas as pd
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QPushButton, \
    QFileDialog, QMessageBox, QGridLayout, QDialog, QFormLayout, QDialogButtonBox, QComboBox, QScrollArea
from typing import List, Optional, Any, Dict
from .model import Model
from .schema import USER_INPUT_COLUMNS, COLUMN_ATTRIBUTES


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


def str_(value: Any) -> str:
    """
    Converts to str for GUI display
    """
    if pd.isna(value):
        return ''
    elif type(value) == pd.Timestamp:
        return value.strftime('%Y-%m-%d')
    else:
        return str(value)


class View(QWidget):

    TITLE = 'ClinUI'
    ICON_PNG = f'{os.getcwd()}/icon/logo.ico'
    WIDTH, HEIGHT = 1280, 768
    BUTTON_NAME_TO_LABEL = {
        'read_clinical_data_table': 'Read Clinical Data Table',
        'import_sequencing_table': 'Import Sequencing Table',
        'save_clinical_data_table': 'Save Clinical Data Table',

        'sort_ascending': 'Sort (A to Z)',
        'sort_descending': 'Sort (Z to A)',
        'delete_selected_rows': 'Delete Selected Rows',
        'reset_table': 'Reset Table',

        'add_new_sample': 'Add New Sample',
        'edit_sample': 'Edit Sample',
        'export_cbioportal_study': 'Export cBioPortal Study',
    }
    BUTTON_NAME_TO_POSITION = {
        'read_clinical_data_table': (0, 0),
        'import_sequencing_table': (1, 0),
        'save_clinical_data_table': (2, 0),

        'sort_ascending': (0, 1),
        'sort_descending': (1, 1),
        'delete_selected_rows': (2, 1),
        'reset_table': (3, 1),

        'add_new_sample': (0, 2),
        'edit_sample': (1, 2),

        'export_cbioportal_study': (2, 2),
    }

    model: Model
    vertical_layout: QVBoxLayout
    table: Table
    button_grid: QGridLayout

    def __init__(self, model: Model):
        super().__init__()
        self.model = model

        self.setWindowTitle(self.TITLE)
        self.setWindowIcon(QIcon(self.ICON_PNG))
        self.resize(self.WIDTH, self.HEIGHT)

        self.__init__vertical_layout()
        self.__init__main_table()
        self.__init__buttons()
        self.__init__methods()

    def __init__vertical_layout(self):
        self.vertical_layout = QVBoxLayout()
        self.setLayout(self.vertical_layout)

    def __init__main_table(self):
        self.table = Table(self.model)
        self.vertical_layout.addWidget(self.table)

    def __init__buttons(self):
        self.button_grid = QGridLayout()
        self.vertical_layout.addLayout(self.button_grid)

        for name, label in self.BUTTON_NAME_TO_LABEL.items():
            setattr(self, f'button_{name}', QPushButton(label))
            button = getattr(self, f'button_{name}')
            pos = self.BUTTON_NAME_TO_POSITION[name]
            self.button_grid.addWidget(button, *pos)

    def __init__methods(self):
        self.file_dialog_open_table = FileDialogOpenTable(self)
        self.file_dialog_save_table = FileDialogSaveTable(self)
        self.file_dialog_open_directory = FileDialogOpenDirectory(self)
        self.message_box_info = MessageBoxInfo(self)
        self.message_box_error = MessageBoxError(self)
        self.message_box_yes_no = MessageBoxYesNo(self)
        self.dialog_edit_sample = DialogEditSample(self)
        self.dialog_project_info = DialogStudyInfo(self)

    def refresh_table(self):
        self.table.refresh_table()

    def get_selected_rows(self) -> List[int]:
        return self.table.get_selected_rows()

    def get_selected_columns(self) -> List[str]:
        return self.table.get_selected_columns()


class FileDialog:

    parent: QWidget

    def __init__(self, parent: QWidget):
        self.parent = parent


class FileDialogOpenTable(FileDialog):

    def __call__(self) -> str:
        fpath, ftype = QFileDialog.getOpenFileName(
            parent=self.parent,
            caption='Open',
            filter='All Files (*.*);;CSV files (*.csv);;Excel files (*.xlsx)',
            initialFilter='CSV files (*.csv)',
            options=QFileDialog.DontUseNativeDialog
        )
        return fpath


class FileDialogSaveTable(FileDialog):

    def __call__(self, filename: str = '') -> str:
        fpath, ftype = QFileDialog.getSaveFileName(
            parent=self.parent,
            caption='Save As',
            directory=filename,
            filter='All Files (*.*);;CSV files (*.csv);;Excel files (*.xlsx)',
            initialFilter='CSV files (*.csv)',
            options=QFileDialog.DontUseNativeDialog
        )
        return fpath


class FileDialogOpenDirectory(FileDialog):

    def __call__(self, caption: str) -> str:
        fpath = QFileDialog.getExistingDirectory(
            parent=self.parent,
            caption=caption,
            options=QFileDialog.DontUseNativeDialog
        )
        return fpath


class MessageBox:

    TITLE: str
    ICON: QMessageBox.Icon

    box: QMessageBox

    def __init__(self, parent: QWidget):
        self.box = QMessageBox(parent)
        self.box.setWindowTitle(self.TITLE)
        self.box.setIcon(self.ICON)

    def __call__(self, msg: str):
        self.box.setText(msg)
        self.box.exec_()


class MessageBoxInfo(MessageBox):

    TITLE = 'Info'
    ICON = QMessageBox.Information


class MessageBoxError(MessageBox):

    TITLE = 'Error'
    ICON = QMessageBox.Warning


class MessageBoxYesNo(MessageBox):

    TITLE = ' '
    ICON = QMessageBox.Question

    def __init__(self, parent: QWidget):
        super(MessageBoxYesNo, self).__init__(parent)
        self.box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.box.setDefaultButton(QMessageBox.No)

    def __call__(self, msg: str) -> bool:
        self.box.setText(msg)
        return self.box.exec_() == QMessageBox.Yes


class DialogComboBoxes:

    WIDTH: int
    HEIGHT: int

    parent: QWidget

    dialog: QDialog
    main_layout: QVBoxLayout
    form_layout: QFormLayout

    field_to_options: Dict[str, List[str]]
    field_to_combo_boxes: Dict[str, QComboBox]

    button_box: QDialogButtonBox

    def __init__(self, parent: QWidget):
        self.parent = parent
        self.init_dialog()
        self.init_layout()
        self.init_field_to_options()
        self.init_field_to_combo_boxes()
        self.init_button_box()

    def init_dialog(self):
        self.dialog = QDialog(parent=self.parent)
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


class DialogEditSample(DialogComboBoxes):

    WIDTH, HEIGHT = 1024, 768

    def init_field_to_options(self):
        self.field_to_options = {}
        for c in USER_INPUT_COLUMNS:
            options = COLUMN_ATTRIBUTES[c].get('options', [])
            self.field_to_options[c] = [str(o) for o in options]

    def __call__(
            self,
            attributes: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, str]]:

        if attributes is None:
            self.set_combo_box_default_text()
        else:
            self.set_combo_box_text(attributes=attributes)

        if self.dialog.exec_() == QDialog.Accepted:
            return {
                field: combo.currentText()
                for field, combo in self.field_to_combo_boxes.items()
            }
        else:
            return None

    def set_combo_box_text(self, attributes: Dict[str, Any]):
        for field, value in attributes.items():
            if field in self.field_to_combo_boxes.keys():
                self.field_to_combo_boxes[field].setCurrentText(str_(value))


class DialogStudyInfo(DialogComboBoxes):

    WIDTH, HEIGHT = 600, 300

    def init_field_to_options(self):
        self.field_to_options = {
            'type_of_cancer': ['hnsc'],
            'cancer_study_identifier': ['hnsc_nycu_2022'],
            'name': ['Head and Neck Squamous Cell Carcinomas (NYCU, 2022)'],
            'description': ['Whole exome sequencing of OSCC tumor/normal pairs'],
            'groups': ['PUBLIC'],
            'reference_genome': ['hg38', 'hg19'],
            'source_data': ['yy_mmdd_dataset'],
        }

    def __call__(self) -> Optional[Dict[str, str]]:

        self.set_combo_box_default_text()

        if self.dialog.exec_() == QDialog.Accepted:
            return {
                field: combo.currentText()
                for field, combo in self.field_to_combo_boxes.items()
            }
        else:
            return None


def to_title(s: str) -> str:
    skip = [
        'of',
        'and',
        'or',
        'on',
        'after',
        'mAb',  # monoclonal antibody
    ]

    words = s.replace('_', ' ').split(' ')

    for i, word in enumerate(words):
        if word in skip:
            continue
        words[i] = word[0].upper() + word[1:]  # only capitalize the first letter

    return ' '.join(words)

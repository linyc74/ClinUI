import sys
from PyQt5.QtWidgets import QApplication
from .model import Model
from .view import View, SelectDataSchemaDialog
from .controller import Controller
from .schema import DATA_SCHEMA_DICT


VERSION = 'v1.3.2-beta'
STARTING_MESSAGE = f'''\
ClinUI {VERSION}
College of Dentistry, National Yang Ming Chiao Tung University (NYCU), Taiwan
Yu-Cheng Lin, DDS, MS, PhD (ylin@nycu.edu.tw)
'''


class Main:

    APP_ID = f'NYCU.Dentistry.ClinUI.{VERSION}'

    schema_name: str

    def main(self):
        app = QApplication(sys.argv)
        print(STARTING_MESSAGE, flush=True)
        self.select_data_schema()
        self.run_app()
        sys.exit(app.exec_())

    def select_data_schema(self):
        dialog = SelectDataSchemaDialog()
        result = None
        while result is None:  # loop until a schema is selected
            result = dialog.show()
        self.schema_name = result

    def run_app(self):
        self.config_taskbar_icon()
        model = Model(schema=DATA_SCHEMA_DICT[self.schema_name])
        view = View(model=model)
        Controller(model=model, view=view)

    def config_taskbar_icon(self):
        try:
            from ctypes import windll  # only exists on Windows
            windll.shell32.SetCurrentProcessExplicitAppUserModelID(self.APP_ID)
        except ImportError as e:
            print(e, flush=True)

import sys
from PyQt5.QtWidgets import QApplication
from .view import View
from .model import Model
from .controller import Controller
from .schema import DATA_SCHEMA_DICT


VERSION = 'v1.5.0-beta'


class Main:

    schema_name: str

    def main(self, schema_name: str):
        self.schema_name = schema_name
        app = QApplication(sys.argv)
        self.print_starting_message()
        self.config_taskbar_icon()
        self.run_app()
        sys.exit(app.exec_())

    def print_starting_message(self):
        msg = f'''\
ClinUI {VERSION} - {self.schema_name}
College of Dentistry, National Yang Ming Chiao Tung University (NYCU), Taiwan
Yu-Cheng Lin, DDS, MS, PhD (ylin@nycu.edu.tw)'''
        print(msg, flush=True)

    def config_taskbar_icon(self):
        n = self.schema_name.replace(' ', '_')
        app_id = f'NYCU.Dentistry.ClinUI.{VERSION}.{n}'
        try:
            from ctypes import windll  # only exists on Windows
            windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
        except ImportError as e:
            print(e, flush=True)

    def run_app(self):
        model = Model(schema=DATA_SCHEMA_DICT[self.schema_name])
        view = View(model=model)
        Controller(model=model, view=view)

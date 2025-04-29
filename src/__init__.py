import sys
from typing import Type
from PyQt5.QtWidgets import QApplication
from .view import View
from .model import Model
from .schema import Schema
from .controller import Controller


VERSION = 'v1.7.0-beta'


class Main:

    schema: Type[Schema]

    def main(self, schema: Type[Schema]):
        self.schema = schema
        app = QApplication(sys.argv)
        self.print_starting_message()
        self.config_taskbar_icon()
        self.run_app()
        sys.exit(app.exec_())

    def print_starting_message(self):
        msg = f'''\
ClinUI {VERSION} - {self.schema.NAME}
College of Dentistry, National Yang Ming Chiao Tung University (NYCU), Taiwan
Yu-Cheng Lin, DDS, MS, PhD (ylin@nycu.edu.tw)'''
        print(msg, flush=True)

    def config_taskbar_icon(self):
        n = self.schema.NAME.replace(' ', '_')
        app_id = f'NYCU.Dentistry.ClinUI.{VERSION}.{n}'
        try:
            from ctypes import windll  # only exists on Windows
            windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
        except ImportError as e:
            print(e, flush=True)

    def run_app(self):
        m = Model(schema=self.schema)
        v = View(model=m)
        Controller(model=m, view=v)

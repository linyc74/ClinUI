import sys
from PyQt5.QtWidgets import QApplication
from .model import Model
from .view import View, SelectDataSchemaDialog
from .controller import Controller


__VERSION__ = 'v1.2.0-alpha.1'


class Main:

    APP_ID = f'NYCU.Dentistry.ClinUI.{__VERSION__}'

    def main(self):
        self.config_taskbar_icon()

        app = QApplication(sys.argv)

        dialog = SelectDataSchemaDialog()
        schema = None
        while schema is None:
            schema = dialog.get_schema()

        m = Model(schema=schema)
        v = View(model=m)
        c = Controller(model=m, view=v)

        sys.exit(app.exec_())

    def config_taskbar_icon(self):
        try:
            from ctypes import windll  # only exists on Windows
            windll.shell32.SetCurrentProcessExplicitAppUserModelID(self.APP_ID)
        except ImportError as e:
            print(e, flush=True)

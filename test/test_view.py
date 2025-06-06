import sys
from PyQt5.QtWidgets import QApplication
from src.view import View
from src.model import Model
from src.schema import NycuOsccSchema, VghtcOsccSchema, VghtpeHnsccSchema


class ShowUI:

    APP_ID = f'NYCU.Dentistry.ClinUI'

    def main(self):
        self.config_taskbar_icon()
        app = QApplication(sys.argv)
        model = Model(schema=VghtcOsccSchema)
        view = View(model=model)
        view.show()
        sys.exit(app.exec_())

    def config_taskbar_icon(self):
        try:
            from ctypes import windll  # only exists on Windows
            windll.shell32.SetCurrentProcessExplicitAppUserModelID(self.APP_ID)
        except ImportError as e:
            print(e, flush=True)


if __name__ == '__main__':
    ShowUI().main()

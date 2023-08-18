import os
from .template import Settings
from .cbio_ingest import cBioIngest
from .view import View
from .model import Model
from .controller import Controller


import sys
from PyQt5.QtWidgets import QApplication


def gui():
    app = QApplication(sys.argv)
    model = Model()
    view = View(model)
    controller = Controller(model, view)
    sys.exit(app.exec_())


def main(
        study_info_xlsx: str,
        clinical_data_xlsx: str,
        maf_dir: str,
        tags_json: str,
        outdir: str):

    os.makedirs(outdir, exist_ok=True)

    settings = Settings(
        workdir='workdir',
        outdir=outdir,
        threads=1,
        mock=False,
        debug=False)

    cBioIngest(settings).main(
        study_info_xlsx=study_info_xlsx,
        clinical_data_xlsx=clinical_data_xlsx,
        maf_dir=maf_dir,
        tags_json=None if tags_json.lower() == 'none' else tags_json)

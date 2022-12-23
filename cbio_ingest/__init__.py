import os
from .template import Settings
from .cbio_ingest import cBioIngest


def main(
        study_info_xlsx: str,
        patient_table_xlsx: str,
        sample_table_xlsx: str,
        maf_dir: str,
        tags_json: str,
        outdir: str):

    os.makedirs(outdir)

    settings = Settings(
        workdir='workdir',
        outdir=outdir,
        threads=1,
        mock=False,
        debug=False)

    cBioIngest(settings).main(
        study_info_xlsx=study_info_xlsx,
        patient_table_xlsx=patient_table_xlsx,
        sample_table_xlsx=sample_table_xlsx,
        maf_dir=maf_dir,
        tags_json=None if tags_json.lower() == 'none' else tags_json)

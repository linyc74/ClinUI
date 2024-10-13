import argparse
from src.model import Model
from src.schema import NycuOsccSchema


PROG = 'python test_cbio.py'
DESCRIPTION = f'Generate a study folder to be validated by a cBioPortal instance (i.e. acceptance test)'
REQUIRED = [
    {
        'keys': ['--clinical-data-table'],
        'properties': {
            'type': str,
            'required': True,
            'help': 'path to the clinical data table (CSV or XLSX format)',
        }
    },
    {
        'keys': ['--maf-dir'],
        'properties': {
            'type': str,
            'required': True,
            'help': 'path to the directory containing MAF files',
        }
    },
]
OPTIONAL = [
    {
        'keys': ['-o', '--outdir'],
        'properties': {
            'type': str,
            'required': False,
            'default': 'hnsc_nycu_2024',
            'help': 'path to the output directory (default: %(default)s)',
        }
    },
    {
        'keys': ['-h', '--help'],
        'properties': {
            'action': 'help',
            'help': 'show this help message',
        }
    },
]


class EntryPoint:

    parser: argparse.ArgumentParser

    def main(self):
        self.set_parser()
        self.add_required_arguments()
        self.add_optional_arguments()
        self.run()

    def set_parser(self):
        self.parser = argparse.ArgumentParser(
            prog=PROG,
            description=DESCRIPTION,
            add_help=False,
            formatter_class=argparse.RawTextHelpFormatter)

    def add_required_arguments(self):
        group = self.parser.add_argument_group('required arguments')
        for item in REQUIRED:
            group.add_argument(*item['keys'], **item['properties'])

    def add_optional_arguments(self):
        group = self.parser.add_argument_group('optional arguments')
        for item in OPTIONAL:
            group.add_argument(*item['keys'], **item['properties'])

    def run(self):
        args = self.parser.parse_args()

        model = Model(NycuOsccSchema)
        model.import_clinical_data_table(file=args.clinical_data_table)
        model.reprocess_table()
        model.export_cbioportal_study(
            maf_dir=args.maf_dir,
            study_info_dict={
                'type_of_cancer': 'hnsc',
                'cancer_study_identifier': 'hnsc_nycu_2024',
                'name': 'Head and Neck Squamous Cell Carcinomas (NYCU, 2024)',
                'description': 'Whole exome sequencing of 11 precancer and OSCC tumor/normal pairs',
                'groups': 'PUBLIC',
                'reference_genome': 'hg38',
            },
            tags_dict={'key': 'val'},
            outdir=args.outdir
        )


if __name__ == '__main__':
    EntryPoint().main()

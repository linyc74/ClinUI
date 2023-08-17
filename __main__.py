import argparse
import cbio_ingest


__VERSION__ = '1.1.0-alpha'


PROG = 'python cbio_ingest'
DESCRIPTION = f'Data ingestion for cBioPortal (version {__VERSION__}) by Yu-Cheng Lin (ylin@nycu.edu.tw)'
REQUIRED = [
    {
        'keys': ['-i', '--study-info-xlsx'],
        'properties': {
            'type': str,
            'required': True,
            'help': 'path to the study info Excel file',
        }
    },
    {
        'keys': ['-c', '--clinical-data-xlsx'],
        'properties': {
            'type': str,
            'required': True,
            'help': 'path to the clinical data Excel file, i.e. sample table',
        }
    },
    {
        'keys': ['-m', '--maf-dir'],
        'properties': {
            'type': str,
            'required': True,
            'help': 'path to the folder containing all maf files, with SAMPLE_ID.maf as file names',
        }
    },
]
OPTIONAL = [
    {
        'keys': ['-j', '--tags-json'],
        'properties': {
            'type': str,
            'required': False,
            'default': 'None',
            'help': 'tags json string (default: %(default)s)',
        }
    },
    {
        'keys': ['-o', '--outdir'],
        'properties': {
            'type': str,
            'required': False,
            'default': 'outdir',
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
    {
        'keys': ['--version'],
        'properties': {
            'action': 'version',
            'version': __VERSION__,
            'help': 'show version',
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
        print(f'Start cBioPortal data ingestion version {__VERSION__}\n', flush=True)
        cbio_ingest.main(
            study_info_xlsx=args.study_info_xlsx,
            clinical_data_xlsx=args.clinical_data_xlsx,
            maf_dir=args.maf_dir,
            tags_json=args.tags_json,
            outdir=args.outdir)


if __name__ == '__main__':
    EntryPoint().main()

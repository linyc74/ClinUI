# cBio Ingest

**Data ingestion for cBioPortal**

## Usage

```bash
git clone https://github.com/linyc74/cbio_ingest.git

python cbio_ingest \
  -i ./study-info.xlsx \
  -s ./sample-table.xlsx \
  -m ./maf-folder \
  -o ./hnsc_nycu_2022
```

Templates can be found in the `excel_template` folder:
- `study-info.xlsx`
- `sample-table.xlsx`

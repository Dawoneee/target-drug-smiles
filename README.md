# target-drug-smiles
Mapping Gene Targets to Drugs Using TTD Data


## Overview
`target-drug-smiles` is a Python script that processes **Therapeutic Target Database (TTD)** data to build a pipeline from **gene targets → drugs → SMILES**.  
It extracts drug information for selected genes, retrieves SMILES strings, and outputs a clean CSV for downstream analysis or modeling.

---

## Features
- Extract **gene–drug relationships** from the **TTD target file**.
- Retrieve **SMILES** strings for each drug from the **TTD drug file**.
- Merge results into a single CSV dataset.
- Flexible configuration of the **list of target genes** and file paths via command-line arguments.


---

## Requirements
- Python 3.8+
- pandas

Install dependencies:
```bash
pip install pandas
```

---

## Input Data
Place the following files in `data/TTD/`(or specify custom paths with `--target_raw_file` and `--drug_raw_file`):
- **`P1-01-TTD_target_download.txt`**: Target–drug relationship data.  
- **`P1-02-TTD_drug_download.txt`**: Drug metadata, including SMILES.

These files can be downloaded from the **Therapeutic Target Database (TTD)** website.

---

## Usage
Run the pipeline with default settings:
```bash
python extract_target_drug_ttd.py
```

Specify custom file paths and output location:
```bash
python extract_target_drug_ttd.py \
    --target_raw_file /path/to/P1-01-TTD_target_download.txt \
    --drug_raw_file /path/to/P1-02-TTD_drug_download.txt \
    --gene_list AKT1 AKT2 EGFR \
    --output /path/to/output/TTD_target_drugs.csv
```

---

## Output
- Default output file: `data/TTD_target_drugs.csv`
- CSV contains merged information for each matching target gene and drug, with SMILES strings.

Example output:
| Gene   | Target                                           | Drug_ID | Drug_name         | Approval_status | SMILES                                                      |
|--------|--------------------------------------------------|---------|-------------------|-----------------|-------------------------------------------------------------|
| AKT1   | RAC-alpha serine/threonine-protein kinase (AKT1) | D01ZAQ  | Capivasertib      | Approved        | C1CN(CCC1(C(=O)NC(CCO)C2=CC=C(C=C2)Cl)N)C3=NC=NC4=C3C=CN4   |

---

## Notes
- Only entries with both target–drug links and SMILES data are included in the output.
- SMILES strings can be used directly for cheminformatics or machine learning applications.
- Output directory is created automatically if it does not exist.

---

## Reference
- **Therapeutic Target Database (TTD)**  
  TTD provides information on therapeutic protein/nucleic acid targets, associated diseases, pathways, and corresponding drugs.  
  Website: [http://db.idrblab.net/ttd/](http://db.idrblab.net/ttd/)  
  Direct download: [http://db.idrblab.net/ttd/](http://db.idrblab.net/ttd/) 



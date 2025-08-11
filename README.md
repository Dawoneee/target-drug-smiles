# target-drug-pipeline
Mapping Gene Targets to Drugs Using TTD Data

```markdown
# target-drug-pipeline

## Overview
`target-drug-pipeline` is a Python script that processes **Therapeutic Target Database (TTD)** data to build a pipeline from **gene targets → drugs → SMILES**.  
It extracts drug information for selected genes, retrieves SMILES strings, and outputs a clean CSV for downstream analysis or modeling.

---

## Features
- Parse **TTD target file** to extract **gene–drug relationships**.
- Parse **TTD drug file** to retrieve **SMILES** for each drug.
- Merge results into a single dataset.
- Easily customize the **list of target genes**.

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
Place the following files in `data/TTD/`:
- **`P1-01-TTD_target_download.txt`**: Target–drug relationship data.  
- **`P1-02-TTD_drug_download.txt`**: Drug metadata, including SMILES.

These files can be downloaded from the **Therapeutic Target Database (TTD)** website (registration may be required).

---

## Usage
Run the pipeline:
```bash
python extract_ttd_mapping.py
```

Modify `search_genes` in the script to set your own target genes:
```python
search_genes = ["AKT1", "AKT2", "AURKB", "CTSK", "EGFR", "HDAC1", "MTOR", "PIK3CA"]
```

---

## Output
- **`data/TTD_target_drugs.csv`** – Final merged dataset.

Example output:
| Gene   | Target                                        | Drug_ID | Drug_name         | Approval_status | SMILES                                                      |
|--------|-----------------------------------------------|---------|-------------------|-----------------|-------------------------------------------------------------|
| AKT2   | RAC-beta serine/threonine-protein kinase (AKT2) | D0M9QJ  | PHT-427           | Investigative   | C1CN(CCC1(C(=O)NC(CCO)C2=CC=C(C=C2)Cl)N)C3=NC=NC4=C3C=CN4    |

---

## Notes
- The output includes only entries with both target–drug links and SMILES data.
- SMILES strings can be used directly for cheminformatics or machine learning applications.

---

## Reference
- **Therapeutic Target Database (TTD)**  
  TTD provides information on therapeutic protein/nucleic acid targets, associated diseases, pathways, and corresponding drugs.  
  Website: [http://db.idrblab.net/ttd/](http://db.idrblab.net/ttd/)  
  Direct download: [http://db.idrblab.net/ttd/](http://db.idrblab.net/ttd/) (registration may be required)
```


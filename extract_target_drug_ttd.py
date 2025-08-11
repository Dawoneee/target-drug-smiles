import os
import pandas as pd
from collections import defaultdict
import argparse


# 1) Parse target file to extract gene → drug mappings
def extract_gene_to_drug_mapping(target_raw_file, search_genes):
    """
    Input format example (target_raw_file.txt):
    T94621	TARGETID	T94621
    T94621	FORMERID	TTDI00101
    T94621	UNIPROID	AKT2_HUMAN
    T94621	TARGNAME	RAC-beta serine/threonine-protein kinase (AKT2)
    T94621	GENENAME	AKT2
    T94621	DRUGINFO	D0M9QJ	PHT-427	Investigative
    T94621	DRUGINFO	D05APZ	Akt inhibitor VIII	Investigative
    T94621	DRUGINFO	D0L2WP	PMID20005102C1	Investigative
    """
    results = []

    target_blocks = defaultdict(list)
    gene_to_target_ids = defaultdict(list)   # gene_name -> target_id

    with open(target_raw_file, "r", encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) < 3: 
                continue

            targetid, key, *values = parts
            target_blocks[targetid].append((key, values))

            if key == "GENENAME":
                gene_name = values[0]
                gene_to_target_ids[gene_name].append(targetid)

    for gene in search_genes:
        target_ids = gene_to_target_ids.get(gene, [])
        for target_id in target_ids:
            block = target_blocks[target_id]

            # Get target name
            target_name = None
            for key, values in block:
                if key == "TARGNAME":
                    target_name = values[0]
                    break

            # Get drug info
            for key, values in block:
                if key == "DRUGINFO" and len(values) >= 3:
                    drug_id, drug_name, approval = values[:3]
                    results.append({
                        'Gene': gene,
                        'Target': target_name,
                        'Drug_ID': drug_id,
                        'Drug_name': drug_name,
                        'Approval_status': approval
                    })
                    
    return results

 
# 2) Parse drug file to get drug_id → SMILES mapping
def build_drug_to_smiles_dict(drug_raw_file):
    """
    Input format example (drug_raw_file.txt):
    D01ZAQ	DRUG__ID	D01ZAQ
    D01ZAQ	TRADNAME	Truqap
    D01ZAQ	DRUGCOMP	AstraZeneca
    D01ZAQ	DRUGTYPE	Small molecular drug
    D01ZAQ	DRUGINCH	1S/C21H25ClN6O2/c22-15-3-1-14(2-4-15)17(6-12-29)27-20(30)21(23)7-10-28(11-8-21)19-16-5-9-24-18(16)25-13-26-19/h1-5,9,13,17,29H,6-8,10-12,23H2,(H,27,30)(H,24,25,26)/t17-/m0/s1
    D01ZAQ	DRUGINKE	JDUBGYFRJFOXQC-KRWDZBQOSA-N
    D01ZAQ	DRUGSMIL	C1CN(CCC1(C(=O)NC(CCO)C2=CC=C(C=C2)Cl)N)C3=NC=NC4=C3C=CN4
    D01ZAQ	HIGHSTAT	Approved
    """

    drug_smiles_dict = {}
    current_drug_id = None

    with open(drug_raw_file, "r", encoding="utf-8") as drug_f:
        for line in drug_f:
            parts = line.strip().split("\t")
            if len(parts) < 3:
                continue

            drugid, key, *values = parts

            if key == "DRUG__ID":
                current_drug_id = values[0]

            elif key == "DRUGSMIL" and current_drug_id:
                drug_smiles_dict[current_drug_id] = values[0]
                
    return drug_smiles_dict


# 3) Merge DRUG and SMILES info and save to CSV
def merge_target_drug_smiles(gene_to_drug_map, drug_smiles_dict, result_csv):
    
    df = pd.DataFrame(gene_to_drug_map)
    df["SMILES"] = df["Drug_ID"].map(drug_smiles_dict)

    print(df)

    df.to_csv(result_csv, index=False)
    
    
def parse_args():
    parser = argparse.ArgumentParser(description="Extract Drugs of Targets")
    
    root_path = os.path.dirname(os.path.abspath(__file__))
    
    parser.add_argument("--target_raw_file", type=str, default=os.path.join(root_path, "data", "TTD", "P1-01-TTD_target_download.txt"), 
                        help="Path to TTD target info TXT file.")
    parser.add_argument("--drug_raw_file", type=str, default=os.path.join(root_path, "data", "TTD", "P1-02-TTD_drug_download.txt"),
                        help="Path to TTD drug info TXT file.")
    
    parser.add_argument("--gene_list", nargs="+", default=["AKT1", "AKT2", "AURKB", "CTSK", "EGFR", "HDAC1", "MTOR", "PIK3CA"],
                        help="List of target genes to search (space-separated).")
    
    parser.add_argument("--output", type=str, default=os.path.join(root_path, "data", "TTD_target_drugs.csv"))
    
    return parser.parse_args()


if __name__=="__main__":
    args = parse_args()

    # 1) Parse target file to extract gene → drug mappings
    gene_to_drug_map = extract_gene_to_drug_mapping(args.target_raw_file, args.gene_list)
    
    # 2) Parse drug file to get drug_id → SMILES mapping
    drug_smiles_dict = build_drug_to_smiles_dict(args.drug_raw_file)
    
    # 3) Merge DRUG and SMILES info and save to CSV
    merge_target_drug_smiles(gene_to_drug_map, drug_smiles_dict, args.output)


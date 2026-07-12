import os
import pandas as pd
import re
from Bio import SeqIO

# ==========================================
# 1. LOAD FASTA (ROBUST)
# ==========================================
def load_fasta(fasta_file):
    sequences = {}
    
    for record in SeqIO.parse(fasta_file, "fasta"):
        header = record.description
        
        # UniProt format: sp|P04637|TP53_HUMAN
        if "|" in header:
            parts = header.split("|")
            if len(parts) > 1:
                uniprot_id = parts[1]
                sequences[uniprot_id] = str(record.seq)
        
        # fallback
        sequences[record.id] = str(record.seq)
    
    return sequences


# ==========================================
# 2. GENE → UNIPROT MAPPING (YOU MUST EDIT)
# ==========================================
gene_to_uniprot = {
    "TP53": "P04637",
    "EGFR": "P00533",
    "ERBB2": "P04626",
    "BRAF": "P15056",
    "ALK": "Q9UM73",
    "ATM": "Q13315",
    "ARID1A": "O14497",
    "CDKN2A": "P42771"
    # add remaining genes
}


# ==========================================
# 3. MUTATION PARSER
# ==========================================
def parse_mutation(mutation):
    match = re.match(r"p\.([A-Z])(\d+)([A-Z])", str(mutation))
    if not match:
        return None
    original, pos, new = match.groups()
    return original, int(pos), new


# ==========================================
# 4. APPLY MUTATION
# ==========================================
def apply_mutation(sequence, mutation):
    parsed = parse_mutation(mutation)
    if not parsed:
        return None, "invalid_format"
    
    original, pos, new = parsed
    pos = pos - 1
    
    if pos >= len(sequence):
        return None, "out_of_bounds"
    
    if sequence[pos] != original:
        return None, "mismatch"
    
    mutated = sequence[:pos] + new + sequence[pos+1:]
    return mutated, "success"


# ==========================================
# 5. PROCESS FOLDER
# ==========================================
def process_folder(folder_path, fasta_path, output_csv):
    
    sequences = load_fasta(fasta_path)
    
    dataset = []
    normal_sequences = set()
    
    stats = {
        "total": 0,
        "success": 0,
        "invalid_format": 0,
        "out_of_bounds": 0,
        "mismatch": 0,
        "missing_gene": 0
    }
    
    for file in os.listdir(folder_path):
        
        if not file.endswith(".csv"):
            continue
        
        # Extract gene from filename
        gene = file.split("_")[0]   # TP53_lung_carcinoma.csv → TP53
        
        if gene not in gene_to_uniprot:
            print(f"[WARNING] Gene mapping missing for {gene}")
            continue
        
        print(f"Processing {gene}...")
        
        df = pd.read_csv(os.path.join(folder_path, file))
        
        # Filter mutations
        df = df[df["Type"].str.contains("Missense", na=False)]
        df = df[~df["AA Mutation"].astype(str).str.contains("=")]
        df = df[df["AA Mutation"].notna()]
        
        uniprot_id = gene_to_uniprot[gene]
        
        if uniprot_id not in sequences:
            print(f"[ERROR] Sequence not found for {gene}")
            stats["missing_gene"] += len(df)
            continue
        
        seq = sequences[uniprot_id]
        
        for _, row in df.iterrows():
            stats["total"] += 1
            
            mutation = row["AA Mutation"]
            
            mutated, status = apply_mutation(seq, mutation)
            
            if status != "success":
                stats[status] += 1
                continue
            
            stats["success"] += 1
            
            # Cancer sequence
            dataset.append({
                "sequence": mutated,
                "label": 1,
                "gene": gene,
                "mutation": mutation,
                "cds_mutation": row.get("CDS Mutation", ""),
                "mutation_id": row.get("Legacy Mutation ID", ""),
                "type": row.get("Type", "")
            })
            
            # Add normal sequence once
            if seq not in normal_sequences:
                dataset.append({
                    "sequence": seq,
                    "label": 0,
                    "gene": gene,
                    "mutation": "WT",
                    "cds_mutation": "",
                    "mutation_id": "",
                    "type": "wildtype"
                })
                normal_sequences.add(seq)
    
    # Save
    out_df = pd.DataFrame(dataset)
    out_df.to_csv(output_csv, index=False)
    
    print("\n===== SUMMARY =====")
    for k, v in stats.items():
        print(f"{k}: {v}")
    
    print("\nFinal dataset size:", len(out_df))


# ==========================================
# 6. RUN
# ==========================================
process_folder(
    folder_path="cosmic_mutations",           # your CSV folder
    fasta_path="final_all_sequences_fixed.fasta",     # your FASTA file
    output_csv="final_dataset.csv"
)
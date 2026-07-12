import pandas as pd
from tqdm import tqdm

# =========================
# LOAD DATASET
# =========================
file_path = "final_merged_dataset.csv"

df = pd.read_csv(file_path)

sequence_column = "sequence"

# Clean sequences
df[sequence_column] = df[sequence_column].astype(str).str.strip()

# =========================
# FAST DUPLICATE REMOVAL
# =========================
seen = set()

unique_rows = []

for _, row in tqdm(df.iterrows(), total=len(df), desc="Removing Duplicates"):

    seq = row[sequence_column]

    # If sequence not seen before
    if seq not in seen:

        seen.add(seq)

        unique_rows.append(row)

# =========================
# CREATE CLEAN DATAFRAME
# =========================
cleaned_df = pd.DataFrame(unique_rows)

cleaned_df = cleaned_df.reset_index(drop=True)

# =========================
# SAVE OUTPUT
# =========================
output_file = "redundancy_removed_dataset.csv"

cleaned_df.to_csv(output_file, index=False)

# =========================
# SUMMARY
# =========================
print("\n===================================")
print("Duplicate removal completed")
print("===================================")
print(f"Original sequences : {len(df)}")
print(f"Removed sequences  : {len(df) - len(cleaned_df)}")
print(f"Remaining sequences: {len(cleaned_df)}")
print(f"Saved file         : {output_file}")
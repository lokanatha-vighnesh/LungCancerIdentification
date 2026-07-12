import pandas as pd
from Bio.Align import PairwiseAligner
from tqdm import tqdm

# =========================
# LOAD DATASET
# =========================
file_path = "final_merged_dataset.csv"

df = pd.read_csv(file_path)

# Sequence column name
sequence_column = "sequence"

# Clean sequences
df[sequence_column] = df[sequence_column].astype(str).str.strip()

# =========================
# GLOBAL ALIGNMENT SETUP
# =========================
aligner = PairwiseAligner()

aligner.mode = "global"

# Scoring scheme
aligner.match_score = 1
aligner.mismatch_score = 0
aligner.open_gap_score = -1
aligner.extend_gap_score = -0.5

# =========================
# SIMILARITY FUNCTION
# =========================
def calculate_similarity(seq1, seq2):

    score = aligner.score(seq1, seq2)

    max_score = max(len(seq1), len(seq2))

    similarity = (score / max_score) * 100

    return similarity

# =========================
# REMOVE DUPLICATES
# =========================
to_remove = set()

total_sequences = len(df)

# Progress bar
for i in tqdm(range(total_sequences), desc="Checking Sequences"):

    # Skip already removed sequence
    if i in to_remove:
        continue

    seq1 = df.iloc[i][sequence_column]

    # Compare with every other sequence
    for j in range(i + 1, total_sequences):

        if j in to_remove:
            continue

        seq2 = df.iloc[j][sequence_column]

        similarity = calculate_similarity(seq1, seq2)

        # Remove if identical
        if similarity == 100.0:

            to_remove.add(j)

# =========================
# CREATE CLEAN DATASET
# =========================
cleaned_df = df.drop(index=list(to_remove))

# Reset index
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
print(f"Removed sequences  : {len(to_remove)}")
print(f"Remaining sequences: {len(cleaned_df)}")
print(f"Saved file         : {output_file}")
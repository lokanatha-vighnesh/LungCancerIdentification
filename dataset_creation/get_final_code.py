import pandas as pd

# ==========================================
# 1. LOAD FILES
# ==========================================
cancer_df = pd.read_csv("final_dataset.csv")
non_cancer_df = pd.read_excel(r"C:\Users\lokan\Document\Introduction to Biological Systems\ENDSEM PROJECT\non_cancer_sequences.xlsx")


# ==========================================
# 2. STANDARDIZE COLUMN NAMES
# ==========================================

# Ensure sequence column exists
cancer_df.rename(columns={"Sequence": "sequence"}, inplace=True)
non_cancer_df.rename(columns={"Sequence": "sequence"}, inplace=True)

# If non-cancer file has no label → add it
if "label" not in non_cancer_df.columns:
    non_cancer_df["label"] = 0

# Force cancer label = 1 (safety)
cancer_df["label"] = 1


# ==========================================
# 3. ALIGN COLUMNS
# ==========================================

# Get all columns from cancer dataset
required_cols = cancer_df.columns

# Add missing columns to non-cancer
for col in required_cols:
    if col not in non_cancer_df.columns:
        non_cancer_df[col] = ""

# Reorder columns
non_cancer_df = non_cancer_df[required_cols]


# ==========================================
# 4. REMOVE DUPLICATES (IMPORTANT)
# ==========================================

# Combine first
combined_df = pd.concat([cancer_df, non_cancer_df], ignore_index=True)

# Drop duplicate sequences (keep cancer if conflict)
combined_df = combined_df.sort_values(by="label", ascending=False)
combined_df = combined_df.drop_duplicates(subset=["sequence"], keep="first")


# ==========================================
# 5. CLEAN DATA
# ==========================================

# Remove empty sequences
combined_df = combined_df[combined_df["sequence"].notna()]
combined_df = combined_df[combined_df["sequence"] != ""]

# Reset index
combined_df = combined_df.reset_index(drop=True)


# ==========================================
# 6. SAVE FINAL DATASET
# ==========================================

combined_df.to_csv("final_merged_dataset.csv", index=False)


# ==========================================
# 7. SUMMARY
# ==========================================

print("Total samples:", len(combined_df))
print("Cancer samples:", (combined_df["label"] == 1).sum())
print("Non-cancer samples:", (combined_df["label"] == 0).sum())
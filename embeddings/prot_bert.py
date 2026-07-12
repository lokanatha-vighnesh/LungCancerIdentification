# ==========================================================
# PROTEIN BERT EMBEDDINGS (FULL WORKING VERSION)
# Compatible with Windows + Python 3.10 / 3.11 preferred
# Uses ProtBERT from Rostlab
# Input File : non_redundant_dataset.xlsx
# Output File: protbert_features.csv
# ==========================================================

# Install first:
# pip install torch transformers pandas openpyxl tqdm sentencepiece

import os
import re
import pandas as pd
import numpy as np
import torch
from tqdm import tqdm
from transformers import BertTokenizer, BertModel

# ==========================================================
# SETTINGS
# ==========================================================
INPUT_FILE = r"C:\Users\lokan\Document\Introduction to Biological Systems\ENDSEM PROJECT\mutations verification\redundancy_removed_dataset.csv"
OUTPUT_FILE = "protbert_features.csv"
MODEL_NAME = "Rostlab/prot_bert"

# ==========================================================
# LOAD DATA
# ==========================================================
df = pd.read_csv(INPUT_FILE)

print("Dataset Loaded Successfully")
print("Shape :", df.shape)
print(df.head())

# Required columns:
# Sequence
# Optional: Label / Gene

if "Sequence" not in df.columns:
    raise Exception("Column 'Sequence' not found in Excel file")

# ==========================================================
# DEVICE
# ==========================================================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using Device:", device)

# ==========================================================
# LOAD TOKENIZER + MODEL
# (Slow tokenizer = stable on Windows)
# ==========================================================
print("Loading ProtBERT model...")

tokenizer = BertTokenizer.from_pretrained(
    MODEL_NAME,
    do_lower_case=False
)

model = BertModel.from_pretrained(MODEL_NAME)
model = model.to(device)
model.eval()

print("Model Loaded Successfully")

# ==========================================================
# CLEAN SEQUENCE
# Replace rare amino acids with X
# ProtBERT standard preprocessing
# ==========================================================
def clean_sequence(seq):
    seq = str(seq).upper()
    seq = re.sub(r"[UZOB]", "X", seq)
    seq = " ".join(list(seq))
    return seq

# ==========================================================
# EMBEDDING FUNCTION
# Mean pooling of token embeddings
# ==========================================================
def get_embedding(sequence):

    sequence = clean_sequence(sequence)

    encoded = tokenizer(
        sequence,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=1024
    )

    input_ids = encoded["input_ids"].to(device)
    attention_mask = encoded["attention_mask"].to(device)

    with torch.no_grad():
        outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask
        )

    token_embeddings = outputs.last_hidden_state

    # Mean pooling
    embedding = token_embeddings.mean(dim=1).squeeze().cpu().numpy()

    return embedding

# ==========================================================
# GENERATE FEATURES
# ==========================================================
print("Generating embeddings...")

all_features = []

for seq in tqdm(df["Sequence"]):
    emb = get_embedding(seq)
    all_features.append(emb)

all_features = np.array(all_features)

print("Embedding Shape:", all_features.shape)

# ==========================================================
# SAVE CSV
# ==========================================================
feature_df = pd.DataFrame(all_features)

# add optional metadata
if "Label" in df.columns:
    feature_df["Label"] = df["Label"]

if "Gene" in df.columns:
    feature_df["Gene"] = df["Gene"]

feature_df.to_csv(OUTPUT_FILE, index=False)

print("Saved Successfully:", OUTPUT_FILE)
print("Done.")
# ==========================================================
# ROBERTA EMBEDDINGS WITH LABEL RETENTION
#
# Input : redundancy_removed_dataset.csv
# Output: roberta_features.csv
# ==========================================================

# INSTALL:
# pip install torch transformers pandas tqdm openpyxl

import pandas as pd
import numpy as np
import torch
from tqdm import tqdm
from transformers import RobertaTokenizer, RobertaModel

# ==========================================================
# SETTINGS
# ==========================================================
INPUT_FILE = r"C:\Users\lokan\Document\Introduction to Biological Systems\ENDSEM PROJECT\mutations verification\redundancy_removed_dataset.csv"

OUTPUT_FILE = "roberta_features.csv"

MODEL_NAME = "roberta-base"

# ==========================================================
# LOAD DATASET
# ==========================================================
df = pd.read_csv(INPUT_FILE)

print("Dataset Loaded Successfully")
print("Shape :", df.shape)

# Required columns
if "sequence" not in df.columns:
    raise Exception("Column 'Sequence' not found")

if "label" not in df.columns:
    raise Exception("Column 'Label' not found")

# ==========================================================
# DEVICE
# ==========================================================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print("Using Device:", device)

# ==========================================================
# LOAD MODEL
# ==========================================================
print("Loading RoBERTa Model...")

tokenizer = RobertaTokenizer.from_pretrained(MODEL_NAME)

model = RobertaModel.from_pretrained(MODEL_NAME)

model = model.to(device)

model.eval()

print("RoBERTa Loaded Successfully")

# ==========================================================
# CLEAN SEQUENCE
# ==========================================================
def clean_sequence(seq):

    seq = str(seq).upper()

    seq = " ".join(list(seq))

    return seq

# ==========================================================
# EMBEDDING FUNCTION
# ==========================================================
def get_embedding(sequence):

    sequence = clean_sequence(sequence)

    encoded = tokenizer(
        sequence,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=512
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
    embedding = token_embeddings.mean(dim=1)

    embedding = embedding.squeeze().cpu().numpy()

    return embedding

# ==========================================================
# GENERATE EMBEDDINGS
# ==========================================================
print("Generating RoBERTa embeddings...")

all_features = []

for seq in tqdm(df["sequence"], desc="Processing"):

    emb = get_embedding(seq)

    all_features.append(emb)

all_features = np.array(all_features)

print("Embedding Shape:", all_features.shape)

# ==========================================================
# CREATE FEATURE DATAFRAME
# ==========================================================
feature_df = pd.DataFrame(all_features)

# Retain Label column
feature_df["Label"] = df["label"].values

# Retain optional metadata
if "Gene" in df.columns:
    feature_df["Gene"] = df["gene"].values

# ==========================================================
# SAVE CSV
# ==========================================================
feature_df.to_csv(OUTPUT_FILE, index=False)

print("\n===================================")
print("RoBERTa Embeddings Generated")
print("===================================")
print("Saved File:", OUTPUT_FILE)
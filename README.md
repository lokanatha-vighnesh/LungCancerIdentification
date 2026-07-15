# Machine Learning-Based Lung Cancer Identification Using Protein Sequences

## Abstract
Lung cancer ranks among the top causes of cancer deaths globally, highlighting the critical importance of early and accurate detection. This project presents a machine learning tool to detect lung cancer based on protein sequences. Protein sequences with mutations related to cancer were gathered from the COSMIC database, and non-cancer protein sequences were retrieved from UniProt. Twenty genes strongly linked to lung cancer mutations were chosen for analysis.

Mutated protein sequences were created by adding mutation data into the original base sequences. To obtain meaningful numerical representations from protein sequences, the BERT, ProtBERT, and RoBERTa embedding methods were applied. Several machine learning models including Support Vector Machine (SVM), DecisionTree, RandomForest, AdaBoost, GaussianNaiveBayes, MLPClassifier, XGBoost, and CatBoost were trained using the extracted embeddings. These models help us understand which sequence is cancer and which is non-cancer.

---

## Introduction
Lung cancer is a very serious and widespread issue worldwide. Presently, traditional diagnostic methods are time-intensive, expensive, and largely depend on clinical expertise. As bioinformatics and artificial intelligence have grown, machine learning techniques have become very useful in disease prediction and bio-sequence analysis.

Proteins play a core role in cell functions, and mutations in those proteins are very much linked to cancer growth. Detection of these mutations offers opportunities for early diagnosis and better treatment planning. In recent years, transformer-based language models such as BERT and ProtBERT have achieved excellent results in feature extraction from biological sequences.

This project's goal is to develop a machine learning-based system capable of identifying lung cancer in protein sequences. We obtained cancer-related mutation sequences from the COSMIC database and healthy protein sequences from UniProt. We applied embedding techniques to the collected sequences and ran them through multiple machine learning algorithms to classify sequences as cancerous or non-cancerous. This system combines bioinformatics, natural language processing techniques, and machine learning models to achieve high accuracy in lung cancer identification.

---

## Literature Survey

| Paper Title | Lung Cancer Classification Models Using Discriminant Information of Mutated Genes in Protein Amino Acids Sequences |
|-------------|---------------------------------------------------------------------------------------------------------------------|
| **Authors** | Mohsin Sattar and Abdul Majid |
| **Summary** | The authors proposed a machine learning-based lung cancer classification framework using discriminant information extracted from mutated genes present in protein amino acid sequences. The study focused on highly mutated genes associated with lung cancer, including TP53, EGFR, KMT2D, ATM, DICER1, and BRCA2. The researchers analysed amino acid composition and mutation patterns in protein sequences to identify features related to lung cancer progression. Different machine learning techniques were used to classify cancerous and non-cancerous sequences. The study demonstrated that discriminant information derived from mutated genes significantly improves classification performance and supports early lung cancer diagnosis. The paper concluded that protein sequence analysis combined with machine learning can serve as an effective computational approach for cancer prediction and prognosis. |

---

## Materials and Methods

### Dataset Collection
The dataset for this project was collected using two major biological databases:
- **COSMIC** for cancer-related mutation data
- **UniProt** for non-cancer protein sequences

Twenty genes highly prone to lung cancer mutations were selected. Mutation files corresponding to each gene were downloaded and processed. Base protein sequences were obtained from UniProt.

**The final dataset contained:**
- Total sequences: **2,285**
- Cancer sequences: **1,467**
- Non-cancer sequences: **818**

### Sequence Extraction
The mutation data obtained from COSMIC was applied to the base sequences to generate mutated sequences. These mutated sequences were labelled as cancer sequences, while non-cancer sequences were directly collected from UniProt and labelled as non-cancer sequences.

After preprocessing, both cancer and non-cancer sequences were combined to create the final dataset used for training and testing.

### Embedding Techniques
Protein sequences cannot be directly processed by machine learning models. Therefore, embedding techniques were implemented to convert sequences into numerical feature vectors.

**The following embedding models were used:**
- BERT
- ProtBERT
- RoBERTa

**Feature extraction details:**
| Embedding Model | Feature Dimension |
|-----------------|-------------------|
| BERT | 768 features |
| RoBERTa | 768 features |
| ProtBERT | 1024 features |

These embeddings captured contextual and biological information from protein sequences and were used as input for machine learning models.

### Machine Learning Models
Several machine learning algorithms were implemented and evaluated on generated embeddings:
- Support Vector Machine (SVM)
- Decision Tree
- Random Forest
- AdaBoost
- Gaussian Naive Bayes
- MLPClassifier
- XGBoost
- CatBoost

The models were trained to classify protein sequences into cancerous and non-cancerous categories.

### Workflow of the Proposed System

```
┌─────────────────────────────────────────────────────────────────────┐
│                     PROPOSED SYSTEM WORKFLOW                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────┐                                       │
│  │ 1. Selection of lung    │                                       │
│  │    cancer-related genes │                                       │
│  └───────────┬─────────────┘                                       │
│              ▼                                                      │
│  ┌─────────────────────────┐                                       │
│  │ 2. Collection of        │                                       │
│  │    mutation data from   │                                       │
│  │    COSMIC               │                                       │
│  └───────────┬─────────────┘                                       │
│              ▼                                                      │
│  ┌─────────────────────────┐                                       │
│  │ 3. Retrieval of base    │                                       │
│  │    protein sequences    │                                       │
│  │    from UniProt         │                                       │
│  └───────────┬─────────────┘                                       │
│              ▼                                                      │
│  ┌─────────────────────────┐                                       │
│  │ 4. Generation of        │                                       │
│  │    mutated protein      │                                       │
│  │    sequences            │                                       │
│  └───────────┬─────────────┘                                       │
│              ▼                                                      │
│  ┌─────────────────────────┐                                       │
│  │ 5. Dataset              │                                       │
│  │    preprocessing and    │                                       │
│  │    labeling             │                                       │
│  └───────────┬─────────────┘                                       │
│              ▼                                                      │
│  ┌─────────────────────────┐                                       │
│  │ 6. Embedding generation │                                       │
│  │    using BERT, ProtBERT,│                                       │
│  │    and RoBERTa          │                                       │
│  └───────────┬─────────────┘                                       │
│              ▼                                                      │
│  ┌─────────────────────────┐                                       │
│  │ 7. Training machine     │                                       │
│  │    learning models      │                                       │
│  └───────────┬─────────────┘                                       │
│              ▼                                                      │
│  ┌─────────────────────────┐                                       │
│  │ 8. Performance          │                                       │
│  │    evaluation using     │                                       │
│  │    classification       │                                       │
│  │    metrics              │                                       │
│  └─────────────────────────┘                                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Architecture of the Model

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              SYSTEM ARCHITECTURE                                    │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                       INPUT LAYER                                            │   │
│  │            Protein sequences collected from COSMIC and UniProt              │   │
│  └──────────────────────────────────┬──────────────────────────────────────────┘   │
│                                     ▼                                              │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                     PREPROCESSING LAYER                                     │   │
│  │              Mutation implementation and sequence labeling                  │   │
│  └──────────────────────────────────┬──────────────────────────────────────────┘   │
│                                     ▼                                              │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                       EMBEDDING LAYER                                       │   │
│  │     Conversion of protein sequences into numerical vectors using           │   │
│  │        transformer-based embedding models (BERT, ProtBERT, RoBERTa)        │   │
│  └──────────────────────────────────┬──────────────────────────────────────────┘   │
│                                     ▼                                              │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                     CLASSIFICATION LAYER                                    │   │
│  │              Machine learning classifiers trained using                    │   │
│  │                      extracted embeddings                                   │   │
│  └──────────────────────────────────┬──────────────────────────────────────────┘   │
│                                     ▼                                              │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                        OUTPUT LAYER                                         │   │
│  │       Prediction of whether a protein sequence is cancerous or             │   │
│  │                         non-cancerous                                       │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Results and Discussion

The proposed system was evaluated using multiple machine learning models and embedding techniques. Transformer-based embeddings demonstrated excellent capability in including important biological information from protein sequences.

**Key Findings:**
- **Highest accuracy achieved: 99.78%**
- Use of state-of-the-art embeddings and machine learning classifiers significantly improved prediction performance
- Confusion matrix analysis showed excellent classification with minimal misclassification
- Models like SVM, XGBoost, and CatBoost performed exceptionally well in terms of prediction accuracy compared to traditional methods

**Compared with existing studies, the proposed system achieved superior performance due to:**
- Use of transformer-based embeddings
- Large combined dataset
- Inclusion of mutated protein sequences
- Evaluation using multiple classifiers

The results indicate that protein sequence-based machine learning systems can provide reliable support for lung cancer identification and early diagnosis.

---

## Conclusion

This project presented a machine learning-based approach for lung cancer identification using protein sequences. Cancer-related mutation data were collected from the COSMIC database, while non-cancer sequences were obtained from UniProt. Protein sequence embeddings were generated using BERT, ProtBERT, and RoBERTa models, and multiple machine learning classifiers were trained for prediction.

The experimental results demonstrated excellent classification performance, with the highest accuracy reaching **99.78%**. The study confirms that transformer-based embeddings combined with machine learning techniques are highly effective for analysing protein sequences and identifying lung cancer-related mutations.

The proposed system can contribute to computational cancer diagnosis and may assist researchers and healthcare professionals in early lung cancer detection.

### Future Work
- Expanding the dataset
- Implementing deep learning architectures
- Integrating explainable AI techniques such as LIME and SHAP for better model interpretability

---

## References

1. Sattar, M., & Majid, A. (2022). Lung Cancer Classification Models Using Discriminant Information of Mutated Genes in Protein Amino Acids Sequences.
2. COSMIC (Catalogue of Somatic Mutations in Cancer) - [https://cancer.sanger.ac.uk/cosmic](https://cancer.sanger.ac.uk/cosmic)
3. UniProt - [https://www.uniprot.org](https://www.uniprot.org)
4. Devlin, J., et al. (2018). BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding.
5. Elnaggar, A., et al. (2020). ProtTrans: Towards Cracking the Language of Life's Code Through Self-Supervised Learning.

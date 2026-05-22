# Partition Names Project

This repository contains the reproducible workflow used for cleaning, processing, and analyzing the Chandigarh voter-roll names dataset.

The original notebook used during experimentation is available in:

```text
notebooks/partition_names_project.ipynb
```

To improve reproducibility and reduce rerun time, the workflow was later separated into modular Python scripts.

---

# Repository Structure

```text
data/
├── raw/                      # Original input dataset
├── interim/                  # Output after Step 3 canonicalization

notebooks/
└── partition_names_project.ipynb

outputs/
└── final_df.csv              # Final processed dataset

scripts/
├── steps_1_to_3.py           # Cleaning + transliteration + canonicalization
├── steps_4_onward.py         # Religion inference + downstream analysis
├── pipeline_support.py       # Shared helper functions
└── reproduce.py              # Wrapper script

third_party/
└── its_all_in_the_name_light_repo/
```

---

# Step-by-Step Reproduction Guide

## Step 1 — Clone the Repository

```powershell
git clone https://github.com/Samnannn/data_unicoding.git
cd data_unicoding
```

---

## Step 2 — Create Python Environment

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

---

## Step 3 — Download and Place the Raw Dataset

Download the raw dataset from:

```text
https://drive.google.com/file/d/1JPOz0cZd5xTkmzNYdPc3SRjvs7qyJcqP/view?usp=sharing
```

Place the downloaded file inside:

```text
data/raw/
```

Expected structure:

```text
data/raw/chandigarh_all.csv
```

---

## Step 4 — Download and Place the AI Bharat Model

Download the AI Bharat religion inference model from:

```text
https://drive.google.com/drive/folders/1xomkvrSwGj40X94IpUaoC9-E5euBJYJf?usp=sharing
```

Place the extracted model files inside:

```text
third_party/its_all_in_the_name_light_repo/
```

---

## Step 5 — Important Dependency Setup

The AI Bharat religion inference model was trained using an older version of scikit-learn.

Before running Step 4 onward inside Jupyter or Google Colab, downgrade scikit-learn:

```python
!pip uninstall -y scikit-learn
!pip install scikit-learn==1.3.2
```

---

# Running the Pipeline

## Option A — Run Full Pipeline From Raw Dataset

### Run Steps 1–3

This stage performs:

- Unicode cleaning
- OCR artifact correction
- Transliteration
- Canonicalization

Run:

```powershell
python scripts\steps_1_to_3.py
```

Output generated:

```text
data/interim/cleaned_2.csv
```

---

### Run Steps 4 Onward

This stage performs:

- Religion inference
- Feature generation
- Aggregations
- Final dataset generation

Run:

```powershell
python scripts\steps_4_onward.py --interim data\interim\cleaned_2.csv --output outputs\final_df.csv
```

Final output:

```text
outputs/final_df.csv
```

---

## Option B — Skip Canonicalization Using Precomputed Interim File

Canonicalization is the slowest stage of the workflow.  
To avoid recomputing it, a pre-generated interim dataset is also shared.

Download the interim dataset from:

```text
https://drive.google.com/file/d/1akGSo8DxwaZqEH2Ko9DEieeIxk2Lpt8X/view?usp=sharing
```

Place it inside:

```text
data/interim/
```

Expected structure:

```text
data/interim/cleaned_2.csv
```

Then directly run:

```powershell
python scripts\steps_4_onward.py --interim data\interim\cleaned_2.csv --output outputs\final_df.csv
```

---

# Final Output Dataset

Final processed dataset:

```text
https://drive.google.com/file/d/1-Nt5G0czeLe_f5sIILDsVRXMQPXvktRZ/view?usp=sharing
```

---

# Google Colab Notebook

If there is any difficulty reproducing locally, the Google Colab notebook can also be used after adjusting file paths.

```text
https://drive.google.com/file/d/1IHLmQAi038dsW0CY0H_pewcOZtIPCUCv/view?usp=sharing
```

---

# Notes

- Canonicalization is currently the most computationally expensive stage of the workflow.
- The interim dataset allows downstream stages to be rerun without recomputing expensive preprocessing steps.
- Large datasets and generated outputs are intentionally excluded from GitHub because of file size constraints.
- Shared helper functions are stored inside `pipeline_support.py`.

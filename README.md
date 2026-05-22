# Partition Names Project

This repository contains the reproducible workflow used for cleaning, processing, and analyzing the Chandigarh voter-roll names dataset.

The original analysis and experimentation notebook is available in:

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

# Workflow Overview

The pipeline was divided into two stages because canonicalization was the most computationally expensive part of the workflow.

## Steps 1–3

This stage performs:

- Unicode cleaning
- OCR artifact correction
- Transliteration
- Canonicalization

Run:

```powershell
python scripts\steps_1_to_3.py
```

Output:

```text
data/interim/cleaned_2.csv
```

---

## Steps 4 Onward

This stage starts from the canonicalized interim dataset and performs:

- Religion inference
- Feature generation
- Aggregations
- Question outputs
- Final dataset generation

Run:

```powershell
python scripts\steps_4_onward.py --interim data\interim\cleaned_2.csv --output outputs\final_df.csv
```

Output:

```text
outputs/final_df.csv
```

---

# Environment Setup

Create a fresh Python environment:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

---

# Important Dependency Note

The AI Bharat religion inference model was trained using an older version of scikit-learn.

Before running religion inference inside Jupyter or Google Colab, downgrade scikit-learn:

```python
!pip uninstall -y scikit-learn
!pip install scikit-learn==1.3.2
```

---

# Input Dataset

Place the raw dataset inside:

```text
data/raw/chandigarh_all.csv
```

The raw dataset is not included in this repository because of file size constraints.

---

# Shared Resources

## GitHub Repository

https://github.com/Samnannn/data_unicoding.git

---

## Raw Dataset

https://drive.google.com/file/d/1JPOz0cZd5xTkmzNYdPc3SRjvs7qyJcqP/view?usp=sharing

---

## Interim Dataset (After Canonicalization)

https://drive.google.com/file/d/1akGSo8DxwaZqEH2Ko9DEieeIxk2Lpt8X/view?usp=sharing

---

## AI Bharat Religion Inference Model

https://drive.google.com/drive/folders/1xomkvrSwGj40X94IpUaoC9-E5euBJYJf?usp=sharing

---

## Final Output Dataset

https://drive.google.com/file/d/1-Nt5G0czeLe_f5sIILDsVRXMQPXvktRZ/view?usp=sharing

---

# Alternative Execution

Custom input/output paths are also supported:

```powershell
python scripts\steps_1_to_3.py --input C:\path\to\chandigarh_all.csv --interim C:\path\to\cleaned_2.csv

python scripts\steps_4_onward.py --interim C:\path\to\cleaned_2.csv --output C:\path\to\final_df.csv
```

---

# Notes

- Canonicalization is currently the slowest stage of the workflow.
- The interim dataset allows downstream stages to be rerun without recomputing expensive preprocessing steps.
- Large datasets and generated outputs are intentionally excluded from GitHub.
- Shared helper functions are stored inside `pipeline_support.py`.
- If there is any difficulty reproducing locally, the Google Colab notebook can also be used after adjusting file paths.

---

# Google Colab Notebook

https://drive.google.com/file/d/1IHLmQAi038dsW0CY0H_pewcOZtIPCUCv/view?usp=sharing

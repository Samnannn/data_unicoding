# Partition Names Project

This repository packages the names-data workflow so it can be run without the
author's Google Drive paths. The original analysis notebook is preserved at
`notebooks/partition_names_project.ipynb`; the submission Python code is split
at the Step 3 canonicalization checkpoint.

## What to submit

The assignment brief asks for three deliverables:

1. `outputs/final_df.csv` after running the pipeline.
2. An answers `.docx` containing Q1-Q6 results and any assumptions.
3. The reproducible Python code in this repository, especially
   `scripts/steps_1_to_3.py` and `scripts/steps_4_onward.py`.

The notebook is useful supporting evidence, but it should not be the only code
artifact sent to the professor.

## Repository layout

```text
data/raw/                         professor-supplied input CSV, not tracked
data/interim/                     generated checkpoint CSV, not tracked
notebooks/partition_names_project.ipynb
outputs/                          generated final CSV, not tracked
scripts/steps_1_to_3.py           raw data through canonicalization
scripts/steps_4_onward.py         Step 4 through final dataset
scripts/reproduce.py              compatibility wrapper
third_party/its_all_in_the_name_light_repo/
```

The third-party religion classifier contains the SVM script and only the model
files used by this project: the multiclass non-concatenated model, vectorizer,
and label mapping. The two `.sav` files are larger than GitHub's normal file
limit and are marked for Git LFS in `.gitattributes`.

## Reproduce

Use a fresh Python environment, then install dependencies:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Place the assignment input file at `data/raw/chandigarh_all.csv`, then run the
first script:

```powershell
python scripts\steps_1_to_3.py
```

This first script replaces the notebook's Colab paths with project-relative
locations, runs Steps 1-3, and writes `data/interim/cleaned_2.csv`.

Step 3 canonicalization is the slowest part of the current notebook. After the
canonicalized checkpoint exists, run the second script:

```powershell
python scripts\steps_4_onward.py --interim data\interim\cleaned_2.csv --output outputs\final_df.csv
```

This second script skips Unicode cleaning, transliteration, and
canonicalization, then runs religion inference and the downstream
variables/questions from Step 4 onward.

When Step 4 onward is run inside Jupyter or Colab, run this setup cell first:

```python
## because ai bharat trained on lower scikit learn library so we have to downgrade

!pip uninstall -y scikit-learn
!pip install scikit-learn==1.3.2
```

The same setup note is kept at the top of `scripts/steps_4_onward.py` as
comments because `!pip` syntax is valid in a notebook cell, not in a normal
`.py` file.

Alternative input and output paths are supported:

```powershell
python scripts\steps_1_to_3.py --input C:\path\to\chandigarh_all.csv --interim C:\path\to\cleaned_2.csv
python scripts\steps_4_onward.py --interim C:\path\to\cleaned_2.csv --output C:\path\to\final_df.csv
```

## GitHub note

Do not push the raw `chandigarh_all.csv`, the large Step 3 checkpoint, or the
generated final dataset unless the professor explicitly wants those files in a
repository and the data-sharing rules allow it. The professor already supplied
the source CSV, so a clean GitHub repository can hold code, notebook, model
assets via Git LFS, and reproduction instructions while the final CSV and
answers DOCX are emailed as requested.

Before committing the large classifier assets to GitHub, initialize Git LFS in
this clone:

```powershell
git lfs install
```

## Method warning to review

The current notebook transliterates with `indic-transliteration`. The task brief
specifically names AI4Bharat IndicXlit. Confirm with the professor whether the
current transliteration implementation is acceptable or replace that step
before treating the project as final.

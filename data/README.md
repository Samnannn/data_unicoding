# Data placement

Place the professor-supplied `chandigarh_all.csv` input at:

```text
data/raw/chandigarh_all.csv
```

The reproducibility script writes the canonicalization checkpoint to
`data/interim/cleaned_2.csv` and the final dataset to `outputs/final_df.csv`.
If `cleaned_2.csv` already exists, run `scripts/steps_4_onward.py` to skip the
slow cleaning, transliteration, and canonicalization steps.

The raw, interim, and generated CSV files are ignored by Git on purpose because
they are large data artifacts from the assignment workflow.

# Notebook setup used before Step 4 in Colab/Jupyter:
# because ai bharat trained on lower scikit learn library so we have to downgrade
# !pip uninstall -y scikit-learn
# !pip install scikit-learn==1.3.2
"""Load cleaned_2.csv and run Step 4 onward to the final dataset."""

from __future__ import annotations

import argparse
from pathlib import Path

from pipeline_support import (
    DEFAULT_INTERIM,
    DEFAULT_OUTPUT,
    MODEL_ROOT,
    PROJECT_ROOT,
    execute_cells,
    notebook_code_cells,
    step_4_start_index,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Resume the pipeline from cleaned_2.csv at Step 4."
    )
    parser.add_argument("--interim", type=Path, default=DEFAULT_INTERIM)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> None:
    import numpy as np
    import pandas as pd
    import re

    args = parse_args()
    if not args.interim.is_file():
        raise FileNotFoundError(
            f"Step 3 checkpoint not found at {args.interim}. Pass --interim with "
            "the canonicalized cleaned_2.csv path."
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    cells = notebook_code_cells()
    namespace: dict[str, object] = {
        "__name__": "__main__",
        "pd": pd,
        "np": np,
        "re": re,
        "df": pd.read_csv(args.interim, low_memory=False),
        "PROJECT_ROOT": PROJECT_ROOT,
        "INTERIM_DATA": args.interim,
        "FINAL_DATA": args.output,
        "RELIGION_MODEL_ROOT": MODEL_ROOT,
    }
    model_was_run = execute_cells(cells, namespace, step_4_start_index(cells))

    if not model_was_run:
        raise RuntimeError("Step 4 onward did not invoke the religion model cell.")
    if not args.output.is_file():
        raise RuntimeError(f"Step 4 onward finished without creating {args.output}.")

    print(f"Started from Step 3 checkpoint at {args.interim}")
    print(f"Wrote final dataset to {args.output}")


if __name__ == "__main__":
    main()

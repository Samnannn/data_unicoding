"""Run Steps 1-3 and stop after the canonicalized checkpoint is written."""

from __future__ import annotations

import argparse
from pathlib import Path

from pipeline_support import (
    DEFAULT_INPUT,
    DEFAULT_INTERIM,
    MODEL_ROOT,
    PROJECT_ROOT,
    execute_cells,
    notebook_code_cells,
    step_4_start_index,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run Steps 1-3 through canonicalization and write cleaned_2.csv."
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--interim", type=Path, default=DEFAULT_INTERIM)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.input.is_file():
        raise FileNotFoundError(
            f"Input CSV not found at {args.input}. Place chandigarh_all.csv there "
            "or pass --input."
        )

    args.interim.parent.mkdir(parents=True, exist_ok=True)
    cells = notebook_code_cells()
    namespace: dict[str, object] = {"__name__": "__main__"}

    for index in range(step_4_start_index(cells)):
        namespace["RAW_DATA"] = args.input
        namespace["INTERIM_DATA"] = args.interim
        namespace["PROJECT_ROOT"] = PROJECT_ROOT
        namespace["RELIGION_MODEL_ROOT"] = MODEL_ROOT
        execute_cells(cells, namespace, start_index=index, stop_index=index + 1)

    if not args.interim.is_file():
        raise RuntimeError(f"Steps 1-3 finished without creating {args.interim}.")

    print(f"Wrote Step 3 checkpoint to {args.interim}")


if __name__ == "__main__":
    main()

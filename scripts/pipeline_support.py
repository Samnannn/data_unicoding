"""Shared helpers for running the notebook pipeline as Python scripts."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = PROJECT_ROOT / "notebooks" / "partition_names_project.ipynb"
MODEL_ROOT = PROJECT_ROOT / "third_party" / "its_all_in_the_name_light_repo"
MODEL_SCRIPT = MODEL_ROOT / "code" / "run_py38.py"
MODEL_INPUT = MODEL_ROOT / "data" / "sample_data.csv"
MODEL_PREDICTION = MODEL_ROOT / "data" / "predictions" / "sample_data.csv"
DEFAULT_INPUT = PROJECT_ROOT / "data" / "raw" / "chandigarh_all.csv"
DEFAULT_INTERIM = PROJECT_ROOT / "data" / "interim" / "cleaned_2.csv"
DEFAULT_OUTPUT = PROJECT_ROOT / "outputs" / "final_df.csv"
STEP_4_MARKER = "## Step 4"


def notebook_code_cells() -> list[str]:
    if not NOTEBOOK_PATH.is_file():
        raise FileNotFoundError(f"Notebook not found at {NOTEBOOK_PATH}.")

    notebook = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))
    return [
        "".join(cell.get("source", []))
        for cell in notebook["cells"]
        if cell.get("cell_type") == "code"
    ]


def step_4_start_index(cells: list[str]) -> int:
    for index, source in enumerate(cells):
        if STEP_4_MARKER in source:
            return index
    raise RuntimeError(f"Could not find notebook marker {STEP_4_MARKER!r}.")


def skip_notebook_only_cell(source: str) -> bool:
    return any(line.lstrip().startswith(("!", "%")) for line in source.splitlines())


def run_religion_model() -> None:
    if not MODEL_SCRIPT.is_file():
        raise FileNotFoundError(f"Religion model script not found at {MODEL_SCRIPT}.")

    MODEL_INPUT.parent.mkdir(parents=True, exist_ok=True)
    MODEL_PREDICTION.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([sys.executable, str(MODEL_SCRIPT)], check=True, cwd=PROJECT_ROOT)


def execute_cells(
    cells: list[str],
    namespace: dict[str, object],
    start_index: int,
    stop_index: int | None = None,
) -> bool:
    model_was_run = False

    for index, source in enumerate(cells[start_index:stop_index], start=start_index):
        if source.lstrip().startswith("!python ") and "run_py38.py" in source:
            run_religion_model()
            model_was_run = True
            continue
        if skip_notebook_only_cell(source):
            continue

        code = compile(source, f"{NOTEBOOK_PATH} cell {index}", "exec")
        exec(code, namespace)

    return model_was_run

"""Compatibility wrapper for the split pipeline scripts.

Prefer `steps_1_to_3.py` and `steps_4_onward.py` for submission and auditing.
"""

from __future__ import annotations

import argparse
import sys

import steps_1_to_3
import steps_4_onward


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the full pipeline or resume from the Step 3 checkpoint."
    )
    parser.add_argument("--from-interim", action="store_true")
    args, remainder = parser.parse_known_args()
    sys.argv = [sys.argv[0], *remainder]
    return args


def main() -> None:
    args = parse_args()
    if args.from_interim:
        steps_4_onward.main()
        return

    steps_1_to_3.main()
    steps_4_onward.main()


if __name__ == "__main__":
    main()

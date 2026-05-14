from __future__ import annotations

import sys
from pathlib import Path

LAB_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(LAB_DIR))

from comparison_utils import print_report, run_tutorial_embedding


def main() -> None:
    report = run_tutorial_embedding(k=3)
    print_report(report)


if __name__ == "__main__":
    main()

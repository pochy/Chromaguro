from __future__ import annotations

import os
import sys
from pathlib import Path

LAB_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(LAB_DIR))

from comparison_utils import print_comparison_table, run_sentence_transformer_embedding, run_tutorial_embedding


def main() -> None:
    reports = [run_tutorial_embedding(k=3)]
    local_run = run_sentence_transformer_embedding(k=3)

    if local_run.status == "ok" and local_run.report is not None:
        reports.append(local_run.report)
    elif local_run.status == "skipped":
        print(f"SKIPPED local embedding model: {local_run.reason}")
    elif local_run.status == "error":
        print(f"ERROR local embedding model: {local_run.reason}", file=sys.stderr)
        if os.getenv("LOCAL_EMBEDDING_MODEL"):
            raise SystemExit(1)

    print_comparison_table(reports)


if __name__ == "__main__":
    main()

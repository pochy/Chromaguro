from __future__ import annotations

import os
import sys
from pathlib import Path

LAB_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(LAB_DIR))

from comparison_utils import print_report, run_sentence_transformer_embedding


def main() -> None:
    run = run_sentence_transformer_embedding(k=3)

    if run.status == "skipped":
        print("SKIPPED: local embedding model is not configured.")
        print(run.reason)
        print("\nExample:")
        print("pip install -r requirements-local-embeddings.txt")
        print(
            "LOCAL_EMBEDDING_MODEL=/path/to/local/sentence-transformers-model "
            "python advanced_labs/local_embedding_comparison/examples/03_compare_local_embedding_model.py"
        )
        return

    if run.status == "error":
        print(f"ERROR: {run.reason}", file=sys.stderr)
        if os.getenv("LOCAL_EMBEDDING_MODEL"):
            raise SystemExit(1)
        return

    if run.report is None:
        raise RuntimeError("local embedding report was not produced")

    print_report(run.report)


if __name__ == "__main__":
    main()

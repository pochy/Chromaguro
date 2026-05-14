from __future__ import annotations

import sys
from pathlib import Path

LAB_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(LAB_DIR))

from comparison_utils import load_questions, load_records, validate_gold_data


def main() -> None:
    errors = validate_gold_data()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)

    records = load_records()
    questions = load_questions()

    print("## Gold data")
    print(f"documents: {len(records)}")
    print(f"questions: {len(questions)}")

    print("\n## Documents")
    for record in records:
        print(f"- {record['id']} topic={record['metadata']['topic']} source={record['metadata']['source']}")

    print("\n## Questions")
    for item in questions:
        print(f"- {item['question']}")
        print(f"  relevant_ids={item['relevant_ids']}")


if __name__ == "__main__":
    main()

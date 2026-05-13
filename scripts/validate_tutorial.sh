#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

PYTHON_BIN="${PYTHON:-}"
if [[ -z "$PYTHON_BIN" ]]; then
  if [[ -x ".venv/bin/python" ]]; then
    PYTHON_BIN=".venv/bin/python"
  else
    PYTHON_BIN="python3"
  fi
fi

RUN_OPTIONAL=0
RUN_HTTP=0
HTTP_HOST="${CHROMA_HOST:-localhost}"
HTTP_PORT="${CHROMA_PORT:-9010}"
CHROMA_BIN="${CHROMA_BIN:-}"

usage() {
  cat <<'USAGE'
Usage: scripts/validate_tutorial.sh [options]

Validates the required Chroma tutorial path:
  - checks tutorial structure
  - checks local Markdown links
  - checks generated DB/cache files are ignored
  - compiles Python examples
  - runs every levels/*/examples/*.py file

Options:
  --optional-integrations  Also run advanced integration labs.
  --http                   Also start a local Chroma server and run the HttpClient lab.
  --host HOST              Host for the HttpClient lab. Default: localhost.
  --port PORT              Port for the HttpClient lab. Default: 9010.
  --python PATH            Python executable to use.
  -h, --help               Show this help.

Environment:
  PYTHON       Python executable override.
  CHROMA_BIN   Chroma CLI override.
  CHROMA_HOST  HttpClient lab host override.
  CHROMA_PORT  HttpClient lab port override.
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --optional-integrations)
      RUN_OPTIONAL=1
      ;;
    --http)
      RUN_HTTP=1
      ;;
    --host)
      shift
      HTTP_HOST="${1:?--host requires a value}"
      ;;
    --port)
      shift
      HTTP_PORT="${1:?--port requires a value}"
      ;;
    --python)
      shift
      PYTHON_BIN="${1:?--python requires a value}"
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
  shift
done

export PYTHONDONTWRITEBYTECODE="${PYTHONDONTWRITEBYTECODE:-1}"

section() {
  printf '\n==> %s\n' "$1"
}

run() {
  printf '+'
  printf ' %q' "$@"
  printf '\n'
  "$@"
}

check_structure() {
  section "Checking tutorial structure"
  run "$PYTHON_BIN" - <<'PY'
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

root = Path(".")
errors: list[str] = []

levels = sorted((root / "levels").glob("level_*"))
if len(levels) != 10:
    errors.append(f"expected 10 level directories, found {len(levels)}")

required_readme_headings = [
    "## この Level でできるようになること",
    "## まず知るべき言葉",
    "## なぜこれを学ぶのか",
    "## 手順 1:",
    "## 手順 2:",
    "## 手順 3:",
    "## よくあるつまずき",
    "## 次の Level に進む条件",
    "## 公式 docs で確認する箇所",
]
required_exercise_headings = [
    "## 1.",
    "## 2.",
    "## 3.",
    "## 提出物",
    "## 進級チェック",
]

for level in levels:
    readme = level / "README.md"
    exercises = level / "exercises.md"
    if not readme.exists():
        errors.append(f"missing {readme}")
    else:
        text = readme.read_text(encoding="utf-8")
        for heading in required_readme_headings:
            if heading not in text:
                errors.append(f"{readme} missing heading containing {heading!r}")
    if not exercises.exists():
        errors.append(f"missing {exercises}")
    else:
        text = exercises.read_text(encoding="utf-8")
        for heading in required_exercise_headings:
            if heading not in text:
                errors.append(f"{exercises} missing heading containing {heading!r}")

examples = sorted((root / "levels").glob("level_*/examples/*.py"))
if len(examples) < 20:
    errors.append(f"expected at least 20 runnable level examples, found {len(examples)}")

ignore_samples = [
    "shared/__pycache__/example.cpython-311.pyc",
    "levels/level_01_intro/examples/chroma_db/chroma.sqlite3",
    "advanced_labs/local_server_http/chroma_server_db/chroma.sqlite3",
    "advanced_labs/integrations/langchain/langchain_chroma_db/chroma.sqlite3",
    "advanced_labs/integrations/llamaindex/llamaindex_chroma_db/chroma.sqlite3",
    "advanced_labs/integrations/mcp_agent/agent_memory_db/chroma.sqlite3",
    "levels/level_06_evaluation/examples/eval_logs.jsonl",
]
for sample in ignore_samples:
    try:
        result = subprocess.run(
            ["git", "check-ignore", "-q", sample],
            cwd=root,
            check=False,
        )
    except FileNotFoundError:
        print("git not found; skipping gitignore validation")
        break
    if result.returncode != 0:
        errors.append(f"{sample} is not ignored by .gitignore")

if errors:
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    raise SystemExit(1)

print(f"levels: {len(levels)}")
print(f"level examples: {len(examples)}")
PY
}

compile_python() {
  section "Compiling Python files"
  run "$PYTHON_BIN" -m compileall -q shared levels advanced_labs
}

check_markdown_links() {
  section "Checking Markdown links"
  run "$PYTHON_BIN" scripts/check_markdown_links.py
}

run_level_examples() {
  section "Running level examples"
  local count=0
  while IFS= read -r example; do
    [[ -n "$example" ]] || continue
    run "$PYTHON_BIN" "$example"
    count=$((count + 1))
  done < <(find levels -path '*/examples/*.py' -type f | sort)
  printf 'Ran %s level examples.\n' "$count"
}

run_optional_integrations() {
  section "Running optional integration labs"
  local labs=(
    "advanced_labs/integrations/mcp_agent/01_local_agentic_memory.py"
    "advanced_labs/integrations/langchain/01_langchain_chroma.py"
    "advanced_labs/integrations/llamaindex/01_llamaindex_chroma.py"
  )
  local lab
  for lab in "${labs[@]}"; do
    run "$PYTHON_BIN" "$lab"
  done
}

find_chroma_bin() {
  if [[ -n "$CHROMA_BIN" ]]; then
    printf '%s\n' "$CHROMA_BIN"
    return
  fi
  if [[ -x ".venv/bin/chroma" ]]; then
    printf '%s\n' ".venv/bin/chroma"
    return
  fi
  command -v chroma
}

run_http_lab() {
  section "Running HttpClient lab"
  local chroma_cli
  if ! chroma_cli="$(find_chroma_bin)"; then
    echo "Chroma CLI was not found. Install requirements.txt or set CHROMA_BIN." >&2
    exit 1
  fi
  local log_file="${TMPDIR:-/tmp}/chromaguro-chroma-${HTTP_PORT}.log"

  rm -f "$log_file"
  "$chroma_cli" run \
    --path ./advanced_labs/local_server_http/chroma_server_db \
    --host "$HTTP_HOST" \
    --port "$HTTP_PORT" \
    >"$log_file" 2>&1 &
  local server_pid=$!

  cleanup_http_server() {
    if kill -0 "$server_pid" >/dev/null 2>&1; then
      kill "$server_pid" >/dev/null 2>&1 || true
      wait "$server_pid" >/dev/null 2>&1 || true
    fi
  }
  trap cleanup_http_server RETURN

  local ready=0
  for _ in {1..30}; do
    if ! kill -0 "$server_pid" >/dev/null 2>&1; then
      cat "$log_file" >&2
      echo "Chroma server exited before it became ready." >&2
      exit 1
    fi
    if CHROMA_HOST="$HTTP_HOST" CHROMA_PORT="$HTTP_PORT" "$PYTHON_BIN" - <<'PY' >/dev/null 2>&1
import os

import chromadb

client = chromadb.HttpClient(
    host=os.environ["CHROMA_HOST"],
    port=int(os.environ["CHROMA_PORT"]),
)
client.heartbeat()
PY
    then
      ready=1
      break
    fi
    sleep 1
  done

  if [[ "$ready" -ne 1 ]]; then
    cat "$log_file" >&2
    echo "Chroma server did not become ready on ${HTTP_HOST}:${HTTP_PORT}." >&2
    exit 1
  fi

  run env CHROMA_HOST="$HTTP_HOST" CHROMA_PORT="$HTTP_PORT" "$PYTHON_BIN" advanced_labs/local_server_http/http_client_smoke.py
}

check_structure
check_markdown_links
compile_python
run_level_examples

if [[ "$RUN_OPTIONAL" -eq 1 ]]; then
  run_optional_integrations
fi

if [[ "$RUN_HTTP" -eq 1 ]]; then
  run_http_lab
fi

section "Validation complete"

#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit


INLINE_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
EXTERNAL_SCHEMES = {
    "http",
    "https",
    "mailto",
    "tel",
    "ftp",
    "app",
}


def tracked_markdown_files(root: Path) -> list[Path]:
    try:
        result = subprocess.run(
            ["git", "ls-files", "*.md"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return sorted(root.rglob("*.md"))

    return [root / line for line in result.stdout.splitlines() if line.strip()]


def normalize_destination(raw_destination: str) -> str:
    destination = raw_destination.strip()
    if destination.startswith("<"):
        closing = destination.find(">")
        if closing != -1:
            return destination[1:closing]
    return destination.split()[0] if destination else destination


def is_external(destination: str) -> bool:
    parsed = urlsplit(destination)
    return parsed.scheme.lower() in EXTERNAL_SCHEMES


def slugify_heading(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"\s+", "-", text)
    return text.strip("-")


def markdown_anchors(path: Path) -> set[str]:
    anchors: set[str] = set()
    counts: Counter[str] = Counter()

    for line in path.read_text(encoding="utf-8").splitlines():
        match = HEADING_RE.match(line)
        if not match:
            continue
        base = slugify_heading(match.group(2))
        if not base:
            continue
        count = counts[base]
        counts[base] += 1
        anchors.add(base if count == 0 else f"{base}-{count}")

    return anchors


def split_destination(destination: str) -> tuple[str, str]:
    parsed = urlsplit(destination)
    path = unquote(parsed.path)
    fragment = unquote(parsed.fragment)
    return path, fragment


def line_links(markdown: str) -> list[tuple[int, str]]:
    links: list[tuple[int, str]] = []
    in_fence = False

    for line_number, line in enumerate(markdown.splitlines(), start=1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for match in INLINE_LINK_RE.finditer(line):
            links.append((line_number, normalize_destination(match.group(1))))

    return links


def validate_link(root: Path, source: Path, line_number: int, destination: str) -> list[str]:
    if not destination or is_external(destination):
        return []

    path_part, fragment = split_destination(destination)
    if not path_part and not fragment:
        return []

    target = source if not path_part else (source.parent / path_part).resolve()
    errors: list[str] = []

    try:
        target.relative_to(root)
    except ValueError:
        errors.append(f"{source.relative_to(root)}:{line_number}: link escapes repo: {destination}")
        return errors

    if not target.exists():
        errors.append(f"{source.relative_to(root)}:{line_number}: missing link target: {destination}")
        return errors

    if fragment and target.suffix.lower() == ".md":
        expected = slugify_heading(fragment)
        if expected and expected not in markdown_anchors(target):
            errors.append(
                f"{source.relative_to(root)}:{line_number}: missing heading #{fragment} in {target.relative_to(root)}"
            )

    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors: list[str] = []

    for path in tracked_markdown_files(root):
        text = path.read_text(encoding="utf-8")
        for line_number, destination in line_links(text):
            errors.extend(validate_link(root, path, line_number, destination))

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("Markdown links: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

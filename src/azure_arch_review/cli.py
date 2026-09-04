from __future__ import annotations

import argparse
from pathlib import Path

from .engine import review_path
from .reporters import as_json, as_markdown, as_sarif
from .rules import load_rules


def main() -> None:
    parser = argparse.ArgumentParser(description="Review Azure IaC architecture changes.")
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--rules", default="rules/azure-rules.json")
    parser.add_argument("--format", choices=("json", "sarif", "markdown"), default="markdown")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--fail-on-hold", action="store_true")
    args = parser.parse_args()

    review = review_path(Path(args.path).resolve(), load_rules(Path(args.rules)))
    rendered = {"json": as_json, "sarif": as_sarif, "markdown": as_markdown}[args.format](review)
    if args.output:
        args.output.write_text(rendered)
    print(rendered, end="")
    if args.fail_on_hold and review.decision == "hold":
        raise SystemExit(2)


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
from pathlib import Path

from .models import Rule


def load_rules(path: Path) -> list[Rule]:
    data = json.loads(path.read_text())
    rules = []
    for item in data["rules"]:
        item["file_extensions"] = tuple(item["file_extensions"])
        rules.append(Rule(**item))
    return rules

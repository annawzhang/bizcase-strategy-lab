from __future__ import annotations

import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT = ROOT / "config" / "case.toml"


def load_case(path: Path = DEFAULT) -> dict:
    with open(path, "rb") as f:
        return tomllib.load(f)

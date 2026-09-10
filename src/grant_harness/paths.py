"""Package paths and optional grant-agent-lab discovery."""
from __future__ import annotations

import os
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _detect_root() -> Path:
    env = os.environ.get("GRANT_HARNESS_ROOT")
    if env:
        return Path(env).expanduser().resolve()
    candidates = [
        HERE.parent.parent,  # repo root when running from src/
        HERE,  # installed: data shipped beside the module
        HERE.parent,
    ]
    for cand in candidates:
        if (cand / "data" / "cases").is_dir():
            return cand
    return HERE.parent.parent


PKG_ROOT = _detect_root()
DATA_DIR = PKG_ROOT / "data"
CASES_DIR = DATA_DIR / "cases"
SAMPLES_DIR = DATA_DIR / "samples"
PACKS_DIR = DATA_DIR / "packs"
FIXTURES_DIR = DATA_DIR / "fixtures"


def lab_root() -> Path | None:
    env = os.environ.get("GRANT_AGENT_LAB_ROOT")
    if env:
        p = Path(env).expanduser().resolve()
        if p.exists():
            return p
    sibling = PKG_ROOT.parent / "grant-agent-lab"
    if sibling.exists():
        return sibling
    return None

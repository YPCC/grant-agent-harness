"""Load YAML harness cases."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from grant_harness.paths import CASES_DIR, SAMPLES_DIR
from grant_harness.yaml_lite import parse_simple_yaml


def case_path(case_id: str) -> Path:
    p = CASES_DIR / f"{case_id}.yaml"
    if not p.exists():
        raise FileNotFoundError(f"Case not found: {case_id} ({p})")
    return p


def list_cases() -> list[dict[str, Any]]:
    rows = []
    for p in sorted(CASES_DIR.glob("*.yaml")):
        data = parse_simple_yaml(p.read_text(encoding="utf-8"))
        rows.append({
            "id": data.get("id", p.stem),
            "mechanism": data.get("mechanism", "R01"),
            "summary": data.get("summary", ""),
            "path": str(p.name),
        })
    return rows


def load_case(case_id: str) -> dict[str, Any]:
    data = parse_simple_yaml(case_path(case_id).read_text(encoding="utf-8"))
    text_file = (data.get("input") or {}).get("text_file")
    if text_file:
        tp = Path(text_file)
        if not tp.is_absolute():
            # allow data/samples/... relative to package root
            from grant_harness.paths import PKG_ROOT

            candidate = PKG_ROOT / text_file
            tp = candidate if candidate.exists() else SAMPLES_DIR / Path(text_file).name
        data["_text"] = tp.read_text(encoding="utf-8")
        data["_text_path"] = str(tp)
    else:
        data["_text"] = (data.get("input") or {}).get("text") or ""
        data["_text_path"] = None
    return data

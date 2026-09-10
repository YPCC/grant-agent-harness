"""R01 essentials + SF424-style checklist scoring (standalone copy of lab catalog)."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from grant_harness.paths import PACKS_DIR
from grant_harness.yaml_lite import parse_simple_yaml

DEFAULT_CATALOG = PACKS_DIR / "r01_essentials.yaml"


def load_catalog(path: Path | None = None) -> dict[str, Any]:
    p = path or DEFAULT_CATALOG
    return parse_simple_yaml(p.read_text(encoding="utf-8"))


def evaluate_checklist(text: str, documents: list[str] | None = None, catalog: dict | None = None) -> dict[str, Any]:
    catalog = catalog or load_catalog()
    hay = ((text or "") + "\n" + " ".join(documents or [])).lower()
    rows = []
    missing_required = []
    for item in catalog.get("items") or []:
        needles = [str(n).lower() for n in (item.get("detect") or [])]
        present = any(n and n in hay for n in needles)
        status = "present" if present else "missing"
        row = {
            "id": item["id"],
            "label": item.get("label", item["id"]),
            "group": item.get("group", ""),
            "required": bool(item.get("required", True)),
            "status": status,
        }
        rows.append(row)
        if row["required"] and status == "missing":
            missing_required.append(row)
    total_req = sum(1 for r in rows if r["required"])
    present_req = total_req - len(missing_required)
    score = int(round(100 * present_req / total_req)) if total_req else 100
    return {
        "agent": "MissingEssentials",
        "mechanism": catalog.get("mechanism", "R01"),
        "title": catalog.get("title", ""),
        "items": rows,
        "missing_required": [m["id"] for m in missing_required],
        "present_required": present_req,
        "total_required": total_req,
        "readiness_score": score,
        "can_freeze": len(missing_required) == 0,
        "summary": (
            f"{present_req}/{total_req} required items present. "
            + (
                "Ready to freeze for Office of Research Aid."
                if not missing_required
                else f"Missing: {', '.join(m['id'] for m in missing_required)}."
            )
        ),
    }

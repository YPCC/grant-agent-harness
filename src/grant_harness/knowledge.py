"""Versioned knowledge packs injected into every harness run."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from grant_harness.paths import FIXTURES_DIR, PACKS_DIR
from grant_harness.yaml_lite import parse_simple_yaml

PACK_FILES = {
    "r01_essentials": PACKS_DIR / "r01_essentials.yaml",
    "ora_intake": PACKS_DIR / "ora_intake.yaml",
    "sf424": PACKS_DIR / "nih_sf424_rules.yaml",
    "gpa_core_questions": PACKS_DIR / "gpa_core_questions.md",
    "ssrb_issue_classes": PACKS_DIR / "ssrb_issue_classes.md",
    "invariants": PACKS_DIR / "invariants.md",
    "reporter_frozen": FIXTURES_DIR / "reporter" / "auditory_cortex_2024.json",
}


def list_packs() -> list[str]:
    return sorted(PACK_FILES)


def load_pack(name: str) -> dict[str, Any]:
    path = PACK_FILES.get(name)
    if path is None:
        raise KeyError(f"Unknown pack {name}. Known: {list_packs()}")
    text = path.read_text(encoding="utf-8")
    payload: Any
    if path.suffix in {".yaml", ".yml"}:
        payload = parse_simple_yaml(text)
    elif path.suffix == ".json":
        import json

        payload = json.loads(text)
    else:
        payload = text
    return {
        "id": name,
        "path": str(path.relative_to(path.parents[2])),
        "version": "2026-09-10",
        "content": payload,
    }


def resolve_packs(names: list[str] | None = None) -> dict[str, Any]:
    wanted = names or list_packs()
    packs = [load_pack(n) for n in wanted]
    return {
        "guideline_versions": {p["id"]: p["version"] for p in packs},
        "packs": packs,
        "last_knowledge_refresh": "fixture",
    }

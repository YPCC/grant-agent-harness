"""In-memory Office of Research Aid package writer. Never NIH ASSIST."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from grant_harness.paths import PKG_ROOT

PACKAGES = PKG_ROOT / "output" / "packages"
BLOCKED_DESTINATIONS = ("NIH_ASSIST", "ASSIST", "GRANTS.GOV", "ERA_COMMONS_SUBMIT")


def _tracking_number(proposal_id: str, stamp: str) -> str:
    digest = hashlib.sha256(f"{proposal_id}:{stamp}".encode()).hexdigest()[:6].upper()
    day = stamp[:10].replace("-", "")
    return f"ORA-{day}-{digest}"


def create_office_package(
    *,
    proposal_id: str = "PR-HARNESS",
    filename: str = "proposal.docx",
    intake: dict[str, Any] | None = None,
    findings: list | None = None,
    text_excerpt: str = "",
    submitted_by: str = "PI",
    destination: str = "Office of Research Aid database",
) -> dict[str, Any]:
    dest_key = destination.replace(" ", "_").upper()
    if any(b in dest_key for b in BLOCKED_DESTINATIONS) or destination.upper() in BLOCKED_DESTINATIONS:
        raise PermissionError("Harness invariant: NIH ASSIST / Grants.gov submit is forbidden")
    if not (intake or {}).get("can_submit_to_office"):
        raise ValueError("Intake form is incomplete; cannot submit to Office of Research Aid")

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    tracking = _tracking_number(proposal_id, stamp)
    dest = PACKAGES / tracking
    dest.mkdir(parents=True, exist_ok=True)
    snapshot = {
        "proposal_id": proposal_id,
        "tracking_number": tracking,
        "destination": "Office of Research Aid database",
        "not": "NIH_ASSIST",
        "submitted_by": submitted_by,
        "submitted_at": stamp,
        "source_filename": filename,
        "intake_complete": True,
        "intake_summary": (intake or {}).get("summary"),
        "findings_count": len(findings or []),
        "status": "received",
    }
    (dest / "MANIFEST.json").write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    (dest / "intake-form.json").write_text(json.dumps(intake or {}, indent=2), encoding="utf-8")
    (dest / "findings.json").write_text(json.dumps(findings or [], indent=2), encoding="utf-8")
    (dest / "proposal-excerpt.txt").write_text((text_excerpt or "")[:8000], encoding="utf-8")
    (dest / "TRACKING.txt").write_text(
        f"{tracking}\nOffice of Research Aid — received {stamp}\nSubmitted by {submitted_by}\n",
        encoding="utf-8",
    )
    snapshot["package_path"] = str(dest.relative_to(PKG_ROOT))
    snapshot["files"] = sorted(p.name for p in dest.iterdir())
    snapshot["message"] = (
        f"Package uploaded to the Office of Research Aid database. "
        f"Tracking number {tracking} is now on the PI record."
    )
    return snapshot

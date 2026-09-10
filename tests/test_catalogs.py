from grant_harness.yaml_lite import parse_simple_yaml
from grant_harness.checklist import load_catalog, evaluate_checklist
from grant_harness.intake import fill_intake


def test_catalog_loads():
    cat = load_catalog()
    assert cat["mechanism"] == "R01"
    assert len(cat["items"]) >= 10


def test_case_yaml_overrides():
    from pathlib import Path
    from grant_harness.paths import CASES_DIR

    data = parse_simple_yaml((CASES_DIR / "complete_ora_packet.yaml").read_text())
    assert data["input"]["intake_overrides"]["PI_CERTIFY"] in ("yes", True)


def test_intake_human_only():
    form = fill_intake("hypothesis specific aim 1 modular budget", "x.txt")
    cert = next(i for i in form["items"] if i["id"] == "PI_CERTIFY")
    assert cert["complete"] is False
    assert form["can_submit_to_office"] is False


def test_weak_text_missing_hypothesis_token():
    result = evaluate_checklist("Hearing is important. Aim 1 characterize.")
    assert "HYPOTHESIS" in result["missing_required"]

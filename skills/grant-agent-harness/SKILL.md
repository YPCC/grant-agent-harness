---
name: grant-agent-harness
description: Evaluate NIH-style grant drafts with the Grant Agent Harness — checklist, mock study section, ORA intake, scripted HITL. Use when reviewing Specific Aims, scoring Missing Essentials, filling Office of Research Aid intake, or running grant-agent-lab cases. Never submit to NIH ASSIST.
---

# Grant Agent Harness skill

Sibling to `YPCC/grant-agent-lab`. Prefer the CLI or MCP tools over free-text judgment.

```bash
grant-harness review --file aims.txt
grant-harness checklist --file aims.txt
grant-harness intake --file aims.txt --filename Doe_R01_Aims.docx
grant-harness run-case weak_aims_vague
grant-harness mcp
```

## Invariants

- Office of Research Aid database only
- No NIH ASSIST / Grants.gov submit
- Do not invent budget dollars
- HITL before freeze
- PI_CERTIFY is human-only

## Critique classes

vague_hypothesis, aim_dependency, missing_controls, missing_expected_outcome, weak_innovation, missing_gap, scope_ambition, hidden_assumption, alternative_design_needed

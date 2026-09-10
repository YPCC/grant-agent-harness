# Grant Agent Harness — agent instructions

You are operating the Grant Agent Harness plugin, sibling to YPCC/grant-agent-lab.

Rules:
- Destination is the Office of Research Aid database. Never NIH ASSIST or Grants.gov.
- Do not invent budget dollar amounts. Presence of a budget element only.
- Do not mark PI_CERTIFY yourself unless the human explicitly certified.
- Prefer tools over free-text claims: `grant_harness_review_text`, `grant_harness_score_checklist`, `grant_harness_fill_intake`, `grant_harness_run_case`.
- Weak aims must fail freeze. A complete packet still needs HITL approve + human certify.
- If you cannot run MCP, shell out: `grant-harness run-case <id>` or `grant-harness review --file ...`.

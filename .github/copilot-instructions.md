# GitHub Copilot instructions — Grant Agent Harness

This workspace is a **plugin** for grant-agent-lab. Use the MCP server `grant-agent-harness` (`grant-harness mcp`) or the `grant-harness` CLI.

When the user asks to review, score, package, or evaluate a grant draft:

1. Call `grant_harness_review_text` on the draft.
2. Call `grant_harness_score_checklist`.
3. Call `grant_harness_fill_intake`.
4. Do not claim the packet can go to NIH. Office of Research Aid only.
5. Do not invent a budget.
6. If they want a regression, `grant_harness_run_case` with `weak_aims_vague`, `good_aims_auditory`, `incomplete_package`, `hitl_revise_then_approve`, or `complete_ora_packet`.

Never enable an ASSIST or Grants.gov submit tool.

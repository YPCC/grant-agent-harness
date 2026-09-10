# Grant Agent Harness

Sibling package to [YPCC/grant-agent-lab](https://github.com/YPCC/grant-agent-lab).

It is an **eval cage + plugin** for the grant agents: fixture cases, versioned knowledge packs, deterministic graders, scripted HITL, and an Office of Research Aid packet writer. It is **not** a fourth runtime and it **does not submit to NIH ASSIST**.

Use it from:

- GitHub Copilot / VS Code MCP
- Cursor, Claude Desktop, or any MCP client
- any LLM tool that can shell out to `grant-harness`
- Grok / Claude / Copilot skills via `skills/grant-agent-harness/SKILL.md`

## Install

```bash
git clone https://github.com/YPCC/grant-agent-harness.git
cd grant-agent-harness
pip install -e ".[dev]"
grant-harness list-cases
grant-harness run-case weak_aims_vague
```

No model key is required. Graders are deterministic.

## Plugin: GitHub Copilot / VS Code

Copy or symlink the workspace MCP config:

```json
{
  "servers": {
    "grant-agent-harness": {
      "command": "grant-harness",
      "args": ["mcp"]
    }
  }
}
```

That file already lives at [`.vscode/mcp.json`](.vscode/mcp.json) and [`plugin/vscode/mcp.json`](plugin/vscode/mcp.json).

Copilot agent instructions: [`.github/copilot-instructions.md`](.github/copilot-instructions.md) and [`.github/agents/grant-harness.agent.md`](.github/agents/grant-harness.agent.md).

After `pip install -e .`, open the repo in VS Code / Copilot Chat and enable the MCP server. Copilot can then call `grant_harness_review_text`, `grant_harness_run_case`, and the other tools.

## Plugin: Claude Desktop

Merge [`plugin/claude-desktop/claude_desktop_config.snippet.json`](plugin/claude-desktop/claude_desktop_config.snippet.json) into `claude_desktop_config.json`.

## Plugin: Cursor

Copy [`plugin/cursor/mcp.json`](plugin/cursor/mcp.json) to `.cursor/mcp.json`.

## CLI (any LLM tool)

```bash
grant-harness review --file aims.txt
grant-harness checklist --file aims.txt
grant-harness intake --file aims.txt --filename Doe_R01_Aims.docx
grant-harness run --file aims.txt --hitl revise,approve
grant-harness run-case complete_ora_packet --package
grant-harness mcp          # stdio MCP server
```

## What it grades

| Layer | Source |
|---|---|
| Missing Essentials | `data/packs/r01_essentials.yaml` (same catalog as the lab) |
| ORA intake | `data/packs/ora_intake.yaml` |
| SF424 rules pack | `data/packs/nih_sf424_rules.yaml` |
| GPA four questions | `data/packs/gpa_core_questions.md` |
| SSRB issue classes | `data/packs/ssrb_issue_classes.md` |
| Frozen RePORTER | `data/fixtures/reporter/` (no live network in CI) |

Hard invariants: Office of Research Aid only, no invented budget dollars, HITL before freeze, `PI_CERTIFY` is human-only.

## Layout

```
grant-agent-harness/
├── src/grant_harness/     # CLI, MCP server, runner, graders
├── data/cases/            # YAML eval cases
├── data/packs/            # knowledge packs
├── data/samples/          # public / synthetic aims
├── plugin/                # Copilot, VS Code, Cursor, Claude snippets
├── skills/                # SKILL.md for tool-using agents
└── tests/
```

Point `GRANT_AGENT_LAB_ROOT` at a local grant-agent-lab checkout if you want the harness to discover the sibling lab. v0 does not import lab code; catalogs are vendored so the plugin stays standalone.

## License

Apache-2.0

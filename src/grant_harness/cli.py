"""CLI for agents that shell out instead of speaking MCP."""
from __future__ import annotations

import argparse
import json
import sys

from grant_harness import __version__
from grant_harness.cases import list_cases, load_case
from grant_harness.checklist import evaluate_checklist
from grant_harness.intake import fill_intake
from grant_harness.knowledge import list_packs, load_pack
from grant_harness.review import review_text
from grant_harness.runner import dumps, run_case, run_pipeline


def _read_text(args: argparse.Namespace) -> str:
    if args.text:
        return args.text
    if args.file:
        return open(args.file, encoding="utf-8").read()
    if not sys.stdin.isatty():
        return sys.stdin.read()
    raise SystemExit("Provide --text, --file, or stdin")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="grant-harness",
        description="Grant Agent Harness — eval cage + plugin surface for Copilot / any LLM tool.",
    )
    p.add_argument("--version", action="version", version=f"grant-harness {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list-cases", help="List bundled evaluation cases")
    sub.add_parser("list-packs", help="List knowledge packs")
    sub.add_parser("mcp", help="Run MCP stdio server for Copilot / Cursor / Claude")

    s = sub.add_parser("run-case", help="Run a bundled case and grade it")
    s.add_argument("case_id")
    s.add_argument("--package", action="store_true", help="Write ORA package if gates pass")

    s = sub.add_parser("review", help="Review free text / a file")
    s.add_argument("--text")
    s.add_argument("--file")
    s.add_argument("--mechanism", default="R01")

    s = sub.add_parser("checklist", help="Score Missing Essentials")
    s.add_argument("--text")
    s.add_argument("--file")

    s = sub.add_parser("intake", help="Fill Office of Research Aid intake")
    s.add_argument("--text")
    s.add_argument("--file")
    s.add_argument("--filename", default="proposal.docx")

    s = sub.add_parser("run", help="Full pipeline on free text")
    s.add_argument("--text")
    s.add_argument("--file")
    s.add_argument("--mechanism", default="R01")
    s.add_argument("--filename", default="proposal.docx")
    s.add_argument("--hitl", default="revise", help="Comma-separated HITL script")
    s.add_argument("--package", action="store_true")

    s = sub.add_parser("pack", help="Print one knowledge pack")
    s.add_argument("name")

    args = p.parse_args(argv)

    if args.cmd == "mcp":
        from grant_harness.mcp_server import serve_stdio

        serve_stdio()
        return 0
    if args.cmd == "list-cases":
        print(dumps(list_cases()))
        return 0
    if args.cmd == "list-packs":
        print(dumps(list_packs()))
        return 0
    if args.cmd == "pack":
        print(dumps(load_pack(args.name)))
        return 0
    if args.cmd == "run-case":
        result = run_case(load_case(args.case_id), allow_package=args.package or None)
        print(dumps(_public(result)))
        return 0 if result["grade"]["passed"] else 2
    text = _read_text(args)
    if args.cmd == "review":
        print(dumps(review_text(text, mechanism=args.mechanism)))
        return 0
    if args.cmd == "checklist":
        print(dumps(evaluate_checklist(text)))
        return 0
    if args.cmd == "intake":
        print(dumps(fill_intake(text, filename=args.filename)))
        return 0
    if args.cmd == "run":
        result = run_pipeline(
            text,
            mechanism=args.mechanism,
            filename=args.filename,
            hitl_script=[s.strip() for s in args.hitl.split(",") if s.strip()],
            allow_package=args.package,
        )
        print(dumps(_public(result)))
        return 0
    return 1


def _public(result: dict) -> dict:
    out = dict(result)
    if "intake" in out and "groups" in out["intake"]:
        slim = dict(out["intake"])
        slim.pop("groups", None)
        out["intake"] = slim
    return out


if __name__ == "__main__":
    raise SystemExit(main())

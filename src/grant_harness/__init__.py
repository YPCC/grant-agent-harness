"""Grant Agent Harness — sibling plugin to YPCC/grant-agent-lab.

Deterministic eval cage + MCP/CLI surface for GitHub Copilot and other LLM tools.
Does not submit to NIH ASSIST. Office of Research Aid packets only.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("grant-agent-harness")
except PackageNotFoundError:
    __version__ = "0.1.0"

PACKAGE_NAME = "grant-agent-harness"

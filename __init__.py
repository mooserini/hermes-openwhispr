"""hermes-openwhispr: agent-side entry point.

This plugin is a skill carrier by design. All OpenWhispr work goes
through the bundled skill (skills/productivity/openwhispr/SKILL.md),
which drives the external `@openwhispr/cli` via the `terminal` tool.

The agent side intentionally registers no tools, hooks, or middleware:
- local bridge (127.0.0.1:8200) is the default, free, no key;
- cloud is opt-in only, via the CLI's own `openwhispr auth login`.

This module exists so the package is a well-formed Hermes plugin.
"""


def register(ctx):
    """Inert by design: functionality lives in the bundled skill."""
    return None

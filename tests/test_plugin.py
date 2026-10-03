"""Tests for hermes-openwhispr. Stdlib + pytest only, no live network."""

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]


def test_manifest_exists_and_declares_no_capabilities():
    text = (ROOT / "plugin.yaml").read_text()
    assert "name: hermes-openwhispr" in text
    assert "tools: []" in text
    assert "hooks: []" in text


def test_register_is_inert():
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "hermes_openwhispr", ROOT / "__init__.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert mod.register(object()) is None


def test_skill_frontmatter_hardline():
    text = (
        ROOT / "skills" / "productivity" / "openwhispr" / "SKILL.md"
    ).read_text()
    assert text.startswith("---")
    m = re.search(r"^description: (.*)$", text, re.MULTILINE)
    assert m, "description frontmatter missing"
    desc = m.group(1).strip()
    assert len(desc) <= 60, f"description {len(desc)} chars"
    assert desc.endswith(".")


def test_no_core_overrides_or_self_updater():
    blob = (ROOT / "__init__.py").read_text()
    for banned in ("sys.modules", "setattr(server", "AIAgent.", "check for updates"):
        assert banned not in blob


def test_readme_discloses_credential_read():
    readme = (ROOT / "README.md").read_text().lower()
    assert "cli-config.json" in readme
    assert "read-only" in readme or "read only" in readme

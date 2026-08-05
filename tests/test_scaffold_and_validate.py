"""End-to-end tests for scaffold + validate."""

from __future__ import annotations

from pathlib import Path

from mermicorn_boot.scaffold import scaffold
from mermicorn_boot.validate import validate


def test_scaffold_produces_valid_project(tmp_path: Path) -> None:
    target = tmp_path / "demo-lab"
    written = scaffold(
        target,
        repo_id="demo-lab",
        display_name="Demo Lab",
        lane="core",
        visibility="public",
        purpose_problem="Demonstrate a working mega-boot scaffold end to end.",
        first_proof="demo-scaffold-proof",
    )
    assert target.is_dir()
    assert (target / "mermicorn.repo.yaml").is_file()
    assert (target / "LICENSE").is_file()
    assert (target / "RIGHTS.md").is_file()
    assert "PROPRIETARY" in (target / "LICENSE").read_text(encoding="utf-8")
    assert (target / ".github" / "workflows" / "mermicorn-validate.yml").is_file()
    assert len(written) > 15

    result = validate(target, expect_id="demo-lab")
    assert result.ok, result.errors


def test_validate_fails_on_missing_contract(tmp_path: Path) -> None:
    empty = tmp_path / "empty"
    empty.mkdir()
    result = validate(empty)
    assert not result.ok
    assert any("mermicorn.repo.yaml" in e for e in result.errors)


def test_validate_rejects_bad_status(tmp_path: Path) -> None:
    target = tmp_path / "bad-status"
    scaffold(
        target,
        repo_id="bad-status",
        display_name="Bad Status",
        lane="core",
        purpose_problem="Should fail schema validation on purpose.",
        first_proof="none",
    )
    contract = target / "mermicorn.repo.yaml"
    text = contract.read_text(encoding="utf-8")
    text = text.replace("status: foundation", "status: not-a-real-status")
    contract.write_text(text, encoding="utf-8")

    result = validate(target, expect_id="bad-status")
    assert not result.ok
    assert any("status" in e.lower() for e in result.errors)

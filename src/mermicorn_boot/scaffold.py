"""Scaffold a compliant Mermicorn repository on disk."""

from __future__ import annotations

from pathlib import Path

from mermicorn_boot import templates
from mermicorn_boot.schema import REQUIRED_DIRS


def scaffold(
    target: Path,
    *,
    repo_id: str,
    display_name: str,
    lane: str,
    visibility: str = "public",
    purpose_problem: str,
    first_proof: str,
) -> list[Path]:
    """Create a full compliant project. Returns list of written paths."""
    target = target.resolve()
    if target.exists() and any(target.iterdir()):
        raise FileExistsError(f"Target is not empty: {target}")

    target.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    files: dict[str, str] = {
        "README.md": templates.readme(display_name, purpose_problem, first_proof, lane),
        "STATUS.md": templates.status(),
        "ROADMAP.md": templates.roadmap(first_proof),
        "ARCHITECTURE.md": templates.architecture(),
        "SECURITY.md": templates.security(),
        "CONTRIBUTING.md": templates.contributing(),
        "CHANGELOG.md": templates.changelog(),
        "agents.md": templates.agents(),
        "goals.md": templates.goals(first_proof),
        "quality.md": templates.quality(),
        "strategy.md": templates.strategy(),
        "RIGHTS.md": templates.rights(),
        "LICENSE": templates.proprietary_license(),
        "mermicorn.repo.yaml": templates.repo_yaml(
            repo_id, display_name, lane, visibility, purpose_problem, first_proof
        ),
        ".gitignore": templates.gitignore(),
    }

    for name, content in files.items():
        path = target / name
        path.write_text(content, encoding="utf-8")
        written.append(path)

    for dirname in REQUIRED_DIRS:
        d = target / dirname
        d.mkdir(parents=True, exist_ok=True)
        keep = d / ".gitkeep"
        keep.write_text("", encoding="utf-8")
        written.append(keep)

    workflows = target / ".github" / "workflows"
    workflows.mkdir(parents=True, exist_ok=True)
    wf = workflows / "mermicorn-validate.yml"
    wf.write_text(_validate_workflow(), encoding="utf-8")
    written.append(wf)

    issue_dir = target / ".github" / "ISSUE_TEMPLATE"
    issue_dir.mkdir(parents=True, exist_ok=True)
    issue = issue_dir / "task.md"
    issue.write_text(
        "---\nname: Task\nabout: Track work in this Mermicorn repository\n---\n\n## Goal\n\n## Definition of done\n\n",
        encoding="utf-8",
    )
    written.append(issue)

    return written


def _validate_workflow() -> str:
    return """name: mermicorn-validate

on:
  push:
    branches: [main]
  pull_request:

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install mermicorn-boot
        run: pip install -e ".[dev]" || pip install pyyaml jsonschema click
      - name: Validate contract
        run: |
          if command -v mermicorn-boot >/dev/null 2>&1; then
            mermicorn-boot validate .
          else
            python -c "import yaml, pathlib; p=pathlib.Path('mermicorn.repo.yaml'); assert p.exists(); yaml.safe_load(p.read_text())"
          fi
"""

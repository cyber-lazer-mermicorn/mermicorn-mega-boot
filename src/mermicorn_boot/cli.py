"""CLI entry point for mermicorn-boot."""

from __future__ import annotations

from pathlib import Path

import click

from mermicorn_boot import __version__
from mermicorn_boot.scaffold import scaffold
from mermicorn_boot.validate import validate


@click.group()
@click.version_option(__version__, prog_name="mermicorn-boot")
def main() -> None:
    """Mermicorn Mega Boot — scaffold and validate compliant projects."""


@main.command("create")
@click.argument("name")
@click.option("--lane", required=True, help="Lane value from the shared contract enum.")
@click.option("--display-name", default=None, help="Human display name (defaults to name).")
@click.option("--visibility", type=click.Choice(["public", "private"]), default="public")
@click.option("--purpose", required=True, help="One-sentence problem statement.")
@click.option("--first-proof", required=True, help="First proof artifact identifier.")
@click.option("--path", "base_path", type=click.Path(), default=".", help="Parent directory.")
def create_cmd(
    name: str,
    lane: str,
    display_name: str | None,
    visibility: str,
    purpose: str,
    first_proof: str,
    base_path: str,
) -> None:
    """Create a new compliant Mermicorn project (proprietary by default)."""
    target = Path(base_path).resolve() / name
    written = scaffold(
        target,
        repo_id=name,
        display_name=display_name or name.replace("-", " ").title(),
        lane=lane,
        visibility=visibility,
        purpose_problem=purpose,
        first_proof=first_proof,
    )
    click.echo(f"Created {target}")
    click.echo(f"Wrote {len(written)} paths")
    result = validate(target, expect_id=name)
    for w in result.warnings:
        click.echo(f"warning: {w}", err=True)
    if not result.ok:
        for e in result.errors:
            click.echo(f"error: {e}", err=True)
        raise SystemExit(1)
    click.echo("Validation: OK")


@main.command("validate")
@click.argument("path", type=click.Path(exists=True), default=".")
@click.option("--expect-id", default=None, help="Require contract id to match this value.")
def validate_cmd(path: str, expect_id: str | None) -> None:
    """Validate an existing Mermicorn repository."""
    result = validate(Path(path), expect_id=expect_id)
    for w in result.warnings:
        click.echo(f"warning: {w}", err=True)
    if result.ok:
        click.echo("Validation: OK")
        return
    for e in result.errors:
        click.echo(f"error: {e}", err=True)
    raise SystemExit(1)


if __name__ == "__main__":
    main()

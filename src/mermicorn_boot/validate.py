"""Validate an existing Mermicorn repository."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

from mermicorn_boot.schema import REPO_SCHEMA, REQUIRED_DIRS, REQUIRED_ROOT_FILES


@dataclass
class ValidationResult:
    ok: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def raise_if_failed(self) -> None:
        if not self.ok:
            raise SystemExit("\n".join(self.errors))


def validate(root: Path, *, expect_id: str | None = None) -> ValidationResult:
    root = root.resolve()
    result = ValidationResult(ok=True)

    if not root.is_dir():
        result.ok = False
        result.errors.append(f"Not a directory: {root}")
        return result

    for name in REQUIRED_ROOT_FILES:
        if not (root / name).is_file():
            result.ok = False
            result.errors.append(f"Missing required file: {name}")

    for name in REQUIRED_DIRS:
        if not (root / name).is_dir():
            result.warnings.append(f"Missing recommended directory: {name}/")

    contract_path = root / "mermicorn.repo.yaml"
    if contract_path.is_file():
        try:
            data = yaml.safe_load(contract_path.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            result.ok = False
            result.errors.append(f"Invalid YAML in mermicorn.repo.yaml: {exc}")
            return result

        validator = Draft202012Validator(REPO_SCHEMA)
        for error in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
            result.ok = False
            path = ".".join(str(p) for p in error.path) or "(root)"
            result.errors.append(f"Schema: {path}: {error.message}")

        if expect_id and isinstance(data, dict) and data.get("id") != expect_id:
            result.ok = False
            result.errors.append(
                f"id mismatch: contract has {data.get('id')!r}, expected {expect_id!r}"
            )

        # Soft check: directory name should match id when possible
        if isinstance(data, dict) and root.name != data.get("id"):
            result.warnings.append(
                f"Directory name {root.name!r} differs from contract id {data.get('id')!r}"
            )
    else:
        result.ok = False
        result.errors.append("Missing mermicorn.repo.yaml")

    return result

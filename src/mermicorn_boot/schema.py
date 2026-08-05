"""JSON Schema for mermicorn.repo.yaml."""

from __future__ import annotations

REPO_SCHEMA: dict = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://mermicorn.local/schemas/mermicorn-repo.schema.json",
    "title": "Mermicorn Repository Contract",
    "type": "object",
    "required": [
        "schema_version",
        "id",
        "display_name",
        "owner",
        "lane",
        "visibility",
        "status",
        "purpose",
        "shared_services",
        "privacy",
        "first_proof",
    ],
    "additionalProperties": False,
    "properties": {
        "schema_version": {"type": "string", "const": "1.0"},
        "id": {
            "type": "string",
            "pattern": "^[a-z0-9][a-z0-9-]{1,62}[a-z0-9]$",
            "description": "Must match repository name",
        },
        "display_name": {"type": "string", "minLength": 1},
        "owner": {"type": "string", "const": "cherry"},
        "lane": {
            "type": "string",
            "enum": [
                "identity-governance",
                "core",
                "passion-commerce",
                "commerce-service",
                "collectibles-commerce",
                "automotive-commerce",
                "gaming",
                "career",
            ],
        },
        "visibility": {"type": "string", "enum": ["public", "private"]},
        "status": {
            "type": "string",
            "enum": [
                "foundation",
                "building",
                "testing",
                "proof_ready",
                "published",
                "blocked",
                "archived",
            ],
        },
        "purpose": {
            "type": "object",
            "required": ["problem", "audience"],
            "properties": {
                "problem": {"type": "string", "minLength": 10},
                "audience": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 1,
                },
            },
            "additionalProperties": False,
        },
        "shared_services": {
            "type": "object",
            "properties": {
                "boot": {"type": "string"},
                "memory": {"type": "string"},
                "token_efficiency": {"type": "string"},
                "graphics": {"type": "string"},
                "commerce": {"type": "string"},
            },
            "additionalProperties": False,
        },
        "privacy": {
            "type": "object",
            "required": ["public", "private"],
            "properties": {
                "public": {"type": "array", "items": {"type": "string"}},
                "private": {"type": "array", "items": {"type": "string"}},
            },
            "additionalProperties": False,
        },
        "first_proof": {
            "type": "object",
            "required": ["artifact", "status"],
            "properties": {
                "artifact": {"type": "string", "minLength": 1},
                "status": {
                    "type": "string",
                    "enum": ["planned", "in-progress", "draft", "tested", "verified", "published"],
                },
            },
            "additionalProperties": False,
        },
    },
}

REQUIRED_ROOT_FILES = (
    "README.md",
    "STATUS.md",
    "ROADMAP.md",
    "ARCHITECTURE.md",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "agents.md",
    "goals.md",
    "quality.md",
    "strategy.md",
    "mermicorn.repo.yaml",
)

REQUIRED_DIRS = ("docs", "examples", "schemas", "tests", ".github")

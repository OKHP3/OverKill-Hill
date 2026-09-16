"""Shared loading and validation for the reviewed browser theme contract."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BRAND_THEME_CONTRACT_PATH = ROOT / "config" / "brand-theme-contract.json"
BRAND_THEME_REQUIRED_FIELDS = (
    "name",
    "bodyClass",
    "storageKey",
    "light",
    "dark",
    "colorScheme",
)
BRAND_THEME_COLOR_RE = re.compile(r"^#[0-9a-fA-F]{6}$")
BRAND_THEME_COLOR_SCHEMES = {"dark light", "light dark"}


def validate_brand_theme_contract(raw_contract: object) -> None:
    """Reject malformed brand theme metadata before generation or release."""
    if not isinstance(raw_contract, dict):
        raise ValueError("Brand theme contract must be a JSON object")

    brands = raw_contract.get("brands")
    if not isinstance(brands, dict) or not brands:
        raise ValueError("Brand theme contract must contain a non-empty 'brands' object")

    seen_names: dict[str, str] = {}
    seen_body_classes: dict[str, str] = {}
    for brand_id, brand in brands.items():
        label = f"brand {brand_id!r}"
        if not isinstance(brand_id, str) or not brand_id.strip():
            raise ValueError(f"Brand entry has an invalid identifier: {brand_id!r}")
        if not isinstance(brand, dict):
            raise ValueError(f"{label} must be a JSON object")

        missing = [field for field in BRAND_THEME_REQUIRED_FIELDS if field not in brand]
        if missing:
            raise ValueError(
                f"{label} is missing required field(s): {', '.join(missing)}"
            )

        for field in ("name", "bodyClass", "storageKey", "colorScheme"):
            value = brand[field]
            if not isinstance(value, str) or not value.strip():
                raise ValueError(
                    f"{label} has invalid {field!r}; expected a non-empty string"
                )

        for field in ("light", "dark"):
            value = brand[field]
            if not isinstance(value, str) or not BRAND_THEME_COLOR_RE.fullmatch(value):
                raise ValueError(
                    f"{label} has invalid {field} color {value!r}; "
                    "expected a six-digit hex color such as '#ffffff'"
                )

        color_scheme = " ".join(brand["colorScheme"].split())
        if color_scheme not in BRAND_THEME_COLOR_SCHEMES:
            expected = " or ".join(sorted(BRAND_THEME_COLOR_SCHEMES))
            raise ValueError(
                f"{label} has invalid 'colorScheme' value "
                f"{brand['colorScheme']!r}; expected {expected!r}"
            )

        name = brand["name"]
        if name in seen_names:
            raise ValueError(
                f"{label} duplicates brand name {name!r} "
                f"from brand {seen_names[name]!r}"
            )
        seen_names[name] = brand_id

        body_class = brand["bodyClass"]
        if body_class in seen_body_classes:
            raise ValueError(
                f"{label} duplicates body class {body_class!r} "
                f"from brand {seen_body_classes[body_class]!r}"
            )
        seen_body_classes[body_class] = brand_id


def load_brand_theme_contract(
    path: Path = BRAND_THEME_CONTRACT_PATH,
) -> dict[str, dict[str, str]]:
    """Load and validate the reviewed brand metadata contract."""
    try:
        raw_contract = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read brand theme contract {path}: {exc}") from exc
    validate_brand_theme_contract(raw_contract)
    return raw_contract["brands"]


def render_brand_theme_block(
    brands: dict[str, dict[str, str]],
) -> str:
    """Render the deterministic JavaScript block embedded in app.js."""
    serialized = json.dumps(brands, ensure_ascii=False, indent=2)
    return (
        "// BEGIN GENERATED BRAND THEME CONFIG. Do not edit this block.\n"
        f"const BRAND_THEME_CONFIG = Object.freeze({serialized});\n"
        "// END GENERATED BRAND THEME CONFIG.\n"
    )
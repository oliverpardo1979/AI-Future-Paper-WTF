"""Plot audited equilibrium paths on both sides of sigma_XL=1.

The chart compares the primary sigma_XL=0.90 and sigma_XL=1 paths with the
sigma_XL=1.10, z=16 finite-boundary path.  All series stop at t=4500, the
window independently shown to overlap across the z=8,12,16 upper-branch
solutions.  This script reads accepted CSVs and never invokes a solver.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Iterable

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import simulate_model as mechanism


RESULT_DIR = ROOT / "numerical_axm"
FIGURE_DIR = ROOT / "figures_axm"
OUTPUT = FIGURE_DIR / "axm_near_unit_equilibrium_paths.png"
DISPLAY_END = 4500.0
MANIFESTS = (
    RESULT_DIR / "near_unit_sigma090_audit_manifest.json",
    RESULT_DIR / "unit_elasticity_audit_manifest.json",
    RESULT_DIR / "near_unit_sigma110_window_audit_manifest.json",
)
LOWER_PATH = RESULT_DIR / "near_unit_sigma090_horizon_paths.csv"
UNIT_PATH = RESULT_DIR / "equilibrium_transition_paths.csv"
UPPER_PATH = RESULT_DIR / "near_unit_sigma110_window_boundary_paths.csv"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def hashed_entries(value: object) -> Iterable[dict[str, object]]:
    if isinstance(value, dict):
        if "path" in value and "sha256" in value:
            yield value
        for child in value.values():
            yield from hashed_entries(child)
    elif isinstance(value, list):
        for child in value:
            yield from hashed_entries(child)


def verify_inputs() -> None:
    declared: set[Path] = set()
    for manifest_path in MANIFESTS:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        accepted = manifest.get("accepted", manifest.get("overall_accepted"))
        if accepted is not True:
            raise ValueError(f"Audit manifest is not accepted: {manifest_path}")
        files_mapping = manifest.get("files", {})
        if isinstance(files_mapping, dict):
            for relative, metadata in files_mapping.items():
                if not isinstance(metadata, dict) or "sha256" not in metadata:
                    continue
                declared_name = metadata.get("path", relative)
                path = (ROOT / str(declared_name).replace("\\", "/")).resolve()
                if sha256(path) != str(metadata["sha256"]):
                    raise ValueError(f"Hash mismatch: {path}")
                declared.add(path)
        for entry in hashed_entries(manifest):
            path = (ROOT / str(entry["path"]).replace("\\", "/")).resolve()
            if sha256(path) != str(entry["sha256"]):
                raise ValueError(f"Hash mismatch: {path}")
            declared.add(path)
    required = {LOWER_PATH.resolve(), UNIT_PATH.resolve(), UPPER_PATH.resolve()}
    if not required.issubset(declared):
        missing = required.difference(declared)
        raise ValueError(f"Plotted files are not audit-bound: {sorted(missing)}")


def read(path: Path) -> list[dict[str, float | str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows: list[dict[str, float | str]] = list(csv.DictReader(handle))
    return rows


def select_rows() -> dict[str, list[dict[str, float | str]]]:
    lower = [
        row
        for row in read(LOWER_PATH)
        if math.isclose(float(row["horizon"]), 5600.0)
        and float(row["time"]) <= DISPLAY_END
    ]
    unit = [
        row
        for row in read(UNIT_PATH)
        if row["scenario"] == "axm_sigma_xl_1_hm_2"
        and float(row["time"]) <= DISPLAY_END
    ]
    upper = [
        row
        for row in read(UPPER_PATH)
        if math.isclose(float(row["terminal_boundary_z"]), 16.0)
        and float(row["time"]) <= DISPLAY_END
    ]
    result = {"lower": lower, "unit": unit, "upper": upper}
    for label, rows in result.items():
        if not rows or float(rows[-1]["time"]) < DISPLAY_END:
            raise ValueError(f"Incomplete displayed path: {label}")
    return result


def main() -> None:
    verify_inputs()
    rows = select_rows()
    labels = {
        "lower": "Final-production elasticity = 0.90",
        "unit": "Final-production elasticity = 1.00",
        "upper": "Final-production elasticity = 1.10",
    }
    palette = {
        "lower": mechanism.COLORS["blue"],
        "unit": mechanism.COLORS["ink"],
        "upper": mechanism.COLORS["orange"],
    }
    markers = {"lower": "circle", "unit": "diamond", "upper": "square"}
    percent = lambda observations, values: 100.0 * values
    mechanism.draw_multiplot(
        OUTPUT,
        "Equilibrium paths around unit elasticity",
        (
            "Same calibration and initial stocks; annual rates and income "
            "shares in percent; common audited window through model year 4,500"
        ),
        [
            {
                "title": "Output growth per capita",
                "field": "output_per_capita_growth",
                "transform": percent,
                "reference_y": 0.0,
                "adaptive_percent_min_decimals": 1,
            },
            {
                "title": "Real-wage growth",
                "field": "wage_growth",
                "transform": percent,
                "reference_y": 0.0,
                "adaptive_percent_min_decimals": 1,
            },
            {
                "title": "Net return to capital",
                "field": "net_capital_return",
                "transform": percent,
                "adaptive_percent_min_decimals": 1,
            },
            {
                "title": "Aggregate labor income / output",
                "field": "aggregate_labor_share",
                "transform": percent,
                "ylim": (0.0, 65.0),
                "adaptive_percent_min_decimals": 0,
            },
        ],
        rows,
        labels,
        palette,
        markers,
    )
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()

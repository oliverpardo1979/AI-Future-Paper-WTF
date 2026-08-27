"""Plot audited near-unit perturbations from the positive-AI BGP.

The script reads the accepted output of
``simulate_axm_near_unit_bgp_perturbation.py`` and never invokes a solver.
Every scenario has ``omega_X=0.20`` and the same predetermined initial stocks
from the analytical ``sigma_XL=1`` balanced-growth path.
"""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCAL_DEPS = ROOT / ".python-packages"
TMP_DEPS = ROOT / "tmp" / "pydeps"
if LOCAL_DEPS.exists():
    sys.path.insert(0, str(LOCAL_DEPS))
elif TMP_DEPS.exists():
    sys.path.insert(0, str(TMP_DEPS))
sys.path.insert(0, str(ROOT / "scripts"))

import numpy as np

import simulate_model as mechanism


RESULT_DIR = ROOT / "numerical_axm"
FIGURE_DIR = ROOT / "figures_axm"
OUTPUT = FIGURE_DIR / "axm_near_unit_equilibrium_paths.png"
MANIFEST_PATH = RESULT_DIR / "near_unit_bgp_perturbation_audit_manifest.json"
PATH_FILE = RESULT_DIR / "near_unit_bgp_perturbation_paths.csv"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_input() -> tuple[dict[str, object], float]:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if manifest.get("accepted") is not True:
        raise ValueError("The near-unit perturbation audit is not accepted.")
    files = manifest.get("files")
    if not isinstance(files, dict):
        raise ValueError("The manifest has no audit-bound files mapping.")
    relative = str(PATH_FILE.relative_to(ROOT)).replace("\\", "/")
    metadata = files.get(relative)
    if not isinstance(metadata, dict) or "sha256" not in metadata:
        raise ValueError(f"The plotted path is not audit-bound: {relative}")
    if sha256(PATH_FILE) != str(metadata["sha256"]):
        raise ValueError(f"Hash mismatch: {PATH_FILE}")
    return manifest, float(manifest["display_horizon"])


def read_paths(display_horizon: float) -> dict[str, list[dict[str, float | str]]]:
    with PATH_FILE.open("r", encoding="utf-8", newline="") as handle:
        observations: list[dict[str, float | str]] = list(csv.DictReader(handle))
    result: dict[str, list[dict[str, float | str]]] = {}
    for sigma_xl, key in ((0.99, "below"), (1.00, "unit"), (1.01, "above")):
        rows = [
            row
            for row in observations
            if np.isclose(float(row["sigma_xl"]), sigma_xl)
            and float(row["time"]) <= display_horizon
        ]
        if not rows or float(rows[-1]["time"]) < display_horizon:
            raise ValueError(f"Incomplete displayed path: {key}")
        result[key] = rows
    return result


def main() -> None:
    manifest, display_horizon = verify_input()
    rows = read_paths(display_horizon)
    labels = {
        "below": "sigma_XL = 0.99",
        "unit": "sigma_XL = 1.00",
        "above": "sigma_XL = 1.01",
    }
    palette = {
        "below": mechanism.COLORS["blue"],
        "unit": mechanism.COLORS["ink"],
        "above": mechanism.COLORS["orange"],
    }
    markers = {"below": "circle", "unit": "diamond", "above": "square"}
    times_one_hundred = lambda observations, values: 100.0 * values
    terminal = float(manifest["solver_terminal_horizon"])
    mechanism.draw_multiplot(
        OUTPUT,
        "Permanent near-unit elasticity perturbations",
        (
            "Same positive-AI BGP stocks at date 0; paths shown through year "
            f"{display_horizon:,.0f}; numerical terminal at year {terminal:,.0f}"
        ),
        [
            {
                "title": "Output per person: log gap x 100",
                "field": "log_output_relative_to_unit_bgp",
                "transform": times_one_hundred,
                "reference_y": 0.0,
                "adaptive_numeric_min_decimals": 0,
            },
            {
                "title": "Real wage: log gap x 100",
                "field": "log_wage_relative_to_unit_bgp",
                "transform": times_one_hundred,
                "reference_y": 0.0,
                "adaptive_numeric_min_decimals": 0,
            },
            {
                "title": "Net interest rate",
                "field": "net_interest",
                "transform": times_one_hundred,
                "adaptive_percent_min_decimals": 2,
            },
            {
                "title": "Labor income / output",
                "field": "labor_share",
                "transform": times_one_hundred,
                "adaptive_percent_min_decimals": 1,
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

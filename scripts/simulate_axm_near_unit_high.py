"""Continue the high-substitution equilibrium branch to sigma_XL=1.10.

The calculation starts from the audited sigma_XL=1.50, z=16 solution,
continues the same finite-boundary branch in sigma_XL, and then solves three
terminal output-capital boundaries at sigma_XL=1.10.  The reported comparison
uses only the common window Y/K<=5, strictly before the smallest boundary z=8.
"""

from __future__ import annotations

import math
import sys
import csv
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]
TMP_DEPS = ROOT / "tmp" / "pydeps"
LOCAL_DEPS = ROOT / ".python-packages"
if LOCAL_DEPS.exists():
    sys.path.insert(0, str(LOCAL_DEPS))
elif TMP_DEPS.exists():
    sys.path.insert(0, str(TMP_DEPS))
sys.path.insert(0, str(ROOT / "scripts"))

import numpy as np
import scipy  # noqa: F401
from scipy.interpolate import CubicSpline
from PIL import Image  # noqa: F401

import simulate_axm_equilibrium as core  # noqa: E402
import simulate_axm_high_sigma_equilibrium as high  # noqa: E402


OUTPUT = ROOT / "numerical_axm"
SOURCE = (
    ROOT
    / "numerical_axm"
    / "high_sigma_sigma150_validated_boundary_paths.csv"
)
SIGMA_SEQUENCE = (
    1.45,
    1.40,
    1.35,
    1.30,
    1.25,
    1.20,
    1.175,
    1.15,
    1.125,
    1.10,
)
BOUNDARY = 16.0
WINDOW_BOUNDARIES = (16.0, 12.0, 8.0)
SOLVER_TOLERANCE = 3e-5


def initial_state() -> tuple[float, float, float]:
    unit = replace(core.Parameters(), sigma_xl=1.0, sigma_hm=2.0, chi=0.01)
    guess = core.fixed_share_guess(
        unit,
        (1.0, 1.0, 1.0),
        horizon=1.0,
        mesh=np.asarray([0.0]),
    )
    return (math.exp(float(guess[0, 0])), 1.0, 1.0)


def load_source_boundary() -> object:
    with SOURCE.open("r", newline="", encoding="utf-8") as handle:
        rows = [
            row
            for row in csv.DictReader(handle)
            if math.isclose(float(row["terminal_boundary_z"]), BOUNDARY)
        ]
    times = np.asarray([float(row["time"]) for row in rows])
    fields = (
        "log_capital",
        "log_capability",
        "log_consumption",
        "log_shadow_value",
    )
    splines = [
        CubicSpline(
            times,
            np.asarray([float(row[field]) for row in rows]),
            bc_type="natural",
        )
        for field in fields
    ]

    def solution(values: np.ndarray | float) -> np.ndarray:
        return np.asarray([spline(values) for spline in splines])

    return SimpleNamespace(
        sol=solution,
        calendar_sol=solution,
        duration=float(times[-1]),
        normalized_domain=False,
    )


def enrich(
    rows: list[dict[str, float | str]],
    parameters: core.Parameters,
    boundary: float,
) -> None:
    for row in rows:
        row["alpha"] = parameters.alpha
        row["eta"] = parameters.eta
        row["sigma_xl"] = parameters.sigma_xl
        row["sigma_hm"] = parameters.sigma_hm
        row["terminal_boundary_z"] = boundary


def main() -> None:
    baseline = replace(core.Parameters(), sigma_hm=2.0, chi=0.01)
    stocks = initial_state()
    previous = load_source_boundary()
    print(
        f"source duration={previous.duration:.9f}; K0={stocks[0]:.12f}",
        flush=True,
    )
    for sigma in SIGMA_SEQUENCE:
        parameters = replace(baseline, sigma_xl=sigma)
        previous, _ = high.solve_high_sigma_equilibrium(
            parameters,
            stocks,
            terminal_output_capital_ratio=BOUNDARY,
            duration_guess=float(previous.duration),
            nodes=301,
            tolerance=3e-5,
            previous_solution=previous,
        )
        if not previous.success:
            raise RuntimeError(
                f"sigma={sigma:.3f} failed: {previous.message}"
            )
        initial = previous.sol(0.0)
        print(
            f"PASS sigma={sigma:.3f} T={previous.duration:.9f} "
            f"nodes={previous.x.size} "
            f"rms={float(np.max(previous.rms_residuals)):.3e} "
            f"logC0={float(initial[2]):.12f} "
            f"logq0={float(initial[3]):.12f}",
            flush=True,
        )

    parameters = replace(baseline, sigma_xl=1.10)
    saved_rows: dict[float, list[dict[str, float | str]]] = {}
    summaries: list[dict[str, float | str]] = []
    for boundary in WINDOW_BOUNDARIES:
        if boundary < WINDOW_BOUNDARIES[0]:
            previous, _ = high.solve_high_sigma_equilibrium(
                parameters,
                stocks,
                terminal_output_capital_ratio=boundary,
                duration_guess=float(previous.duration),
                nodes=401,
                tolerance=SOLVER_TOLERANCE,
                previous_solution=previous,
            )
            high._check_continuation_solution(
                previous, f"sigma=1.10 window boundary z={boundary:g}"
            )
        rows = high.evaluate_free_boundary_solution(
            f"near_unit_sigma_1.10_z_{boundary:g}",
            previous,
            parameters,
            step=1.0,
        )
        enrich(rows, parameters, boundary)
        saved_rows[boundary] = rows
        initial = previous.sol(0.0)
        summaries.append(
            {
                "terminal_boundary_z": boundary,
                "duration": float(previous.duration),
                "solver_tolerance": SOLVER_TOLERANCE,
                "max_rms_residual": float(np.max(previous.rms_residuals)),
                "mesh_nodes": int(previous.x.size),
                "initial_log_consumption": float(initial[2]),
                "initial_log_shadow_value": float(initial[3]),
                "source": (
                    "continued from the audited sigma_XL=1.50 z=16 path"
                    if boundary == BOUNDARY
                    else "boundary continuation from z=16"
                ),
            }
        )
        print(
            f"PASS z={boundary:g} T={previous.duration:.9f} "
            f"nodes={previous.x.size} "
            f"rms={float(np.max(previous.rms_residuals)):.3e}",
            flush=True,
        )

    high.write_rows(
        OUTPUT / "near_unit_sigma110_window_summary.csv", summaries
    )
    high.write_rows(
        OUTPUT / "near_unit_sigma110_window_boundary_paths.csv",
        [
            row
            for value in sorted(saved_rows)
            for row in saved_rows[value]
        ],
    )


if __name__ == "__main__":
    main()

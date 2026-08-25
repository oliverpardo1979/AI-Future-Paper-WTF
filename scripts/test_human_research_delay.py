"""Test whether human participation in AI research delays takeoff.

The paper's current numerical implementation calls AI capability ``A``.  The
reorganized Section 3 calls it ``B``.  This experiment preserves the existing
simulation field names (for example, ``log_capability``) and uses ``B`` only in
reader-facing labels.

The experiment reports two comparisons against the published
``omega_H=0.65`` equilibrium at ``sigma_XL=1.5``:

1. fixed research productivity ``chi``;
2. ``chi`` recalibrated in the ``omega_H=0`` benchmark so that initial
   capability growth equals the published equilibrium's initial value.

The second comparison separates the dynamic human bottleneck from the
one-time change in the level normalization of the research technology.
"""

from __future__ import annotations

import csv
import json
import math
from dataclasses import replace
from pathlib import Path
from typing import Iterable

import numpy as np

import simulate_axm_equilibrium as equilibrium
import simulate_axm_high_sigma_equilibrium as high_sigma


ROOT = Path(__file__).resolve().parents[1]
RESULT_DIR = ROOT / "numerical_axm"
FIGURE_DIR = ROOT / "figures_axm"
REFERENCE_PATH = (
    RESULT_DIR
    / "high_sigma_sigma150_z128_validated_boundary_paths.csv"
)
REFERENCE_CONVERGENCE_PATHS = (
    RESULT_DIR / "high_sigma_sigma150_validated_free_continuation.csv",
    RESULT_DIR
    / "high_sigma_sigma150_z128_validated_free_continuation.csv",
)
OUTPUT_PREFIX = "human_research_delay_sigma150"
SIGMA_SEQUENCE = high_sigma.PUBLISHED_SIGMA_SEQUENCE
HORIZON_SEQUENCE = high_sigma.PUBLISHED_HORIZON_SEQUENCE
COARSE_BOUNDARY_SEQUENCE = high_sigma.PUBLISHED_COARSE_FREE_BOUNDARY_SEQUENCE
REPORTED_BOUNDARIES = (16.0, 32.0, 64.0, 128.0)
PRELIMINARY_TOLERANCE = high_sigma.PUBLISHED_PRELIMINARY_TOLERANCE
REPORTED_TOLERANCE = high_sigma.PUBLISHED_REPORTED_TOLERANCE

# Preserve the exact predetermined initial state used by the published
# high-sigma continuation.  Its capital normalization comes from the current
# unit-elasticity equilibrium seed; capability and population start at one.
_REFERENCE_BASELINE = replace(
    equilibrium.Parameters(),
    chi=0.01,
    sigma_xl=1.0,
    sigma_hm=2.0,
)
_REFERENCE_SEED = equilibrium.fixed_share_guess(
    _REFERENCE_BASELINE,
    (1.0, 1.0, 1.0),
    horizon=1.0,
    mesh=np.asarray([0.0]),
)
INITIAL_STATE = (
    math.exp(float(_REFERENCE_SEED[0, 0])),
    1.0,
    1.0,
)


def read_rows(path: Path) -> list[dict[str, float | str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows: list[dict[str, float | str]] = []
        for raw in csv.DictReader(handle):
            row: dict[str, float | str] = {}
            for key, value in raw.items():
                if value is None:
                    row[key] = ""
                    continue
                try:
                    row[key] = float(value)
                except ValueError:
                    row[key] = value
            rows.append(row)
        return rows


def write_rows(
    path: Path,
    rows: Iterable[dict[str, float | str]],
) -> None:
    materialized = list(rows)
    if not materialized:
        raise ValueError(f"Cannot write an empty table to {path}.")
    fieldnames = list(
        dict.fromkeys(key for row in materialized for key in row)
    )
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(materialized)


def check_solution(solution: object, stage: str) -> None:
    if not solution.success:
        raise RuntimeError(f"{stage}: {solution.message}")
    maximum_residual = float(np.max(solution.rms_residuals))
    if not math.isfinite(maximum_residual):
        raise RuntimeError(f"{stage}: non-finite collocation residual.")
    print(
        f"{stage}: duration={float(solution.duration):.6f}, "
        f"nodes={solution.x.size}, max RMS={maximum_residual:.3e}",
        flush=True,
    )


def solve_zero_h_fixed_chi(
    chi: float,
    nodes: int = 301,
) -> tuple[
    equilibrium.Parameters,
    object,
    dict[float, object],
    list[dict[str, float]],
]:
    """Solve the exact omega_H=0 branch using the published continuation."""

    unit_parameters = replace(
        equilibrium.Parameters(),
        chi=chi,
        omega_m=1.0,
        sigma_hm=2.0,
        sigma_xl=1.0,
    )
    solution, _ = equilibrium.solve_equilibrium(
        unit_parameters,
        INITIAL_STATE,
        horizon=1600.0,
        nodes=nodes,
        tolerance=PRELIMINARY_TOLERANCE,
    )
    if not solution.success:
        raise RuntimeError(f"omega_H=0 unit seed: {solution.message}")
    solution.duration = 1600.0
    solution.normalized_domain = False
    solution.calendar_sol = solution.sol
    print(
        "omega_H=0 unit seed: "
        f"nodes={solution.x.size}, max RMS="
        f"{float(np.max(solution.rms_residuals)):.3e}",
        flush=True,
    )

    parameters = unit_parameters
    for sigma_xl in SIGMA_SEQUENCE:
        parameters = replace(unit_parameters, sigma_xl=sigma_xl)
        solution, _ = high_sigma.solve_high_sigma_fixed_horizon(
            parameters,
            INITIAL_STATE,
            horizon=100.0,
            terminal_z_guess=1.0,
            nodes=nodes,
            tolerance=PRELIMINARY_TOLERANCE,
            previous_solution=solution,
        )
        check_solution(solution, f"omega_H=0 sigma_XL={sigma_xl:g}")

    for horizon in HORIZON_SEQUENCE:
        solution, _ = high_sigma.solve_high_sigma_fixed_horizon(
            parameters,
            INITIAL_STATE,
            horizon=horizon,
            terminal_z_guess=1.0,
            nodes=nodes,
            tolerance=PRELIMINARY_TOLERANCE,
            previous_solution=solution,
        )
        check_solution(solution, f"omega_H=0 horizon={horizon:g}")

    for boundary in COARSE_BOUNDARY_SEQUENCE:
        solution, _ = high_sigma.solve_high_sigma_equilibrium(
            parameters,
            INITIAL_STATE,
            terminal_output_capital_ratio=boundary,
            duration_guess=float(solution.duration),
            nodes=nodes,
            tolerance=PRELIMINARY_TOLERANCE,
            previous_solution=solution,
        )
        check_solution(solution, f"omega_H=0 coarse z={boundary:g}")

    reported: dict[float, object] = {}
    convergence: list[dict[str, float]] = []
    for boundary in REPORTED_BOUNDARIES:
        solution, targets = high_sigma.solve_high_sigma_equilibrium(
            parameters,
            INITIAL_STATE,
            terminal_output_capital_ratio=boundary,
            duration_guess=float(solution.duration),
            nodes=nodes,
            tolerance=REPORTED_TOLERANCE,
            previous_solution=solution,
        )
        check_solution(solution, f"omega_H=0 refined z={boundary:g}")
        reported[boundary] = solution
        convergence.append(
            continuation_row(
                "omega_H=0; fixed chi",
                "fixed chi",
                parameters,
                solution,
                boundary,
                targets,
            )
        )
    return parameters, solution, reported, convergence


def initial_capability_growth(
    solution: object,
    parameters: equilibrium.Parameters,
) -> float:
    rates, _ = equilibrium.equilibrium_rates(
        0.0,
        solution.calendar_sol(0.0),
        parameters,
    )
    return float(rates[1])


def continue_in_chi(
    solution: object,
    parameters: equilibrium.Parameters,
    target_chi: float,
    nodes: int,
    steps: int = 4,
) -> tuple[object, equilibrium.Parameters]:
    """Move chi geometrically while holding the z=128 boundary fixed."""

    start_log = math.log(parameters.chi)
    target_log = math.log(target_chi)
    for fraction in np.linspace(0.0, 1.0, steps + 1)[1:]:
        next_chi = math.exp(start_log + float(fraction) * (target_log - start_log))
        next_parameters = replace(parameters, chi=next_chi)
        solution, _ = high_sigma.solve_high_sigma_equilibrium(
            next_parameters,
            INITIAL_STATE,
            terminal_output_capital_ratio=128.0,
            duration_guess=float(solution.duration),
            nodes=nodes,
            tolerance=PRELIMINARY_TOLERANCE,
            previous_solution=solution,
        )
        check_solution(solution, f"matched-growth chi={next_chi:.8f}")
        parameters = next_parameters
    return solution, parameters


def calibrate_zero_h_chi(
    fixed_solution: object,
    fixed_parameters: equilibrium.Parameters,
    target_initial_growth: float,
    nodes: int = 301,
) -> tuple[equilibrium.Parameters, object, list[dict[str, float]]]:
    """Choose chi so omega_H=0 matches the reference initial growth of B."""

    solution = fixed_solution
    parameters = fixed_parameters
    for iteration in range(6):
        current_growth = initial_capability_growth(solution, parameters)
        relative_error = current_growth / target_initial_growth - 1.0
        print(
            f"chi match iteration {iteration}: chi={parameters.chi:.9f}, "
            f"gB(0)={current_growth:.9f}, error={relative_error:.3e}",
            flush=True,
        )
        if abs(relative_error) <= 2e-4:
            break
        # With q fixed, g_B is proportional to chi**(1/(1-eta)).
        # Re-solving the BVP after each update allows q to adjust endogenously.
        target_chi = parameters.chi * (
            target_initial_growth / current_growth
        ) ** (1.0 - parameters.eta)
        solution, parameters = continue_in_chi(
            solution,
            parameters,
            target_chi,
            nodes=nodes,
        )
    else:
        raise RuntimeError("Could not match initial capability growth in chi.")

    # Re-establish boundary convergence under the final calibrated chi.
    convergence: list[dict[str, float]] = []
    for boundary in (64.0, 128.0):
        solution, targets = high_sigma.solve_high_sigma_equilibrium(
            parameters,
            INITIAL_STATE,
            terminal_output_capital_ratio=boundary,
            duration_guess=float(solution.duration),
            nodes=nodes,
            tolerance=REPORTED_TOLERANCE,
            previous_solution=solution,
        )
        check_solution(solution, f"matched-growth refined z={boundary:g}")
        convergence.append(
            continuation_row(
                "omega_H=0; matched initial g_B",
                "matched initial capability growth",
                parameters,
                solution,
                boundary,
                targets,
            )
        )
    final_error = (
        initial_capability_growth(solution, parameters)
        / target_initial_growth
        - 1.0
    )
    if abs(final_error) > 5e-4:
        raise RuntimeError(
            "Strict boundary refinement moved the initial-growth match: "
            f"relative error={final_error:.3e}."
        )
    return parameters, solution, convergence


def continuation_row(
    scenario: str,
    normalization: str,
    parameters: equilibrium.Parameters,
    solution: object,
    boundary: float,
    targets: dict[str, float],
) -> dict[str, float | str]:
    return {
        "scenario": scenario,
        "normalization": normalization,
        "omega_h": 1.0 - parameters.omega_m,
        "omega_m": parameters.omega_m,
        "chi": parameters.chi,
        "sigma_xl": parameters.sigma_xl,
        "sigma_hm": parameters.sigma_hm,
        "terminal_output_capital_ratio": boundary,
        "duration": float(solution.duration),
        "estimated_singularity_time": (
            float(solution.duration)
            + 1.0 / targets["singularity_rate"] / boundary
        ),
        "initial_capability_growth": initial_capability_growth(
            solution, parameters
        ),
        "mesh_nodes": float(solution.x.size),
        "max_rms_residual": float(np.max(solution.rms_residuals)),
    }


def first_crossing(
    rows: list[dict[str, float | str]],
    field: str,
    threshold: float,
    direction: str,
) -> float:
    ordered = sorted(rows, key=lambda row: float(row["time"]))
    for left, right in zip(ordered[:-1], ordered[1:]):
        left_value = float(left[field])
        right_value = float(right[field])
        crossed = (
            left_value < threshold <= right_value
            if direction == "up"
            else left_value > threshold >= right_value
        )
        if not crossed:
            continue
        if right_value == left_value:
            return float(right["time"])
        weight = (threshold - left_value) / (right_value - left_value)
        return float(left["time"]) + weight * (
            float(right["time"]) - float(left["time"])
        )
    first_value = float(ordered[0][field])
    if (direction == "up" and first_value >= threshold) or (
        direction == "down" and first_value <= threshold
    ):
        return float(ordered[0]["time"])
    return math.nan


def validation_metrics(
    rows: list[dict[str, float | str]],
) -> dict[str, float]:
    residual_fields = (
        "monopoly_foc_log_error",
        "final_production_log_error",
        "inference_identity_log_error",
        "research_ces_log_error",
        "research_compute_foc_log_error",
        "research_human_foc_log_error",
        "labor_market_error",
        "euler_residual",
        "capital_law_residual",
        "capability_law_residual",
        "consumption_euler_path_residual",
        "shadow_costate_residual",
    )
    return {
        "max_abs_equation_residual": max(
            abs(float(row[field]))
            for row in rows
            for field in residual_fields
        ),
        "max_abs_resource_residual": max(
            abs(float(row["resource_share_sum"]) - 1.0) for row in rows
        ),
        "minimum_consumption_share": min(
            float(row["consumption_share"]) for row in rows
        ),
        "minimum_investment_share": min(
            float(row["investment_share"]) for row in rows
        ),
        "minimum_monopoly_soc_margin": min(
            float(row["monopoly_soc_margin"]) for row in rows
        ),
    }


def scenario_summary(
    scenario: str,
    normalization: str,
    omega_h: float,
    chi: float,
    rows: list[dict[str, float | str]],
    singularity_time: float,
) -> dict[str, float | str]:
    initial = min(rows, key=lambda row: float(row["time"]))
    summary: dict[str, float | str] = {
        "scenario": scenario,
        "normalization": normalization,
        "omega_h": omega_h,
        "chi": chi,
        "initial_capability_growth": float(initial["capability_growth"]),
        "initial_output_per_capita_growth": float(
            initial["output_per_capita_growth"]
        ),
        "initial_aggregate_labor_share": float(
            initial["aggregate_labor_share"]
        ),
        "initial_automated_research_share": float(
            initial["automated_research_share"]
        ),
        "estimated_singularity_time": singularity_time,
    }
    for percentage in (0.02, 0.05, 0.10, 0.25, 1.00):
        summary[f"year_output_pc_growth_above_{percentage:g}"] = first_crossing(
            rows,
            "output_per_capita_growth",
            percentage,
            "up",
        )
    for share in (0.50, 0.25, 0.10):
        summary[f"year_labor_share_below_{share:g}"] = first_crossing(
            rows,
            "aggregate_labor_share",
            share,
            "down",
        )
    for share in (0.50, 0.90, 0.99):
        summary[f"year_research_automation_above_{share:g}"] = first_crossing(
            rows,
            "automated_research_share",
            share,
            "up",
        )
    summary.update(validation_metrics(rows))
    return summary


def comparison_rows(
    scenario_rows: dict[str, list[dict[str, float | str]]],
    metadata: dict[str, tuple[str, float, float]],
) -> list[dict[str, float | str]]:
    fields = (
        "time",
        "time_to_terminal",
        "log_capability",
        "log_output_per_capita",
        "capability_growth",
        "output_per_capita_growth",
        "wage_growth",
        "aggregate_labor_share",
        "human_research_share",
        "automated_research_share",
        "ai_share",
        "output_capital_ratio",
        "singularity_time_estimate",
    )
    output: list[dict[str, float | str]] = []
    for scenario, rows in scenario_rows.items():
        normalization, omega_h, chi = metadata[scenario]
        for row in rows:
            output.append(
                {
                    "scenario": scenario,
                    "normalization": normalization,
                    "omega_h": omega_h,
                    "chi": chi,
                    **{field: row[field] for field in fields},
                }
            )
    return output


def draw_comparison(
    scenario_rows: dict[str, list[dict[str, float | str]]],
) -> None:
    labels = {
        "humans_current": r"Human research (omega_H=0.65)",
        "zero_h_fixed": r"No human research; fixed chi",
        "zero_h_matched": r"No human research; matched initial g_B",
    }
    palette = {
        "humans_current": equilibrium.mechanism.COLORS["blue"],
        "zero_h_fixed": equilibrium.mechanism.COLORS["orange"],
        "zero_h_matched": equilibrium.mechanism.COLORS["pink"],
    }
    markers = {
        "humans_current": "circle",
        "zero_h_fixed": "square",
        "zero_h_matched": "triangle",
    }

    def log_growth(
        rows: list[dict[str, float | str]], values: np.ndarray
    ) -> np.ndarray:
        del rows
        return np.log10(np.maximum(100.0 * values, 1e-4))

    def log_growth_label(value: float) -> str:
        level = 10.0**value
        if level < 0.1:
            return f"{level:.2f}%"
        if level < 10.0:
            return f"{level:.1f}%"
        return f"{level:.0f}%"

    percent = lambda rows, values: 100.0 * values
    log_change = lambda rows, values: values - values[0]
    maximum_year = math.ceil(
        max(float(rows[-1]["singularity_time_estimate"]) for rows in scenario_rows.values())
        / 100.0
    ) * 100.0
    equilibrium.mechanism.draw_multiplot(
        FIGURE_DIR / f"{OUTPUT_PREFIX}_comparison.png",
        "Human participation in AI research and the timing of takeoff",
        (
            "Equilibrium paths at sigma_XL=1.5; growth-rate panels use a "
            "logarithmic percent scale"
        ),
        [
            {
                "title": "Output growth per capita",
                "field": "output_per_capita_growth",
                "transform": log_growth,
                "format": log_growth_label,
                "xlim": (0.0, maximum_year),
            },
            {
                "title": "AI capability growth",
                "field": "capability_growth",
                "transform": log_growth,
                "format": log_growth_label,
                "xlim": (0.0, maximum_year),
            },
            {
                "title": "Aggregate labor income share",
                "field": "aggregate_labor_share",
                "transform": percent,
                "format": lambda value: f"{value:.0f}%",
                "ylim": (0.0, 70.0),
                "xlim": (0.0, maximum_year),
            },
            {
                "title": "Automated contribution to AI research",
                "field": "automated_research_share",
                "transform": percent,
                "format": lambda value: f"{value:.0f}%",
                "ylim": (0.0, 100.0),
                "xlim": (0.0, maximum_year),
            },
        ],
        scenario_rows,
        labels,
        palette,
        markers,
    )


def reference_convergence_rows() -> list[dict[str, float | str]]:
    rows: list[dict[str, float | str]] = []
    for path in REFERENCE_CONVERGENCE_PATHS:
        for row in read_rows(path):
            rows.append(
                {
                    "scenario": "omega_H=0.65; published equilibrium",
                    "normalization": "fixed chi",
                    "omega_h": 0.65,
                    "omega_m": 0.35,
                    "chi": 0.01,
                    **row,
                }
            )
    return rows


def main() -> None:
    RESULT_DIR.mkdir(exist_ok=True)
    FIGURE_DIR.mkdir(exist_ok=True)
    reference_rows = read_rows(REFERENCE_PATH)
    reference_initial_growth = float(reference_rows[0]["capability_growth"])
    reference_tstar = float(reference_rows[-1]["singularity_time_estimate"])

    fixed_parameters, fixed_solution, _, fixed_convergence = (
        solve_zero_h_fixed_chi(chi=0.01)
    )
    fixed_rows = high_sigma.evaluate_free_boundary_solution(
        "omega_H=0; fixed chi",
        fixed_solution,
        fixed_parameters,
        step=1.0,
    )
    fixed_rows_path = RESULT_DIR / f"{OUTPUT_PREFIX}_zero_h_fixed_paths.csv"
    write_rows(fixed_rows_path, fixed_rows)

    matched_parameters, matched_solution, matched_convergence = (
        calibrate_zero_h_chi(
            fixed_solution,
            fixed_parameters,
            reference_initial_growth,
        )
    )
    matched_rows = high_sigma.evaluate_free_boundary_solution(
        "omega_H=0; matched initial g_B",
        matched_solution,
        matched_parameters,
        step=1.0,
    )
    matched_rows_path = (
        RESULT_DIR / f"{OUTPUT_PREFIX}_zero_h_matched_paths.csv"
    )
    write_rows(matched_rows_path, matched_rows)

    scenario_rows = {
        "humans_current": reference_rows,
        "zero_h_fixed": fixed_rows,
        "zero_h_matched": matched_rows,
    }
    metadata = {
        "humans_current": ("fixed chi", 0.65, 0.01),
        "zero_h_fixed": ("fixed chi", 0.0, fixed_parameters.chi),
        "zero_h_matched": (
            "matched initial capability growth",
            0.0,
            matched_parameters.chi,
        ),
    }
    compact_rows = comparison_rows(scenario_rows, metadata)
    write_rows(
        RESULT_DIR / f"{OUTPUT_PREFIX}_comparison_paths.csv",
        compact_rows,
    )

    fixed_tstar = float(fixed_rows[-1]["singularity_time_estimate"])
    matched_tstar = float(matched_rows[-1]["singularity_time_estimate"])
    summaries = [
        scenario_summary(
            "humans_current",
            "fixed chi",
            0.65,
            0.01,
            reference_rows,
            reference_tstar,
        ),
        scenario_summary(
            "zero_h_fixed",
            "fixed chi",
            0.0,
            fixed_parameters.chi,
            fixed_rows,
            fixed_tstar,
        ),
        scenario_summary(
            "zero_h_matched",
            "matched initial capability growth",
            0.0,
            matched_parameters.chi,
            matched_rows,
            matched_tstar,
        ),
    ]
    write_rows(
        RESULT_DIR / f"{OUTPUT_PREFIX}_summary.csv",
        summaries,
    )
    convergence = (
        reference_convergence_rows()
        + fixed_convergence
        + matched_convergence
    )
    write_rows(
        RESULT_DIR / f"{OUTPUT_PREFIX}_boundary_convergence.csv",
        convergence,
    )
    draw_comparison(scenario_rows)

    manifest = {
        "question": (
            "Does human participation in AI research delay takeoff when "
            "sigma_XL=1.5?"
        ),
        "reference_source": REFERENCE_PATH.relative_to(ROOT).as_posix(),
        "reference_omega_h": 0.65,
        "reference_chi": 0.01,
        "matched_zero_h_chi": matched_parameters.chi,
        "matched_initial_capability_growth_target": reference_initial_growth,
        "fixed_chi_comparison": True,
        "matched_initial_growth_comparison": True,
        "reported_boundaries_fixed_chi": REPORTED_BOUNDARIES,
        "reported_boundaries_matched_growth": (64.0, 128.0),
        "preliminary_tolerance": PRELIMINARY_TOLERANCE,
        "reported_tolerance": REPORTED_TOLERANCE,
        "outputs": {
            "summary": f"numerical_axm/{OUTPUT_PREFIX}_summary.csv",
            "comparison_paths": (
                f"numerical_axm/{OUTPUT_PREFIX}_comparison_paths.csv"
            ),
            "boundary_convergence": (
                f"numerical_axm/{OUTPUT_PREFIX}_boundary_convergence.csv"
            ),
            "zero_h_fixed_full_path": (
                fixed_rows_path.relative_to(ROOT).as_posix()
            ),
            "zero_h_matched_full_path": (
                matched_rows_path.relative_to(ROOT).as_posix()
            ),
            "figure": f"figures_axm/{OUTPUT_PREFIX}_comparison.png",
        },
    }
    with (
        RESULT_DIR / f"{OUTPUT_PREFIX}_manifest.json"
    ).open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)

    print("Human-research delay experiment complete.", flush=True)
    for row in summaries:
        print(
            f"  {row['scenario']}: chi={float(row['chi']):.8f}, "
            f"gB0={float(row['initial_capability_growth']):.6f}, "
            f"T*={float(row['estimated_singularity_time']):.3f}",
            flush=True,
        )


if __name__ == "__main__":
    main()

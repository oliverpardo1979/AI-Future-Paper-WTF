"""Simulate permanent near-unit elasticity perturbations from the AI BGP.

All scenarios keep ``omega_X = 0.20`` and inherit the same predetermined
stocks from the analytical ``sigma_XL = 1`` balanced-growth path.  At date
zero, ``sigma_XL`` is set permanently to 0.99, 1.00, or 1.01.  Consumption and
the shadow value of capability are jump variables selected by the same
finite-window boundary-value problem in every scenario.

The calculation is a controlled comparison on a common finite window.  It
does not impose or infer a common long-run limit for nonunit elasticities.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
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

from define_positive_ai_branch import (  # noqa: E402
    PositiveAIBalancedGrowth,
    PositiveAIBenchmarkParameters,
    balanced_growth_seed,
)
from solve_near_unit_ai_bvp import (  # noqa: E402
    NearUnitAITransitionSolution,
    audit_near_unit_solution,
    elasticity_coordinate,
    solve_monopoly_static_block,
    solve_near_unit_transition,
)
from solve_positive_ai_bvp import solve_transition  # noqa: E402


RESULT_DIR = ROOT / "numerical_axm"
PATH_FILE = RESULT_DIR / "near_unit_bgp_perturbation_paths.csv"
SUMMARY_FILE = RESULT_DIR / "near_unit_bgp_perturbation_summary.csv"
MANIFEST_FILE = RESULT_DIR / "near_unit_bgp_perturbation_audit_manifest.json"

SIGMA_VALUES = (0.99, 1.00, 1.01)
DISPLAY_HORIZON = 2_500.0
SOLVER_HORIZONS = tuple(float(year) for year in range(100, 3_001, 100))
HORIZON_AUDIT_HORIZONS = tuple(
    float(year) for year in range(100, 3_501, 100)
)
COMMON_AUDIT_WINDOW = DISPLAY_HORIZON
PATH_STEP = 1.0
TOLERANCE = 1.0e-9
BOUNDARY_TOLERANCE = 1.0e-11
INITIAL_NODES = 181
MAXIMUM_NODES = 50_000
ELASTICITY_STEPS = 8


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_csv(path: Path, rows: list[dict[str, float | str]]) -> None:
    if not rows:
        raise ValueError(f"Cannot write an empty CSV: {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def evaluate_path(
    solution: NearUnitAITransitionSolution,
    times: np.ndarray,
) -> list[dict[str, float | str]]:
    """Reconstruct levels, prices, growth rates, and income shares."""

    parameters = solution.parameters
    seed = solution.seed
    deviations = np.asarray(solution.raw.sol(times), dtype=float)
    derivative_deviations = np.asarray(solution.raw.sol(times, 1), dtype=float)
    reference_initial = np.log(
        np.asarray(
            [seed.capital, seed.capability, seed.consumption, seed.shadow_value]
        )
    )
    reference_rates = np.asarray(
        [
            seed.output_growth,
            seed.capability_growth,
            seed.output_growth,
            seed.shadow_value_growth,
        ]
    )
    raw_logs = (
        reference_initial[:, None]
        + reference_rates[:, None] * times[None, :]
        + deviations
    )
    raw_growth = reference_rates[:, None] + derivative_deviations
    effective_labor_growth = (
        parameters.population_growth + parameters.labor_productivity_growth
    )
    unit_log_ai_labor_ratio = (
        math.log(seed.ai_services)
        - math.log(seed.labor_productivity * seed.population)
        + (
            seed.capability_growth
            + seed.output_growth
            - effective_labor_growth
        )
        * times
    )
    varphi = elasticity_coordinate(solution.sigma_xl)

    rows: list[dict[str, float | str]] = []
    for index, time in enumerate(times):
        log_capital, log_capability, log_consumption, log_shadow = raw_logs[
            :, index
        ]
        capital_growth, capability_growth, consumption_growth, shadow_growth = (
            raw_growth[:, index]
        )
        log_population = (
            math.log(parameters.initial_population)
            + parameters.population_growth * float(time)
        )
        log_effective_labor = (
            math.log(parameters.initial_labor_productivity)
            + math.log(parameters.initial_population)
            + effective_labor_growth * float(time)
        )
        static = solve_monopoly_static_block(
            float(log_capital),
            float(log_capability),
            log_effective_labor,
            solution.sigma_xl,
            parameters,
        )
        log_research = (
            log_shadow
            + math.log(parameters.chi)
            + math.log(parameters.eta)
            + parameters.eta * log_capability
        ) / (1.0 - parameters.eta)
        output_capital_ratio = math.exp(static.log_output - log_capital)
        net_interest = (
            parameters.alpha * output_capital_ratio
            - parameters.depreciation
        )
        log_wage = (
            math.log1p(-parameters.alpha)
            + math.log1p(-static.ai_ces_share)
            + static.log_output
            - log_population
        )
        inference_share = math.exp(
            static.log_inference_compute - static.log_output
        )
        research_share = math.exp(log_research - static.log_output)
        labor_share = (
            (1.0 - parameters.alpha) * (1.0 - static.ai_ces_share)
        )
        gross_capital_share = parameters.alpha
        profit_share = (
            (1.0 - parameters.alpha) * static.ai_ces_share
            - inference_share
            - research_share
        )
        accounting_residual = (
            gross_capital_share
            + labor_share
            + profit_share
            + inference_share
            + research_share
            - 1.0
        )

        ratio_capital_gradient = (
            static.ai_services_log_gradient[0]
        )
        ratio_capability_gradient = (
            static.ai_services_log_gradient[1]
        )
        ratio_labor_gradient = parameters.alpha / static.monopoly_derivative
        ai_labor_ratio_growth = (
            ratio_capital_gradient * capital_growth
            + ratio_capability_gradient * capability_growth
            + ratio_labor_gradient * effective_labor_growth
        )
        output_labor_gradient = (
            (1.0 - parameters.alpha)
            * (
                1.0
                + static.ai_ces_share * ratio_labor_gradient
            )
        )
        output_growth = (
            static.output_log_gradient[0] * capital_growth
            + static.output_log_gradient[1] * capability_growth
            + output_labor_gradient * effective_labor_growth
        )
        wage_growth = (
            output_growth
            - parameters.population_growth
            - varphi * static.ai_ces_share * ai_labor_ratio_growth
        )

        reference_log_output = math.log(seed.output) + seed.output_growth * time
        reference_log_wage = (
            math.log(seed.wage)
            + (seed.output_growth - parameters.population_growth) * time
        )
        rows.append(
            {
                "scenario": f"sigma_xl_{solution.sigma_xl:.4f}",
                "sigma_xl": float(solution.sigma_xl),
                "time": float(time),
                "log_capital": float(log_capital),
                "log_capability": float(log_capability),
                "log_consumption": float(log_consumption),
                "log_shadow_value": float(log_shadow),
                "log_output": float(static.log_output),
                "log_wage": float(log_wage),
                "log_ai_services": float(static.log_ai_services),
                "log_inference_compute": float(static.log_inference_compute),
                "log_research_compute": float(log_research),
                "log_output_relative_to_unit_bgp": float(
                    static.log_output - reference_log_output
                ),
                "log_wage_relative_to_unit_bgp": float(
                    log_wage - reference_log_wage
                ),
                "log_capability_relative_to_unit_bgp": float(
                    deviations[1, index]
                ),
                "log_ai_labor_ratio": float(static.log_ai_labor_ratio),
                "log_ai_labor_ratio_relative_to_unit_bgp": float(
                    static.log_ai_labor_ratio
                    - unit_log_ai_labor_ratio[index]
                ),
                "capital_growth": float(capital_growth),
                "capability_growth": float(capability_growth),
                "consumption_growth": float(consumption_growth),
                "shadow_value_growth": float(shadow_growth),
                "output_growth": float(output_growth),
                "output_per_capita_growth": float(
                    output_growth - parameters.population_growth
                ),
                "wage_growth": float(wage_growth),
                "net_interest": float(net_interest),
                "ai_ces_share": float(static.ai_ces_share),
                "gross_capital_share": float(gross_capital_share),
                "labor_share": float(labor_share),
                "profit_share": float(profit_share),
                "inference_share": float(inference_share),
                "research_share": float(research_share),
                "accounting_residual": float(accounting_residual),
                "monopoly_foc_log_residual": float(
                    static.monopoly_foc_log_residual
                ),
                "monopoly_soc_margin": float(static.monopoly_soc_margin),
            }
        )
    return rows


def _solve_unit_reference(
    parameters: PositiveAIBenchmarkParameters,
    seed: PositiveAIBalancedGrowth,
    horizons: tuple[float, ...],
    *,
    nodes: int,
    tolerance: float,
):
    return solve_transition(
        parameters,
        seed.capital,
        seed.capability,
        horizons=horizons,
        continuation_steps=1,
        initial_nodes=nodes,
        tolerance=tolerance,
        boundary_tolerance=BOUNDARY_TOLERANCE,
        maximum_nodes=MAXIMUM_NODES,
    )


def _solve_scenario(
    parameters: PositiveAIBenchmarkParameters,
    seed: PositiveAIBalancedGrowth,
    sigma_xl: float,
    unit_solution,
    horizons: tuple[float, ...],
    *,
    nodes: int,
    tolerance: float,
    elasticity_steps: int,
) -> NearUnitAITransitionSolution:
    return solve_near_unit_transition(
        parameters,
        seed.capital,
        seed.capability,
        sigma_xl,
        accepted_unit_solution=unit_solution,
        horizons=horizons,
        stock_continuation_steps=1,
        elasticity_continuation_steps=elasticity_steps,
        initial_nodes=nodes,
        tolerance=tolerance,
        boundary_tolerance=BOUNDARY_TOLERANCE,
        maximum_nodes=MAXIMUM_NODES,
    )


def solve_experiment() -> tuple[
    list[dict[str, float | str]],
    list[dict[str, float | str]],
    dict[str, object],
]:
    parameters = PositiveAIBenchmarkParameters(omega_x=0.20)
    seed = balanced_growth_seed(parameters)
    unit_solution = _solve_unit_reference(
        parameters,
        seed,
        SOLVER_HORIZONS,
        nodes=INITIAL_NODES,
        tolerance=TOLERANCE,
    )
    times = np.arange(0.0, DISPLAY_HORIZON + 0.5 * PATH_STEP, PATH_STEP)
    common_times = np.linspace(0.0, COMMON_AUDIT_WINDOW, 501)
    solutions: dict[float, NearUnitAITransitionSolution] = {}
    path_rows: list[dict[str, float | str]] = []
    audits: dict[str, dict[str, float | bool | int]] = {}

    for sigma_xl in SIGMA_VALUES:
        solution = _solve_scenario(
            parameters,
            seed,
            sigma_xl,
            unit_solution,
            SOLVER_HORIZONS,
            nodes=INITIAL_NODES,
            tolerance=TOLERANCE,
            elasticity_steps=ELASTICITY_STEPS,
        )
        solutions[sigma_xl] = solution
        path_rows.extend(evaluate_path(solution, times))
        audits[f"sigma_xl_{sigma_xl:.4f}"] = audit_near_unit_solution(
            solution, sample_points=1_001
        )

    # The plotted path stops 500 years before its terminal projection.  I
    # rebuild the reference and both nonunit paths with a terminal 500 years
    # farther out and compare the entire displayed window.
    horizon_audit_unit = _solve_unit_reference(
        parameters,
        seed,
        HORIZON_AUDIT_HORIZONS,
        nodes=121,
        tolerance=1.0e-8,
    )
    horizon_gaps: dict[str, float] = {}
    for sigma_xl in (SIGMA_VALUES[0], SIGMA_VALUES[-1]):
        horizon_audit = _solve_scenario(
            parameters,
            seed,
            sigma_xl,
            horizon_audit_unit,
            HORIZON_AUDIT_HORIZONS,
            nodes=121,
            tolerance=1.0e-8,
            elasticity_steps=6,
        )
        horizon_gaps[f"sigma_xl_{sigma_xl:.4f}"] = float(
            np.max(
                np.abs(
                    horizon_audit.evaluate_deviations(common_times)
                    - solutions[sigma_xl].evaluate_deviations(common_times)
                )
            )
        )

    # A lower-accuracy implementation should recover the same initial window.
    base_unit = _solve_unit_reference(
        parameters,
        seed,
        SOLVER_HORIZONS,
        nodes=121,
        tolerance=1.0e-8,
    )
    refinement_gaps: dict[str, float] = {}
    for sigma_xl in (SIGMA_VALUES[0], SIGMA_VALUES[-1]):
        base = _solve_scenario(
            parameters,
            seed,
            sigma_xl,
            base_unit,
            SOLVER_HORIZONS,
            nodes=121,
            tolerance=1.0e-8,
            elasticity_steps=4,
        )
        refinement_gaps[f"sigma_xl_{sigma_xl:.4f}"] = float(
            np.max(
                np.abs(
                    base.evaluate_deviations(common_times)
                    - solutions[sigma_xl].evaluate_deviations(common_times)
                )
            )
        )

    scenario_rows = {
        sigma_xl: [
            row for row in path_rows if float(row["sigma_xl"]) == sigma_xl
        ]
        for sigma_xl in SIGMA_VALUES
    }
    summary_rows: list[dict[str, float | str]] = []
    for sigma_xl, rows in scenario_rows.items():
        for target_time in (
            0.0,
            500.0,
            1_000.0,
            1_500.0,
            2_000.0,
            2_500.0,
        ):
            row = min(rows, key=lambda item: abs(float(item["time"]) - target_time))
            summary_rows.append(
                {
                    "sigma_xl": sigma_xl,
                    "time": float(row["time"]),
                    "output_pc_log_gap": float(
                        row["log_output_relative_to_unit_bgp"]
                    ),
                    "wage_log_gap": float(
                        row["log_wage_relative_to_unit_bgp"]
                    ),
                    "output_pc_growth": float(row["output_per_capita_growth"]),
                    "wage_growth": float(row["wage_growth"]),
                    "net_interest": float(row["net_interest"]),
                    "labor_share": float(row["labor_share"]),
                    "ai_ces_share": float(row["ai_ces_share"]),
                }
            )

    maximum_accounting_residual = max(
        abs(float(row["accounting_residual"])) for row in path_rows
    )
    maximum_static_residual = max(
        abs(float(row["monopoly_foc_log_residual"])) for row in path_rows
    )
    minimum_soc_margin = min(
        float(row["monopoly_soc_margin"]) for row in path_rows
    )
    maximum_solver_residual = max(
        float(audit["max_normalized_ode_residual"])
        for audit in audits.values()
    )
    maximum_backward_gap = max(
        float(audit["segmented_backward_reconstruction_gap"])
        for audit in audits.values()
    )
    maximum_horizon_gap = max(horizon_gaps.values())
    maximum_refinement_gap = max(refinement_gaps.values())
    gates = {
        "all_solvers_successful": all(
            bool(audit["success"]) for audit in audits.values()
        ),
        "equilibrium_residuals": maximum_solver_residual < 2.0e-8,
        "backward_reconstruction": maximum_backward_gap < 2.0e-8,
        "accounting_closure": maximum_accounting_residual < 1.0e-12,
        "monopoly_foc": maximum_static_residual < 2.0e-11,
        "monopoly_soc": minimum_soc_margin > 0.0,
        "horizon_stability": maximum_horizon_gap < 2.0e-4,
        "refinement_stability": maximum_refinement_gap < 2.0e-6,
    }
    manifest: dict[str, object] = {
        "accepted": all(gates.values()),
        "interpretation": (
            "Permanent sigma_XL perturbations from common unit-elastic BGP "
            "stocks; accepted only on the displayed finite window."
        ),
        "parameters": {
            "omega_x": parameters.omega_x,
            "sigma_xl_values": SIGMA_VALUES,
            "initial_capital": seed.capital,
            "initial_capability": seed.capability,
        },
        "display_horizon": DISPLAY_HORIZON,
        "solver_terminal_horizon": SOLVER_HORIZONS[-1],
        "horizon_audit_terminal_horizon": HORIZON_AUDIT_HORIZONS[-1],
        "common_audit_window": COMMON_AUDIT_WINDOW,
        "audits": audits,
        "horizon_gaps": horizon_gaps,
        "refinement_gaps": refinement_gaps,
        "maximum_accounting_residual": maximum_accounting_residual,
        "maximum_static_residual": maximum_static_residual,
        "minimum_monopoly_soc_margin": minimum_soc_margin,
        "maximum_solver_residual": maximum_solver_residual,
        "maximum_backward_gap": maximum_backward_gap,
        "maximum_horizon_gap": maximum_horizon_gap,
        "maximum_refinement_gap": maximum_refinement_gap,
        "gates": gates,
    }
    return path_rows, summary_rows, manifest


def main() -> None:
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    path_rows, summary_rows, manifest = solve_experiment()
    write_csv(PATH_FILE, path_rows)
    write_csv(SUMMARY_FILE, summary_rows)
    manifest["files"] = {
        PATH_FILE.relative_to(ROOT).as_posix(): {
            "sha256": sha256_file(PATH_FILE),
            "rows": len(path_rows),
        },
        SUMMARY_FILE.relative_to(ROOT).as_posix(): {
            "sha256": sha256_file(SUMMARY_FILE),
            "rows": len(summary_rows),
        },
    }
    MANIFEST_FILE.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if not bool(manifest["accepted"]):
        raise RuntimeError("Near-unit BGP perturbation failed acceptance gates.")
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

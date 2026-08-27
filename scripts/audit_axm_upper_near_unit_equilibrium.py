"""Audit the missing upper near-unit branch under the equilibrium definition.

The finite-window continuation around ``sigma_XL = 1`` does not supply an
infinite-horizon terminal condition when ``sigma_XL > 1``.  This audit keeps
the agreed continuation order: it starts from the exact strictly-positive-AI
unit-elastic equilibrium, moves to the target elasticity on a short horizon,
and then lengthens the horizon while imposing the gross-substitutes terminal
ratios.  The calculation is classified as a pre-singular necessary-condition
branch unless a separate admissible infinite-horizon tail is found.

The script deliberately writes no trajectory for plotting.  Its output is a
machine-readable admission audit, not a source of paper figures.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import replace
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
LOCAL_DEPS = ROOT / ".python-packages"
TMP_DEPS = ROOT / "tmp" / "pydeps"
if LOCAL_DEPS.exists():
    sys.path.insert(0, str(LOCAL_DEPS))
elif TMP_DEPS.exists():
    sys.path.insert(0, str(TMP_DEPS))
sys.path.insert(0, str(ROOT / "scripts"))

from define_positive_ai_branch import (  # noqa: E402
    PositiveAIBenchmarkParameters,
    balanced_growth_seed,
)
import simulate_axm_equilibrium as equilibrium  # noqa: E402
import simulate_axm_high_sigma_equilibrium as high_sigma  # noqa: E402


OUTPUT = (
    ROOT / "numerical_axm" / "upper_near_unit_equilibrium_audit.json"
)
DEFAULT_HORIZONS = (
    100.0,
    150.0,
    200.0,
    300.0,
    400.0,
    600.0,
    800.0,
    900.0,
    1_000.0,
    1_100.0,
    1_200.0,
    1_400.0,
    1_600.0,
    1_800.0,
    2_000.0,
    2_200.0,
    2_400.0,
    2_600.0,
    2_800.0,
    3_000.0,
    3_200.0,
    3_400.0,
    3_600.0,
    3_800.0,
    4_000.0,
    4_200.0,
    4_400.0,
    4_600.0,
    4_800.0,
    5_000.0,
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sigma-xl", type=float, default=1.01)
    parser.add_argument(
        "--horizons",
        default=",".join(f"{value:g}" for value in DEFAULT_HORIZONS),
        help="Comma-separated fixed-horizon continuation schedule.",
    )
    parser.add_argument("--tolerance", type=float, default=1.0e-4)
    parser.add_argument("--nodes", type=int, default=161)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    return parser.parse_args()


def canonical_problem(
    sigma_xl: float,
) -> tuple[
    PositiveAIBenchmarkParameters,
    equilibrium.Parameters,
    equilibrium.Parameters,
    tuple[float, float, float],
]:
    if sigma_xl <= 1.0:
        raise ValueError("The upper near-unit audit requires sigma_XL > 1.")
    benchmark = PositiveAIBenchmarkParameters(omega_x=0.20)
    seed = balanced_growth_seed(benchmark)
    unit = equilibrium.Parameters(
        alpha=benchmark.alpha,
        omega_x=benchmark.omega_x,
        sigma_xl=1.0,
        n=benchmark.population_growth,
        labor_productivity_growth=benchmark.labor_productivity_growth,
        initial_labor_productivity=benchmark.initial_labor_productivity,
        delta=benchmark.depreciation,
        discount=benchmark.discount,
        omega_m=1.0,
        sigma_hm=2.0,
        eta=benchmark.eta,
        chi=benchmark.chi,
    )
    target = replace(unit, sigma_xl=float(sigma_xl))
    stocks = (
        seed.capital,
        seed.capability,
        benchmark.initial_population,
    )
    return benchmark, unit, target, stocks


def terminal_diagnostics(
    solution: object,
    parameters: equilibrium.Parameters,
    horizon: float,
) -> dict[str, float]:
    terminal = np.asarray(solution.sol(horizon), dtype=float)
    rates, block = equilibrium.equilibrium_rates(
        horizon, terminal, parameters
    )
    return {
        "terminal_output_capital_ratio": math.exp(
            float(block["log_output"]) - float(terminal[0])
        ),
        "terminal_ai_share": float(block["ai_share"]),
        "terminal_capability_growth": float(rates[1]),
        "terminal_net_interest": float(block["gross_capital_return"])
        - parameters.delta,
    }


def run_audit(
    sigma_xl: float,
    horizons: tuple[float, ...],
    tolerance: float,
    nodes: int,
) -> dict[str, object]:
    if not horizons or horizons[0] != 100.0:
        raise ValueError("The audited continuation must start at T=100.")
    if any(right <= left for left, right in zip(horizons, horizons[1:])):
        raise ValueError("Continuation horizons must be strictly increasing.")

    benchmark, unit, target, stocks = canonical_problem(sigma_xl)
    unit_solution, _ = equilibrium.solve_equilibrium(
        unit,
        stocks,
        horizon=horizons[0],
        nodes=nodes,
        tolerance=min(tolerance, 1.0e-7),
    )
    if not bool(unit_solution.success):
        raise RuntimeError(f"Unit seed failed: {unit_solution.message}")
    unit_solution.duration = horizons[0]
    unit_solution.normalized_domain = False
    unit_solution.calendar_sol = unit_solution.sol

    previous: object = unit_solution
    records: list[dict[str, float | int | bool | str]] = []
    for horizon in horizons:
        solution, _ = high_sigma.solve_high_sigma_fixed_horizon(
            target,
            stocks,
            horizon=horizon,
            terminal_z_guess=1.0,
            nodes=nodes,
            tolerance=tolerance,
            previous_solution=previous,
        )
        initial = np.asarray(solution.sol(0.0), dtype=float)
        record: dict[str, float | int | bool | str] = {
            "horizon": horizon,
            "success": bool(solution.success),
            "message": str(solution.message),
            "nodes": int(solution.x.size),
            "maximum_rms_residual": float(
                np.max(np.asarray(solution.rms_residuals, dtype=float))
            ),
            "log_initial_consumption": float(initial[2]),
            "log_initial_shadow_value": float(initial[3]),
        }
        if bool(solution.success):
            record.update(terminal_diagnostics(solution, target, horizon))
        records.append(record)
        print(json.dumps(record, sort_keys=True), flush=True)
        if not bool(solution.success):
            break
        previous = solution

    all_solved = len(records) == len(horizons) and all(
        bool(record["success"]) for record in records
    )
    varphi = (sigma_xl - 1.0) / sigma_xl
    effective_labor_growth = (
        benchmark.population_growth
        + benchmark.labor_productivity_growth
    )
    complement_capability_growth = benchmark.eta * effective_labor_growth
    separation_rate = varphi * complement_capability_growth
    final_record = records[-1]
    return {
        "accepted": False,
        "classification": (
            "finite_horizon_pre_singular_necessary_condition_branch"
        ),
        "reason_not_admitted": (
            "No admissible regular infinite-horizon tail was found. A "
            "regular bounded-capability tail contradicts the developer "
            "costate equation, while the regular unbounded AI-dominated "
            "tail reaches a finite-time singularity. The latter is only a "
            "maximal pre-singular necessary-condition branch."
        ),
        "sigma_xl": sigma_xl,
        "omega_x": benchmark.omega_x,
        "initial_stocks": {
            "capital": stocks[0],
            "capability": stocks[1],
            "population": stocks[2],
        },
        "continuation_settings": {
            "horizons": horizons,
            "solver_tolerance": tolerance,
            "initial_nodes": nodes,
        },
        "fixed_horizon_continuation_completed": all_solved,
        "finite_window_diagnostics": {
            "last_horizon": float(final_record["horizon"]),
            "terminal_ai_share": final_record.get("terminal_ai_share"),
            "distance_from_ai_dominated_share_limit": (
                1.0 - float(final_record["terminal_ai_share"])
                if "terminal_ai_share" in final_record
                else None
            ),
            "near_unit_separation_rate": separation_rate,
            "inverse_near_unit_separation_rate": 1.0 / separation_rate,
            "interpretation": (
                "Near-unit separation is slow on finite windows. Agreement "
                "of initial jumps does not supply a valid infinite-horizon "
                "terminal regime."
            ),
        },
        "regular_tail_audit": {
            "bounded_capability_tail": (
                "rejected: with positive limiting K/(AN) and C/(AN), "
                "service demand grows with AN, the research FOC implies "
                "q tends to zero, and qdot=rq-X/B^2-eta*g_B*q then becomes "
                "strictly negative without bound"
            ),
            "unbounded_ai_dominated_tail": (
                "rejected as an infinite-horizon equilibrium tail: its "
                "leading law dot(Y/K)=theta*h*(Y/K)^2 reaches infinity in "
                "finite time"
            ),
            "admissible_regular_infinite_horizon_tail_found": False,
        },
        "developer_optimality_audit": {
            "limiting_service_capability_elasticity": 1.0 / benchmark.alpha,
            "limiting_profit_concavity_margin": 2.0 - 1.0 / benchmark.alpha,
            "unit_elasticity_global_sufficiency_applies": False,
        },
        "records": records,
        "equilibrium_definition_requires": (
            "A strictly admissible path for every t >= 0, both TVCs, and "
            "global agent optimality."
        ),
    }


def main() -> None:
    arguments = parse_arguments()
    horizons = tuple(
        float(value) for value in arguments.horizons.split(",") if value
    )
    result = run_audit(
        sigma_xl=arguments.sigma_xl,
        horizons=horizons,
        tolerance=arguments.tolerance,
        nodes=arguments.nodes,
    )
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {arguments.output}", flush=True)


if __name__ == "__main__":
    main()

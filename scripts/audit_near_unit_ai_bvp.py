"""Run a reproducible bilateral audit of the near-unit equilibrium branch."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from define_positive_ai_branch import (  # noqa: E402
    PositiveAIBenchmarkParameters,
    balanced_growth_seed,
    initial_stocks_matching_bgp_capital_output_ratio,
)
from solve_near_unit_ai_bvp import (  # noqa: E402
    audit_near_unit_solution,
    solve_near_unit_transition,
)
from solve_positive_ai_bvp import audit_solution, solve_transition  # noqa: E402


def _parse_sigmas(value: str) -> tuple[float, ...]:
    try:
        sigmas = tuple(float(item.strip()) for item in value.split(","))
    except ValueError as error:
        raise argparse.ArgumentTypeError("Invalid sigma list.") from error
    if not sigmas or any(sigma <= 0.0 for sigma in sigmas):
        raise argparse.ArgumentTypeError(
            "Every supplied elasticity must be strictly positive."
        )
    return sigmas


def _parse_horizons(value: str) -> tuple[float, ...]:
    try:
        horizons = tuple(float(item.strip()) for item in value.split(","))
    except ValueError as error:
        raise argparse.ArgumentTypeError("Invalid horizon list.") from error
    if not horizons or any(horizon <= 0.0 for horizon in horizons):
        raise argparse.ArgumentTypeError(
            "Every supplied horizon must be strictly positive."
        )
    if any(right <= left for left, right in zip(horizons, horizons[1:])):
        raise argparse.ArgumentTypeError("Horizons must be strictly increasing.")
    return horizons


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sigmas",
        type=_parse_sigmas,
        default=(0.99, 0.999, 0.9999, 1.0, 1.0001, 1.001, 1.01),
        help="Comma-separated positive sigma_XL values.",
    )
    parser.add_argument(
        "--horizons",
        type=_parse_horizons,
        default=(100.0, 150.0, 200.0, 250.0),
        help="Comma-separated unit-branch horizon continuation schedule.",
    )
    parser.add_argument("--stock-steps", type=int, default=16)
    parser.add_argument("--elasticity-steps", type=int, default=6)
    parser.add_argument("--nodes", type=int, default=181)
    parser.add_argument("--tolerance", type=float, default=1e-9)
    parser.add_argument("--common-window", type=float, default=50.0)
    parser.add_argument("--sample-points", type=int, default=501)
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    parameters = PositiveAIBenchmarkParameters()
    seed = balanced_growth_seed(parameters)
    target = initial_stocks_matching_bgp_capital_output_ratio(
        parameters, 1.0, seed
    )
    unit_solution = solve_transition(
        parameters,
        target.capital,
        target.capability,
        horizons=arguments.horizons,
        continuation_steps=arguments.stock_steps,
        initial_nodes=arguments.nodes,
        tolerance=arguments.tolerance,
    )
    unit_times = np.linspace(
        0.0, min(arguments.common_window, unit_solution.horizon), 401
    )
    unit_path = unit_solution.evaluate_deviations(unit_times)
    rows = []
    for sigma_xl in arguments.sigmas:
        solution = solve_near_unit_transition(
            parameters,
            target.capital,
            target.capability,
            sigma_xl,
            accepted_unit_solution=unit_solution,
            horizons=arguments.horizons,
            stock_continuation_steps=arguments.stock_steps,
            elasticity_continuation_steps=arguments.elasticity_steps,
            initial_nodes=arguments.nodes,
            tolerance=arguments.tolerance,
        )
        audit = audit_near_unit_solution(
            solution, sample_points=arguments.sample_points
        )
        path_gap = float(
            np.max(
                np.abs(solution.evaluate_deviations(unit_times) - unit_path)
            )
        )
        distance = abs(sigma_xl - 1.0)
        rows.append(
            {
                "sigma_xl": sigma_xl,
                "distance_from_one": distance,
                "common_window_max_log_path_gap": path_gap,
                "gap_per_unit_distance": (
                    path_gap / distance if distance > 0.0 else 0.0
                ),
                "initial_consumption_deviation": float(
                    solution.initial_deviations[2]
                ),
                "initial_shadow_value_deviation": float(
                    solution.initial_deviations[3]
                ),
                "audit": audit,
            }
        )
    report = {
        "parameters": {
            "omega_x": parameters.omega_x,
            "alpha": parameters.alpha,
            "eta": parameters.eta,
            "population_growth": parameters.population_growth,
            "labor_productivity_growth": parameters.labor_productivity_growth,
        },
        "initial_stocks": {
            "capital": target.capital,
            "capability": target.capability,
        },
        "horizons": arguments.horizons,
        "common_window": float(unit_times[-1]),
        "unit_audit": audit_solution(
            unit_solution, sample_points=arguments.sample_points
        ),
        "near_unit_results": rows,
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

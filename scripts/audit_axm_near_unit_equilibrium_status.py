"""Audit the equilibrium status of the near-unit comparison.

The plotted nonunit paths use the unit-elastic terminal projection.  This
script performs the additional regime-specific check currently available for
``sigma_XL=0.99``: it solves the same dated model from the same predetermined
stocks with the complementary-input terminal restrictions and extends the
terminal horizon by continuation. Agreement on the displayed window is
evidence that the lower-elasticity segment lies on the complementary branch.
The audit also verifies a path-specific global-optimality condition for the
developer: optimized operating profit is concave in capability over every
capability level reachable from the predetermined initial stock.

For ``sigma_XL=1.01`` the model has no finite-rate balanced-growth terminal
condition.  The existing free-boundary algorithm describes a conditional
maximal pre-singular branch, not an infinite-horizon equilibrium under the
paper's definition.  This status is recorded explicitly rather than hidden
behind a numerical acceptance gate.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
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
from audit_axm_profit_concavity import (  # noqa: E402
    maximum_service_capability_elasticity,
    share_at_lower_capability,
)


SOURCE_PATH = ROOT / "numerical_axm" / "near_unit_bgp_perturbation_paths.csv"
OUTPUT_PATH = (
    ROOT / "numerical_axm" / "near_unit_equilibrium_status_audit.json"
)
EQUILIBRIUM_PATH = (
    ROOT / "numerical_axm" / "near_unit_equilibrium_paths.csv"
)
SIGMA_LOWER = 0.99
DISPLAY_HORIZON = 2_500.0
HORIZONS = tuple(
    [2_500.0]
    + [float(value) for value in range(3_000, 12_001, 500)]
)
TOLERANCE = 1.0e-6


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_csv(path: Path, rows: list[dict[str, float | str]]) -> None:
    if not rows:
        raise ValueError(f"Cannot write an empty CSV: {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def canonical_parameters() -> tuple[
    PositiveAIBenchmarkParameters,
    equilibrium.Parameters,
    tuple[float, float, float],
]:
    benchmark = PositiveAIBenchmarkParameters(omega_x=0.20)
    seed = balanced_growth_seed(benchmark)
    parameters = equilibrium.Parameters(
        alpha=benchmark.alpha,
        omega_x=benchmark.omega_x,
        sigma_xl=SIGMA_LOWER,
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
    initial_state = (
        seed.capital,
        seed.capability,
        benchmark.initial_population,
    )
    return benchmark, parameters, initial_state


def load_plotted_lower_path() -> dict[float, np.ndarray]:
    result: dict[float, np.ndarray] = {}
    with SOURCE_PATH.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if not math.isclose(float(row["sigma_xl"]), SIGMA_LOWER):
                continue
            time = float(row["time"])
            if time <= DISPLAY_HORIZON:
                result[time] = np.asarray(
                    [
                        float(row["log_capital"]),
                        float(row["log_capability"]),
                        float(row["log_consumption"]),
                        float(row["log_shadow_value"]),
                    ]
                )
    if len(result) != int(DISPLAY_HORIZON) + 1:
        raise RuntimeError("The plotted lower-elasticity path is incomplete.")
    return result


def tvc_log_objects(
    solution: object,
    parameters: equilibrium.Parameters,
    horizon: float,
) -> tuple[float, float]:
    times = np.linspace(0.0, horizon, 2_401)
    states = np.asarray(solution.sol(times))
    net_returns = np.empty_like(times)
    for index, time in enumerate(times):
        _, block = equilibrium.equilibrium_rates(
            float(time), states[:, index], parameters, 0.0
        )
        net_returns[index] = float(
            block["gross_capital_return"] - parameters.delta
        )
    discounted_interest = float(np.trapezoid(net_returns, times))
    terminal = states[:, -1]
    household = (
        -parameters.discount * horizon
        + parameters.n * horizon
        + float(terminal[0])
        - float(terminal[2])
    )
    developer = (
        -discounted_interest + float(terminal[3]) + float(terminal[1])
    )
    return household, developer


def profit_concavity_audit(
    solution: object,
    parameters: equilibrium.Parameters,
    initial_capability: float,
    horizon: float,
) -> dict[str, float | bool]:
    """Verify concavity of optimized operating profit for reachable ``B``."""

    times = np.linspace(0.0, horizon, 12_001)
    states = np.asarray(solution.sol(times))
    log_lower_capability = math.log(initial_capability)
    maximum_counterfactual_share = 0.0
    maximum_share_time = 0.0
    for index, time in enumerate(times):
        state = states[:, index]
        _, block = equilibrium.equilibrium_rates(
            float(time), state, parameters, 0.0
        )
        counterfactual_share = share_at_lower_capability(
            current_share=float(block["ai_share"]),
            log_current_capability=float(state[1]),
            log_lower_capability=log_lower_capability,
            sigma_xl=parameters.sigma_xl,
            alpha=parameters.alpha,
            omega_x=parameters.omega_x,
        )
        if counterfactual_share > maximum_counterfactual_share:
            maximum_counterfactual_share = counterfactual_share
            maximum_share_time = float(time)

    limiting_share = (1.0 - parameters.sigma_xl) / (
        1.0 - parameters.alpha * parameters.sigma_xl
    )
    curvature = maximum_service_capability_elasticity(
        lower_share=limiting_share,
        upper_share=maximum_counterfactual_share,
        sigma_xl=parameters.sigma_xl,
        alpha=parameters.alpha,
    )
    return {
        "initial_capability_lower_bound": initial_capability,
        "limiting_ai_share": limiting_share,
        "maximum_counterfactual_ai_share_at_initial_capability": (
            maximum_counterfactual_share
        ),
        "date_of_maximum_counterfactual_share": maximum_share_time,
        **curvature,
        "optimized_operating_profit_concave": (
            float(curvature["profit_concavity_margin"]) > 0.0
        ),
    }


def run_audit() -> dict[str, object]:
    benchmark, parameters, initial_state = canonical_parameters()
    seed = balanced_growth_seed(benchmark)
    plotted = load_plotted_lower_path()
    previous = None
    records: list[dict[str, float | int | bool]] = []
    common_times = np.arange(0.0, DISPLAY_HORIZON + 1.0, 1.0)
    previous_common_path = None
    maximum_successive_gap = 0.0

    for horizon in HORIZONS:
        solution, targets = equilibrium.solve_equilibrium(
            parameters,
            initial_state,
            horizon,
            nodes=181,
            tolerance=TOLERANCE,
            previous_solution=previous,
        )
        if not bool(solution.success):
            raise RuntimeError(
                f"Complement-tail continuation failed at T={horizon:g}: "
                f"{solution.message}"
            )
        common_path = np.asarray(solution.sol(common_times))
        successive_gap = (
            0.0
            if previous_common_path is None
            else float(np.max(np.abs(common_path - previous_common_path)))
        )
        maximum_successive_gap = max(maximum_successive_gap, successive_gap)
        records.append(
            {
                "horizon": horizon,
                "success": bool(solution.success),
                "nodes": int(solution.x.size),
                "maximum_rms_residual": float(np.max(solution.rms_residuals)),
                "log_initial_consumption": float(solution.sol(0.0)[2]),
                "log_initial_shadow_value": float(solution.sol(0.0)[3]),
                "successive_display_window_gap": successive_gap,
            }
        )
        previous = solution
        previous_common_path = common_path

    assert previous is not None
    assert previous_common_path is not None
    refined, targets = equilibrium.solve_equilibrium(
        parameters,
        initial_state,
        HORIZONS[-1],
        nodes=361,
        tolerance=1.0e-8,
        previous_solution=previous,
    )
    if not bool(refined.success):
        raise RuntimeError(
            "Final complement-tail refinement failed: "
            f"{refined.message}"
        )
    refined_common_path = np.asarray(refined.sol(common_times))
    refinement_gap = float(
        np.max(np.abs(refined_common_path - previous_common_path))
    )
    previous = refined
    previous_common_path = refined_common_path
    plotted_matrix = np.column_stack(
        [plotted[float(time)] for time in common_times]
    )
    regime_connection_gap = float(
        np.max(np.abs(previous_common_path - plotted_matrix))
    )
    household_tvc_log, developer_tvc_log = tvc_log_objects(
        previous, parameters, HORIZONS[-1]
    )
    targets = equilibrium.asymptotic_targets(parameters)
    expected_household_tvc_rate = parameters.n - parameters.discount
    expected_developer_tvc_rate = (
        (1.0 - parameters.eta)
        * (parameters.n + parameters.labor_productivity_growth)
        - (parameters.discount + parameters.labor_productivity_growth)
    )
    concavity = profit_concavity_audit(
        previous,
        parameters,
        initial_state[1],
        HORIZONS[-1],
    )
    gates = {
        "all_lower_tail_solves_successful": all(
            bool(record["success"]) for record in records
        ),
        "lower_tail_residuals": max(
            float(record["maximum_rms_residual"]) for record in records
        ) < 2.0e-5,
        "lower_tail_final_refinement": (
            float(np.max(refined.rms_residuals)) < 2.0e-8
            and refinement_gap < 2.0e-6
        ),
        "lower_tail_horizon_stability": float(
            records[-1]["successive_display_window_gap"]
        ) < 2.0e-6,
        "lower_segment_matches_regime_terminal_solution": (
            regime_connection_gap < 2.0e-6
        ),
        "lower_tail_tvc_rates_negative": (
            expected_household_tvc_rate < 0.0
            and expected_developer_tvc_rate < 0.0
        ),
        "lower_reachable_operating_profit_is_concave": bool(
            concavity["optimized_operating_profit_concave"]
        ),
        "lower_research_technology_is_jointly_concave": (
            2.0 * parameters.eta <= 1.0
        ),
    }
    lower_rows = equilibrium.evaluate_solution(
        "sigma_xl_0.9900",
        previous,
        parameters,
        DISPLAY_HORIZON,
        step=1.0,
        initial_population=benchmark.initial_population,
    )
    equilibrium_rows: list[dict[str, float | str]] = []
    for row in lower_rows:
        time = float(row["time"])
        reference_log_output = math.log(seed.output) + seed.output_growth * time
        reference_log_wage = (
            math.log(seed.wage)
            + (seed.output_growth - benchmark.population_growth) * time
        )
        equilibrium_rows.append(
            {
                "scenario": "sigma_xl_0.9900",
                "sigma_xl": SIGMA_LOWER,
                "time": time,
                "log_capital": float(row["log_capital"]),
                "log_capability": float(row["log_capability"]),
                "log_consumption": float(row["log_consumption"]),
                "log_shadow_value": float(row["log_shadow_value"]),
                "log_output_relative_to_unit_bgp": (
                    float(row["log_output"]) - reference_log_output
                ),
                "log_wage_relative_to_unit_bgp": (
                    float(row["log_wage"]) - reference_log_wage
                ),
                "net_interest": float(row["net_capital_return"]),
                "labor_share": float(row["production_labor_share"]),
            }
        )
    for time in np.arange(0.0, DISPLAY_HORIZON + 1.0, 1.0):
        equilibrium_rows.append(
            {
                "scenario": "sigma_xl_1.0000",
                "sigma_xl": 1.0,
                "time": float(time),
                "log_capital": math.log(seed.capital) + seed.output_growth * time,
                "log_capability": (
                    math.log(seed.capability) + seed.capability_growth * time
                ),
                "log_consumption": (
                    math.log(seed.consumption) + seed.output_growth * time
                ),
                "log_shadow_value": (
                    math.log(seed.shadow_value) + seed.shadow_value_growth * time
                ),
                "log_output_relative_to_unit_bgp": 0.0,
                "log_wage_relative_to_unit_bgp": 0.0,
                "net_interest": seed.net_interest_rate,
                "labor_share": (
                    (1.0 - benchmark.alpha) * (1.0 - benchmark.omega_x)
                ),
            }
        )
    equilibrium_rows.sort(
        key=lambda row: (float(row["sigma_xl"]), float(row["time"]))
    )
    write_csv(EQUILIBRIUM_PATH, equilibrium_rows)
    gates["only_admitted_trajectories_are_exported"] = {
        float(row["sigma_xl"]) for row in equilibrium_rows
    } == {0.99, 1.0}
    return {
        "accepted": all(gates.values()),
        "purpose": (
            "Classify the three near-unit paths without treating finite-window "
            "equation closure as an infinite-horizon equilibrium proof."
        ),
        "status": {
            "sigma_xl_0.99": {
                "classification": "numerically_admitted_equilibrium_trajectory",
                "verified": (
                    "The plotted segment matches a complementary-tail BVP "
                    "from the same stocks; the asymptotic tail makes both "
                    "TVC objects decay; and optimized operating profit and "
                    "the research technology are concave on the reachable "
                    "domain."
                ),
                "qualification": "Numerical equilibrium, not an existence proof.",
            },
            "sigma_xl_1.00": {
                "classification": "analytical_infinite_horizon_equilibrium",
                "verified": (
                    "The exact balanced-growth construction satisfies the "
                    "dated conditions, optimality, and both TVCs."
                ),
            },
            "sigma_xl_1.01": {
                "classification": "excluded_from_presented_trajectories",
                "verified": (
                    "The plotted segment satisfies the dated equilibrium "
                    "conditions and numerical robustness gates."
                ),
                "not_proved": (
                    "An admissible infinite-horizon tail; a finite-time "
                    "singular continuation is not an equilibrium under the "
                    "paper's infinite-horizon definition."
                ),
            },
        },
        "lower_tail": {
            "sigma_xl": SIGMA_LOWER,
            "terminal_horizons": HORIZONS,
            "terminal_targets": targets,
            "records": records,
            "final_refinement": {
                "nodes": int(refined.x.size),
                "maximum_rms_residual": float(
                    np.max(refined.rms_residuals)
                ),
                "display_window_gap": refinement_gap,
            },
            "maximum_successive_display_window_gap": maximum_successive_gap,
            "last_successive_display_window_gap": float(
                records[-1]["successive_display_window_gap"]
            ),
            "plotted_to_regime_connection_gap": regime_connection_gap,
            "terminal_household_tvc_log_object": household_tvc_log,
            "terminal_developer_tvc_log_object": developer_tvc_log,
            "expected_household_tvc_log_rate": expected_household_tvc_rate,
            "expected_developer_tvc_log_rate": expected_developer_tvc_rate,
            "developer_global_optimality": concavity,
        },
        "exported_path": {
            "path": str(EQUILIBRIUM_PATH.relative_to(ROOT)).replace("\\", "/"),
            "rows": len(equilibrium_rows),
            "sha256": sha256(EQUILIBRIUM_PATH),
            "sigma_xl_values": [0.99, 1.0],
        },
        "gates": gates,
    }


def main() -> None:
    audit = run_audit()
    OUTPUT_PATH.write_text(
        json.dumps(audit, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(audit, indent=2, sort_keys=True))
    if not bool(audit["accepted"]):
        raise SystemExit("Near-unit equilibrium-status audit failed.")


if __name__ == "__main__":
    main()

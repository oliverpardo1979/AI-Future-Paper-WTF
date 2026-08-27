"""Solve and audit the unit-elastic AI-adoption experiment.

The economy is initially on the no-AI Ramsey--Cass--Koopmans balanced-growth
path.  At date zero the production weight on AI services changes from
``omega_X = 0`` to ``omega_X = 0.20``, while ``sigma_XL = 1``.  Capital,
labor productivity, and population are predetermined and therefore continuous.

Capability did not affect the no-AI economy, so its date-zero value is not
inherited from that equilibrium.  This experiment calibrates it by requiring
date-zero output continuity.  At unit elasticity this is equivalent to
``X_0 = A_0 L_0`` and implies

    B_0 = 1 / (beta**2 * Y_0),

where ``beta = (1-alpha)*omega_X`` and the initial normalizations are
``A_0 = N_0 = 1``.  This is a substantive adoption-threshold calibration, not
an equilibrium condition and not a mechanical continuation through
``omega_X = 0``.  The positive-AI boundary-value solver determines the two
jump variables ``C(0+)`` and ``q(0+)``.

The script writes audited numerical paths used by the two adoption figures.
It does not modify the legacy numerical exercises.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from dataclasses import asdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOCAL_DEPS = ROOT / ".python-packages"
TMP_DEPS = ROOT / "tmp" / "pydeps"
if LOCAL_DEPS.exists():
    sys.path.insert(0, str(LOCAL_DEPS))
elif TMP_DEPS.exists():
    sys.path.insert(0, str(TMP_DEPS))
sys.path.insert(0, str(ROOT / "scripts"))

import numpy as np  # noqa: E402

from define_positive_ai_branch import (  # noqa: E402
    PositiveAIBenchmarkParameters,
    balanced_growth_seed,
)
from solve_positive_ai_bvp import audit_solution, solve_transition  # noqa: E402
from solve_rck_no_ai_bvp import RCKParameters, steady_state  # noqa: E402


RESULT_DIR = ROOT / "numerical_axm"
PATH_FILE = RESULT_DIR / "ai_adoption_unit_elasticity_paths.csv"
SUMMARY_FILE = RESULT_DIR / "ai_adoption_unit_elasticity_summary.csv"
MANIFEST_FILE = RESULT_DIR / "ai_adoption_unit_elasticity_audit_manifest.json"

DISPLAY_HORIZON = 250.0
SOLVER_HORIZONS = (100.0, 200.0, 300.0, 400.0, 500.0, 600.0)
PATH_POINTS = 1201
TOLERANCE = 1.0e-9
BOUNDARY_TOLERANCE = 1.0e-11
CONTINUATION_STEPS = 32
INITIAL_NODES = 181
MAXIMUM_NODES = 75_000


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def adoption_capability_for_output_continuity(
    initial_capital: float,
    initial_output: float,
    parameters: PositiveAIBenchmarkParameters,
) -> float:
    """Return B0 that preserves date-zero output at sigma_XL=1."""

    seed = balanced_growth_seed(parameters)
    effective_labor = (
        parameters.initial_labor_productivity
        * parameters.initial_population
    )
    numerator = initial_output ** (1.0 - seed.beta)
    denominator = (
        initial_capital**parameters.alpha
        * effective_labor**seed.labor_exponent
    )
    return (numerator / denominator) ** (1.0 / seed.beta) / seed.inference_share


def write_csv(path: Path, rows: list[dict[str, float | str]]) -> None:
    if not rows:
        raise ValueError(f"Cannot write an empty CSV: {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def solve_experiment() -> tuple[
    list[dict[str, float | str]],
    list[dict[str, float | str]],
    dict[str, object],
]:
    rck_parameters = RCKParameters()
    ai_parameters = PositiveAIBenchmarkParameters(omega_x=0.20)
    if not math.isclose(rck_parameters.alpha, ai_parameters.alpha):
        raise ValueError("The no-AI and AI scenarios must share alpha.")
    if not math.isclose(
        rck_parameters.population_growth, ai_parameters.population_growth
    ):
        raise ValueError("The no-AI and AI scenarios must share n.")
    if not math.isclose(
        rck_parameters.labor_productivity_growth,
        ai_parameters.labor_productivity_growth,
    ):
        raise ValueError("The no-AI and AI scenarios must share gamma_A.")
    if not math.isclose(
        rck_parameters.depreciation, ai_parameters.depreciation
    ):
        raise ValueError("The no-AI and AI scenarios must share delta.")
    if not math.isclose(rck_parameters.discount, ai_parameters.discount):
        raise ValueError("The no-AI and AI scenarios must share rho.")

    rck = steady_state(rck_parameters)
    seed = balanced_growth_seed(ai_parameters)
    initial_capital = rck.capital
    initial_capability = adoption_capability_for_output_continuity(
        initial_capital, rck.output, ai_parameters
    )
    solution = solve_transition(
        ai_parameters,
        initial_capital,
        initial_capability,
        horizons=SOLVER_HORIZONS,
        continuation_steps=CONTINUATION_STEPS,
        initial_nodes=INITIAL_NODES,
        tolerance=TOLERANCE,
        boundary_tolerance=BOUNDARY_TOLERANCE,
        maximum_nodes=MAXIMUM_NODES,
    )
    solver_audit = audit_solution(solution, sample_points=3001)

    times = np.linspace(0.0, SOLVER_HORIZONS[-1], PATH_POINTS)
    deviations = np.asarray(solution.raw.sol(times), dtype=float)
    derivatives = np.asarray(solution.raw.sol(times, 1), dtype=float)
    xi_k, xi_b, xi_c, xi_q = deviations
    dxi_k, dxi_b, dxi_c, dxi_q = derivatives

    output_k_loading = ai_parameters.alpha / (1.0 - seed.beta)
    output_b_loading = seed.beta / (1.0 - seed.beta)
    output_deviation = output_k_loading * xi_k + output_b_loading * xi_b
    output_deviation_growth = (
        output_k_loading * dxi_k + output_b_loading * dxi_b
    )
    research_deviation = (
        xi_q + ai_parameters.eta * xi_b
    ) / (1.0 - ai_parameters.eta)

    population = np.exp(ai_parameters.population_growth * times)
    labor_productivity = np.exp(
        ai_parameters.labor_productivity_growth * times
    )
    effective_labor = population * labor_productivity

    no_ai_output = rck.output * effective_labor
    no_ai_capital = rck.capital * effective_labor
    no_ai_consumption = rck.consumption * effective_labor
    no_ai_output_pc = no_ai_output / population
    no_ai_consumption_pc = no_ai_consumption / population
    no_ai_wage = rck.wage_per_efficiency_unit * labor_productivity

    ai_output = seed.output * np.exp(seed.output_growth * times + output_deviation)
    ai_capital = seed.capital * np.exp(seed.output_growth * times + xi_k)
    ai_consumption = seed.consumption * np.exp(seed.output_growth * times + xi_c)
    ai_capability = seed.capability * np.exp(
        seed.capability_growth * times + xi_b
    )
    ai_shadow_value = seed.shadow_value * np.exp(
        seed.shadow_value_growth * times + xi_q
    )
    ai_output_pc = ai_output / population
    ai_consumption_pc = ai_consumption / population
    ai_wage = seed.labor_exponent * ai_output / population
    ai_net_interest = ai_parameters.alpha * ai_output / ai_capital - ai_parameters.depreciation
    ai_output_pc_growth = (
        seed.output_growth
        + output_deviation_growth
        - ai_parameters.population_growth
    )
    ai_capability_growth = seed.capability_growth + dxi_b

    ai_inference = seed.inference_share * ai_output
    ai_research = seed.research_compute * np.exp(
        seed.output_growth * times + research_deviation
    )
    ai_services = ai_capability * ai_inference
    ai_research_share = ai_research / ai_output
    ai_profit_share = seed.beta - seed.inference_share - ai_research_share
    ai_shadow_capability_to_output = (
        ai_shadow_value * ai_capability / ai_output
    )

    output_pc_denominator = rck.output
    consumption_pc_denominator = rck.consumption
    wage_denominator = rck.wage_per_efficiency_unit

    path_rows: list[dict[str, float | str]] = []
    for index, time in enumerate(times):
        path_rows.append(
            {
                "time": float(time),
                "display_window": float(time <= DISPLAY_HORIZON + 1.0e-12),
                "no_ai_output": float(no_ai_output[index]),
                "ai_output": float(ai_output[index]),
                "no_ai_capital": float(no_ai_capital[index]),
                "ai_capital": float(ai_capital[index]),
                "no_ai_consumption": float(no_ai_consumption[index]),
                "ai_consumption": float(ai_consumption[index]),
                "ai_capability": float(ai_capability[index]),
                "ai_shadow_value": float(ai_shadow_value[index]),
                "ai_inference_compute": float(ai_inference[index]),
                "ai_research_compute": float(ai_research[index]),
                "ai_services": float(ai_services[index]),
                "no_ai_output_pc_index": float(
                    no_ai_output_pc[index] / output_pc_denominator
                ),
                "ai_output_pc_index": float(
                    ai_output_pc[index] / output_pc_denominator
                ),
                "no_ai_consumption_pc_index": float(
                    no_ai_consumption_pc[index] / consumption_pc_denominator
                ),
                "ai_consumption_pc_index": float(
                    ai_consumption_pc[index] / consumption_pc_denominator
                ),
                "no_ai_wage_index": float(no_ai_wage[index] / wage_denominator),
                "ai_wage_index": float(ai_wage[index] / wage_denominator),
                "no_ai_output_pc_growth": float(
                    rck_parameters.labor_productivity_growth
                ),
                "ai_output_pc_growth": float(ai_output_pc_growth[index]),
                "no_ai_net_interest": float(rck.net_interest_rate),
                "ai_net_interest": float(ai_net_interest[index]),
                "ai_capability_index": float(
                    ai_capability[index] / initial_capability
                ),
                "ai_capability_growth": float(ai_capability_growth[index]),
                "ai_shadow_capability_to_output": float(
                    ai_shadow_capability_to_output[index]
                ),
                "no_ai_gross_capital_share": float(rck_parameters.alpha),
                "no_ai_labor_share": float(1.0 - rck_parameters.alpha),
                "ai_gross_capital_share": float(ai_parameters.alpha),
                "ai_labor_share": float(seed.labor_exponent),
                "ai_inference_share": float(seed.inference_share),
                "ai_research_share": float(ai_research_share[index]),
                "ai_profit_share": float(ai_profit_share[index]),
                "ai_log_capital_deviation": float(xi_k[index]),
                "ai_log_capability_deviation": float(xi_b[index]),
                "ai_log_consumption_deviation": float(xi_c[index]),
                "ai_log_shadow_deviation": float(xi_q[index]),
            }
        )

    def nearest_row(target_time: float) -> dict[str, float | str]:
        position = int(np.argmin(np.abs(times - target_time)))
        return path_rows[position]

    summary_rows: list[dict[str, float | str]] = []
    for target_time in (0.0, 25.0, 50.0, 100.0, 250.0):
        row = nearest_row(target_time)
        summary_rows.append(
            {
                "point": f"t={target_time:g}",
                "time": target_time,
                "ai_to_no_ai_output_pc": float(row["ai_output_pc_index"])
                / float(row["no_ai_output_pc_index"]),
                "ai_to_no_ai_consumption_pc": float(
                    row["ai_consumption_pc_index"]
                )
                / float(row["no_ai_consumption_pc_index"]),
                "ai_to_no_ai_wage": float(row["ai_wage_index"])
                / float(row["no_ai_wage_index"]),
                "ai_output_pc_growth": float(row["ai_output_pc_growth"]),
                "ai_net_interest": float(row["ai_net_interest"]),
                "ai_capability_index": float(row["ai_capability_index"]),
                "ai_shadow_capability_to_output": float(
                    row["ai_shadow_capability_to_output"]
                ),
                "ai_labor_share": float(row["ai_labor_share"]),
                "ai_profit_share": float(row["ai_profit_share"]),
                "ai_inference_share": float(row["ai_inference_share"]),
                "ai_research_share": float(row["ai_research_share"]),
            }
        )
    summary_rows.append(
        {
            "point": "AI BGP",
            "time": math.nan,
            "ai_to_no_ai_output_pc": math.nan,
            "ai_to_no_ai_consumption_pc": math.nan,
            "ai_to_no_ai_wage": math.nan,
            "ai_output_pc_growth": seed.output_growth - ai_parameters.population_growth,
            "ai_net_interest": seed.net_interest_rate,
            "ai_capability_index": math.nan,
            "ai_shadow_capability_to_output": (
                seed.shadow_value * seed.capability / seed.output
            ),
            "ai_labor_share": seed.labor_exponent,
            "ai_profit_share": (
                seed.beta - seed.inference_share - seed.research_share
            ),
            "ai_inference_share": seed.inference_share,
            "ai_research_share": seed.research_share,
        }
    )

    ai_accounting = (
        ai_parameters.alpha
        + seed.labor_exponent
        + seed.inference_share
        + ai_research_share
        + ai_profit_share
    )
    initial_output_log_gap = abs(math.log(ai_output[0] / rck.output))
    initial_capital_log_gap = abs(math.log(ai_capital[0] / rck.capital))
    initial_services_log_gap = abs(
        math.log(
            ai_services[0]
            / (
                ai_parameters.initial_labor_productivity
                * ai_parameters.initial_population
            )
        )
    )
    maximum_accounting_error = float(np.max(np.abs(ai_accounting - 1.0)))
    minimum_profit_share = float(np.min(ai_profit_share))
    gates = {
        "solver_success": bool(solver_audit["success"]),
        "initial_output_continuity": initial_output_log_gap < 1.0e-10,
        "initial_capital_continuity": initial_capital_log_gap < 1.0e-10,
        "initial_service_matching": initial_services_log_gap < 1.0e-10,
        "equation_residuals": max(
            float(solver_audit["max_resource_residual"]),
            float(solver_audit["max_euler_residual"]),
            float(solver_audit["max_capability_residual"]),
            float(solver_audit["max_costate_residual"]),
        )
        < 1.0e-7,
        "boundary_residual": float(solver_audit["max_boundary_residual"])
        < 1.0e-9,
        "horizon_stability": float(
            solver_audit["last_horizon_initial_jump_change"]
        )
        < 1.0e-6,
        "accounting_identity": maximum_accounting_error < 1.0e-12,
        "positive_consumption": bool(np.all(ai_consumption > 0.0)),
        "positive_research": bool(np.all(ai_research > 0.0)),
        "nonnegative_profit_share": minimum_profit_share >= -1.0e-12,
        "declining_household_tvc_proxy": float(
            solver_audit["household_log_tvc_change"]
        )
        < 0.0,
        "declining_developer_tvc_proxy": float(
            solver_audit["developer_log_tvc_change"]
        )
        < 0.0,
    }
    manifest: dict[str, object] = {
        "accepted": all(gates.values()),
        "experiment": (
            "Unexpected adoption of omega_X=0.20 at sigma_XL=1 from the "
            "no-AI RCK balanced-growth path"
        ),
        "initial_condition_rule": (
            "K0, A0, and N0 are inherited from the no-AI BGP; B0 makes "
            "Y(0+) equal Y(0-) and therefore X0=A0*L0; C0 and q0 are "
            "selected by the positive-AI boundary-value problem"
        ),
        "rck_parameters": asdict(rck_parameters),
        "ai_parameters": asdict(ai_parameters),
        "rck_balanced_growth": asdict(rck),
        "ai_balanced_growth_seed": asdict(seed),
        "initial_conditions": {
            "initial_capital": initial_capital,
            "initial_capability": initial_capability,
            "initial_no_ai_output": rck.output,
            "initial_ai_output": float(ai_output[0]),
            "initial_ai_services": float(ai_services[0]),
            "initial_ai_consumption": float(ai_consumption[0]),
            "initial_ai_shadow_value": float(ai_shadow_value[0]),
            "initial_log_deviations": solution.initial_deviations.tolist(),
        },
        "solver_configuration": {
            "horizons": list(SOLVER_HORIZONS),
            "display_horizon": DISPLAY_HORIZON,
            "continuation_steps": CONTINUATION_STEPS,
            "initial_nodes": INITIAL_NODES,
            "tolerance": TOLERANCE,
            "boundary_tolerance": BOUNDARY_TOLERANCE,
            "maximum_nodes": MAXIMUM_NODES,
        },
        "solver_audit": solver_audit,
        "additional_audit": {
            "initial_output_log_gap": initial_output_log_gap,
            "initial_capital_log_gap": initial_capital_log_gap,
            "initial_services_log_gap": initial_services_log_gap,
            "maximum_accounting_error": maximum_accounting_error,
            "minimum_profit_share": minimum_profit_share,
        },
        "gates": gates,
    }
    return path_rows, summary_rows, manifest


def main() -> None:
    RESULT_DIR.mkdir(exist_ok=True)
    path_rows, summary_rows, manifest = solve_experiment()
    if manifest["accepted"] is not True:
        failed = [
            name for name, passed in manifest["gates"].items() if not passed
        ]
        raise RuntimeError("Adoption experiment failed gates: " + ", ".join(failed))
    write_csv(PATH_FILE, path_rows)
    write_csv(SUMMARY_FILE, summary_rows)
    manifest["artifacts"] = {
        "paths": {
            "path": str(PATH_FILE.relative_to(ROOT)),
            "sha256": sha256_file(PATH_FILE),
            "bytes": PATH_FILE.stat().st_size,
        },
        "summary": {
            "path": str(SUMMARY_FILE.relative_to(ROOT)),
            "sha256": sha256_file(SUMMARY_FILE),
            "bytes": SUMMARY_FILE.stat().st_size,
        },
    }
    with MANIFEST_FILE.open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps({
        "accepted": manifest["accepted"],
        "initial_conditions": manifest["initial_conditions"],
        "solver_audit": manifest["solver_audit"],
        "artifacts": manifest["artifacts"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

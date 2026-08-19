"""Independent audit for the displayed sigma_XL=1.10 equilibrium window.

The three finite-boundary solutions terminate at Y/K in {8,12,16}.  The audit
checks the equations and their overlap only on t in [0,4500], before any of the
artificial boundaries.  It makes no claim about the singular tail or an
infinite-horizon equilibrium.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import platform
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import audit_axm_high_sigma as independent


RESULT_DIR = ROOT / "numerical_axm"
PATH_NAME = "near_unit_sigma110_window_boundary_paths.csv"
SUMMARY_NAME = "near_unit_sigma110_window_summary.csv"
REPORT_NAME = "near_unit_sigma110_window_acceptance_report.csv"
RESIDUAL_NAME = "near_unit_sigma110_window_equation_residuals.csv"
MANIFEST_NAME = "near_unit_sigma110_window_audit_manifest.json"
BOUNDARIES = (8.0, 12.0, 16.0)
DISPLAY_END = 4500.0


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    fields = list(dict.fromkeys(key for row in rows for key in row))
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def gate(
    rows: list[dict[str, object]],
    category: str,
    metric: str,
    value: float,
    relation: str,
    threshold: float,
    passed: bool,
    details: str = "",
) -> None:
    rows.append(
        {
            "category": category,
            "metric": metric,
            "value": value,
            "relation": relation,
            "threshold": threshold,
            "status": "pass" if passed else "fail",
            "details": details,
        }
    )


def main() -> None:
    paths_path = RESULT_DIR / PATH_NAME
    summary_path = RESULT_DIR / SUMMARY_NAME
    grouped = independent.group_combined_paths(read_csv(paths_path))
    if set(grouped) != set(BOUNDARIES):
        raise ValueError("Expected z=8,12,16 and no other boundaries.")
    summaries = {
        independent.as_float(row, "terminal_boundary_z"): row
        for row in read_csv(summary_path)
    }
    if set(summaries) != set(BOUNDARIES):
        raise ValueError("Boundary summary does not match the path file.")
    parameters = independent.Parameters(sigma_xl=1.10)

    truncated: dict[float, list[dict[str, str]]] = {}
    terminal_errors: list[float] = []
    residuals: list[dict[str, object]] = []
    for boundary, rows in grouped.items():
        ordered = sorted(rows, key=lambda row: independent.as_float(row, "time"))
        terminal = ordered[-1]
        terminal_errors.append(
            abs(
                math.log(
                    independent.as_float(terminal, "output_capital_ratio")
                    / boundary
                )
            )
        )
        truncated[boundary] = [
            row
            for row in ordered
            if independent.as_float(row, "time") <= DISPLAY_END + 1e-10
        ]
        if independent.as_float(truncated[boundary][-1], "time") < DISPLAY_END:
            raise ValueError(f"Boundary z={boundary:g} does not cover t=4500.")
        residuals.extend(
            independent.reconstruct_row(row, parameters)
            for row in truncated[boundary]
        )

    log_equations = (
        "population_law_log_residual",
        "final_ces_log_residual",
        "final_output_log_residual",
        "inference_identity_log_residual",
        "research_service_identity_log_residual",
        "research_ces_log_residual",
        "wage_log_residual",
        "ai_price_log_residual",
        "ai_marginal_cost_log_residual",
    )
    level_equations = (
        "ai_share_residual",
        "capability_law_level_residual",
        "gross_return_residual",
        "net_return_residual",
        "inverse_elasticity_residual",
        "labor_market_residual",
        "resource_constraint_residual",
        "household_budget_residual",
        "final_firm_zero_profit_residual",
        "research_machine_technology_share_residual",
        "research_machine_cost_share_residual",
        "inference_resource_share_residual",
        "research_resource_share_residual",
        "investment_share_residual",
        "consumption_share_residual",
        "resource_share_sum_residual",
        "production_labor_income_share_residual",
        "aggregate_labor_income_share_residual",
        "ai_operating_profit_share_residual",
        "ai_markup_residual",
        "shadow_capability_to_capital_residual",
    )
    foc_equations = (
        "monopoly_foc_log_residual",
        "research_compute_foc_log_residual",
        "research_human_foc_log_residual",
    )
    rhs_equations = (
        "capital_rhs_residual",
        "capability_rhs_residual",
        "consumption_euler_rhs_residual",
        "shadow_costate_rhs_residual",
    )
    report: list[dict[str, object]] = []
    solver_rms = max(
        independent.as_float(row, "max_rms_residual")
        for row in summaries.values()
    )
    gate(report, "solver", "maximum_rms_residual", solver_rms, "<=", 3.01e-5, solver_rms <= 3.01e-5)
    gate(report, "boundary", "terminal_Y_over_K_error", max(terminal_errors), "<=", 5e-7, max(terminal_errors) <= 5e-7)
    for metric, fields, threshold in (
        ("technologies_and_prices", log_equations, 5e-8),
        ("shares_and_resources", level_equations, 5e-8),
        ("static_first_order_conditions", foc_equations, 5e-7),
        ("dynamic_rhs_reconstruction", rhs_equations, 5e-8),
        (
            "saved_path_derivative_residuals",
            tuple(f"stored_{field}" for field in independent.STORED_DYNAMIC_FIELDS),
            3e-5,
        ),
    ):
        value = independent.maximum_absolute(residuals, fields)
        gate(report, "equations", metric, value, "<=", threshold, value <= threshold)

    continuation = {
        boundary: {"duration": str(DISPLAY_END)} for boundary in BOUNDARIES
    }
    dynamic_error, location = independent.independent_dynamic_error(
        continuation, truncated, terminal_buffer=0.0
    )
    gate(
        report,
        "dynamics",
        "independently_differenced_display_window",
        dynamic_error,
        "<=",
        5e-5,
        dynamic_error <= 5e-5,
        location,
    )
    positive = min(int(row["positive_and_interior"]) for row in residuals)
    clipping = max(
        int(row["share_clipping_detected"])
        + int(row["bounded_exp_clipping_detected"])
        for row in residuals
    )
    gate(report, "domain", "positive_and_interior", float(positive), "=", 1.0, positive == 1)
    gate(report, "domain", "clipping_detected", float(clipping), "=", 0.0, clipping == 0)

    initial_c = [
        independent.as_float(summaries[boundary], "initial_log_consumption")
        for boundary in BOUNDARIES
    ]
    initial_q = [
        independent.as_float(summaries[boundary], "initial_log_shadow_value")
        for boundary in BOUNDARIES
    ]
    for metric, values in (("initial_log_consumption_range", initial_c), ("initial_log_shadow_value_range", initial_q)):
        spread = max(values) - min(values)
        gate(report, "boundary_stability", metric, spread, "<=", 1e-7, spread <= 1e-7)

    grid = independent.regular_grid(0.0, DISPLAY_END, 1001)
    for field in independent.STATE_LOG_FIELDS:
        spread = independent.window_spread(truncated, field, grid)
        gate(report, "window_stability", f"maximum_{field}_spread", spread, "<=", 5e-4, spread <= 5e-4)
    for field in (
        "output_per_capita_growth",
        "wage_growth",
        "net_capital_return",
        "aggregate_labor_share",
        "ai_share",
    ):
        spread = independent.window_spread(truncated, field, grid)
        gate(report, "window_stability", f"maximum_{field}_spread", spread, "<=", 5e-5, spread <= 5e-5)

    accepted = all(row["status"] == "pass" for row in report)
    write_csv(RESULT_DIR / REPORT_NAME, report)
    write_csv(RESULT_DIR / RESIDUAL_NAME, residuals)
    files = [
        ROOT / "scripts" / "simulate_axm_near_unit_high.py",
        ROOT / "scripts" / "audit_axm_near_unit_high.py",
        paths_path,
        summary_path,
        RESULT_DIR / REPORT_NAME,
        RESULT_DIR / RESIDUAL_NAME,
    ]
    manifest = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "overall_accepted": accepted,
        "accepted_claim": (
            "The three finite-boundary solutions satisfy the audited dated "
            "conditions and overlap on the displayed interval t in [0,4500]."
        ),
        "claims_not_established": [
            "convergence of the singular tail",
            "existence of an infinite-horizon equilibrium",
            "transversality at infinity",
            "global optimality or uniqueness",
        ],
        "parameters": asdict(parameters),
        "boundaries": BOUNDARIES,
        "display_end": DISPLAY_END,
        "python": platform.python_version(),
        "files": {
            str(path.relative_to(ROOT)).replace("\\", "/"): {
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
            for path in files
        },
    }
    (RESULT_DIR / MANIFEST_NAME).write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(f"near-unit upper-window audit: {'ACCEPTED' if accepted else 'REJECTED'}")
    if not accepted:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

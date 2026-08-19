"""Independent audit of the sigma_XL=0.90 finite-horizon paths.

This module imports only the equation-reconstruction utilities from the
gross-complements auditor.  It never imports the equilibrium solver.  The
audit reconstructs the static block, differentiates the four saved log paths,
checks the two imposed terminal restrictions, and tests horizon stability.
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

import audit_axm_complements as independent


RESULT_DIR = ROOT / "numerical_axm"
PATH_NAME = "near_unit_sigma090_horizon_paths.csv"
SUMMARY_NAME = "near_unit_sigma090_horizon_summary.csv"
REPORT_NAME = "near_unit_sigma090_acceptance_report.csv"
RESIDUAL_NAME = "near_unit_sigma090_equation_residuals.csv"
MANIFEST_NAME = "near_unit_sigma090_audit_manifest.json"
HORIZONS = (5000.0, 5300.0, 5600.0)
SIGMA_HM = 2.0


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def check(
    rows: list[dict[str, object]],
    category: str,
    scenario: str,
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
            "scenario": scenario,
            "sigma_xl": 0.90,
            "sigma_hm": SIGMA_HM,
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
    paths = read_csv(paths_path)
    summaries = read_csv(summary_path)
    independent.PARAMETERS = independent.Parameters(sigma_xl=0.90)
    p = independent.PARAMETERS
    gates = independent.GATES

    grouped = independent.group_paths(paths)
    summary_by_name = {row["scenario"]: row for row in summaries}
    expected = {
        f"near_unit_sigma_xl_090_hm_2_T_{horizon:g}"
        for horizon in HORIZONS
    }
    if set(grouped) != expected or set(summary_by_name) != expected:
        raise ValueError("Near-unit scenario coverage is incomplete.")

    report: list[dict[str, object]] = []
    residuals: list[dict[str, object]] = []
    initial_c: list[float] = []
    initial_q: list[float] = []
    target_sx = (1.0 - p.sigma_xl) / (1.0 - p.alpha * p.sigma_xl)
    targets = independent.target_values(SIGMA_HM)

    for name in sorted(grouped):
        rows = grouped[name]
        summary = summary_by_name[name]
        horizon = independent.number(rows[0], "horizon")
        rebuilt = [independent.reconstruct_row(row, SIGMA_HM) for row in rows]
        derivatives = {
            field: independent.independent_derivatives(rows, field)
            for field in independent.STATE_LOG_FIELDS
        }
        static_max = 0.0
        stored_max = 0.0
        dynamic_max = 0.0
        foc_max = 0.0
        soc_min = math.inf
        fallback_max = 0.0
        clipping_count = 0.0
        for index, (raw, recovered) in enumerate(zip(rows, rebuilt)):
            record: dict[str, object] = {
                "scenario": name,
                "time": independent.number(raw, "time"),
                **recovered,
            }
            for state, rate, rhs in zip(
                independent.STATE_LOG_FIELDS,
                independent.RATE_FIELDS,
                (
                    "rhs_capital_growth",
                    "rhs_capability_growth",
                    "rhs_consumption_growth",
                    "rhs_shadow_growth",
                ),
            ):
                if index in derivatives[state]:
                    error = derivatives[state][index] - recovered[rhs]
                    record[f"fd_{rate}_residual"] = error
                    dynamic_max = max(dynamic_max, abs(error))
                else:
                    record[f"fd_{rate}_residual"] = ""
            residuals.append(record)
            static_max = max(static_max, recovered["static_max_abs_error"])
            stored_max = max(
                stored_max,
                *(abs(recovered[field]) for field in (
                    "stored_capital_rate_error",
                    "stored_capability_rate_error",
                    "stored_consumption_rate_error",
                    "stored_shadow_rate_error",
                )),
            )
            foc_max = max(
                foc_max,
                abs(recovered["monopoly_foc_log_error_independent"]),
            )
            soc_min = min(
                soc_min, recovered["monopoly_soc_margin_independent"]
            )
            fallback_max = max(
                fallback_max,
                independent.number(raw, "monopoly_root_fallback"),
                independent.number(raw, "labor_root_fallback"),
            )
            clipping_count += recovered["bounded_exp_clipping_count"]

        terminal = rows[-1]
        terminal_rebuilt = rebuilt[-1]
        imposed_error = max(
            abs(
                independent.number(terminal, "consumption_share")
                - targets["consumption_share"]
            ),
            abs(
                terminal_rebuilt["profit_shadow_ratio_independent"]
                - targets["profit_shadow_ratio"]
            ),
        )
        nonimposed_error = max(
            abs(independent.number(terminal, "output_per_capita_growth")),
            abs(
                independent.number(terminal, "net_capital_return")
                - p.discount
            ),
            abs(independent.number(terminal, "ai_share") - target_sx),
        )
        discounted_interest = independent.trapezoid_integral(
            rows, "net_capital_return"
        )
        household_tvc = (
            -p.discount * horizon
            + independent.number(terminal, "log_population")
            + independent.number(terminal, "log_capital")
            - independent.number(terminal, "log_consumption")
        )
        developer_tvc = (
            -discounted_interest
            + independent.number(terminal, "log_shadow_value")
            + independent.number(terminal, "log_capability")
        )
        initial_c.append(independent.number(rows[0], "log_consumption"))
        initial_q.append(independent.number(rows[0], "log_shadow_value"))

        checks = (
            ("solver", "solver_success", independent.number(summary, "solver_success"), "=", 1.0, independent.number(summary, "solver_success") == 1.0, ""),
            ("solver", "maximum_rms_residual", independent.number(summary, "max_rms_residual"), "<", gates.solver_rms, independent.number(summary, "max_rms_residual") < gates.solver_rms, ""),
            ("equations", "maximum_static_equation_error", static_max, "<", gates.static_equations, static_max < gates.static_equations, "independent reconstruction"),
            ("equations", "maximum_saved_rate_error", stored_max, "<", gates.independent_dynamics, stored_max < gates.independent_dynamics, "independent RHS"),
            ("equations", "maximum_independent_dynamic_error", dynamic_max, "<", gates.independent_dynamics, dynamic_max < gates.independent_dynamics, "centered seven-point derivatives"),
            ("monopoly", "maximum_monopoly_foc_log_error", foc_max, "<", gates.monopoly_foc_log, foc_max < gates.monopoly_foc_log, ""),
            ("monopoly", "minimum_monopoly_soc_margin", soc_min, ">", 0.0, soc_min > 0.0, ""),
            ("terminal", "maximum_imposed_terminal_error", imposed_error, "<", gates.imposed_terminal, imposed_error < gates.imposed_terminal, "C/Y and X/(qA^2)"),
            ("terminal", "maximum_nonimposed_limit_error", nonimposed_error, "<", 5e-4, nonimposed_error < 5e-4, "growth, r, and s_X"),
            ("implementation", "maximum_fallback_flag", fallback_max, "=", 0.0, fallback_max == 0.0, ""),
            ("implementation", "bounded_exp_clipping_count", clipping_count, "=", 0.0, clipping_count == 0.0, ""),
            ("transversality", "household_tvc_log_proxy", household_tvc, "<", gates.tvc_log_proxy, household_tvc < gates.tvc_log_proxy, "finite-horizon diagnostic"),
            ("transversality", "developer_tvc_log_proxy", developer_tvc, "<", gates.tvc_log_proxy, developer_tvc < gates.tvc_log_proxy, "finite-horizon diagnostic"),
        )
        for category, metric, value, relation, threshold, passed, details in checks:
            check(report, category, name, metric, float(value), relation, float(threshold), bool(passed), details)

    for label, values in (("log_consumption", initial_c), ("log_shadow_value", initial_q)):
        spread = max(values) - min(values)
        check(
            report,
            "horizon_stability",
            "all",
            f"initial_{label}_range",
            spread,
            "<",
            gates.initial_jump_range,
            spread < gates.initial_jump_range,
            "three independently solved horizons",
        )

    accepted = all(row["status"] == "pass" for row in report)
    write_csv(RESULT_DIR / REPORT_NAME, report)
    write_csv(RESULT_DIR / RESIDUAL_NAME, residuals)
    files = [
        ROOT / "scripts" / "simulate_axm_near_unit_lower.py",
        ROOT / "scripts" / "audit_axm_near_unit_lower.py",
        paths_path,
        summary_path,
        RESULT_DIR / REPORT_NAME,
        RESULT_DIR / RESIDUAL_NAME,
    ]
    manifest = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "accepted": accepted,
        "parameters": asdict(p),
        "horizons": HORIZONS,
        "python": platform.python_version(),
        "files": {
            str(path.relative_to(ROOT)).replace("\\", "/"): {
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
            for path in files
        },
        "claim_not_established": [
            "existence or uniqueness of an infinite-horizon equilibrium",
            "global optimality",
            "transversality from a finite-horizon proxy alone",
        ],
    }
    (RESULT_DIR / MANIFEST_NAME).write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(f"near-unit lower audit: {'ACCEPTED' if accepted else 'REJECTED'}")
    if not accepted:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

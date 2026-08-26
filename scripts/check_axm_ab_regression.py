"""Regression gate for the A--B notation and labor-productivity migration.

Commit ``d019192`` froze the last accepted outputs before the solver migration.
At gamma_A=0 and A(0)=1, the migrated outputs must agree with those archived
paths within the published solver tolerances.  The migrated dated map must also
reconstruct its saved allocations and four canonical growth rates.  This script
checks both invariants without solving or rewriting a numerical artifact.
"""

from __future__ import annotations

import csv
import io
import math
import subprocess
from dataclasses import replace
from pathlib import Path

import numpy as np

import simulate_axm_equilibrium as equilibrium


ROOT = Path(__file__).resolve().parents[1]
NUMERICAL_DIR = ROOT / "numerical_axm"
TOLERANCE = 2e-10
PATH_TOLERANCE = 5e-5
BASELINE_COMMIT = "d019192"

DATASETS = (
    ("unit", NUMERICAL_DIR / "equilibrium_transition_paths.csv"),
    ("complements", NUMERICAL_DIR / "complements_transition_paths.csv"),
    (
        "gross_substitutes",
        NUMERICAL_DIR / "high_sigma_sigma150_z128_validated_boundary_paths.csv",
    ),
)

STATIC_FIELDS = {
    "log_output": "log_output",
    "log_wage": "log_wage",
    "log_ai_services": "log_ai_services",
    "log_inference_compute": "log_inference_compute",
    "log_human_research": "log_human_research",
    "log_production_labor": "log_production_labor",
    "log_automated_research": "log_automated_research",
    "log_automated_research_services": "log_automated_research_services",
    "log_effective_research": "log_effective_research",
    "capability_growth": "capability_growth",
    "gross_capital_return": "gross_capital_return",
    "human_research_share": "human_share",
    "ai_share": "ai_share",
    "automated_research_share": "automated_research_share",
    "inference_share": "inference_share",
    "research_resource_share": "research_resource_share",
}

DYNAMIC_FIELDS = (
    "capital_growth",
    "capability_growth",
    "consumption_growth",
    "shadow_growth",
)

PATH_COMPATIBILITY_FIELDS = (
    "log_capital",
    "log_capability",
    "log_consumption",
    "log_shadow_value",
    *STATIC_FIELDS,
    *DYNAMIC_FIELDS,
    "net_capital_return",
    "consumption_share",
    "investment_share",
    "aggregate_labor_share",
    "resource_share_sum",
)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_archived_rows(path: Path) -> list[dict[str, str]]:
    relative = path.relative_to(ROOT).as_posix()
    result = subprocess.run(
        ["git", "show", f"{BASELINE_COMMIT}:{relative}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return list(csv.DictReader(io.StringIO(result.stdout)))


def row_key(row: dict[str, str]) -> tuple[str, float, float]:
    return (
        row["scenario"],
        round(float(row["time"]), 9),
        round(float(row.get("terminal_boundary_z") or 0.0), 9),
    )


def sample_rows(rows: list[dict[str, str]], count: int = 31) -> list[dict[str, str]]:
    if len(rows) <= count:
        return rows
    indexes = np.linspace(0, len(rows) - 1, count, dtype=int)
    return [rows[int(index)] for index in sorted(set(indexes))]


def parameters_for(row: dict[str, str]) -> equilibrium.Parameters:
    name = row["scenario"]
    if "sigma_xl_1_hm_1" in name:
        sigma_xl, sigma_hm = 1.0, 1.0
    elif "sigma_xl_1_hm_2" in name:
        sigma_xl, sigma_hm = 1.0, 2.0
    else:
        sigma_xl = float(row.get("sigma_xl") or 1.0)
        sigma_hm = float(row.get("sigma_hm") or 2.0)
    return replace(
        equilibrium.Parameters(),
        sigma_xl=sigma_xl,
        sigma_hm=sigma_hm,
        labor_productivity_growth=0.0,
        initial_labor_productivity=1.0,
    )


def finite_error(left: float, right: float) -> float:
    if math.isinf(left) and math.isinf(right) and left == right:
        return 0.0
    return abs(left - right)


def check_dataset(label: str, path: Path) -> tuple[int, float]:
    rows = read_rows(path)
    checked = sample_rows(rows)
    maximum = 0.0
    for row in checked:
        parameters = parameters_for(row)
        time = float(row["time"])
        log_initial_population = float(row["log_population"]) - parameters.n * time
        state = np.asarray(
            [
                float(row["log_capital"]),
                float(row["log_capability"]),
                float(row["log_consumption"]),
                float(row["log_shadow_value"]),
            ]
        )
        rates, block = equilibrium.equilibrium_rates(
            time,
            state,
            parameters,
            log_initial_population,
        )
        for saved_field, block_field in STATIC_FIELDS.items():
            maximum = max(
                maximum,
                finite_error(
                    float(row[saved_field]), float(block[block_field])
                ),
            )
        for index, field in enumerate(DYNAMIC_FIELDS):
            maximum = max(
                maximum,
                finite_error(float(row[field]), float(rates[index])),
            )
        if block["log_labor_productivity"] != 0.0:
            raise AssertionError("The gamma_A=0 regression did not keep A(t)=1.")
        if finite_error(
            block["log_effective_production_labor"],
            block["log_production_labor"],
        ) > TOLERANCE:
            raise AssertionError("Effective and raw labor differ when A(t)=1.")
    if maximum > TOLERANCE:
        raise AssertionError(
            f"{label}: maximum A--B regression error {maximum:.3e} "
            f"exceeds {TOLERANCE:.3e}."
        )
    return len(checked), maximum


def check_archived_path_compatibility(
    label: str, path: Path
) -> tuple[int, float, str]:
    current = {row_key(row): row for row in read_rows(path)}
    archived_rows = read_archived_rows(path)
    checked = sample_rows(archived_rows)
    maximum = 0.0
    maximum_field = ""
    for archived in checked:
        key = row_key(archived)
        if key not in current:
            raise AssertionError(f"{label}: migrated path is missing {key}.")
        migrated = current[key]
        for field in PATH_COMPATIBILITY_FIELDS:
            if field not in archived or field not in migrated:
                continue
            error = finite_error(float(archived[field]), float(migrated[field]))
            if error > maximum:
                maximum = error
                maximum_field = field
    if maximum > PATH_TOLERANCE:
        raise AssertionError(
            f"{label}: archived-path error {maximum:.3e} in {maximum_field} "
            f"exceeds {PATH_TOLERANCE:.3e}."
        )
    return len(checked), maximum, maximum_field


def check_positive_productivity_balanced_growth() -> None:
    cases = (
        (
            "automated_benchmark",
            replace(
                equilibrium.Parameters(),
                omega_m=1.0,
                sigma_xl=1.0,
                sigma_hm=2.0,
                labor_productivity_growth=0.01,
            ),
        ),
        (
            "human_research_cobb_douglas",
            replace(
                equilibrium.Parameters(),
                sigma_xl=1.0,
                sigma_hm=1.0,
                labor_productivity_growth=0.01,
            ),
        ),
    )
    for label, parameters in cases:
        levels = equilibrium.unit_balanced_growth_levels(parameters)
        targets = equilibrium.asymptotic_targets(parameters)
        growth = np.asarray(
            [
                targets["aggregate_growth"],
                targets["capability_growth"],
                targets["aggregate_growth"],
                targets["shadow_growth"],
            ],
            dtype=float,
        )
        initial_state = np.log(
            [
                levels["capital"],
                levels["capability"],
                levels["consumption"],
                levels["shadow_value"],
            ]
        )
        maximum = 0.0
        for time in (0.0, 10.0, 100.0):
            rates, block = equilibrium.equilibrium_rates(
                time,
                initial_state + growth * time,
                parameters,
                0.0,
            )
            maximum = max(maximum, float(np.max(np.abs(rates - growth))))
            expected_log_a = parameters.labor_productivity_growth * time
            maximum = max(
                maximum,
                abs(block["log_labor_productivity"] - expected_log_a),
            )
        if maximum > TOLERANCE:
            raise AssertionError(
                f"{label}: exact balanced-growth error {maximum:.3e} "
                f"exceeds {TOLERANCE:.3e}."
            )
        print(
            f"{label}: PASS; gamma_A="
            f"{parameters.labor_productivity_growth:.3f}; "
            f"max_abs_error={maximum:.3e}"
        )


def main() -> None:
    for label, path in DATASETS:
        archived_observations, archived_maximum, archived_field = (
            check_archived_path_compatibility(label, path)
        )
        print(
            f"{label}: ARCHIVED PATH PASS; baseline={BASELINE_COMMIT}; "
            f"sampled_observations={archived_observations}; "
            f"max_abs_error={archived_maximum:.3e}; "
            f"max_field={archived_field or 'none'}"
        )
        observations, maximum = check_dataset(label, path)
        print(
            f"{label}: PASS; sampled_observations={observations}; "
            f"max_abs_error={maximum:.3e}"
        )
    check_positive_productivity_balanced_growth()


if __name__ == "__main__":
    main()

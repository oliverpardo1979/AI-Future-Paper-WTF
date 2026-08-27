"""Audit global developer optimality on presented complementary paths.

The existing complements audit checks dated equations, terminal convergence,
and transversality. This separate audit supplies the missing nonunit
optimality gate. For every saved date it asks how large the AI-service share
could be over the entire reachable state domain ``B >= B(0)``. It then verifies
that optimized operating profit is concave in capability over the resulting
share interval and that the research technology is jointly concave.
"""

from __future__ import annotations

import csv
import json
import math
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from audit_axm_profit_concavity import (  # noqa: E402
    maximum_service_capability_elasticity,
    share_at_lower_capability,
)


SOURCE = ROOT / "numerical_axm" / "complements_transition_paths.csv"
OUTPUT = (
    ROOT
    / "numerical_axm"
    / "complements_global_optimality_audit.json"
)


def run_audit() -> dict[str, object]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    with SOURCE.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            grouped[row["scenario"]].append(row)
    if not grouped:
        raise RuntimeError("The canonical complements path file is empty.")

    scenarios: dict[str, object] = {}
    for scenario, rows in sorted(grouped.items()):
        rows.sort(key=lambda row: float(row["time"]))
        alpha = float(rows[0]["alpha"])
        eta = float(rows[0]["eta"])
        sigma_xl = float(rows[0]["sigma_xl"])
        sigma_hm = float(rows[0]["sigma_hm"])
        omega_x = 0.20
        omega_m = 0.35
        initial_log_capability = float(rows[0]["log_capability"])
        minimum_capability_gap = min(
            float(row["log_capability"]) - initial_log_capability
            for row in rows
        )
        maximum_counterfactual_share = 0.0
        maximum_share_time = 0.0
        for row in rows:
            counterfactual_share = share_at_lower_capability(
                current_share=float(row["ai_share"]),
                log_current_capability=float(row["log_capability"]),
                log_lower_capability=initial_log_capability,
                sigma_xl=sigma_xl,
                alpha=alpha,
                omega_x=omega_x,
            )
            if counterfactual_share > maximum_counterfactual_share:
                maximum_counterfactual_share = counterfactual_share
                maximum_share_time = float(row["time"])

        limiting_share = (1.0 - sigma_xl) / (
            1.0 - alpha * sigma_xl
        )
        curvature = maximum_service_capability_elasticity(
            lower_share=limiting_share,
            upper_share=maximum_counterfactual_share,
            sigma_xl=sigma_xl,
            alpha=alpha,
        )
        if math.isclose(sigma_hm, 1.0):
            research_concavity_margin = 1.0 - eta * (1.0 + omega_m)
            research_condition = "eta*(1+omega_M)<=1"
        elif math.isclose(sigma_hm, 2.0):
            research_concavity_margin = 1.0 - 2.0 * eta
            research_condition = "2*eta<=1"
        else:
            raise ValueError(
                "No joint-concavity theorem is coded for this sigma_HM."
            )
        gates = {
            "capability_never_below_initial_stock": (
                minimum_capability_gap >= -1.0e-10
            ),
            "optimized_operating_profit_concave_on_reachable_domain": (
                float(curvature["profit_concavity_margin"]) > 0.0
            ),
            "research_technology_jointly_concave": (
                research_concavity_margin >= 0.0
            ),
        }
        scenarios[scenario] = {
            "accepted": all(gates.values()),
            "sigma_xl": sigma_xl,
            "sigma_hm": sigma_hm,
            "initial_capability": math.exp(initial_log_capability),
            "minimum_log_capability_gap_from_initial": minimum_capability_gap,
            "limiting_ai_share": limiting_share,
            "maximum_counterfactual_ai_share_at_initial_capability": (
                maximum_counterfactual_share
            ),
            "date_of_maximum_counterfactual_share": maximum_share_time,
            **curvature,
            "research_concavity_condition": research_condition,
            "research_concavity_margin": research_concavity_margin,
            "gates": gates,
        }

    return {
        "accepted": all(
            bool(result["accepted"]) for result in scenarios.values()
        ),
        "purpose": (
            "Supply the nonunit global-optimality gate missing from the "
            "dated-equation and terminal audits for presented complements."
        ),
        "source": str(SOURCE.relative_to(ROOT)).replace("\\", "/"),
        "scenarios": scenarios,
    }


def main() -> None:
    result = run_audit()
    OUTPUT.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if not bool(result["accepted"]):
        raise SystemExit("Complements global-optimality audit failed.")


if __name__ == "__main__":
    main()

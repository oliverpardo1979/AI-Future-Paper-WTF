"""Audit the analytical and numerical status of ``sigma_XL > 1``.

The gross-substitutes calculation is allowed to solve dated necessary
conditions on finite windows, but it is never exported as an equilibrium
trajectory.  This audit records why the two regular long-run continuations
used by the algorithm fail and why neither a zero-research corner nor the
paper's global concavity theorem repairs the missing infinite-horizon result.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from audit_axm_profit_concavity import (  # noqa: E402
    first_profit_concavity_failure_share,
    service_capability_elasticity,
)
from define_positive_ai_branch import (  # noqa: E402
    PositiveAIBenchmarkParameters,
)


UPPER_AUDIT = (
    ROOT / "numerical_axm" / "upper_near_unit_equilibrium_audit.json"
)
PRESENTED_PATH = (
    ROOT / "numerical_axm" / "near_unit_equilibrium_paths.csv"
)
OUTPUT = (
    ROOT / "numerical_axm" / "gross_substitutes_status_audit.json"
)


def presented_sigmas() -> list[float]:
    with PRESENTED_PATH.open("r", encoding="utf-8", newline="") as handle:
        values = {float(row["sigma_xl"]) for row in csv.DictReader(handle)}
    return sorted(values)


def run_audit() -> dict[str, object]:
    upper = json.loads(UPPER_AUDIT.read_text(encoding="utf-8"))
    parameters = PositiveAIBenchmarkParameters(
        omega_x=float(upper["omega_x"])
    )
    sigma_xl = float(upper["sigma_xl"])
    threshold = first_profit_concavity_failure_share(
        sigma_xl=sigma_xl,
        alpha=parameters.alpha,
    )
    limit_elasticity = service_capability_elasticity(
        share=1.0,
        sigma_xl=sigma_xl,
        alpha=parameters.alpha,
    )
    sigmas = presented_sigmas()

    gates = {
        "gross_substitutes_case": sigma_xl > 1.0,
        "finite_window_branch_rejected": upper.get("accepted") is False,
        "no_regular_infinite_horizon_continuation_found": (
            upper.get("regular_tail_audit", {}).get(
                "admissible_regular_infinite_horizon_tail_found"
            )
            is False
        ),
        "bounded_regular_continuation_rejected": "rejected"
        in str(
            upper.get("regular_tail_audit", {}).get(
                "bounded_capability_tail", ""
            )
        ),
        "ai_dominated_regular_continuation_is_finite_time": (
            "finite time"
            in str(
                upper.get("regular_tail_audit", {}).get(
                    "unbounded_ai_dominated_tail", ""
                )
            )
        ),
        "zero_research_corner_unavailable_at_finite_dates": (
            0.0 < parameters.eta < 1.0
        ),
        "global_concavity_gate_fails": (
            parameters.alpha < 0.5
            and threshold is not None
            and limit_elasticity > 2.0
        ),
        "no_gross_substitutes_trajectory_is_presented": all(
            value <= 1.0 for value in sigmas
        ),
    }
    return {
        "audit_passed": all(gates.values()),
        "trajectory_admitted": False,
        "classification": (
            "no_admitted_infinite_horizon_equilibrium_in_the_audited_"
            "regular_continuation_class"
        ),
        "sigma_xl": sigma_xl,
        "parameters": {
            "alpha": parameters.alpha,
            "eta": parameters.eta,
            "omega_x": parameters.omega_x,
            "effective_labor_growth": (
                parameters.population_growth
                + parameters.labor_productivity_growth
            ),
        },
        "regular_continuations_audited": {
            "bounded_capability": (
                "Rejected under positive limiting K/(AN) and C/(AN), "
                "bounded r, and g_B tending to zero."
            ),
            "unbounded_ai_dominated": (
                "Rejected as an infinite-horizon continuation under positive "
                "regular limiting shares because dot(Y/K) is asymptotic to "
                "a positive constant times (Y/K)^2."
            ),
        },
        "corner_audit": {
            "zero_research_at_a_finite_date": "ruled_out",
            "reason": (
                "With q>0 and 0<eta<1, the right marginal product of M at "
                "zero is infinite. This does not rule out M tending to zero "
                "asymptotically."
            ),
        },
        "developer_global_optimality": {
            "concavity_gate_available": False,
            "first_failure_ai_share": threshold,
            "limiting_service_capability_elasticity": limit_elasticity,
            "reason": (
                "At fixed dated K, A, and L, the counterfactual service share "
                "approaches one as B grows. The service-capability elasticity "
                "then approaches 1/alpha, which exceeds two."
            ),
        },
        "presented_sigma_xl_values": sigmas,
        "remaining_open_class": (
            "Asymptotically irregular paths, paths without convergent resource "
            "shares, and terminal regimes outside the two classes above are "
            "not ruled out."
        ),
        "gates": gates,
    }


def main() -> None:
    result = run_audit()
    OUTPUT.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if not bool(result["audit_passed"]):
        raise SystemExit("Gross-substitutes status audit failed.")


if __name__ == "__main__":
    main()

"""Regression tests for the nonunit developer-optimality audit."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from audit_axm_profit_concavity import (  # noqa: E402
    maximum_service_capability_elasticity,
)


class ProfitConcavityAuditTests(unittest.TestCase):
    def test_near_unit_lower_bound_matches_saved_audit(self) -> None:
        audit = json.loads(
            (
                ROOT
                / "numerical_axm"
                / "near_unit_equilibrium_status_audit.json"
            ).read_text(encoding="utf-8")
        )
        saved = audit["lower_tail"]["developer_global_optimality"]
        recomputed = maximum_service_capability_elasticity(
            lower_share=float(saved["limiting_ai_share"]),
            upper_share=float(
                saved[
                    "maximum_counterfactual_ai_share_at_initial_capability"
                ]
            ),
            sigma_xl=0.99,
            alpha=0.33,
        )
        self.assertAlmostEqual(
            recomputed["maximum_service_capability_elasticity"],
            saved["maximum_service_capability_elasticity"],
            places=12,
        )
        self.assertGreater(recomputed["profit_concavity_margin"], 0.0)

    def test_gross_substitute_limit_fails_concavity_gate(self) -> None:
        self.assertLess(2.0 - 1.0 / 0.33, 0.0)


if __name__ == "__main__":
    unittest.main()

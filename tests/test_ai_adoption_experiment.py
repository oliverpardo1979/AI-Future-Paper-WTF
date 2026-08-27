"""Regression tests for the unit-elastic AI-adoption experiment."""

from __future__ import annotations

import csv
import json
import math
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from define_positive_ai_branch import (  # noqa: E402
    PositiveAIBenchmarkParameters,
    balanced_growth_seed,
)
from simulate_axm_ai_adoption import (  # noqa: E402
    MANIFEST_FILE,
    PATH_FILE,
    adoption_capability_for_output_continuity,
)
from solve_rck_no_ai_bvp import RCKParameters, steady_state  # noqa: E402


class AIAdoptionExperimentTests(unittest.TestCase):
    def test_capability_rule_preserves_output_and_matches_services(self) -> None:
        rck = steady_state(RCKParameters())
        parameters = PositiveAIBenchmarkParameters(omega_x=0.20)
        seed = balanced_growth_seed(parameters)
        capability = adoption_capability_for_output_continuity(
            rck.capital, rck.output, parameters
        )
        reconstructed_output = (
            rck.capital**parameters.alpha
            * (
                parameters.initial_labor_productivity
                * parameters.initial_population
            )
            ** seed.labor_exponent
            * (seed.inference_share * capability) ** seed.beta
        ) ** (1.0 / (1.0 - seed.beta))
        ai_services = seed.inference_share * capability * reconstructed_output
        self.assertAlmostEqual(reconstructed_output, rck.output, places=12)
        self.assertAlmostEqual(ai_services, 1.0, places=12)

    def test_saved_experiment_is_accepted_and_accounting_closes(self) -> None:
        with MANIFEST_FILE.open("r", encoding="utf-8") as handle:
            manifest = json.load(handle)
        self.assertTrue(manifest["accepted"])
        self.assertTrue(all(manifest["gates"].values()))
        self.assertTrue(manifest["gates"]["terminal_bgp_convergence"])
        self.assertLess(
            manifest["solver_audit"]["terminal_deviation_norm"], 1.0e-2
        )
        self.assertLess(
            manifest["additional_audit"]["terminal_output_pc_growth_gap"],
            5.0e-6,
        )
        self.assertLess(
            manifest["additional_audit"]["terminal_net_interest_gap"],
            5.0e-6,
        )

        with PATH_FILE.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertGreaterEqual(len(rows), 1000)
        self.assertAlmostEqual(float(rows[-1]["time"]), 3000.0, places=10)
        terminal_interest = float(rows[-1]["ai_net_interest"])
        analytical_interest = float(rows[-1]["ai_bgp_net_interest"])
        self.assertLess(abs(terminal_interest - analytical_interest), 5.0e-6)
        for row in (rows[0], rows[len(rows) // 2], rows[-1]):
            total = sum(
                float(row[field])
                for field in (
                    "ai_gross_capital_share",
                    "ai_labor_share",
                    "ai_profit_share",
                    "ai_inference_share",
                    "ai_research_share",
                )
            )
            self.assertTrue(math.isclose(total, 1.0, abs_tol=1.0e-12))


if __name__ == "__main__":
    unittest.main()

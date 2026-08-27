"""Tests for positive-AI transitions away from balanced growth."""

from __future__ import annotations

import sys
import unittest
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
    initial_stocks_matching_bgp_capital_output_ratio,
)
from solve_positive_ai_bvp import audit_solution, solve_transition  # noqa: E402


class PositiveAIBVPSolverTests(unittest.TestCase):
    """Verify the exact seed and off-BGP collocation solution."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.parameters = PositiveAIBenchmarkParameters()
        cls.seed = balanced_growth_seed(cls.parameters)

    def test_exact_bgp_is_a_zero_transition(self) -> None:
        solution = solve_transition(
            self.parameters,
            self.seed.capital,
            self.seed.capability,
            horizons=(100.0,),
            continuation_steps=2,
            initial_nodes=41,
            tolerance=1e-9,
        )
        audit = audit_solution(solution, sample_points=301)
        self.assertTrue(audit["success"])
        self.assertLess(audit["max_normalized_ode_residual"], 1e-12)
        self.assertLess(audit["max_boundary_residual"], 1e-12)
        self.assertLess(audit["terminal_deviation_norm"], 1e-12)

    def test_local_off_bgp_transition_passes_independent_audit(self) -> None:
        target = initial_stocks_matching_bgp_capital_output_ratio(
            self.parameters, 1.10 * self.seed.capability, self.seed
        )
        solution = solve_transition(
            self.parameters,
            target.capital,
            target.capability,
            horizons=(100.0, 150.0, 200.0, 250.0),
            continuation_steps=5,
            initial_nodes=81,
            tolerance=1e-8,
        )
        audit = audit_solution(solution, sample_points=1001)
        self.assertTrue(audit["success"])
        self.assertLess(audit["maximum_rms_residual"], 2e-8)
        self.assertLess(audit["max_normalized_ode_residual"], 2e-7)
        self.assertLess(audit["max_resource_residual"], 2e-7)
        self.assertLess(audit["max_euler_residual"], 2e-7)
        self.assertLess(audit["max_capability_residual"], 2e-7)
        self.assertLess(audit["max_costate_residual"], 2e-7)
        self.assertLess(audit["max_boundary_residual"], 1e-9)
        self.assertGreater(audit["minimum_consumption_share"], 0.0)
        self.assertGreater(audit["minimum_research_share"], 0.0)
        # Acceptance rests on stability of the initial jumps and the common
        # finite-window path, not on forcing the T endpoint to the BGP.
        self.assertLess(audit["last_horizon_initial_jump_change"], 1e-5)
        self.assertLess(audit["household_log_tvc_change"], 0.0)
        self.assertLess(audit["developer_log_tvc_change"], 0.0)
        self.assertLess(
            audit["segmented_backward_reconstruction_gap"], 2e-7
        )

    def test_paper_initial_stocks_are_off_bgp_and_numerically_stable(
        self,
    ) -> None:
        target = initial_stocks_matching_bgp_capital_output_ratio(
            self.parameters, 1.0, self.seed
        )
        self.assertGreater(
            abs(target.log_capability_deviation_from_bgp), 0.5
        )
        base = solve_transition(
            self.parameters,
            target.capital,
            target.capability,
            horizons=(100.0, 150.0, 200.0, 250.0),
            continuation_steps=12,
            initial_nodes=121,
            tolerance=1e-8,
        )
        refined = solve_transition(
            self.parameters,
            target.capital,
            target.capability,
            horizons=(100.0, 150.0, 200.0, 250.0),
            continuation_steps=16,
            initial_nodes=181,
            tolerance=1e-9,
        )
        audit = audit_solution(refined, sample_points=1001)
        times = np.linspace(0.0, 50.0, 401)
        jump_gap = float(
            np.max(
                np.abs(
                    base.initial_deviations[2:]
                    - refined.initial_deviations[2:]
                )
            )
        )
        window_gap = float(
            np.max(
                np.abs(
                    base.evaluate_deviations(times)
                    - refined.evaluate_deviations(times)
                )
            )
        )
        self.assertTrue(audit["success"])
        self.assertLess(audit["max_resource_residual"], 5e-9)
        self.assertLess(audit["max_boundary_residual"], 1e-10)
        self.assertLess(
            audit["segmented_backward_reconstruction_gap"], 1e-8
        )
        self.assertLess(audit["last_horizon_initial_jump_change"], 3e-6)
        self.assertLess(jump_gap, 1e-9)
        self.assertLess(window_gap, 1e-7)


if __name__ == "__main__":
    unittest.main()

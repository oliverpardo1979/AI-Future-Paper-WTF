"""Regression and continuity tests for the near-unit positive-AI BVP."""

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
    normalized_dynamics,
    normalized_jacobian,
)
from solve_near_unit_ai_bvp import (  # noqa: E402
    audit_near_unit_solution,
    dated_normalized_dynamics,
    dated_normalized_jacobian,
    elasticity_continuation_schedule,
    elasticity_coordinate,
    sigma_from_coordinate,
    solve_monopoly_static_block,
    solve_near_unit_transition,
)


class NearUnitAIBVPSolverTests(unittest.TestCase):
    """Check exact nesting at one and local continuation on both sides."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.parameters = PositiveAIBenchmarkParameters()
        cls.seed = balanced_growth_seed(cls.parameters)
        cls.target = initial_stocks_matching_bgp_capital_output_ratio(
            cls.parameters, 1.0, cls.seed
        )

    def test_regular_coordinate_round_trip_and_schedule(self) -> None:
        for sigma_xl in (0.99, 0.9999, 1.0, 1.0001, 1.01):
            self.assertAlmostEqual(
                sigma_from_coordinate(elasticity_coordinate(sigma_xl)),
                sigma_xl,
                places=14,
            )
        schedule = elasticity_continuation_schedule(0.99, steps=4)
        self.assertEqual(schedule[0], 0.0)
        self.assertAlmostEqual(schedule[-1], elasticity_coordinate(0.99))
        self.assertTrue(all(np.diff(schedule) < 0.0))
        self.assertEqual(
            elasticity_continuation_schedule(1.0, steps=4), (0.0,)
        )

    def test_dated_system_reproduces_exact_unit_system(self) -> None:
        times = np.asarray([0.0, 13.0, 47.0])
        deviations = np.asarray(
            [
                [0.08, 0.03, -0.02],
                [0.12, 0.07, 0.01],
                [0.04, 0.02, -0.03],
                [-0.09, -0.04, 0.02],
            ]
        )
        expected = normalized_dynamics(
            deviations, self.parameters, self.seed
        )
        actual = dated_normalized_dynamics(
            times, deviations, 1.0, self.parameters, self.seed
        )
        np.testing.assert_allclose(actual, expected, atol=2e-14, rtol=2e-13)

        expected_jacobian = normalized_jacobian(
            deviations, self.parameters, self.seed
        )
        actual_jacobian = dated_normalized_jacobian(
            times, deviations, 1.0, self.parameters, self.seed
        )
        np.testing.assert_allclose(
            actual_jacobian, expected_jacobian, atol=2e-14, rtol=3e-13
        )

    def test_static_block_is_continuous_and_satisfies_monopoly_foc(self) -> None:
        logs = (
            np.log(self.target.capital),
            np.log(self.target.capability),
            0.0,
        )
        unit = solve_monopoly_static_block(
            *logs, 1.0, self.parameters
        )
        errors = []
        for distance in (1e-2, 1e-3, 1e-4):
            pair_error = 0.0
            for sigma_xl in (1.0 - distance, 1.0 + distance):
                block = solve_monopoly_static_block(
                    *logs, sigma_xl, self.parameters
                )
                self.assertLess(abs(block.monopoly_foc_log_residual), 2e-12)
                self.assertGreater(block.monopoly_soc_margin, 0.0)
                pair_error = max(
                    pair_error,
                    abs(block.log_output - unit.log_output),
                    abs(block.log_ai_services - unit.log_ai_services),
                    abs(block.ai_ces_share - unit.ai_ces_share),
                )
            errors.append(pair_error)
        self.assertGreater(errors[0], errors[1])
        self.assertGreater(errors[1], errors[2])

    def test_nonunit_analytic_jacobian_matches_finite_differences(self) -> None:
        time = 37.0
        deviations = np.asarray([0.05, 0.09, 0.02, -0.07])
        step = 1e-6
        for sigma_xl in (0.99, 1.01):
            with self.subTest(sigma_xl=sigma_xl):
                analytic = dated_normalized_jacobian(
                    time,
                    deviations,
                    sigma_xl,
                    self.parameters,
                    self.seed,
                )
                numerical = np.empty((4, 4))
                for column in range(4):
                    change = np.zeros(4)
                    change[column] = step
                    upper = dated_normalized_dynamics(
                        time,
                        deviations + change,
                        sigma_xl,
                        self.parameters,
                        self.seed,
                    )
                    lower = dated_normalized_dynamics(
                        time,
                        deviations - change,
                        sigma_xl,
                        self.parameters,
                        self.seed,
                    )
                    numerical[:, column] = (upper - lower) / (2.0 * step)
                np.testing.assert_allclose(
                    analytic, numerical, atol=2e-9, rtol=2e-7
                )

    def test_both_near_unit_regimes_pass_equation_audits(self) -> None:
        for sigma_xl in (0.99, 1.01):
            with self.subTest(sigma_xl=sigma_xl):
                solution = solve_near_unit_transition(
                    self.parameters,
                    self.target.capital,
                    self.target.capability,
                    sigma_xl,
                    horizons=(100.0,),
                    stock_continuation_steps=10,
                    elasticity_continuation_steps=4,
                    initial_nodes=101,
                    tolerance=1e-8,
                )
                audit = audit_near_unit_solution(
                    solution, sample_points=301
                )
                self.assertTrue(audit["success"])
                self.assertLess(audit["maximum_rms_residual"], 2e-8)
                self.assertLess(audit["max_normalized_ode_residual"], 2e-7)
                self.assertLess(audit["max_resource_residual"], 2e-7)
                self.assertLess(audit["max_euler_residual"], 2e-7)
                self.assertLess(audit["max_capability_residual"], 2e-7)
                self.assertLess(audit["max_costate_residual"], 2e-7)
                self.assertLess(
                    audit["max_monopoly_foc_log_residual"], 2e-11
                )
                self.assertLess(
                    audit["max_research_foc_log_residual"], 2e-11
                )
                self.assertLess(audit["max_boundary_residual"], 1e-9)
                self.assertLess(
                    audit["segmented_backward_reconstruction_gap"], 2e-7
                )
                self.assertGreater(audit["minimum_consumption_share"], 0.0)
                self.assertGreater(audit["minimum_research_share"], 0.0)
                self.assertGreater(audit["minimum_inference_share"], 0.0)
                self.assertGreater(
                    audit["minimum_monopoly_soc_margin"], 0.0
                )

    def test_paths_converge_bilaterally_to_unit_elasticity(self) -> None:
        unit = solve_near_unit_transition(
            self.parameters,
            self.target.capital,
            self.target.capability,
            1.0,
            horizons=(100.0,),
            stock_continuation_steps=10,
            elasticity_continuation_steps=1,
            initial_nodes=101,
            tolerance=1e-8,
        )
        times = np.linspace(0.0, 50.0, 101)
        unit_path = unit.evaluate_deviations(times)
        side_errors: dict[str, list[float]] = {"below": [], "above": []}
        for label, sign in (("below", -1.0), ("above", 1.0)):
            for distance in (1e-2, 1e-3, 1e-4):
                solution = solve_near_unit_transition(
                    self.parameters,
                    self.target.capital,
                    self.target.capability,
                    1.0 + sign * distance,
                    horizons=(100.0,),
                    stock_continuation_steps=10,
                    elasticity_continuation_steps=3,
                    initial_nodes=101,
                    tolerance=1e-8,
                )
                error = float(
                    np.max(
                        np.abs(solution.evaluate_deviations(times) - unit_path)
                    )
                )
                side_errors[label].append(error)
            self.assertGreater(side_errors[label][0], side_errors[label][1])
            self.assertGreater(side_errors[label][1], side_errors[label][2])
            self.assertLess(side_errors[label][2], 2e-3)

    def test_both_regimes_are_stable_to_numerical_refinement(self) -> None:
        times = np.linspace(0.0, 50.0, 101)
        for sigma_xl in (0.99, 1.01):
            with self.subTest(sigma_xl=sigma_xl):
                base = solve_near_unit_transition(
                    self.parameters,
                    self.target.capital,
                    self.target.capability,
                    sigma_xl,
                    horizons=(100.0,),
                    stock_continuation_steps=10,
                    elasticity_continuation_steps=4,
                    initial_nodes=81,
                    tolerance=1e-8,
                )
                refined = solve_near_unit_transition(
                    self.parameters,
                    self.target.capital,
                    self.target.capability,
                    sigma_xl,
                    horizons=(100.0,),
                    stock_continuation_steps=14,
                    elasticity_continuation_steps=6,
                    initial_nodes=141,
                    tolerance=1e-9,
                )
                jump_gap = float(
                    np.max(
                        np.abs(
                            base.initial_deviations[2:]
                            - refined.initial_deviations[2:]
                        )
                    )
                )
                path_gap = float(
                    np.max(
                        np.abs(
                            base.evaluate_deviations(times)
                            - refined.evaluate_deviations(times)
                        )
                    )
                )
                self.assertLess(jump_gap, 2e-8)
                self.assertLess(path_gap, 2e-7)

    def test_common_window_is_stable_when_horizon_is_extended(self) -> None:
        times = np.linspace(0.0, 50.0, 101)
        for sigma_xl in (0.99, 1.01):
            with self.subTest(sigma_xl=sigma_xl):
                shorter = solve_near_unit_transition(
                    self.parameters,
                    self.target.capital,
                    self.target.capability,
                    sigma_xl,
                    horizons=(100.0, 150.0, 200.0),
                    stock_continuation_steps=12,
                    elasticity_continuation_steps=5,
                    initial_nodes=121,
                    tolerance=1e-8,
                )
                longer = solve_near_unit_transition(
                    self.parameters,
                    self.target.capital,
                    self.target.capability,
                    sigma_xl,
                    horizons=(100.0, 150.0, 200.0, 250.0),
                    stock_continuation_steps=12,
                    elasticity_continuation_steps=5,
                    initial_nodes=121,
                    tolerance=1e-8,
                )
                jump_gap = float(
                    np.max(
                        np.abs(
                            shorter.initial_deviations[2:]
                            - longer.initial_deviations[2:]
                        )
                    )
                )
                path_gap = float(
                    np.max(
                        np.abs(
                            shorter.evaluate_deviations(times)
                            - longer.evaluate_deviations(times)
                        )
                    )
                )
                # The horizon effect must remain much smaller than the roughly
                # 1.6e-2 parameter effect generated by moving sigma by 0.01.
                self.assertLess(jump_gap, 2e-5)
                self.assertLess(path_gap, 2e-5)


if __name__ == "__main__":
    unittest.main()

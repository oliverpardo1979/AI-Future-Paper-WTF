"""Analytic tests for the nondegenerate positive-AI branch definition."""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from define_positive_ai_branch import (  # noqa: E402
    PositiveAIBenchmarkParameters,
    balanced_growth_seed,
    boundary_jacobians,
    boundary_residual,
    canonical_seed_residuals,
    initial_stocks_matching_bgp_capital_output_ratio,
    normalized_dynamics,
    normalized_jacobian,
    positive_weight_schedule,
    stable_subspace,
    state_continuation_schedule,
)


class PositiveAIBranchDefinitionTests(unittest.TestCase):
    """Check the analytic seed, saddle structure, and continuation guards."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.parameters = PositiveAIBenchmarkParameters()
        cls.seed = balanced_growth_seed(cls.parameters)
        cls.subspace = stable_subspace(cls.parameters, cls.seed)

    def test_seed_satisfies_every_reconstructed_equilibrium_equation(self) -> None:
        audit = canonical_seed_residuals(self.parameters, self.seed)
        self.assertLess(audit["max_abs_equilibrium_residual"], 1e-13)
        self.assertGreater(audit["tvc_decay_rate"], 0.0)
        self.assertGreater(self.seed.consumption_share, 0.0)
        self.assertGreater(self.seed.research_share, 0.0)
        self.assertAlmostEqual(
            self.seed.inference_share,
            self.seed.beta**2,
        )

    def test_normalized_origin_and_analytic_jacobian(self) -> None:
        origin = np.zeros(4)
        residual = normalized_dynamics(origin, self.parameters, self.seed)
        self.assertLess(float(np.max(np.abs(residual))), 1e-13)

        analytic = normalized_jacobian(origin, self.parameters, self.seed)
        step = 1e-6
        numerical = np.column_stack(
            [
                (
                    normalized_dynamics(
                        origin + step * np.eye(4)[index],
                        self.parameters,
                        self.seed,
                    )
                    - normalized_dynamics(
                        origin - step * np.eye(4)[index],
                        self.parameters,
                        self.seed,
                    )
                )
                / (2.0 * step)
                for index in range(4)
            ]
        )
        self.assertLess(float(np.max(np.abs(analytic - numerical))), 1e-9)

        vectorized = normalized_jacobian(
            np.zeros((4, 3)), self.parameters, self.seed
        )
        self.assertEqual(vectorized.shape, (4, 4, 3))
        for index in range(3):
            np.testing.assert_allclose(vectorized[:, :, index], analytic)

    def test_two_state_two_jump_boundary_system_is_well_posed(self) -> None:
        eigenvalues = self.subspace.eigenvalues
        self.assertEqual(int(np.sum(eigenvalues.real < 0.0)), 2)
        self.assertEqual(int(np.sum(eigenvalues.real > 0.0)), 2)
        self.assertGreater(
            abs(self.subspace.state_projection_determinant), 1e-4
        )
        self.assertTrue(
            math.isfinite(self.subspace.state_projection_condition_number)
        )
        np.testing.assert_allclose(
            self.subspace.terminal_matrix @ self.subspace.stable_basis,
            np.zeros((2, 2)),
            atol=1e-13,
        )

        stable_terminal = self.subspace.stable_basis @ np.asarray([0.2, -0.1])
        initial_states = np.asarray([0.05, 0.15])
        left = np.asarray([0.05, 0.15, -0.02, 0.01])
        residual = boundary_residual(
            left, stable_terminal, initial_states, self.subspace
        )
        np.testing.assert_allclose(residual, np.zeros(4), atol=1e-13)

        left_jacobian, right_jacobian = boundary_jacobians(self.subspace)
        np.testing.assert_allclose(left_jacobian[:2, :2], np.eye(2))
        np.testing.assert_allclose(left_jacobian[2:, :], 0.0)
        np.testing.assert_allclose(right_jacobian[:2, :], 0.0)
        np.testing.assert_allclose(
            right_jacobian[2:, :], self.subspace.terminal_matrix
        )

    def test_zero_is_rejected_as_a_positive_ai_continuation_point(self) -> None:
        with self.assertRaises(ValueError):
            PositiveAIBenchmarkParameters(omega_x=0.0)
        with self.assertRaises(ValueError):
            positive_weight_schedule(0.0, 0.20, stages=4)

        schedule = positive_weight_schedule(0.10, 0.20, stages=4)
        self.assertAlmostEqual(schedule[0], 0.10)
        self.assertAlmostEqual(schedule[-1], 0.20)
        self.assertTrue(all(0.0 < weight < 1.0 for weight in schedule))

    def test_stock_continuation_starts_on_bgp_and_reaches_normalization(self) -> None:
        target = initial_stocks_matching_bgp_capital_output_ratio(
            self.parameters, capability=1.0, seed=self.seed
        )
        self.assertAlmostEqual(target.capability, 1.0)
        self.assertAlmostEqual(
            target.capital_output_ratio, self.seed.capital_output_ratio
        )
        self.assertNotAlmostEqual(self.seed.capability, 1.0)

        steps = state_continuation_schedule(
            np.asarray(
                [
                    target.log_capital_deviation_from_bgp,
                    target.log_capability_deviation_from_bgp,
                ]
            ),
            stages=5,
        )
        np.testing.assert_allclose(steps[0], np.zeros(2))
        np.testing.assert_allclose(
            steps[-1],
            np.asarray(
                [
                    target.log_capital_deviation_from_bgp,
                    target.log_capability_deviation_from_bgp,
                ]
            ),
        )

        ai_services = (
            self.seed.inference_share
            * target.capability
            * target.implied_output
        )
        composite = (
            self.parameters.initial_labor_productivity
            * self.parameters.initial_population
        ) ** self.parameters.omega_l * ai_services**self.parameters.omega_x
        reconstructed_output = (
            target.capital**self.parameters.alpha
            * composite ** (1.0 - self.parameters.alpha)
        )
        self.assertAlmostEqual(reconstructed_output, target.implied_output)


if __name__ == "__main__":
    unittest.main()

"""Algebra and source scope of the restored low-eta result; no simulations."""
from fractions import Fraction as F
import json
from pathlib import Path
import unittest

from test_rewrite_proposition_structure import source

ROOT = Path(__file__).resolve().parents[1]


class ResearchScale(unittest.TestCase):
    def test_composed_exponent_crosses_one_exactly_at_alpha(self):
        for alpha in (F(1, 10), F(33, 100), F(1, 2), F(9, 10)):
            for eta in (alpha / 2, alpha, (1 + alpha) / 2):
                expenditure_to_efficiency = eta / (1 - eta)
                efficiency_to_profit = (1 - alpha) / alpha
                exponent = expenditure_to_efficiency * efficiency_to_profit
                self.assertEqual(exponent - 1, (eta - alpha) / (alpha * (1 - eta)))
                self.assertEqual(exponent < 1, eta < alpha)
                self.assertEqual(exponent > 1, eta > alpha)

    def test_sublinear_profit_bound_has_a_finite_maximum(self):
        # Check the bound C0+C1*S**p-D*S, not a solved equilibrium path.
        for p in (0.1, 0.5075757575757576, 0.9):
            C0, C1, D = 2., 3., 0.7
            peak = (p * C1 / D) ** (1 / (1 - p))
            upper = lambda S: C0 + C1 * S**p - D * S
            self.assertAlmostEqual(C1 * p * peak**(p - 1), D)
            for factor in (0., 0.5, 2., 10.):
                self.assertLessEqual(upper(factor * peak), upper(peak))
            # Once C1*S**p <= D*S/2, the bound is <= C0-D*S/2.
            threshold = (2 * C1 / D) ** (1 / (1 - p))
            S = threshold * 10
            self.assertLessEqual(upper(S), C0 - D * S / 2)

    def test_statement_distinguishes_bounded_value_from_existence(self):
        body = source('sections_rewrite/05_uncapped_equilibria.tex')
        statement = body.split(r'\label{prop:rewrite-research-scale}')[1].split(
            r'\end{proposition}')[0]
        self.assertEqual(statement.count(r'\item'), 2)
        self.assertIn(r'\eqref{eq:rewrite-developer-reduced}', statement)
        self.assertIn('positive continuous paths', statement)
        self.assertIn('integrable interest-rate path', statement)
        self.assertNotIn('attains', statement)
        normalized = ' '.join(body.split())
        self.assertIn('Part (i) does not establish an infinite-horizon equilibrium', normalized)
        self.assertIn('not needed to bound', normalized)
        proof = source('sections_rewrite/appendix.tex')
        self.assertIn(r'\emph{Part (i).}', proof)
        self.assertIn(r'\emph{Part (ii).}', proof)
        self.assertIn(r'\label{eq:rewrite-truncated-value-bound}', proof)

    def test_calibration_is_unchanged_and_motivation_is_referenced(self):
        for folder in ('rsi_research_share_2023', 'rsi_activation_half_decline'):
            params = json.loads((ROOT / 'numerical_rewrite' / folder /
                                 'paths_manifest.json').read_text())['parameters']
            self.assertEqual(params['eta'], 0.2)
            self.assertEqual(params['alpha'], 0.33)
            p = params['eta'] * (1 - params['alpha']) / (params['alpha'] * (1 - params['eta']))
            self.assertAlmostEqual(p, 0.5075757575757576)
        for path in ('sections_rewrite/08_rsi_design.tex',
                     'sections_rewrite/rsi_parameters.tex'):
            self.assertIn(r'\ref{prop:rewrite-research-scale}(i)', source(path))


if __name__ == '__main__':
    unittest.main()

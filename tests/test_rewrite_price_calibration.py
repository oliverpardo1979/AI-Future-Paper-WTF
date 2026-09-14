"""Price-target mapping, preserved calibration, and saved-path admission."""
from dataclasses import asdict
import json
import math
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / '.python-packages'), str(ROOT / 'scripts')]
import numpy as np
from calibrate_rewrite_ai_price import (
    make_design, log_price_ratio, TARGET_YEARS, TARGET_PRICE_RATIO, OUTPUT, CACHE,
)
from simulate_rewrite_finite_frontier import (
    PARAMETERS, FRONTIER, MAIN_DESIGN, RAMSEY_START_DESIGN, RAMSEY_START_STEADY_STATE,
    SIGMAS, load_solution, key,
)
from solve_near_unit_ai_bvp import solve_monopoly_static_block
from audit_rewrite_equilibria import independent_residuals
from audit_rewrite_hamiltonian_support import audit_support
from types import SimpleNamespace


class PriceCalibration(unittest.TestCase):
    def test_only_chi_changes_and_stocks_are_predetermined(self):
        design = make_design(51.0)
        original, changed = asdict(PARAMETERS), asdict(design.parameters)
        original.pop('chi'); changed.pop('chi')
        self.assertEqual(original, changed)
        self.assertEqual(design.initial_capital, RAMSEY_START_STEADY_STATE.capital)
        self.assertEqual(design.frontier, FRONTIER)
        self.assertAlmostEqual(design.initial_capability/FRONTIER, .1)
        self.assertEqual(design.sigmas, SIGMAS)
        self.assertNotEqual(design.cache_directory, MAIN_DESIGN.cache_directory)
        self.assertNotEqual(design.output_directory, RAMSEY_START_DESIGN.output_directory)

    def test_target_is_cumulative_over_27_months(self):
        self.assertEqual(TARGET_YEARS, 2.25)
        self.assertEqual(TARGET_PRICE_RATIO, .2)
        annual_ratio = TARGET_PRICE_RATIO**(1/TARGET_YEARS)
        self.assertAlmostEqual(annual_ratio**TARGET_YEARS, .2)
        self.assertNotEqual(annual_ratio, .2)

    def test_unit_price_identity_and_revenue_share(self):
        p = make_design(51.0).parameters
        for b in (.1*FRONTIER, .5*FRONTIER, .9*FRONTIER):
            static = solve_monopoly_static_block(math.log(5.94), math.log(b), 0., 1., p)
            price = (1-p.alpha)*static.ai_ces_share*math.exp(static.log_output-static.log_ai_services)
            self.assertAlmostEqual(price*b, 1/((1-p.alpha)*p.omega_x), places=10)
            self.assertAlmostEqual((1-p.alpha)*static.ai_ces_share, .134)

    def test_price_ratio_uses_exact_target_date(self):
        solution = SimpleNamespace(horizon=10., parameters=PARAMETERS,
                                   terminal=SimpleNamespace(sigma_xl=1.),
                                   raw=SimpleNamespace(sol=lambda t: np.zeros((4,len(t)))))
        values = dict(ai_ces_share=np.array([.2,.2]), log_capability=np.log([10.,50.]))
        with patch('calibrate_rewrite_ai_price.reconstruct_levels', return_value=values):
            self.assertAlmostEqual(math.exp(log_price_ratio(solution)), .2)
        with self.assertRaises(ValueError):
            log_price_ratio(solution, years=11.)

    def test_audits_reject_out_of_horizon_early_dates(self):
        solution = SimpleNamespace(horizon=5.)
        with self.assertRaises(ValueError):
            independent_residuals(solution, .001, [0.])
        with self.assertRaises(ValueError):
            audit_support(solution, sample_times=[6.])

    @unittest.skipUnless((OUTPUT/'figure_manifest.json').exists()
                         and (CACHE/f'{key(1.)}_long.npz').exists(),
                         'Regenerate local checkpoints to test the saved numerical match')
    def test_published_results_are_admitted_and_match_target(self):
        calibration=json.loads((OUTPUT/'calibration.json').read_text())
        self.assertEqual(calibration['status'], 'numerically_admitted')
        design=make_design(calibration['chi'])
        for sigma in SIGMAS:
            report=json.loads((OUTPUT/f'{key(sigma)}_audit.json').read_text())
            self.assertTrue(report['equilibrium_certified'])
            self.assertTrue(report['early_window_checks']['passes'])
            self.assertEqual(report['parameters'], asdict(design.parameters))
        unit=load_solution(CACHE/f'{key(1.)}_long.npz')
        self.assertLess(abs(log_price_ratio(unit)-math.log(.2)), 2e-5)


if __name__ == '__main__':
    unittest.main()

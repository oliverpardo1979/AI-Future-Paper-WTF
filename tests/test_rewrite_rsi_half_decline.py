"""The slower price-target exercise changes chi, not initial stocks or technology."""
from dataclasses import asdict
import hashlib
import json
import math
import re
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'.python-packages'), str(ROOT/'scripts')]
from calibrate_rewrite_ai_price import (
    TARGET_YEARS, TARGET_PRICE_RATIO, make_design, target_price_ratio,
    design_price_target, calibrated_design, log_price_ratio,
)
from simulate_rewrite_finite_frontier import SIGMAS, key, design_initial_stocks, load_solution
from analyze_axm_finite_cap_bvp import terminal_point

VARIANT = 'rsi_activation_half_decline'
OUT = ROOT/'numerical_rewrite'/VARIANT
CACHE = ROOT/'tmp'/f'rewrite_bvp_{VARIANT}'


class HalfDeclineTarget(unittest.TestCase):
    def test_target_halves_percentage_decline_not_log_change(self):
        self.assertEqual(TARGET_PRICE_RATIO, 0.2)
        self.assertEqual(TARGET_YEARS, 2.25)
        self.assertAlmostEqual(target_price_ratio(VARIANT), 0.6)
        self.assertAlmostEqual(1-target_price_ratio(VARIANT), 0.5*(1-TARGET_PRICE_RATIO))
        self.assertNotAlmostEqual(target_price_ratio(VARIANT), math.sqrt(TARGET_PRICE_RATIO))
        for variant in ('baseline', 'low_ai', 'rsi_activation'):
            self.assertEqual(target_price_ratio(variant), 0.2)

    def test_same_parameters_and_initial_stocks_at_given_chi(self):
        old, new = make_design(10., 'rsi_activation'), make_design(10., VARIANT)
        self.assertEqual(asdict(old.parameters), asdict(new.parameters))
        self.assertEqual(old.frontier, new.frontier)
        self.assertEqual(old.initial_capital_rule, new.initial_capital_rule)
        self.assertEqual(old.display_horizon, new.display_horizon)
        for sigma in SIGMAS:
            self.assertEqual(design_initial_stocks(old, sigma), design_initial_stocks(new, sigma))

    def test_distinct_outputs_and_matching_target(self):
        old, new = make_design(10., 'rsi_activation'), make_design(10., VARIANT)
        self.assertNotEqual(old.output_directory, new.output_directory)
        self.assertNotEqual(old.cache_directory, new.cache_directory)
        self.assertEqual(design_price_target(old), 0.2)
        self.assertEqual(design_price_target(new), 0.6)
        with self.assertRaises(ValueError):
            target_price_ratio('unknown')

    @unittest.skipUnless((OUT/'calibration.json').exists(), 'Run the new calibration first')
    def test_refit_changes_only_chi(self):
        old, new = calibrated_design('rsi_activation'), calibrated_design(VARIANT)
        a,b = asdict(old.parameters), asdict(new.parameters)
        self.assertNotEqual(a.pop('chi'), b.pop('chi'))
        self.assertEqual(a,b)
        for sigma in SIGMAS:
            self.assertEqual(design_initial_stocks(old,sigma), design_initial_stocks(new,sigma))
        calibration=json.loads((OUT/'calibration.json').read_text())
        self.assertEqual(calibration['target_decline_fraction_of_observed'], 0.5)

    @unittest.skipUnless((OUT/'calibration.json').exists(), 'Run the new calibration first')
    def test_same_long_run_growth_and_interest(self):
        old, new = calibrated_design('rsi_activation'), calibrated_design(VARIANT)
        for sigma in SIGMAS:
            a=terminal_point(sigma,old.frontier,old.parameters)
            b=terminal_point(sigma,new.frontier,new.parameters)
            self.assertEqual(a.regime,b.regime)
            # Compare the economic limiting rates, not chi-dependent normalization scales.
            self.assertAlmostEqual(a.net_interest_rate,b.net_interest_rate)
            self.assertAlmostEqual(a.terminal_growth,b.terminal_growth)
            self.assertAlmostEqual(a.labor_income_share,b.labor_income_share)

    @unittest.skipUnless((OUT/'calibration.json').exists(), 'Run the new calibration first')
    def test_parameter_table_matches_stored_calibration(self):
        d=calibrated_design(VARIANT)
        text=(ROOT/'sections_rewrite/rsi_half_decline_parameters.tex').read_text()
        table=dict(re.findall(r'^\$([^$]+)\$ & (.*?) &',text,re.M))
        self.assertAlmostEqual(float(table[r'\chi']),d.parameters.chi,places=6)
        self.assertAlmostEqual(float(table[r'\overline B'].replace(',','')),d.frontier,places=6)
        self.assertAlmostEqual(float(table['B_0']),d.initial_capability,places=6)
        for sigma, value in zip(SIGMAS,table['K_0'].split(';')):
            self.assertAlmostEqual(float(value),design_initial_stocks(d,sigma)[0],places=6)

    @unittest.skipUnless((OUT/'activation_audit.json').exists()
        and all((CACHE/f'{key(s)}_long.npz').exists() for s in SIGMAS),
        'Regenerate and audit the four BVP checkpoints first')
    def test_equilibrium_admission_and_price_match(self):
        event=json.loads((OUT/'activation_audit.json').read_text())
        self.assertTrue(event['passes'])
        for sigma in SIGMAS:
            report=json.loads((OUT/f'{key(sigma)}_audit.json').read_text())
            self.assertTrue(report['equilibrium_certified'])
            self.assertTrue(report['early_window_checks']['passes'])
            self.assertEqual(hashlib.sha256((CACHE/report['checkpoint_filename']).read_bytes()).hexdigest(),
                             report['checkpoint_sha256'])
            self.assertLess(max(event['scenarios'][key(sigma)]['level_log_gaps'].values()),1e-9)
        solution=load_solution(CACHE/f'{key(1.)}_long.npz')
        self.assertLess(abs(log_price_ratio(solution)-math.log(.6)),2e-5)

    @unittest.skipUnless((OUT/'figure_manifest.json').exists(), 'Render the new comparison first')
    def test_export_provenance_and_target_marker(self):
        manifest=json.loads((OUT/'figure_manifest.json').read_text())
        self.assertTrue(manifest['all_scenarios_admitted'])
        if manifest.get('active_calibration_record') == 'research_share_target.json':
            self.assertIsNone(manifest['price_target'])
            self.assertEqual(manifest['price_outcome_marker'], dict(years=2.25,ratio=.6))
        else:  # Historical price-only reproduction remains available.
            self.assertEqual(manifest['price_target'], dict(years=2.25,ratio=.6))
        self.assertEqual(manifest['data_sha256'],hashlib.sha256((OUT/'equilibrium_paths.csv').read_bytes()).hexdigest())
        self.assertEqual(manifest['activation_audit_sha256'],hashlib.sha256((OUT/'activation_audit.json').read_bytes()).hexdigest())
        self.assertEqual(len(manifest['two_window_views']),3)

    @unittest.skipUnless((OUT/'comparison_to_full_decline.json').exists(), 'Finish the comparison first')
    def test_comparison_is_bound_to_both_exports(self):
        comparison=json.loads((OUT/'comparison_to_full_decline.json').read_text())
        self.assertTrue(comparison['same_parameters_except_chi'])
        self.assertTrue(comparison['same_initial_stocks'])
        for variant, values in comparison['cases'].items():
            folder=ROOT/'numerical_rewrite'/variant
            self.assertEqual(values['data_sha256'],hashlib.sha256((folder/'equilibrium_paths.csv').read_bytes()).hexdigest())
            self.assertEqual(values['activation_audit_sha256'],hashlib.sha256((folder/'activation_audit.json').read_bytes()).hexdigest())


if __name__ == '__main__':
    unittest.main()

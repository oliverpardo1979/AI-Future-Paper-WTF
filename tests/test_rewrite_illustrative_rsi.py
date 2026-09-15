"""Reproducible design, equilibrium admission, provenance and paper numbers."""
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from simulate_rewrite_illustrative_rsi import make_design, PRODUCTIVITIES, SIGMAS, key, design_initial_stocks
from report_rewrite_illustrative_rsi import admitted_data
from test_rewrite_simulation_selection import quantitative_text


class IllustrativeRSI(unittest.TestCase):
    def test_only_chi_differs(self):
        high, low = [make_design(c) for c in PRODUCTIVITIES]
        p, q = [asdict(d.parameters) for d in (high, low)]
        self.assertEqual(p.pop('chi')/q.pop('chi'), 5)
        self.assertEqual(p, q)
        self.assertEqual(p['omega_x'], .1)
        self.assertEqual(p['eta'], .2)
        self.assertEqual(high.frontier, low.frontier)
        self.assertEqual(high.initial_capability, .01*high.frontier)
        for sigma in SIGMAS:
            self.assertEqual(design_initial_stocks(high,sigma), design_initial_stocks(low,sigma))
        self.assertNotEqual(high.cache_directory, low.cache_directory)

    def test_all_eight_admitted_and_horizon_stable(self):
        for chi in PRODUCTIVITIES:
            d = admitted_data(make_design(chi).name)
            self.assertIsNone(d['spec']['empirical_target'])
            self.assertTrue(d['spec']['outcomes_not_targets'])
            for r in d['reports']:
                with self.subTest(chi=chi, sigma=r['sigma_xl']):
                    self.assertTrue(r['equilibrium_certified'])
                    self.assertLess(r['horizon_comparison']['maximum_common_window_coordinate_change'],1e-5)
                    for c in r['independent_dated_checks']+r['early_window_checks']['independent_residuals']:
                        self.assertLess(c['maximum_ode_residual'],1e-6)
                        self.assertLess(c['maximum_monopoly_foc_residual'],1e-9)
                        self.assertLess(c['maximum_research_foc_residual'],1e-9)
                    self.assertLess(r['audit']['asymptotic_household_tvc_growth'],0)
                    self.assertLess(r['audit']['asymptotic_developer_tvc_growth'],0)
                    self.assertTrue(r['audit']['newton_safeguard_not_binding'])
                    if r['sigma_xl']==1.5:
                        self.assertTrue(all(g['support_diagnostic_passes'] for g in r['global_hamiltonian_support']))
                        self.assertGreater(r['analytical_support_continuation']['analytical_limiting_margin'],0)
                    else:
                        self.assertTrue(r['counterfactual_developer_sufficiency']['developer_sufficiency_gate_passes'])

    def test_pre_rsi_bgp_and_continuity(self):
        for chi in PRODUCTIVITIES:
            d = admitted_data(make_design(chi).name)
            for k in (key(s) for s in SIGMAS):
                event = d['event']['scenarios'][k]
                self.assertTrue(event['passes'])
                self.assertEqual(event['pre']['research_compute'],0)
                self.assertGreater(event['pre']['inference_compute'],0)
                self.assertAlmostEqual(event['pre']['capital_output_ratio'],3.3)
                self.assertLess(max(abs(x) for x in event['level_log_gaps'].values()),1e-9)

    def test_reported_outcomes_match_paths(self):
        from report_rewrite_illustrative_rsi import percent
        for chi in PRODUCTIVITIES:
            name=make_design(chi).name
            d=admitted_data(name)
            text=(ROOT/'sections_rewrite'/f'{name}_results.tex').read_text()
            for sigma in SIGMAS:
                row=d['summary']['scenarios'][key(sigma)]['snapshots']['0.0']
                self.assertIn(percent(row['output_per_person_growth']),text)
                moment=d['annual']['scenarios'][key(sigma)]
                self.assertLess(moment['maximum_horizon_log_change'],2e-5)
            self.assertIn(percent(d['annual']['scenarios']['sigma_1_00']['first_year']['share'],3),text)
            self.assertIn('not calibration targets',text)
            self.assertIsNone(d['figures']['price_target'])

    def test_paper_selection_and_earlier_cases_are_recoverable(self):
        text=quantitative_text()
        self.assertIn('7.5 (higher)',text)
        self.assertIn('1.5 (lower)',text)
        self.assertNotIn('7.616305 (central)',text)
        self.assertNotIn('1.4378 (slow)',text)
        old=quantitative_text(calibrated=True)
        self.assertIn('7.616305 (central)',old)
        self.assertIn('1.4378 (slow)',old)
        for chi in PRODUCTIVITIES:
            name=make_design(chi).name
            for suffix in ('accumulation_growth','growth_returns','ai_distribution'):
                path=ROOT/'figures_rewrite'/f'equilibrium_{name}_{suffix}_windows.pdf'
                self.assertTrue(path.exists())
                self.assertGreater(path.stat().st_size,10000)


if __name__ == '__main__':
    unittest.main()

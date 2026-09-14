"""Low empirical target changes chi, not the equilibrium or initial stocks."""
from dataclasses import asdict
import csv
import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'.python-packages'),str(ROOT/'scripts')]
import calibrate_rewrite_research_share_low as low
from calibrate_rewrite_research_share import checked_moment
from calibrate_rewrite_ai_price import make_design as price_design
from simulate_rewrite_finite_frontier import design_initial_stocks,load_solution


class LowerResearchShare(unittest.TestCase):
    def setUp(self):
        self.folder=ROOT/'numerical_rewrite'/low.NAME
        self.c=json.loads((self.folder/'calibration.json').read_text())

    def test_lowest_dated_proxy_and_nearest_archived_candidate(self):
        self.assertEqual(low.SOURCE['year'],2023)
        self.assertAlmostEqual(low.TARGET_SHARE,18.46/27811.517)
        row,_=low.select_candidate()
        self.assertAlmostEqual(row['chi'],1.4378)
        self.assertEqual(self.c['chi'],row['chi'])

    def test_no_economic_changes_except_chi(self):
        new=low.make_design(self.c['chi'])
        original=price_design(self.c['chi'],'rsi_activation')
        self.assertEqual(asdict(new.parameters),asdict(original.parameters))
        self.assertEqual(new.frontier,original.frontier)
        self.assertEqual(design_initial_stocks(new,1.),design_initial_stocks(original,1.))
        self.assertEqual(new.sigmas,(1.,))
        self.assertNotEqual(new.output_directory,original.output_directory)

    def test_approximation_is_not_a_relaxed_equilibrium_tolerance(self):
        self.assertEqual(self.c['status'],'numerically_admitted_approximate_calibration')
        self.assertFalse(self.c['target_exactly_matched'])
        self.assertTrue(self.c['numerical_tolerances_unchanged'])
        error=1e4*(self.c['matched_share']-low.TARGET_SHARE)
        self.assertAlmostEqual(error,self.c['error_basis_points'])
        self.assertLess(abs(error),1.)
        self.assertLess(self.c['moment_log_change_after_two_horizon_extensions'],2e-5)
        self.assertLess(self.c['first_year']['quadrature_log_gap'],1e-8)

    def test_equilibrium_admission_and_provenance(self):
        digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
        a=json.loads((self.folder/'sigma_1_00_audit.json').read_text())
        self.assertTrue(a['equilibrium_certified'])
        self.assertTrue(a['early_window_checks']['passes'])
        self.assertLess(a['maximum_terminal_coordinate_gap'],1e-4)
        self.assertEqual(digest(self.folder/'equilibrium_paths.csv'),self.c['csv_sha256'])
        for path,sha in self.c['figure_sha256'].items():
            self.assertEqual(digest(ROOT/path),sha)
        row,selection_hash=low.select_candidate()
        self.assertEqual(selection_hash,self.c['selection_diagnostic_sha256'])
        checkpoint=low.make_design(row['chi']).cache_directory/a['checkpoint_filename']
        if checkpoint.exists():
            self.assertEqual(digest(checkpoint),self.c['checkpoint_sha256'])
            self.assertAlmostEqual(checked_moment(load_solution(checkpoint))['share'],
                self.c['matched_share'],places=12)

    def test_initial_level_continuity_and_modest_growth_effect(self):
        event=json.loads((self.folder/'activation_audit.json').read_text())
        self.assertTrue(event['passes'])
        p=event['scenarios']['sigma_1_00']
        self.assertLess(max(p['level_log_gaps'].values()),1e-9)
        self.assertAlmostEqual(p['pre']['capital_output_ratio'],3.3)
        with (self.folder/'equilibrium_paths.csv').open(newline='') as f:
            rows=list(csv.DictReader(f))
        self.assertEqual({float(r['sigma']) for r in rows},{1.})
        self.assertAlmostEqual(float(rows[0]['output_per_person_growth']),.01225026799,places=9)
        self.assertLess(max(float(r['wage_growth']) for r in rows),.014)
        self.assertLess(max(float(r['net_interest']) for r in rows),.053)

    def test_active_subsection_replaced_but_high_case_preserved(self):
        active=(ROOT/'sections_rewrite/10_rsi_research_share.tex').read_text()
        archived=(ROOT/'sections_rewrite/preserved/10_rsi_research_share_high.tex').read_text()
        self.assertIn('2023',active)
        self.assertNotIn('81.084809',active)
        self.assertIn('81.084809',archived)
        self.assertEqual(active.count('\\begin{figure}'),3)
        self.assertEqual(active.count('figures_rewrite/equilibrium_rsi_research_share_2023_'),3)
        self.assertIn('0.26',active)


if __name__=='__main__':
    unittest.main()

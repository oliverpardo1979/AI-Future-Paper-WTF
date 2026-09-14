"""Annual expenditure calibration reuses the existing equilibrium problem."""
from dataclasses import asdict
import csv
import hashlib
import json
import math
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'.python-packages'),str(ROOT/'scripts')]
import numpy as np
import calibrate_rewrite_research_share as research
from calibrate_rewrite_ai_price import make_design as price_design
from simulate_rewrite_finite_frontier import SIGMAS,key,design_initial_stocks,load_solution

OUT=research.make_design(1.).output_directory
CACHE=research.make_design(1.).cache_directory


class ResearchMoment(unittest.TestCase):
    def setUp(self):
        self.solution=SimpleNamespace(horizon=2.,raw=SimpleNamespace(sol=lambda t:t))

    def test_high_target_is_2025_dated_estimate(self):
        self.assertAlmostEqual(research.TARGET_SHARE,109.58/30762.099)
        self.assertEqual(research.SOURCE['year'],2025)
        self.assertEqual(research.TARGET_YEARS,1.)

    def test_ratio_of_integrals_not_mean_share(self):
        def levels(t,raw,solution):
            return {'log_research_compute':math.log(.02)+.4*t,
                    'log_output':math.log(2.)+.1*t}
        exact=.01*(math.expm1(.4)/.4)/(math.expm1(.1)/.1)
        wrong_mean=.01*math.expm1(.3)/.3
        with patch.object(research,'reconstruct_levels',side_effect=levels):
            value=research.checked_moment(self.solution)
            self.assertAlmostEqual(value['share'],exact,places=13)
            self.assertGreater(abs(value['share']-wrong_mean),1e-5)
            self.assertLess(value['quadrature_log_gap'],1e-12)

    def test_log_quadrature_handles_large_common_scale(self):
        def levels(t,raw,solution):
            return {'log_research_compute':np.full_like(t,1000.+math.log(.003)),
                    'log_output':np.full_like(t,1000.)}
        with patch.object(research,'reconstruct_levels',side_effect=levels):
            self.assertAlmostEqual(research.annual_research_share(self.solution),.003,places=13)

    def test_reject_extrapolation(self):
        for start,years in ((-1,1),(1,2),(0,0)):
            with self.assertRaises(ValueError):
                research.annual_research_share(self.solution,start,years)

    def test_same_economics_separate_outputs(self):
        new=research.make_design(2.)
        old=price_design(2.,'rsi_activation')
        self.assertEqual(asdict(old.parameters),asdict(new.parameters))
        self.assertEqual(old.frontier,new.frontier)
        self.assertNotEqual(old.output_directory,new.output_directory)
        self.assertNotEqual(old.cache_directory,new.cache_directory)
        for sigma in SIGMAS:
            self.assertEqual(design_initial_stocks(old,sigma),design_initial_stocks(new,sigma))

    def test_refined_moment_must_match_before_export(self):
        with patch.object(research,'checked_moment',return_value={
                'share':2*research.TARGET_SHARE,'quadrature_log_gap':0.}):
            with self.assertRaises(RuntimeError):
                research.validate_final_moment(self.solution)

    def test_turning_point_below_target_is_not_reported_as_fit(self):
        # A smooth, strictly negative log target residual with an interior peak.
        objective=lambda x: -.1-(x-math.log(80.))**2
        with patch.object(research,'trial_objective',return_value=objective), \
             patch.object(research,'diagnose',return_value={}) as diagnosis:
            with self.assertRaisesRegex(RuntimeError,'turns below target'):
                research.calibrate()
            diagnosis.assert_called_once()

    def test_diagnostic_does_not_promote_solver_failure_to_zero(self):
        def objective(x):
            if math.exp(x)>200:
                raise RuntimeError('Synthetic failed BVP')
            return -.1-(x-math.log(80.))**2
        with patch.object(research,'trial_objective',return_value=objective), \
             patch.object(research,'write_json'),patch('builtins.print'):
            result=research.diagnose()
        self.assertEqual(result['status'],'diagnostic_only_not_a_fitted_calibration')
        self.assertEqual(len(result['solver_failures']),1)
        self.assertAlmostEqual(result['local_peak_chi'],80.,places=6)
        self.assertGreater(result['relative_target_shortfall'],0)

    @unittest.skipUnless((OUT/'peak_verification.json').exists(),'Run the local peak diagnostic first')
    def test_verified_peak_is_explicitly_not_a_fit(self):
        peak=json.loads((OUT/'peak_verification.json').read_text())
        diagnostic=json.loads((OUT/'feasibility_diagnostic.json').read_text())
        self.assertEqual(peak['status'],'verified_diagnostic_peak_not_a_target_fit')
        self.assertTrue(peak['passes'])
        self.assertTrue(peak['early_window_passes'])
        self.assertTrue(peak['original_equilibrium_report']['equilibrium_certified'])
        self.assertLess(peak['first_year']['share'],research.TARGET_SHARE)
        self.assertLess(peak['moment_log_change_after_two_horizon_extensions'],2e-5)
        self.assertEqual(diagnostic['parameters_except_chi']['omega_x'],.1)
        self.assertNotIn('chi',diagnostic['parameters_except_chi'])
        self.assertGreater(len(diagnostic['solver_failures']),0)
        checkpoint=ROOT/peak['checkpoint']
        if checkpoint.exists():
            self.assertEqual(hashlib.sha256(checkpoint.read_bytes()).hexdigest(),
                peak['original_equilibrium_report']['checkpoint_sha256'])
            self.assertAlmostEqual(research.checked_moment(load_solution(checkpoint))['share'],
                peak['first_year']['share'],places=12)

    @unittest.skipUnless((OUT/'published_comparison.json').exists(),'Measure the published paths first')
    def test_published_comparison_preserves_price_targets(self):
        comparison=json.loads((OUT/'published_comparison.json').read_text())
        full=comparison['rsi_activation']
        half=comparison['rsi_activation_half_decline']
        self.assertAlmostEqual(full['price_ratio_27_months'],.2,places=7)
        self.assertAlmostEqual(half['price_ratio_27_months'],.6,places=7)
        self.assertGreater(full['first_year']['share'],half['first_year']['share'])
        for name,row in comparison.items():
            original=json.loads((ROOT/'numerical_rewrite'/name/f'{key(1.)}_audit.json').read_text())
            self.assertEqual(row['checkpoint_sha256'],original['checkpoint_sha256'])
            self.assertLess(row['first_year']['quadrature_log_gap'],1e-8)

    @unittest.skipUnless((OUT/'annual_moments.json').exists(),'Run all four equilibria first')
    def test_admission_target_and_provenance(self):
        design=research.calibrated_design()
        calibration=json.loads((OUT/'calibration.json').read_text())
        manifest=json.loads((OUT/'figure_manifest.json').read_text())
        annual=json.loads((OUT/'annual_moments.json').read_text())
        event=json.loads((OUT/'activation_audit.json').read_text())
        self.assertEqual(calibration['status'],'numerically_admitted')
        self.assertTrue(manifest['all_scenarios_admitted'])
        self.assertIsNone(manifest['price_target'])
        self.assertTrue(event['passes'])
        digest=hashlib.sha256((OUT/'equilibrium_paths.csv').read_bytes()).hexdigest()
        self.assertEqual(manifest['data_sha256'],digest)
        self.assertEqual(annual['csv_sha256'],digest)
        for sigma in SIGMAS:
            report=json.loads((OUT/f'{key(sigma)}_audit.json').read_text())
            self.assertTrue(report['equilibrium_certified'])
            self.assertTrue(report['early_window_checks']['passes'])
            checkpoint=CACHE/report['checkpoint_filename']
            if checkpoint.exists():
                self.assertEqual(report['checkpoint_sha256'],hashlib.sha256(checkpoint.read_bytes()).hexdigest())
                sol=load_solution(checkpoint)
                self.assertAlmostEqual(research.checked_moment(sol)['share'],
                    annual['scenarios'][key(sigma)]['first_year']['share'],places=12)
        fitted=annual['scenarios'][key(1.)]['first_year']['share']
        self.assertLess(abs(math.log(fitted/research.TARGET_SHARE)),research.TARGET_LOG_TOLERANCE)
        self.assertAlmostEqual(design.parameters.chi,calibration['chi'])


class PublishedApproximation(unittest.TestCase):
    def setUp(self):
        self.folder=OUT/'published_unit'
        self.calibration=json.loads((self.folder/'calibration.json').read_text())
        self.manifest=json.loads((self.folder/'figure_manifest.json').read_text())

    def test_scope_and_empirical_discrepancy_are_explicit(self):
        c=self.calibration
        self.assertEqual(c['status'],'numerically_admitted_approximate_calibration')
        self.assertEqual(c['sigmas'],[1.])
        self.assertFalse(c['target_exactly_matched'])
        self.assertTrue(c['numerical_tolerances_unchanged'])
        self.assertAlmostEqual(c['target_share'],research.TARGET_SHARE)
        self.assertAlmostEqual(c['relative_shortfall'],1-c['matched_share']/c['target_share'])
        self.assertGreater(c['relative_shortfall'],.09)
        self.assertLess(c['relative_shortfall'],.10)

    def test_publication_is_bound_to_verified_data_and_figures(self):
        digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
        c=self.calibration
        self.assertEqual(c['peak_verification_sha256'],digest(OUT/'peak_verification.json'))
        self.assertEqual(c['csv_sha256'],digest(self.folder/'equilibrium_paths.csv'))
        self.assertEqual(self.manifest['data_sha256'],c['csv_sha256'])
        self.assertEqual(len(c['figure_sha256']),6)
        for filename,sha in c['figure_sha256'].items():
            self.assertEqual(sha,digest(ROOT/filename.replace('\\','/')))
        with (self.folder/'equilibrium_paths.csv').open(newline='') as file:
            rows=list(csv.DictReader(file))
        self.assertEqual({float(row['sigma']) for row in rows},{1.})
        self.assertGreater(len(rows),4000)

    def test_original_equilibrium_gates_and_correct_reference(self):
        audit=json.loads((self.folder/'sigma_1_00_audit.json').read_text())
        event=json.loads((self.folder/'activation_audit.json').read_text())
        self.assertTrue(audit['equilibrium_certified'])
        self.assertTrue(audit['early_window_checks']['passes'])
        self.assertTrue(event['passes'])
        self.assertTrue(self.manifest['all_scenarios_admitted'])
        self.assertEqual(set(self.manifest['analytical_limits']),{'sigma_1_00'})
        self.assertIsNone(self.manifest['price_target'])
        limits=self.manifest['analytical_limits']['sigma_1_00']
        self.assertAlmostEqual(limits['net_interest'],.05)
        self.assertAlmostEqual(limits['labor_income_share'],.603)

    def test_subsection_keeps_three_figures_and_parameter_table(self):
        source=(ROOT/'sections_rewrite/preserved/10_rsi_research_share_high.tex').read_text()
        main=(ROOT/'main_rewrite.tex').read_text()
        self.assertIn('\\input{sections_rewrite/10_rsi_research_share}',main)
        self.assertIn('\\input{sections_rewrite/09_rsi_half_decline}',main)
        self.assertIn('\\input{sections_rewrite/preserved/rsi_research_share_high_parameters}',source)
        self.assertEqual(source.count('\\begin{figure}'),3)
        self.assertIn('9.75\\%',source)
        self.assertIn('instantaneous',source)


if __name__=='__main__':
    unittest.main()

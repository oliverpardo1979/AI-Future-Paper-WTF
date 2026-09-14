"""Pre-RSI reference, event continuity, and the admitted post-event paths."""
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
from calibrate_rewrite_ai_price import make_design, calibrated_design, log_price_ratio
from simulate_rewrite_finite_frontier import (
    SIGMAS, fixed_efficiency_bgp, design_initial_stocks, load_solution, key,
    validate_solution_design,
)
from solve_near_unit_ai_bvp import solve_monopoly_static_block


class RSIActivation(unittest.TestCase):
    def test_only_initial_reference_changes_from_previous_design(self):
        old,new=make_design(36.,'low_ai'),make_design(36.,'rsi_activation')
        self.assertEqual(asdict(old.parameters),asdict(new.parameters))
        self.assertEqual(old.frontier,new.frontier)
        self.assertEqual(old.initial_capability,new.initial_capability)
        self.assertEqual(new.initial_capital_rule,'fixed_efficiency_bgp')
        self.assertIsNone(new.initial_capital)
        self.assertNotEqual(old.output_directory,new.output_directory)
        self.assertNotEqual(old.cache_directory,new.cache_directory)

    def test_fixed_B_reference_and_homogeneity(self):
        d=make_design(36.,'rsi_activation'); p=d.parameters
        capitals=[]
        for sigma in SIGMAS:
            v=fixed_efficiency_bgp(sigma,d.initial_capability,p)
            capitals.append(v['capital'])
            self.assertGreater(v['consumption'],0)
            self.assertAlmostEqual(v['capital_output_ratio'],3.3,places=10)
            self.assertAlmostEqual(v['interest_rate'],.05,places=12)
            self.assertEqual(v['research_compute'],0)
            self.assertFalse(v['pre_event_research_available'])
            self.assertAlmostEqual(sum(v[k] for k in ('labor_income_share',
                'profit_output_share','inference_output_share'))+p.alpha,1)
            for t in (-10.,0.,10.):
                g=(p.population_growth+p.labor_productivity_growth)*t
                s=solve_monopoly_static_block(math.log(v['capital'])+g,
                     math.log(d.initial_capability),g,sigma,p)
                self.assertAlmostEqual(s.log_output,math.log(v['output'])+g,places=10)
            self.assertEqual(design_initial_stocks(d,sigma),(v['capital'],v['capability']))
        self.assertEqual(len(set(capitals)),4)

    def test_chi_does_not_change_pre_event_stocks_or_static_choices(self):
        for sigma in SIGMAS:
            a,b=make_design(1.,'rsi_activation'),make_design(80.,'rsi_activation')
            self.assertEqual(fixed_efficiency_bgp(sigma,a.initial_capability,a.parameters),
                             fixed_efficiency_bgp(sigma,b.initial_capability,b.parameters))

    def test_invalid_reference_is_not_silently_accepted(self):
        d=make_design(36.,'rsi_activation')
        for sigma,b in ((0.,d.initial_capability),(1.,0.),(1.5,2*d.frontier)):
            with self.assertRaises(ValueError):
                fixed_efficiency_bgp(sigma,b,d.parameters)

    def test_editorial_switch_preserves_legacy_sources(self):
        main=(ROOT/'main_rewrite.tex').read_text(encoding='utf-8')
        self.assertIn(r'\showlegacysimulationsfalse',main)
        self.assertIn(r'\input{sections_rewrite/05_quantitative_equilibria}',main)
        self.assertIn(r'\input{sections_rewrite/08_rsi_activation}',main)
        appendix=(ROOT/'sections_rewrite/appendix.tex').read_text(encoding='utf-8')
        self.assertIn(r'\ifshowlegacysimulations',appendix)
        self.assertIn(r'\input{sections_rewrite/appendix_rsi_activation}',appendix)

    def test_new_parameter_table_matches_calibration(self):
        d=calibrated_design('rsi_activation')
        text=(ROOT/'sections_rewrite/rsi_activation_parameters.tex').read_text(encoding='utf-8')
        table=dict(re.findall(r'^\$([^$]+)\$ & (.*?) &',text,re.M))
        self.assertAlmostEqual(float(table[r'\chi']),d.parameters.chi,places=6)
        self.assertAlmostEqual(float(table[r'\overline B'].replace(',','')),d.frontier,places=6)
        self.assertAlmostEqual(float(table['B_0']),d.initial_capability,places=6)
        self.assertEqual(float(table['K_0/Y_0']),3.3)
        for sigma,value in zip(SIGMAS,table['K_0'].split(';')):
            self.assertAlmostEqual(float(value),design_initial_stocks(d,sigma)[0],places=6)

    @unittest.skipUnless(
        (ROOT/'numerical_rewrite/rsi_activation/activation_audit.json').exists()
        and all((ROOT/'tmp/rewrite_bvp_rsi_activation'/f'{key(s)}_long.npz').exists()
                for s in SIGMAS),
        'Regenerate untracked BVP checkpoints before testing saved paths')
    def test_admitted_paths_and_no_production_jump(self):
        d=calibrated_design('rsi_activation')
        event=json.loads((d.output_directory/'activation_audit.json').read_text())
        self.assertTrue(event['passes'])
        for sigma in SIGMAS:
            c=event['scenarios'][key(sigma)]
            self.assertTrue(c['passes'])
            self.assertLess(max(c['level_log_gaps'].values()),1e-9)
            self.assertLess(c['resource_reallocation_residual'],1e-9)
            report=json.loads((d.output_directory/f'{key(sigma)}_audit.json').read_text())
            self.assertTrue(report['equilibrium_certified'])
            self.assertTrue(report['early_window_checks']['passes'])
            checkpoint=d.cache_directory/report['checkpoint_filename']
            self.assertEqual(hashlib.sha256(checkpoint.read_bytes()).hexdigest(),report['checkpoint_sha256'])
            validate_solution_design(load_solution(checkpoint),d,sigma)
        unit=load_solution(d.cache_directory/f'{key(1.)}_long.npz')
        self.assertLess(abs(log_price_ratio(unit)-math.log(.2)),2e-5)

    @unittest.skipUnless((ROOT/'numerical_rewrite/rsi_activation/figure_manifest.json').exists(),
                         'Render the admitted comparison first')
    def test_figures_bind_to_admitted_data_and_event(self):
        d=calibrated_design('rsi_activation')
        manifest=json.loads((d.output_directory/'figure_manifest.json').read_text())
        self.assertEqual(manifest['data_sha256'],hashlib.sha256(
            (d.output_directory/'equilibrium_paths.csv').read_bytes()).hexdigest())
        self.assertEqual(manifest['activation_audit_sha256'],hashlib.sha256(
            (d.output_directory/'activation_audit.json').read_bytes()).hexdigest())
        self.assertTrue(manifest['all_scenarios_admitted'])
        self.assertEqual(len(manifest['two_window_views']),3)
        for view in manifest['two_window_views']:
            self.assertEqual(view['windows'],[[-2.,10.],[10.,500.]])
        for sigma in SIGMAS:
            self.assertEqual(manifest['pre_event_bgp'][key(sigma)],
                fixed_efficiency_bgp(sigma,d.initial_capability,d.parameters))


if __name__=='__main__':
    unittest.main()

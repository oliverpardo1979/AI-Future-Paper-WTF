"""Design checks for the standalone experiment; never rerun simulations."""
import hashlib
import json
import math
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'.python-packages'), str(ROOT/'scripts')]
from calibrate_rewrite_research_share_omega005 import make_design, TARGET_SHARE
from calibrate_rewrite_ai_price import make_design as price_design
from simulate_rewrite_finite_frontier import SIGMAS, design_initial_stocks, fixed_efficiency_bgp
from analyze_axm_finite_cap_bvp import critical_capability_frontier, terminal_point
from dataclasses import asdict
from types import SimpleNamespace
from solve_near_unit_ai_bvp import solve_monopoly_static_block
from simulate_rewrite_finite_frontier import validate_solution_design


class ExperimentDesignTests(unittest.TestCase):
    def test_complementary_monopoly_near_zero_marginal_revenue(self):
        d = make_design(152.5484592857292)
        k,_ = design_initial_stocks(d,.9)
        for scale in (0.,10.,50.):
            for ratio in (.01,.1,.9,.999999):
                st = solve_monopoly_static_block(math.log(k)+scale,
                    math.log(ratio*d.frontier),scale,.9,d.parameters)
                s = st.ai_ces_share
                # Reconstruct MR*B from production/pricing, not the returned residual.
                margin = (.9-1)/.9+(1/.9-d.parameters.alpha)*s
                residual = (math.log((1-d.parameters.alpha)*s*margin)
                            +st.log_output+math.log(ratio*d.frontier)-st.log_ai_services)
                self.assertLess(abs(residual),1e-9)

    def test_derived_stock_cache_accepts_roundoff_not_changed_initial_conditions(self):
        d = make_design(2.)
        k,b = design_initial_stocks(d,.9)
        stub = SimpleNamespace(parameters=d.parameters,
            terminal=SimpleNamespace(frontier=d.frontier,sigma_xl=.9),
            initial_capital=math.nextafter(k,math.inf),initial_capability=b)
        validate_solution_design(stub,d,.9)
        stub.initial_capital = k*(1+1e-12)
        with self.assertRaises(ValueError):
            validate_solution_design(stub,d,.9)

    def test_target_units(self):
        self.assertAlmostEqual(100*TARGET_SHARE, 0.0664)

    def test_only_requested_parameter_and_derived_cap_changes(self):
        old, new = price_design(2., 'rsi_activation'), make_design(2.)
        previous, current = asdict(old.parameters), asdict(new.parameters)
        previous['omega_x'] = 0.05
        self.assertEqual(previous, current)
        self.assertAlmostEqual(new.frontier/old.frontier, 8.)
        self.assertAlmostEqual(new.initial_capability/new.frontier, 0.01)
        self.assertNotEqual(new.output_directory, old.output_directory)
        self.assertNotEqual(new.cache_directory, old.cache_directory)

    def test_all_four_regimes_and_cap_rule(self):
        d = make_design(2.)
        self.assertEqual(d.sigmas, SIGMAS)
        self.assertAlmostEqual(d.frontier/critical_capability_frontier(1.5,d.parameters),1.1)
        self.assertLess(d.frontier,critical_capability_frontier(1.1,d.parameters))
        self.assertEqual([terminal_point(s,d.frontier,d.parameters).regime for s in SIGMAS],
                         ['labor_supported']*3+['ai_dominated'])

    def test_initial_stocks_and_reference(self):
        d = make_design(2.)
        for s in SIGMAS:
            pre = fixed_efficiency_bgp(s,d.initial_capability,d.parameters)
            k0,b0 = design_initial_stocks(d,s)
            self.assertEqual(k0,pre['capital'])
            self.assertEqual(b0,d.initial_capability)
            self.assertAlmostEqual(pre['capital_output_ratio'],3.3)
            self.assertAlmostEqual(pre['interest_rate'],0.05)
            self.assertGreater(pre['consumption'],0)
            self.assertGreater(pre['inference_compute'],0)
            self.assertEqual(pre['research_compute'],0)

    def test_chi_does_not_change_predetermined_stocks_or_terminal_returns(self):
        low,high = make_design(.5),make_design(5.)
        for s in SIGMAS:
            self.assertEqual(design_initial_stocks(low,s),design_initial_stocks(high,s))
            self.assertEqual(terminal_point(s,low.frontier,low.parameters).net_interest_rate,
                             terminal_point(s,high.frontier,high.parameters).net_interest_rate)


@unittest.skipUnless((ROOT/'numerical_rewrite/rsi_research_share_omega005/figure_manifest.json').exists(),
                     'New experiment has not yet passed admission and exported its figures.')
class ExperimentOutputTests(unittest.TestCase):
    def test_calibration_and_all_four_admission_checks(self):
        out = ROOT/'numerical_rewrite/rsi_research_share_omega005'
        record = json.loads((out/'calibration.json').read_text())
        self.assertEqual(record['status'],'numerically_admitted')
        self.assertEqual(record['calibration_sigma'],1.)
        self.assertEqual(record['target_share'],TARGET_SHARE)
        self.assertLess(abs(record['matched_share']/TARGET_SHARE-1),2e-5)
        design = make_design(record['chi'])
        for s in SIGMAS:
            audit = json.loads((out/f'{key_for_test(s)}_audit.json').read_text())
            self.assertTrue(audit['equilibrium_certified'])
            self.assertTrue(audit['early_window_checks']['passes'])
            self.assertLess(audit['maximum_terminal_coordinate_gap'],1e-4)
            checkpoint = design.cache_directory/audit['checkpoint_filename']
            self.assertEqual(hashlib.sha256(checkpoint.read_bytes()).hexdigest(),audit['checkpoint_sha256'])

    def test_data_and_annual_moment_provenance(self):
        out = ROOT/'numerical_rewrite/rsi_research_share_omega005'
        manifest = json.loads((out/'figure_manifest.json').read_text())
        self.assertEqual(hashlib.sha256((out/'equilibrium_paths.csv').read_bytes()).hexdigest(),
                         manifest['data_sha256'])
        self.assertIsNone(manifest['price_target'])
        self.assertEqual(len(manifest['two_window_views']),3)
        event = json.loads((out/'activation_audit.json').read_text())
        self.assertTrue(event['passes'])
        moments = json.loads((out/'annual_moments.json').read_text())
        self.assertEqual(set(moments['scenarios']),{key_for_test(s) for s in SIGMAS})
        for case in moments['scenarios'].values():
            self.assertLess(case['maximum_horizon_log_change'],2e-5)
            self.assertLess(case['first_year']['quadrature_log_gap'],1e-8)


def key_for_test(sigma):
    return f'sigma_{sigma:.2f}'.replace('.','_')


if __name__ == '__main__':
    unittest.main()

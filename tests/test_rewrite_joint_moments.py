"""Source comparability and calibration identities, not invented trajectories."""
from dataclasses import replace
import hashlib
import json
import math
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'.python-packages'), str(ROOT/'scripts')]
import numpy as np
from calibrate_rewrite_joint_moments import (
    revenue_floor, omega_from_unit_share, load_references, make_joint_design,
    local_log_sensitivity,
)
from simulate_rewrite_finite_frontier import PARAMETERS, MAIN_DESIGN, RAMSEY_START_DESIGN
from simulate_rewrite_finite_frontier import load_solution, validate_solution_design
from calibrate_rewrite_ai_price import log_price_ratio
from solve_near_unit_ai_bvp import solve_monopoly_static_block


class JointMoments(unittest.TestCase):
    def test_unit_share_identity(self):
        for share in (.0001,.001,.002315515390070992,.067):
            p=replace(PARAMETERS, omega_x=omega_from_unit_share(share))
            block=solve_monopoly_static_block(math.log(5.94), math.log(1.7), 0., 1., p)
            self.assertAlmostEqual((1-p.alpha)*block.ai_ces_share, share, places=13)
            log_revenue=math.log((1-p.alpha)*block.ai_ces_share)+block.log_output
            self.assertAlmostEqual(math.exp(block.log_inference_compute-log_revenue),
                                   share, places=11)

    def test_complementarity_floor(self):
        self.assertAlmostEqual(revenue_floor(.9), .09530583214793738)
        self.assertAlmostEqual(revenue_floor(.999), .000999507705160146)
        self.assertEqual(revenue_floor(1.),0.)
        self.assertEqual(revenue_floor(1.5),0.)
        for sigma in (.9,.99,.999):
            # Check both sides of the analytical marginal-revenue boundary.
            boundary=revenue_floor(sigma)/(1-PARAMETERS.alpha)
            for multiplier in (.99,1.01):
                s=boundary*multiplier
                e=(1-s)/sigma+PARAMETERS.alpha*s
                self.assertEqual(e<1,multiplier>1)
            for omega in (.1,.2):
                p=replace(PARAMETERS,omega_x=omega)
                block=solve_monopoly_static_block(math.log(5.94),math.log(1.7),0.,sigma,p)
                self.assertGreater((1-p.alpha)*block.ai_ces_share,revenue_floor(sigma))
                self.assertLess(abs(block.monopoly_foc_log_residual),1e-9)

    def test_invalid_domains(self):
        for s in (-1,0,float('nan')):
            with self.assertRaises(ValueError): revenue_floor(s)
        for share in (-1,0,.67,1,float('nan')):
            with self.assertRaises(ValueError): omega_from_unit_share(share)
        for alpha in (-1,0,1,float('nan')):
            with self.assertRaises(ValueError): omega_from_unit_share(.1,alpha)
        for values in ([],[0.],[[1.]]):
            with self.assertRaises(ValueError): local_log_sensitivity(lambda x:x,values)

    def test_matching_geography_and_period(self):
        ref, rows, target=load_references()
        self.assertEqual(ref['services_source']['geography'],'USA')
        self.assertEqual(target['year'],2024)
        self.assertEqual(target['gdp_usd'],29298013000000)
        self.assertAlmostEqual(target['revenue_gdp_share'],67.84e9/29298013000000)
        self.assertFalse(ref['research_moment']['fit'])
        self.assertEqual([r['year'] for r in rows],[2023,2024,2025])

    def test_new_design_does_not_overwrite_existing(self):
        d=make_joint_design(5.,170.12401740519473)
        self.assertEqual(d.parameters.eta,.2)
        self.assertEqual(d.sigmas,(1.,))
        self.assertEqual(d.initial_capital,RAMSEY_START_DESIGN.initial_capital)
        self.assertAlmostEqual(d.initial_capability/d.frontier,.01)
        for previous in (MAIN_DESIGN,RAMSEY_START_DESIGN):
            self.assertNotEqual(d.output_directory,previous.output_directory)
            self.assertNotEqual(d.cache_directory,previous.cache_directory)
        other=make_joint_design(5.,1360.9921392415592)
        self.assertNotEqual(d.cache_directory,other.cache_directory)
        self.assertNotEqual(d.cache_directory,make_joint_design(5.,d.frontier,.1).cache_directory)

    def test_three_moments_can_be_redundant(self):
        # Pure mathematical test: first and third moments have identical information.
        result=local_log_sensitivity(lambda x:np.array([x[0],x[1]*x[2],x[0]**2]),[.1,5.,2.])
        self.assertIn('not global identification',result['scope'])
        for check in result['checks']:
            singular=check['singular_values']
            self.assertLess(singular[-1]/singular[0],1e-8)

    def test_independent_log_sensitivities(self):
        result=local_log_sensitivity(lambda x:x,[.1,5.,2.])
        for check in result['checks']:
            np.testing.assert_allclose(check['jacobian'],np.eye(3),atol=1e-9)

    @unittest.skipUnless((ROOT/'numerical_rewrite/joint_us_proxy/1351533afdbe/calibration.json').exists(),
                         'Run the separate fit to create admitted records')
    def test_saved_fits_pass_admission(self):
        completed=0
        for path in (ROOT/'numerical_rewrite/joint_us_proxy').glob('*/calibration.json'):
            record=json.loads(path.read_text(encoding='utf-8'))
            self.assertEqual(record['status'],'numerically_admitted')
            self.assertFalse(record['fit_is_global_identification'])
            self.assertFalse(record['research_moment_fitted'])
            report=json.loads((path.parent/'sigma_1_00_audit.json').read_text(encoding='utf-8'))
            self.assertTrue(report['equilibrium_certified'])
            self.assertLess(report['maximum_terminal_coordinate_gap'],1e-4)
            self.assertTrue(report['early_optimality']['developer_sufficiency_gate_passes'])
            for check in report['early_window_checks']:
                self.assertLess(check['maximum_ode_residual'],1e-6)
                self.assertLess(check['maximum_research_foc_residual'],1e-9)
                self.assertLess(check['maximum_monopoly_foc_residual'],1e-9)
            d=make_joint_design(record['parameters']['chi'],record['frontier'],
                                record['initial_capability']/record['frontier'])
            self.assertEqual(record['design'],'joint_us_proxy_'+path.parent.name)
            checkpoint=ROOT/'tmp/rewrite_bvp_joint_us_proxy'/path.parent.name/'sigma_1_00_long.npz'
            # A fresh clone can inspect reports without the ignored local caches.
            if checkpoint.exists():
                self.assertEqual(hashlib.sha256(checkpoint.read_bytes()).hexdigest(),
                                 record['checkpoint_sha256'])
                sol=load_solution(checkpoint)
                validate_solution_design(sol,d,1.)
                self.assertLess(abs(log_price_ratio(sol)-math.log(.2)),2e-5)
            completed+=1
        self.assertGreaterEqual(completed,1)


if __name__=='__main__':
    unittest.main()

"""The production terminal dispatcher must implement the rewrite's formulas."""
import math
from pathlib import Path
import sys
import unittest
import tempfile
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.python-packages'))
sys.path.insert(0, str(ROOT / 'scripts'))
import numpy as np
from analyze_axm_finite_cap_bvp import (
    terminal_point, terminal_residual, terminal_linearization,
    solve_local_terminal_bvp, log_critical_capability_frontier,
)
from define_positive_ai_branch import PositiveAIBenchmarkParameters
from simulate_rewrite_finite_frontier import (
    SIGMAS, FRONTIER, save_solution, load_solution, real_wage_growth,
)
from scipy.interpolate import PPoly
from solve_near_unit_ai_bvp import solve_monopoly_static_block


class RewriteSimulationDesign(unittest.TestCase):
    def setUp(self):
        self.p = PositiveAIBenchmarkParameters()

    def test_four_agreed_regimes_and_annual_parameters(self):
        p = self.p
        self.assertEqual((p.alpha, p.depreciation, p.discount, p.population_growth,
                          p.labor_productivity_growth, p.eta, p.chi, p.omega_x),
                         (.33, .05, .04, .003, .01, .2, .01, .2))
        for sigma in SIGMAS:
            t = terminal_point(sigma, FRONTIER, p)
            self.assertEqual(t.regime, 'ai_dominated' if sigma == 1.5 else 'labor_supported')
            np.testing.assert_allclose(terminal_residual(t, p), 0, atol=2e-11)
            roots = terminal_linearization(t, p)
            self.assertEqual(len(roots.stable_eigenvalues), 3)
            self.assertEqual(len(roots.unstable_eigenvalues), 2)
            self.assertAlmostEqual(t.terminal_growth-p.population_growth,
                                    .0313499758138466 if sigma == 1.5 else .01)

    def test_unit_terminal_is_the_analytical_capped_limit(self):
        p = self.p
        t = terminal_point(1, FRONTIER, p)
        beta = (1-p.alpha)*p.omega_x
        required = (p.discount+p.labor_productivity_growth+p.depreciation)/p.alpha
        exact = ((beta*beta*FRONTIER)**beta*required**(beta-1))**(1/(1-p.alpha-beta))
        self.assertAlmostEqual(t.auxiliary['capital_effective_labor_ratio']/exact, 1, places=12)
        self.assertIsNone(t.critical_frontier)
        self.assertAlmostEqual(t.labor_income_share, .536)
        self.assertAlmostEqual(t.inference_output_share, beta*beta)

    def test_near_unit_terminal_continuity_without_threshold_overflow(self):
        baseline = terminal_point(1, FRONTIER, self.p)
        for sign in (-1, 1):
            errors = []
            for epsilon in (1e-2, 1e-3, 1e-4, 1e-6, 1e-8):
                sigma = 1+sign*epsilon
                t = terminal_point(sigma, FRONTIER, self.p)
                errors.append(float(np.max(np.abs(t.coordinates-baseline.coordinates))))
                self.assertTrue(math.isfinite(log_critical_capability_frontier(sigma, self.p)))
                np.testing.assert_allclose(terminal_residual(t, self.p), 0, atol=2e-11)
            self.assertTrue(all(b < a for a, b in zip(errors, errors[1:])))
            self.assertLess(errors[-1], 1e-6)

    def test_real_wage_growth_matches_the_differentiated_static_wage(self):
        p = self.p
        capital_growth = .031
        capability_growth = .004
        effective_labor_growth = p.population_growth+p.labor_productivity_growth
        for sigma in (.9, 1., 1.1, 1.5):
            log_capital, log_capability, log_effective_labor = math.log(2.), math.log(1.2), .1
            static = solve_monopoly_static_block(
                log_capital, log_capability, log_effective_labor, sigma, p)
            yk, yb = static.output_log_gradient[:2]
            output_growth = (
                yk*capital_growth + yb*capability_growth
                + (1-yk)*effective_labor_growth
            )
            exact = real_wage_growth(
                static, sigma, capital_growth, capability_growth,
                effective_labor_growth, output_growth, p.population_growth)
            step = 1e-5
            wages = []
            for sign in (-1, 1):
                trial = solve_monopoly_static_block(
                    log_capital+sign*step*capital_growth,
                    log_capability+sign*step*capability_growth,
                    log_effective_labor+sign*step*effective_labor_growth,
                    sigma, p)
                wages.append(
                    math.log1p(-trial.ai_ces_share)+trial.log_output
                    - sign*step*p.population_growth)
            numerical = (wages[1]-wages[0])/(2*step)
            self.assertAlmostEqual(exact, numerical, places=8)

    def test_local_nonlinear_bvps_below_and_at_one(self):
        for sigma in (.9, 1):
            t = terminal_point(sigma, FRONTIER, self.p)
            result = solve_local_terminal_bvp(t, self.p, np.array([.01, -.01, 1e-5]),
                                               horizon=200, nodes=81, tolerance=1e-8)
            self.assertTrue(result.raw.success)
            self.assertLess(result.maximum_boundary_residual, 1e-8)

    def test_checkpoint_preserves_vector_interpolation_axis(self):
        t=terminal_point(1, FRONTIER, self.p)
        polynomial=PPoly.construct_fast(np.arange(32,dtype=float).reshape(4,2,4)/100,
                                        np.array([0.,1.,2.]),axis=1)
        raw=SimpleNamespace(sol=polynomial,x=np.array([0.,1.,2.]),
                            rms_residuals=np.zeros(2),niter=1)
        fake=SimpleNamespace(raw=raw,terminal=t,parameters=self.p,
            initial_capital=2.,initial_capability=.5,initial_effective_labor_scale=1.,
            horizon=2.,stages=[])
        with tempfile.TemporaryDirectory() as directory:
            filename=Path(directory)/'interpolation.npz'
            save_solution(fake,filename)
            loaded=load_solution(filename)
            for times in (.3,np.array([.1,.4,1.3])):
                np.testing.assert_allclose(loaded.raw.sol(times),polynomial(times))
                np.testing.assert_allclose(loaded.raw.sol(times,1),polynomial(times,1))

    def test_maximized_hamiltonian_and_its_support_slope(self):
        p=self.p
        b=.7*FRONTIER
        rdepth=-FRONTIER*math.log1p(-b/FRONTIER)
        qr=.3
        m=(qr*p.chi*p.eta*b**p.eta)**(1/(1-p.eta))
        static=solve_monopoly_static_block(math.log(2.),math.log(b),0.,1.5,p)
        u=math.exp(static.log_inference_compute)
        slope=(1-b/FRONTIER)*(u+m)/b
        def h(depth):
            trial=FRONTIER*(-math.expm1(-depth/FRONTIER))
            s=solve_monopoly_static_block(math.log(2.),math.log(trial),0.,1.5,p)
            profit=(1-p.alpha)*s.ai_ces_share*math.exp(s.log_output)-math.exp(s.log_inference_compute)
            mt=(qr*p.chi*p.eta*trial**p.eta)**(1/(1-p.eta))
            direct=profit-mt+qr*p.chi*(trial*mt)**p.eta
            reduced=profit+(1-p.eta)/p.eta*m*(trial/b)**(p.eta/(1-p.eta))
            self.assertAlmostEqual(direct,reduced,places=12)
            return reduced
        for step in (.01,.001):
            numerical=(h(rdepth+step)-h(rdepth-step))/(2*step)
            self.assertAlmostEqual(numerical/slope,1,places=6)

    def test_uniform_elasticity_bound_for_terminal_support(self):
        p=self.p
        for sigma in (1.01,1.1,1.5,1/p.alpha):
            for s in np.linspace(.0001,.9999,200):
                e=(1-s)/sigma+p.alpha*s
                den=e*(1-e)+(p.alpha-1/sigma)*(1-1/sigma)*s*(1-s)
                self.assertLessEqual((1-e)/den,1/p.alpha+1e-12)


if __name__ == '__main__':
    unittest.main()

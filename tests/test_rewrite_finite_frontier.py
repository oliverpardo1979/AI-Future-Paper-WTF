"""Algebra and linearization checks for rewrite Section 4.

This file constructs terminal points and differentiates the exact normalized
equations. It neither simulates transition paths nor certifies a numerical
equilibrium. The existence proof is in appendix_finite_frontier.tex.
Run: python -m unittest discover -s tests -p test_rewrite_finite_frontier.py -v
"""
from dataclasses import replace
from pathlib import Path
import math
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
if (ROOT / ".python-packages").exists():
    sys.path.insert(0, str(ROOT / ".python-packages"))
elif (ROOT / "tmp" / "pydeps").exists():
    sys.path.insert(0, str(ROOT / "tmp" / "pydeps"))
sys.path.insert(0, str(ROOT / "scripts"))

import numpy as np
from scipy.optimize import brentq
from scipy.special import expit
from define_positive_ai_branch import PositiveAIBenchmarkParameters
from analyze_axm_finite_cap_bvp import (
    critical_capability_frontier, terminal_point, terminal_residual,
    terminal_linearization, ai_dominated_dynamics, ai_dominated_jacobian,
)


def ces(log_x, sigma, p):
    phi = (sigma - 1.0) / sigma
    if sigma == 1.0:
        return p.omega_x * log_x, p.omega_x
    argument = phi * log_x
    # log1p/expm1 remove cancellation around the Cobb-Douglas limit.
    log_z = (math.log1p(p.omega_x * math.expm1(argument)) / phi
             if abs(argument) < 0.5 else
             np.logaddexp(math.log1p(-p.omega_x),
                          math.log(p.omega_x) + argument) / phi)
    share = expit(math.log(p.omega_x / (1 - p.omega_x)) + argument)
    return log_z, share


def static(log_k, log_b, sigma, p):
    def residual(log_x):
        log_z, s = ces(log_x, sigma, p)
        margin = (sigma - 1) / sigma + (1 / sigma - p.alpha) * s
        if margin <= 0:
            return -1e6  # Outside the positive-marginal-revenue domain.
        log_y = p.alpha * log_k + (1 - p.alpha) * log_z
        return (log_b + math.log1p(-p.alpha) + math.log(s)
                + math.log(margin) + log_y - log_x)
    # Fixed finite bounds cover the deliberately moderate test configurations.
    log_x = brentq(residual, -200, 200, xtol=2e-13, rtol=1e-14)
    log_z, s = ces(log_x, sigma, p)
    y = math.exp(p.alpha * log_k + (1 - p.alpha) * log_z)
    x = math.exp(log_x)
    return y, x, math.exp(log_x - log_b), s


def labor_point(sigma, p):
    log_x = math.log(0.7)
    _, share = ces(log_x, sigma, p)
    margin = (sigma - 1) / sigma + (1 / sigma - p.alpha) * share
    if margin <= 0:
        lower = (1 - sigma) / (1 - p.alpha * sigma)
        share = (1 + lower) / 2
        log_x = math.log((1 - p.omega_x) * share /
                        (p.omega_x * (1 - share))) / ((sigma - 1) / sigma)
    log_z, share = ces(log_x, sigma, p)
    margin = (sigma - 1) / sigma + (1 / sigma - p.alpha) * share
    required = (p.discount + p.labor_productivity_growth + p.depreciation) / p.alpha
    k = math.exp(log_z - math.log(required) / (1 - p.alpha))
    y, x = required * k, math.exp(log_x)
    u = (1 - p.alpha) * share * margin * y
    frontier = x / u
    growth = p.population_growth + p.labor_productivity_growth
    r = p.discount + p.labor_productivity_growth
    c = y - u - (p.depreciation + growth) * k
    q = x / (r * frontier**2)
    research = (growth * frontier**(1 - p.eta) / p.chi)**(1 / p.eta)
    d = research / (p.eta * growth * q)
    return dict(k=k, c=c, y=y, x=x, u=u, b=frontier, q=q, d=d,
                research=research, r=r, growth=growth, share=share)


def dynamics(deviations, t, sigma, p):
    lk, lc, ld, lq, scaled_tau = deviations
    k, c, d, q = [t[name] * math.exp(v)
                   for name, v in zip(("k", "c", "d", "q"), (lk, lc, ld, lq))]
    tau = scaled_tau * t["b"] / t["d"]
    b = t["b"] - d * tau
    y, x, u, _ = static(math.log(k), math.log(b), sigma, p)
    research = (q * d * p.chi * p.eta * b**p.eta / t["b"])**(1 / (1-p.eta))
    approach = p.chi * b**p.eta * research**p.eta / t["b"]
    r = p.alpha * y / k - p.depreciation
    g = t["growth"]
    return np.array([(y-c-u-research*tau)/k-p.depreciation-g,
                     r-p.discount-p.labor_productivity_growth,
                     g-approach,
                     r-x/(q*b*b)-p.eta*approach*d*tau/b+approach-g,
                     -g*scaled_tau])


def jacobian(t, sigma, p):
    s = t["share"]
    e = (1-s)/sigma + p.alpha*s
    curvature = e*(1-e)+(p.alpha-1/sigma)*(1-1/sigma)*s*(1-s)
    elasticity = (1-e)/curvature
    xk = p.alpha*elasticity
    yk = p.alpha+(1-p.alpha)*s*xk
    yb = (1-p.alpha)*s*elasticity
    mu, g, r = p.eta/(1-p.eta), t["growth"], t["r"]
    rk = (r+p.depreciation)*(yk-1)
    rtau = -(r+p.depreciation)*yb
    j = np.zeros((5,5))
    j[0,0] = (t["y"]*yk-t["u"]*xk)/t["k"]-p.depreciation-g
    j[0,1] = -t["c"]/t["k"]
    j[0,4] = (-(t["y"]*yb-t["u"]*(elasticity-1))
                -t["research"]*t["b"]/t["d"])/t["k"]
    j[1,0], j[1,4] = rk, rtau
    j[2,2], j[2,3], j[2,4] = -g*mu, -g*mu, g*mu
    j[3,0] = rk-r*xk
    j[3,2], j[3,3] = g*mu, r+g*mu
    j[3,4] = rtau+r*(elasticity-2)-p.eta*g-g*mu
    j[4,4] = -g
    return j


class FiniteFrontierProofChecks(unittest.TestCase):
    sigmas = (0.25, 0.5, 0.9, 0.99, 0.9999, 1.0, 1.0001, 1.01, 1.5, 2.0, 5.0)

    def test_labor_terminal_equations_and_saddle_projection(self):
        p = PositiveAIBenchmarkParameters()
        for sigma in self.sigmas:
            with self.subTest(sigma=sigma):
                t = labor_point(sigma, p)
                self.assertGreater(t["c"], 0)
                if sigma != 1:
                    # Work in logs: the threshold diverges/vanishes near one.
                    required = (p.discount+p.labor_productivity_growth+p.depreciation)/p.alpha
                    log_critical = (p.alpha/(1-p.alpha)*math.log(required)
                                    -2*math.log1p(-p.alpha)
                                    -sigma/(sigma-1)*math.log(p.omega_x))
                    self.assertGreater((math.log(t["b"])-log_critical)*(1-sigma), 0)
                np.testing.assert_allclose(dynamics(np.zeros(5), t, sigma, p),
                                           0, atol=2e-11)
                j = jacobian(t, sigma, p)
                values, vectors = np.linalg.eig(j)
                self.assertEqual(np.count_nonzero(values.real < 0), 3)
                self.assertEqual(np.count_nonzero(values.real > 0), 2)
                projection = vectors[:, values.real < 0][[0,2,4], :]
                self.assertGreater(np.linalg.svd(projection)[1][-1], 1e-5)
                self.assertLess(j[1,0], 0)
                for step in (1e-4, 1e-5):
                    # Two central-difference scales check truncation/roundoff;
                    # these are diagnostic tolerances, not equilibrium criteria.
                    numerical = np.column_stack([
                        (dynamics(np.eye(5)[i]*step, t, sigma, p)
                         - dynamics(-np.eye(5)[i]*step, t, sigma, p))/(2*step)
                        for i in range(5)])
                    np.testing.assert_allclose(j, numerical, rtol=3e-6, atol=3e-8)

    def test_unit_formula_and_continuity_of_static_limit(self):
        p = PositiveAIBenchmarkParameters()
        t = labor_point(1.0, p)
        beta = (1-p.alpha)*p.omega_x
        required = (p.discount+p.labor_productivity_growth+p.depreciation)/p.alpha
        exact = ((beta*beta*t["b"])**beta * required**(beta-1))**(1/(1-p.alpha-beta))
        self.assertAlmostEqual(t["k"]/exact, 1, places=12)
        for sign in (-1,1):
            errors = []
            for epsilon in (1e-2, 1e-3, 1e-4):
                result = static(math.log(t["k"]), math.log(t["b"]), 1+sign*epsilon, p)
                errors.append(np.max(np.abs(np.log(np.array(result[:3]) /
                                                   np.array([t["y"], t["x"], t["u"]])))))
            self.assertTrue(all(b < a for a,b in zip(errors, errors[1:])))
            self.assertLess(errors[-1], 1e-3)

    def test_consumption_positivity_is_not_an_extra_assumption(self):
        for alpha in (0.2, 0.33, 0.8, 0.95):
            p = replace(PositiveAIBenchmarkParameters(), alpha=alpha, eta=min(0.1, alpha/2))
            for sigma in (0.25, 0.9, 1.0, 1.5, 5.0, 20.0):
                t = labor_point(sigma, p)
                self.assertGreater(t["c"]/t["y"], 0)
                self.assertLess(t["u"]/t["y"], 1-alpha)

    def test_ai_branch_existing_equations_and_linearization(self):
        p = PositiveAIBenchmarkParameters()
        for sigma in (1.1, 1.5, 2.0, 5.0):
            b = 2*critical_capability_frontier(sigma, p)
            t = terminal_point(sigma, b, p)
            np.testing.assert_allclose(terminal_residual(t, p), 0, atol=2e-11)
            linear = terminal_linearization(t, p)
            self.assertEqual(len(linear.stable_eigenvalues), 3)
            self.assertEqual(len(linear.unstable_eigenvalues), 2)
            self.assertGreater(abs(linear.state_projection_determinant), 1e-7)
            j = ai_dominated_jacobian(t, p)
            # One-sided differences at h=0; central differences elsewhere.
            numeric = []
            for i in range(5):
                step = 1e-8 if i == 0 else 1e-5
                shift = np.eye(5)[i]*step
                origin = t.coordinates
                value = ((ai_dominated_dynamics(origin+shift, t, p)
                          -ai_dominated_dynamics(origin, t, p))/step if i == 0 else
                         (ai_dominated_dynamics(origin+shift, t, p)
                          -ai_dominated_dynamics(origin-shift, t, p))/(2*step))
                numeric.append(value)
            np.testing.assert_allclose(j, np.column_stack(numeric),
                                       rtol=3e-5, atol=3e-7)

    def test_interest_frontier_derivative_and_growth_accounting(self):
        p = PositiveAIBenchmarkParameters()
        theta = (1-p.alpha)/p.alpha
        for sigma in (1.1, 1.5, 2.0, 5.0):
            critical = critical_capability_frontier(sigma, p)
            for ratio in (1.1, 2, 10):
                b = critical*ratio
                def interest(frontier):
                    return ((p.discount+p.labor_productivity_growth+p.depreciation)
                            * (frontier/critical)**theta-p.depreciation)
                r = interest(b)
                slope = theta*(r+p.depreciation)/b
                step = b*1e-5
                numerical = (interest(b+step)-interest(b-step))/(2*step)
                self.assertAlmostEqual(numerical/slope, 1, places=8)
                growth = p.population_growth+r-p.discount
                self.assertGreater(growth-p.population_growth, p.labor_productivity_growth)
                self.assertAlmostEqual(growth-r, p.population_growth-p.discount)
            self.assertAlmostEqual(interest(critical),
                                   p.discount+p.labor_productivity_growth)


if __name__ == "__main__":
    unittest.main()

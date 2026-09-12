"""Algebra and scope checks for uncapped complements, not trajectory simulations.

The main-text bound is a feasibility theorem. The asymptotic characterization
is conditional and these arithmetic tests do not prove equilibrium existence.
Tolerances cover floating-point differentiation/root finding, not model rules.
"""
from pathlib import Path
import re
import unittest

import numpy as np
from scipy.optimize import brentq
from scipy.special import expit, logsumexp

ROOT = Path(__file__).resolve().parents[1]


class UncappedComplements(unittest.TestCase):
    def test_ces_bound_and_normalized_capital_barrier(self):
        for sigma in (0.25, 0.5, 0.9, 0.99):
            v = (sigma - 1) / sigma
            for alpha in (0.33, 0.6):
                for wx in (0.1, 0.2, 0.6):
                    wl = 1 - wx
                    coefficient = np.exp((1 - alpha) * np.log(wl) / v)
                    dilution = 0.05 + 0.003 + 0.01
                    barrier = (coefficient / dilution)**(1 / (1 - alpha))
                    for k in (0.1, 1, 10):
                        for lx in (-20, -2, 2, 20):
                            lz = logsumexp([np.log(wl), np.log(wx) + v*lx]) / v
                            self.assertLessEqual(lz, np.log(wl)/v + 1e-12)
                            y = np.exp(alpha*np.log(k) + (1-alpha)*lz)
                            self.assertLessEqual(y, coefficient*k**alpha*(1+1e-12))
                    for multiple in (1.01, 2, 100):
                        k = multiple * barrier
                        self.assertLess(coefficient*k**alpha - dilution*k, 0)

    def test_limiting_monopoly_and_income_accounting(self):
        for sigma in (0.1, 0.5, 0.9, 0.99):
            for alpha in (0.2, 0.33, 0.7):
                s = (1-sigma)/(1-alpha*sigma)
                labor = sigma*(1-alpha)**2/(1-alpha*sigma)
                revenue = (1-alpha)*(1-sigma)/(1-alpha*sigma)
                self.assertGreater(s, 0)
                self.assertLess(s, 1)
                self.assertAlmostEqual((1-s)/sigma + alpha*s, 1)
                self.assertAlmostEqual(labor, (1-alpha)*(1-s))
                self.assertAlmostEqual(revenue, (1-alpha)*s)
                self.assertAlmostEqual(alpha+labor+revenue, 1)
                self.assertGreater(labor, 0)
                self.assertGreater(revenue, 0)

    def test_static_choices_approach_revenue_maximizer(self):
        # Scale B by the marginal cost inducing X/(AL)=x_infinity/2.
        # This avoids mistaking the enormous level scales near sigma=1 for
        # a discontinuity of the static solver.
        alpha, wx, wl, k = 0.33, 0.2, 0.8, 2.0
        for sigma in (0.5, 0.9, 0.99):
            v = (sigma-1)/sigma
            s0 = (1-sigma)/(1-alpha*sigma)
            lx0 = np.log(wl*s0/(wx*(1-s0)))/v

            def log_mr(lx):
                s = expit(np.log(wx/wl)+v*lx)
                margin = (1-alpha*sigma)/sigma*(s-s0)
                if margin <= 0:
                    return -1e6  # sign-only endpoint at zero marginal revenue
                lz = logsumexp([np.log(wl), np.log(wx)+v*lx])/v
                ly = alpha*np.log(k)+(1-alpha)*lz
                return np.log(1-alpha)+np.log(s)+ly-lx+np.log(margin)

            base_log_B = -log_mr(lx0-np.log(2))
            gaps = []
            for multiplier in (1, 100, 10000):
                log_B = base_log_B+np.log(multiplier)
                lx = brentq(lambda z: log_mr(z)+log_B,
                            lx0-100, lx0, xtol=1e-12)
                self.assertLess(abs(log_mr(lx)+log_B), 2e-7)
                self.assertLess(lx, lx0)
                gaps.append(lx0-lx)
            self.assertTrue(all(a > b for a, b in zip(gaps, gaps[1:])))
            self.assertLess(gaps[-1], 3e-4)

    def test_conditional_research_costate_and_tvc_rates(self):
        for eta in (0.1, 0.2, 0.5, 0.8):
            n, gamma, rho = 0.003, 0.01, 0.04
            total, r = n+gamma, rho+gamma
            gb, gm = eta*total, (1-eta)*total
            denominator = r-(1-eta)**2*total
            m_to_u = eta**2*total/denominator
            gq = (1-eta)*gm-eta*gb
            self.assertGreater(denominator, 0)
            self.assertGreater(m_to_u, 0)
            self.assertAlmostEqual((1-eta)*gb, eta*gm)
            self.assertAlmostEqual(gq, r-eta*gb/m_to_u-eta*gb)
            self.assertAlmostEqual(gq+gb-r, -(rho-n)-eta*total)
            self.assertLess(gm-total, 0)
            self.assertLess(gq+gb-r, 0)

    def test_new_section_order_and_explicit_conditional_scope(self):
        main = (ROOT/"main_rewrite.tex").read_text(encoding="utf-8")
        body = (ROOT/"sections_rewrite/05_uncapped_equilibria.tex").read_text(encoding="utf-8")
        proofs = (ROOT/"sections_rewrite/appendix_uncapped_complements_proofs.tex").read_text(encoding="utf-8")
        appendix = (ROOT/"sections_rewrite/appendix.tex").read_text(encoding="utf-8")
        locations = [main.index(r"\input{sections_rewrite/"+name+"}") for name in (
            "04_equilibrium_regimes", "05_uncapped_equilibria", "05_quantitative_equilibria")]
        self.assertEqual(locations, sorted(locations))
        self.assertIn("does not by itself", body)
        self.assertIn("without proving its", body)
        self.assertIn("equilibrium-existence theorem", body)
        self.assertIn(r"\begin{conditionalresult}", body)
        self.assertIn("Suppose", body)
        self.assertIn("have finite limits", body)
        self.assertIn("in addition", body)
        self.assertIn("does not establish existence from any initial state", body)
        self.assertNotRegex(proofs, r"\\(?:sub)*section\{")
        for kind, label in (
            ("Proposition", "prop:rewrite-uncapped-complements-bounds"),
            ("Conditional result", "cond:rewrite-uncapped-complements-limits"),
        ):
            self.assertIn(r"\label{"+label+"}", body)
            self.assertIn(r"\begin{proof}[Proof of "+kind+r"~\ref{"+label+"}]", proofs)
        self.assertLess(
            appendix.index(r"\input{sections_rewrite/appendix_uncapped_complements_proofs}"),
            appendix.index(r"\section{Numerical algorithm"))


if __name__ == "__main__":
    unittest.main()

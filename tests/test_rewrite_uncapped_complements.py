"""Algebra and scope checks for uncapped complements, not trajectory simulations.

The main-text bound is a feasibility theorem. The asymptotic characterization
is conditional and these arithmetic tests do not prove equilibrium existence.
Tolerances cover floating-point differentiation/root finding, not model rules.
"""
from pathlib import Path
from fractions import Fraction
import re
import unittest

import numpy as np
from scipy.optimize import brentq
from scipy.special import expit, logsumexp

ROOT = Path(__file__).resolve().parents[1]


class UncappedComplements(unittest.TestCase):
    def test_static_return_is_decreasing_in_normalized_capital(self):
        # Analytic derivative on the positive-marginal-revenue branch.
        for sigma in (Fraction(1, 10), Fraction(1, 2), Fraction(99, 100)):
            varphi = (sigma-1)/sigma
            for alpha in (Fraction(1, 5), Fraction(33, 100), Fraction(9, 10)):
                lower = (1-sigma)/(1-alpha*sigma)
                for weight in (Fraction(1, 100), Fraction(1, 2), Fraction(99, 100)):
                    s = lower+(1-lower)*weight
                    e = (1-s)/sigma+alpha*s
                    e_prime = (alpha-1/sigma)*varphi*s*(1-s)
                    mr_elasticity = e+e_prime/(1-e)
                    output_elasticity = alpha+alpha*(1-alpha)*s/mr_elasticity
                    self.assertGreater(e_prime, 0)
                    self.assertGreater(mr_elasticity, alpha*s)
                    self.assertGreater(output_elasticity, alpha)
                    self.assertLess(output_elasticity, 1)

    def test_ramsey_limit_has_positive_dulac_divergence_and_is_a_saddle(self):
        # Exact differentiation of (F(k)-c)/c^2 and h(k)/c.
        # This validates identities in the proof, not a convergence theorem.
        alpha, rho, n, gamma, delta = map(
            Fraction, ("0.33", "0.04", "0.003", "0.01", "0.05")
        )
        for c in (Fraction(1, 100), Fraction(2), Fraction(100)):
            for marginal_product in (Fraction(1, 100), Fraction(1, 2), Fraction(20)):
                f_prime = marginal_product-delta-n-gamma
                h = marginal_product-delta-rho-gamma
                self.assertEqual((f_prime-h)/c**2, (rho-n)/c**2)
                self.assertGreater((f_prime-h)/c**2, 0)
        for k in (Fraction(1, 10), Fraction(5), Fraction(100)):
            c_star = k*((rho+gamma+delta)/alpha-(delta+n+gamma))
            j21 = c_star*(alpha-1)*(rho+gamma+delta)/k
            self.assertGreater(c_star, 0)
            self.assertLess(j21, 0)  # determinant of [[rho-n,-1],[j21,0]]

    def test_weighted_transversality_identity_exactly_cancels_research(self):
        # Exact arithmetic: the identity is not confined to eta <= 1/2 or
        # eta < alpha. This checks the algebra, not equilibrium existence.
        alpha = Fraction(33, 100)
        Y, C, U, K = map(Fraction, (7, 2, 1, 5))
        delta = Fraction(1, 20)
        r = alpha*Y/K-delta
        for eta in (Fraction(1, 10), Fraction(1, 3), Fraction(1, 2),
                    Fraction(4, 5), Fraction(99, 100)):
            for M in (Fraction(1, 10), Fraction(3), Fraction(50)):
                gb = Fraction(2, 7)
                qb = M/(eta*gb)  # research FOC
                gq = r-U/qb-eta*gb  # costate
                d_qb = (gq+gb)*qb
                self.assertEqual(d_qb-r*qb, -U+(1-eta)*M/eta)
                d_k = Y-C-U-M-delta*K
                weighted = d_k-r*K+eta/(1-eta)*(d_qb-r*qb)
                self.assertEqual(weighted, (1-alpha)*Y-C-U/(1-eta))
                gm = (gq+eta*gb)/(1-eta)
                self.assertEqual((1-eta)*gm, r-U/qb)
                self.assertLess(gm, r/(1-eta))

    def test_derived_capital_consumption_ratios_are_positive(self):
        for alpha in (Fraction(1, 100), Fraction(33, 100), Fraction(99, 100)):
            for n in (Fraction(0), Fraction(3, 1000), Fraction(1, 10)):
                for margin in (Fraction(1, 1000000), Fraction(1, 25)):
                    rho = n+margin
                    for gamma in (Fraction(1, 10000), Fraction(1, 100)):
                        for delta in (Fraction(0), Fraction(1, 20)):
                            ky = alpha/(rho+gamma+delta)
                            cy = 1-(delta+n+gamma)*ky
                            self.assertGreater(ky, 0)
                            self.assertGreater(cy, 0)
                            self.assertEqual(alpha/ky-delta, rho+gamma)
                            self.assertEqual((1-cy)/ky-delta, n+gamma)
                            self.assertEqual(
                                cy, (rho-n+(1-alpha)*(n+gamma+delta))
                                /(rho+gamma+delta),
                            )

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

    def test_static_identity_and_simple_marginal_revenue_zero(self):
        # Dated identity used before taking a limit; these are algebraic
        # static configurations, not asserted equilibrium trajectories.
        wx, wl, k = 0.2, 0.8, 2.0
        for sigma in (0.25, 0.5, 0.9, 0.99):
            varphi = (sigma-1)/sigma
            for alpha in (0.2, 0.33, 0.7):
                s0 = (1-sigma)/(1-alpha*sigma)
                lx0 = np.log(wl*s0/(wx*(1-s0)))/varphi
                # de_X/d(log x)>0 gives the simple negative slope of MR
                # at its zero, since its remaining factors are positive.
                de_dlogx = (alpha-1/sigma)*varphi*s0*(1-s0)
                self.assertGreater(de_dlogx, 0)
                self.assertTrue(np.isfinite(lx0))
                for weight in (0.001, 0.1, 0.8):
                    s = s0+(1-s0)*weight
                    lx = np.log(wl*s/(wx*(1-s)))/varphi
                    lf = (1-alpha)*logsumexp(
                        [np.log(wl), np.log(wx)+varphi*lx]
                    )/varphi
                    ly = alpha*np.log(k)+lf
                    margin = 1-((1-s)/sigma+alpha*s)
                    lB = lx-ly-np.log((1-alpha)*s*margin)
                    left = alpha/(1-alpha)*(ly-np.log(k))
                    right = (lB+np.log(1-alpha)+sigma/(sigma-1)*np.log(wx)
                             + np.log(margin)-np.log(s)/(sigma-1))
                    self.assertAlmostEqual(left, right, places=10)

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
        propositions = re.findall(
            r"\\begin\{proposition\}.*?\\end\{proposition\}", body, re.S
        )
        characterization = next(
            block for block in propositions
            if r"\label{cond:rewrite-uncapped-complements-limits}" in block
        )
        self.assertNotIn(r"\begin{conditionalresult}", body)
        self.assertNotIn(r"\newtheorem{conditionalresult}", main)
        for condition in (
            "and an equilibrium satisfies", r"$B\to\infty$",
            r"\label{eq:rewrite-uncapped-complements-allocation-ratios}",
        ):
            self.assertIn(condition, characterization)
        premises = characterization.split("Then", 1)[0]
        self.assertNotIn("finite limit", premises)
        self.assertNotIn("g_C", premises)
        self.assertNotIn(r"$K/(AL)$", premises)
        self.assertNotIn(r"$C/(AL)$", premises)
        self.assertNotIn(r"g_Y", premises)
        self.assertNotIn(r"g_w", premises)
        self.assertNotIn(r"\eta", premises)
        self.assertNotIn("The capital and consumption ratios are conclusions, not assumptions.", body)
        self.assertIn("The proposition remains conditional on equilibrium existence",
                      " ".join(body.split()))
        self.assertIn("not an equilibrium-existence theorem", proofs)
        for label in (
            "eq:rewrite-household-tvc", "eq:rewrite-developer-tvc",
            "eq:rewrite-complements-household-wealth-bound",
            "eq:rewrite-complements-effective-labor-pv-bound",
            "eq:rewrite-complements-research-pv-bound",
            "eq:rewrite-complements-research-growth-bound",
            "eq:rewrite-complements-limiting-ramsey",
        ):
            self.assertIn(label, proofs)
        self.assertIn("A convergent level need not have a convergent derivative", proofs)
        self.assertIn("Capital cannot repeatedly approach zero", proofs)
        self.assertIn("No convergence of a growth rate or allocation ratio is assumed", proofs)
        self.assertIn("complete orbit", proofs)
        self.assertNotIn("If, in addition", characterization)
        self.assertNotIn("For the additional research characterization", proofs)
        self.assertNotIn("Under the additional research limits", body)
        for removed_label in (
            "eq:rewrite-uncapped-complements-research-rates",
            "eq:rewrite-uncapped-complements-compute-shares",
            "eq:rewrite-uncapped-complements-research-ratio",
        ):
            self.assertNotIn(removed_label, body + proofs)
        self.assertNotRegex(proofs, r"\\(?:sub)*section\{")
        for kind, label in (
            ("Proposition", "prop:rewrite-uncapped-complements-bounds"),
            ("Proposition", "cond:rewrite-uncapped-complements-limits"),
        ):
            self.assertIn(r"\label{"+label+"}", body)
            self.assertIn(r"\begin{proof}[Proof of "+kind+r"~\ref{"+label+"}]", proofs)
        self.assertLess(
            appendix.index(r"\input{sections_rewrite/appendix_uncapped_complements_proofs}"),
            appendix.index(r"\section{Numerical algorithm"))


if __name__ == "__main__":
    unittest.main()

"""Analytical checks for the investment-optimality extension of Proposition 5.

No transition is simulated. Exact rational checks validate the identities
and comparison signs; source checks validate scope and proof references.
They supplement, not replace, the written nonexistence proof.
"""
from fractions import Fraction as Q
import math
from pathlib import Path
import re
import unittest
from rewrite_section_sources import preserved_section_53

ROOT = Path(__file__).resolve().parents[1]


class InvestmentOptimality(unittest.TestCase):
    def test_capital_euler_identity_and_riccati_bound(self):
        d, delta, z = Q(37, 1000), Q(1, 20), Q(7)
        for alpha in (Q(1, 5), Q(33, 100), Q(3, 5)):
            for eps in (alpha/4, alpha/2, alpha*Q(99, 100)):
                for i in (Q(-2), Q(-1, 10), Q(0), eps/2, eps):
                    self.assertEqual((alpha*z-delta-d)-(i*z-delta),
                                     (alpha-i)*z-d)
                    a = (alpha-eps)/(1-eps)
                    self.assertGreater(a, 0)
                    self.assertEqual((alpha-i)/(1-i)-a,
                                     (1-alpha)*(eps-i)/((1-i)*(1-eps)))
                    self.assertGreaterEqual((alpha-i)/(1-i), a)
                    v = 4*d/a
                    self.assertLessEqual(-a+d/v, -a/2)

    def test_reduced_static_monotonicity_exactly(self):
        for alpha in (Q(1, 100), Q(33, 100), Q(3, 5), Q(99, 100)):
            for sigma in (Q(10001, 10000), Q(3, 2), Q(4), Q(100)):
                for s in (Q(1, 1000), Q(1, 2), Q(999, 1000)):
                    e = (1-s)/sigma+alpha*s
                    phi = (sigma-1)/sigma
                    D = e*(1-e)+(alpha-1/sigma)*phi*s*(1-s)
                    N = (sigma-2)*(1-alpha*sigma)*s-(sigma-1)
                    self.assertEqual(D-alpha*s*(1-e), -(1-s)*N/sigma**2)
                    self.assertGreater(D, alpha*s*(1-e))
                    p = alpha+alpha*(1-alpha)*s*(1-e)/D
                    self.assertGreater(p, alpha)
                    self.assertLess(p, 1)
                    # Independent differentiation of k(s,B) and z(s,B).
                    a = s*(1/sigma-alpha)/(1-e)
                    theta = (1-alpha)/alpha
                    dk = 1/(phi*(1-s))-1-a-theta*(a-1/(sigma-1))
                    dz = theta*(a-1/(sigma-1))
                    self.assertEqual(dk, D/(alpha*(1-e)*phi*(1-s)))
                    self.assertEqual(dz/dk, p-1)
                    # k(s,B)=B^(-1/alpha) F(s): fixing k gives
                    # d log s/d log B = 1/(alpha*dk).
                    db = theta+dz/(alpha*dk)
                    self.assertEqual(db, (1-alpha)*s*(1-e)/D)
                    self.assertGreater(db, 0)
                    exponent = sigma/(sigma-1)-1+theta/(sigma-1)
                    self.assertEqual(exponent, 1/(alpha*(sigma-1)))
                    self.assertGreater(exponent, 0)

    def test_inference_share_is_uniformly_below_one_minus_alpha(self):
        for alpha in (Q(1, 100), Q(33, 100), Q(99, 100)):
            for sigma in (Q(101, 100), Q(3, 2), Q(100)):
                bound = (1-alpha)*(1-min(alpha, 1/sigma))
                self.assertLess(bound, 1-alpha)
                for s in (Q(1, 1000), Q(1, 2), Q(1)):
                    e = (1-s)/sigma+alpha*s
                    u = (1-alpha)*s*(1-e)
                    self.assertLessEqual(u, bound)
                    self.assertGreater(1-u, alpha)

    def test_shadow_stock_and_shadow_capital_equations(self):
        alpha, delta, z, u = Q(33, 100), Q(1, 20), Q(3), Q(2, 5)
        r = alpha*z-delta
        for eta in (Q(1, 5), alpha, Q(3, 5)):
            for i in (Q(-1, 10), alpha, Q(3, 5)):
                for h, m in ((Q(2), Q(1, 10)), (Q(7, 2), Q(1, 100))):
                    gB = m*z/(eta*h)  # M = eta*qB*gB.
                    gq = r-u*z/h-eta*gB
                    stock_growth = gq+gB
                    self.assertEqual(stock_growth*h,
                                     r*h-u*z+(1-eta)/eta*m*z)
                    dh_rescaled = h*(stock_growth-(i*z-delta))/z
                    self.assertEqual(dh_rescaled,
                                     (alpha-i)*h+(1-eta)/eta*m-u)

    def test_shadow_pv_against_unit_elastic_equilibrium(self):
        # An existing analytical BGP checks the PV identity independently.
        # It is NOT subject to the sigma>1 nonexistence result.
        for alpha, eta, omega in ((0.33, 0.2, 0.2), (0.4, 0.15, 0.1)):
            n, gamma, rho = 0.003, 0.01, 0.04
            gy = (1-eta)*(1-omega)/(1-eta-omega)*(n+gamma)
            gb = eta*gy/(1-eta)
            u = ((1-alpha)*omega)**2
            m = u*eta*gb/(rho-n+eta*gy)
            direct = m/(eta*gb)
            pv = (u-(1-eta)/eta*m)/(rho-n)
            self.assertTrue(math.isclose(direct, pv, rel_tol=2e-14))

    def test_discount_elimination_and_capped_difference(self):
        # Euler implies D_s/D_t = exp[-(rho-n)(s-t)] C_t/C_s.
        d, r, gap_closure = Q(37, 1000), Q(1, 5), Q(163, 1000)
        gc = r-d
        self.assertEqual(-r+gc, -d)
        # A finite bound adds +gap_closure*qB to the shadow-stock equation.
        # Its limiting PV denominator is d+gap_closure, not d.
        self.assertEqual(d+gap_closure, r)
        u = Q(67, 100)**2
        self.assertEqual(u/(d+gap_closure), u/r)
        self.assertNotEqual(u/(d+gap_closure), u/d)

    def test_research_scale_rearrangement(self):
        for eta in (Q(1, 5), Q(1, 3), Q(3, 5)):
            B = Q(2)**eta.denominator
            M = Q(3)**eta.denominator
            B_eta = Q(2)**eta.numerator
            M_one_minus_eta = Q(3)**(eta.denominator-eta.numerator)
            chi, Y = Q(7, 5), Q(11)
            q = M_one_minus_eta/(chi*eta*B_eta)
            gb = chi*B_eta*Q(3)**eta.numerator/B
            self.assertEqual(eta*q*B*gb, M)
            m, value_share = M/Y, q*B/Y
            self.assertEqual(m/(eta*value_share), gb)
            evaluated = (math.log(float(chi*eta*value_share))/(1-float(eta))
                         +float(eta)/(1-float(eta))*math.log(float(Y))
                         -math.log(float(B)))
            self.assertAlmostEqual(evaluated, math.log(float(m)), places=12)

    def test_proposition_excludes_convergent_shares_not_all_equilibria(self):
        body = preserved_section_53()
        proof = (ROOT/'sections_rewrite/appendix_uncapped_substitutes_proof.tex').read_text(encoding='utf-8')
        statement = next(block for block in re.findall(
            r'\\begin\{proposition\}.*?\\end\{proposition\}', body, re.S)
            if r'\label{prop:rewrite-uncapped-substitutes-explosion}' in block)
        self.assertEqual(len(re.findall(r'\\item\b', statement)), 2)
        self.assertIn('zero limiting shares are also excluded', statement)
        self.assertIn('both exist and are finite', statement)
        self.assertNotIn(r'B\to\infty', statement)
        self.assertNotIn(r's_X\to1', statement)
        self.assertNotIn('derivatives', statement)
        self.assertEqual(proof.count(r'\begin{proof}'), 1)
        self.assertEqual(proof.count(r'\end{proof}'), 1)
        self.assertIn('Both possible limits of the increasing stock $B$ have been excluded', proof)
        self.assertIn('dominated convergence', proof)
        self.assertIn(r'\eqref{eq:rewrite-developer-tvc}', proof)
        self.assertIn('paths with nonconvergent investment shares remain to be analyzed',
                      ' '.join(body.split()))
        self.assertIn(r'\limsup_{t\to\infty}i_t\geq\alpha', proof)


if __name__ == '__main__':
    unittest.main()

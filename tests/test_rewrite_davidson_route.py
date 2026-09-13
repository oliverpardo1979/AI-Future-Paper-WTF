"""Algebra/source checks for Proposition 5 and its Section 4 bridge.

Fraction arithmetic checks identities/signs exactly. Log-level evaluations
avoid overflow near sigma=1; their bound is only a roundoff allowance.
"""
from fractions import Fraction as Q
import math
from pathlib import Path
import unittest
from rewrite_section_sources import preserved_section_53


ROOT = Path(__file__).resolve().parents[1]


class DavidsonRoute(unittest.TestCase):
    def test_exact_static_derivative_sign(self):
        for alpha in (Q(1, 100), Q(1, 5), Q(33, 100), Q(3, 5), Q(99, 100)):
            for sigma in (Q(10001, 10000), Q(101, 100), Q(3, 2), Q(2), Q(4), Q(100)):
                for s in (Q(1, 10000), Q(1, 5), Q(4, 5), Q(99999, 100000), Q(1)):
                    e = (1-s)/sigma+alpha*s
                    direct = s*(1/sigma-alpha)/(1-e)-1/(sigma-1)
                    N = (sigma-2)*(1-alpha*sigma)*s-(sigma-1)
                    self.assertEqual(direct, N/(sigma*(sigma-1)*(1-e)))
                    self.assertLess(direct, 0)
                self.assertEqual((sigma-2)*(1-alpha*sigma)-(sigma-1),
                                 -(1-alpha+alpha*(sigma-1)**2))

    def test_return_bound_at_finite_static_allocations(self):
        for alpha in (0.01, 0.2, 0.33, 0.6, 0.99):
            theta = (1-alpha)/alpha
            for sigma in (1.0001, 1.001, 1.01, 1.5, 2.0, 4.0, 100.0):
                for s in (0.0001, 0.2, 0.8, 0.99999, 1.0):
                    e = (1-s)/sigma+alpha*s
                    # log[(Y/K)/(d B^theta)]; common factors cancel.
                    log_gap = theta*(math.log1p(-e)-math.log1p(-alpha)
                                     -math.log(s)/(sigma-1))
                    allowance = 100*math.ulp(max(1.0, abs(log_gap)))
                    self.assertGreaterEqual(log_gap, -allowance)
                    if s == 1:
                        self.assertAlmostEqual(log_gap, 0.0, places=12)

    def test_feedback_exponent_and_integration_on_both_sides(self):
        for alpha in (Q(1, 5), Q(33, 100), Q(3, 5)):
            theta = (1-alpha)/alpha
            for eta in (alpha/2, alpha, (1+alpha)/2):
                p = (1-eta)/alpha
                self.assertGreater(p, 0)
                self.assertEqual(theta*(1-eta)-eta, p-1)
                self.assertEqual(eta*(1+theta)+p, 1/alpha)
                self.assertGreater(1/alpha, 1)
                iota, chi, d_power = Q(1, 20), Q(3, 2), Q(7, 4)
                # d_power denotes d^(1-eta); integration is exact regardless
                # of whether that positive real number is rational.
                integrand_coefficient = eta*iota*d_power/(2*chi)
                H = eta*iota*alpha*d_power/(2*chi*(1-eta))
                self.assertEqual(H*p, integrand_coefficient)
                self.assertGreater(H, 0)
                c, B_power = Q(2, 7), Q(5, 3)
                escape_bound = B_power/((1/alpha-1)*c)
                self.assertGreater(escape_bound, 0)
                self.assertEqual(B_power-(1/alpha-1)*c*escape_bound, 0)

    def test_constant_share_rule_preserves_positive_consumption(self):
        for alpha in (Q(1, 100), Q(33, 100), Q(3, 5), Q(99, 100)):
            for sigma in (Q(101, 100), Q(3, 2), Q(4), Q(100)):
                for s in (Q(1, 1000), Q(1, 2), Q(999, 1000)):
                    e = (1-s)/sigma+alpha*s
                    u = (1-alpha)*s*(1-e)
                    investment = research = alpha/4
                    consumption = 1-u-investment-research
                    self.assertGreater(u, 0)
                    self.assertLess(u, 1-alpha)
                    self.assertGreater(consumption, alpha/2)
                    self.assertEqual(u+investment+research+consumption, 1)

    def test_research_euler_transformation_exactly(self):
        for eta in (Q(1, 10), Q(1, 5), Q(33, 100), Q(1, 2), Q(9, 10)):
            r, u_over_qb, gB = Q(3, 25), Q(1, 20), Q(7, 50)
            gq = r-u_over_qb-eta*gB
            gP = gq+eta*gB
            self.assertEqual(gP, r-u_over_qb)
            gM = gP/(1-eta)
            self.assertEqual((1-eta)*gM, r-u_over_qb)
            # P=chi*eta*q*B^eta implies P/(qB)=chi*eta*B^(eta-1).
            self.assertEqual(eta-1, -(1-eta))

    def test_research_identity_against_preserved_unit_elastic_bgp(self):
        # An independently evaluated positive BGP supplies a real equilibrium
        # check for D9, even though the explosion theorem excludes sigma=1.
        alpha, eta, omega = 0.33, 0.2, 0.2
        n, gamma, rho, delta, chi = 0.003, 0.01, 0.04, 0.05, 1.4378
        beta, lam = (1-alpha)*omega, (1-alpha)*(1-omega)
        gy = (1-eta)*(1-omega)/(1-eta-omega)*(n+gamma)
        gb = eta*gy/(1-eta)
        r = rho+gy-n
        k = alpha/(r+delta)
        u = beta**2
        m = u*eta*gb/(rho-n+eta*gy)
        feedback = (1-alpha)*(1-eta-omega)
        b0 = (k**(alpha/lam)*u**(beta/lam)*m*(chi/gb)**(1/eta))**(eta*lam/feedback)
        y0 = k**(alpha/lam)*(u*b0)**(beta/lam)
        M, U = m*y0, u*y0
        decay = r-gy+(1-eta)*gb
        self.assertGreater(decay, 0)
        integral = chi*eta*U*b0**(eta-1)/decay
        self.assertTrue(math.isclose(M**(1-eta), integral, rel_tol=2e-13))

    def test_note_keeps_technology_and_equilibrium_distinct(self):
        note = (ROOT/'audit/rewrite_davidson_route.md').read_text(encoding='utf-8')
        text = ' '.join(note.split())
        for phrase in (
            'now incorporated in Proposition 5',
            'No new transition simulation is computed',
            'This divergence is derived, not assumed',
            'Dividing two lower bounds would be invalid',
            'NOT an equilibrium',
            'general nonexistence is not established by this note',
        ):
            self.assertIn(phrase, text)
        self.assertIn('D1', note)
        self.assertIn('D9', note)

    def test_preserved_proposition_does_not_assume_explosion(self):
        import re
        body = preserved_section_53()
        proof = (ROOT/'sections_rewrite/appendix_uncapped_substitutes_proof.tex').read_text(encoding='utf-8')
        statement = next(block for block in re.findall(
            r'\\begin\{proposition\}.*?\\end\{proposition\}', body, re.S)
            if r'\label{prop:rewrite-uncapped-substitutes-explosion}' in block)
        self.assertIn(r'\frac{\dot K_t+\delta K_t}{Y_t}\geq\iota', statement)
        self.assertIn(r'\frac{M_t}{Y_t}\geq\mu', statement)
        self.assertNotIn(r'B\to\infty', statement)
        self.assertNotIn(r's_X\to1', statement)
        self.assertNotIn('log', statement)
        section_context = (ROOT/'sections_rewrite/05_uncapped_equilibria.tex').read_text(
            encoding='utf-8')
        for label in ('eq:rewrite-ai-terminal-ratio', 'eq:rewrite-resource',
                      'eq:rewrite-uncapped-unit-law'):
            self.assertIn(r'\eqref{'+label+'}', section_context+proof)
        self.assertIn(r'\dot B\geq c_BB^{1/\alpha}', proof)
        self.assertIn(r'\emph{upper}', proof)
        self.assertIn('derived, not assumed', proof)
        self.assertIn('not yet a proof of general equilibrium nonexistence',
                      ' '.join(body.split()))
        self.assertIn(r'\label{eq:rewrite-uncapped-research-pv}', body)
        self.assertIn(r'\eqref{eq:rewrite-developer-tvc}', body)

    def test_capped_terminal_investment_limit_and_research_scale(self):
        # Check Section 4's analytical fixed point, not transition paths.
        # Parametrize returns above rho+gamma to avoid huge powers when
        # sigma is close to one. The corresponding finite bound is positive.
        alpha, n, gamma, rho, delta, chi = 0.33, 0.003, 0.01, 0.04, 0.05, 1.4378
        for r in (rho+gamma+0.001, 0.1, 1.0, 10.0, 100.0):
            growth = n+r-rho
            y = (r+delta)/alpha
            u = (1-alpha)**2*y
            c = alpha*(1-alpha)*y+rho-n
            # Resource condition with M/K -> 0, evaluated independently.
            direct = 1-u/y-c/y
            formula = alpha*(n+r-rho+delta)/(r+delta)
            self.assertTrue(math.isclose(direct, formula, rel_tol=2e-14))
            self.assertGreater(formula, 0)
            self.assertLess(formula, alpha)
            self.assertAlmostEqual(alpha-formula, alpha*(rho-n)/(r+delta))
            for eta in (0.2, alpha, 0.6):
                bound = 50.0
                log_M = (math.log(growth)+(1-eta)*math.log(bound)-math.log(chi))/eta
                # dot[(Bbar-B)K]=0 requires this closure rate to equal growth.
                closure = math.exp(math.log(chi)+(eta-1)*math.log(bound)+eta*log_M)
                self.assertTrue(math.isclose(closure, growth, rel_tol=2e-14))
                # M is finite for each fixed bound, whereas Y has positive
                # limiting growth. Thus M/Y -> 0 analytically, not by a
                # finite-grid claim of convergence.
                self.assertTrue(math.isfinite(log_M))
                self.assertGreater(growth, 0)

    def test_research_identity_with_and_without_a_bound(self):
        # The psi derivative cancels exactly. This verifies why the PV
        # formula differs by a psi factor, rather than by a new saving rule.
        for eta in (Q(1, 5), Q(1, 3), Q(3, 5)):
            for psi in (Q(1), Q(1, 2), Q(1, 100)):
                # B and B^eta are exact rational powers on this grid.
                B, B_eta = Q(2)**eta.denominator, Q(2)**eta.numerator
                chi, q, U = Q(7, 5), Q(3), Q(2)
                r, gB = Q(1, 10), Q(1, 25)
                gpsi = Q(0) if psi == 1 else -gB*(1-psi)/psi
                gq = r-U/(q*B)-eta*gB-gpsi
                self.assertEqual(gq+eta*gB+gpsi, r-U/(q*B))
                P = chi*eta*q*B_eta*psi
                derivative = P*(gq+eta*gB+gpsi)
                self.assertEqual(derivative, r*P-chi*eta*U*(B_eta/B)*psi)


if __name__ == '__main__':
    unittest.main()

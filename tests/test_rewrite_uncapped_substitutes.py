"""Algebra checks preserving the archived asymptotic explosion result.

These are not transition simulations or evidence of equilibrium existence.
Rational identities use exact arithmetic; a log-level check avoids overflow
near unit elasticity and uses a tolerance only for floating-point roundoff.
"""
from fractions import Fraction as Q
from pathlib import Path
import math
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


def source(name):
    return re.sub(r"(?<!\\)%[^\n]*", "", (ROOT / name).read_text(encoding="utf-8"))


def coefficients(alpha, sigma, s):
    theta = (1-alpha)/alpha
    e = (1-s)/sigma + alpha*s
    D = 1+s*(1/sigma-alpha)/(1-e)
    E = theta*(D-1-1/(sigma-1))
    v = (sigma-1)/sigma
    F = (1-s)*v/(1-(1-s)*v*D)
    return theta, e, D, E, F


class UncappedSubstitutionExplosion(unittest.TestCase):
    def test_static_identity_in_log_levels_near_one(self):
        for alpha in (0.2, 0.33, 0.6):
            for sigma in (1.0001, 1.001, 1.01, 1.5, 4.0):
                for s in (0.2, 0.8, 0.99999):
                    theta, e, _, _, _ = coefficients(alpha, sigma, s)
                    logB, logY = 3.2, 2.1
                    omega = 0.2
                    # Build Z and K directly from pricing, CES and production.
                    logU = logY + math.log((1-alpha)*s*(1-e))
                    logX = logB + logU
                    logZ = logX + sigma/(sigma-1)*(math.log(omega)-math.log(s))
                    logK = (logY-(1-alpha)*logZ)/alpha
                    direct = logY-logK
                    stated = theta*(sigma/(sigma-1)*math.log(omega)+logB
                                    +math.log(1-alpha)+math.log(1-e)
                                    -math.log(s)/(sigma-1))
                    # About 20 double-precision operations, allowing 100 ulps
                    # at the largest intermediate scale (including cancellation).
                    scale = max(1.0, abs(logZ), abs(logK), abs(stated),
                                abs(theta*sigma/(sigma-1)*math.log(omega)),
                                abs(theta/(sigma-1)*math.log(s)))
                    self.assertLessEqual(abs(direct-stated), 100*math.ulp(scale))

    def test_exact_differentiation_and_share_elimination(self):
        for alpha in (Q(1, 5), Q(33, 100), Q(3, 5)):
            for sigma in (Q(10001, 10000), Q(101, 100), Q(3, 2), Q(4)):
                for s in (Q(1, 5), Q(4, 5), Q(99999, 100000)):
                    theta, e, D, E, F = coefficients(alpha, sigma, s)
                    gB, gY, G = Q(7, 10), Q(11, 10), Q(13, 1000)
                    gs = F*(gB+gY-G)
                    gX = gB+gY+D*gs
                    # Independently differentiate the original CES and
                    # production equations, without using z(B,s).
                    self.assertEqual(gs, (1-s)*(sigma-1)/sigma*(gX-G))
                    gZ = (1-s)*G+s*gX
                    gz_production = theta*(gZ-gY)
                    self.assertEqual(gz_production, theta*gB+E*gs)
                    # D is independently d log[u(s)] / d log s.
                    u = (1-alpha)*s*(1-e)
                    du = (1-alpha)*((1-e)+s*(1/sigma-alpha))
                    self.assertEqual(D, s*du/u)

    def test_exact_research_logistic_reduction(self):
        alpha, sigma, s = Q(33, 100), Q(3, 2), Q(9, 10)
        theta, _, _, E, F = coefficients(alpha, sigma, s)
        for eta in (Q(1, 5), alpha, Q(1, 2), Q(9, 10)):
            h, y, m, G_over_z = Q(2, 7), Q(7, 20), Q(3, 8), Q(1, 100)
            gz_over_z = (theta+E*F)*h+E*F*(y-G_over_z)
            direct = (eta-1)*h+eta*m-gz_over_z
            a = eta*m-E*F*(y-G_over_z)
            b = 1+theta-eta+E*F
            self.assertEqual(direct, a-b*h)

    def test_positive_limits_below_at_and_above_alpha(self):
        for alpha in (Q(1, 5), Q(33, 100), Q(3, 5)):
            for eta in (alpha/2, alpha, (1+alpha)/2):
                theta = (1-alpha)/alpha
                h = eta*alpha/(1+theta-eta)
                a = eta*alpha*(1-alpha)/(1-alpha*eta)
                self.assertEqual(h, eta*alpha**2/(1-alpha*eta))
                self.assertEqual(theta*h, a)
                self.assertEqual(alpha-a, alpha*(1-eta)/(1-alpha*eta))
                self.assertGreater(h, 0)
                self.assertGreater(a, 0)
                self.assertGreater(alpha-a, 0)
                # An independent reciprocal-linear solution of dot z = a z^2
                # validates the scalar comparison, not an economic trajectory.
                z0, fraction = Q(3), Q(2, 5)
                escape = 1/(a*z0)
                t = fraction*escape
                z = 1/(1/z0-a*t)
                self.assertEqual(z, z0/(1-fraction))
                self.assertEqual(a/(1/z0-a*t)**2, a*z*z)

    def test_archived_result_and_active_automatic_proof_links(self):
        body = source("sections_rewrite/05_uncapped_equilibria.tex")
        proof = source("sections_rewrite/appendix_uncapped_substitutes_proof.tex")
        appendix = source("sections_rewrite/appendix.tex")
        self.assertIn(r"\input{sections_rewrite/appendix_uncapped_substitutes_proof}", appendix)
        self.assertNotRegex(proof, r"\\(?:sub)*section\{")
        self.assertIn(r"\begin{proof}[Proof of Proposition~\ref{prop:rewrite-uncapped-substitutes-explosion}]", proof)
        self.assertIn(r"\hyperref[proof:rewrite-uncapped-substitutes-explosion]", body)
        # Preserve the exact earlier result, but do not mistake its source
        # assertions for checks of the newly adopted theorem.
        archived_body = source("audit/archive/uncapped_section_before_persistent_investment.tex")
        archived_proof = source("audit/archive/uncapped_asymptotic_explosion_proof.tex")
        normalized = " ".join(archived_body.split())
        self.assertIn(r"$K,B,C,M>0$", archived_body)
        self.assertIn("where $T$ may initially be infinite", normalized)
        self.assertIn("does not construct a path satisfying its hypotheses", normalized)
        self.assertIn("Convergence of the shares alone would not imply", normalized)
        self.assertIn(r"$\eta<\alpha$, $\eta=\alpha$, or $\eta>\alpha$", normalized)
        self.assertIn("No convergence of $h$ was assumed", archived_proof)
        self.assertIn("logistic equations", archived_proof)
        self.assertIn("finite allocations at every finite date", " ".join(proof.split()))
        self.assertIn(r"{ceballosetal2011}", proof)

    def test_cited_primary_source_is_in_bibliography(self):
        bib = source("references.bib")
        self.assertIn("@article{ceballosetal2011,", bib)
        self.assertIn("https://ejde.math.txstate.edu/Volumes/2011/05/ceballos.pdf", bib)
        body = " ".join(source("sections_rewrite/05_uncapped_equilibria.tex").split())
        self.assertIn("holds saving and factor-allocation shares fixed", body)
        self.assertIn("cannot apply its explosion theorem directly", body)


if __name__ == "__main__":
    unittest.main()

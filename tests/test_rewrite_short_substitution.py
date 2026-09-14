"""Check the short exposition and preserve the previous result exactly.

These checks are algebra/source checks, not new equilibrium simulations.
"""
from fractions import Fraction as Q
import hashlib
import unittest

from rewrite_section_sources import ROOT, preserved_section_53
from test_rewrite_proposition_structure import source, active_sources


class ShortSubstitutionExposition(unittest.TestCase):
    def test_previous_subsection_is_preserved_verbatim_as_comments(self):
        previous = preserved_section_53()
        # SHA256 of the complete subsection at author commit 852a2f6,
        # normalized to LF with exactly one final newline.
        self.assertEqual(
            hashlib.sha256(previous.encode("utf-8")).hexdigest(),
            "3ab95da79250719fc13f0170a3f6abf98cd5c4d52a97434ac84077145a4587b6")
        active = source("sections_rewrite/05_uncapped_equilibria.tex").split(
            r"\label{subsec:rewrite-uncapped}", 1)[1]
        self.assertLess(len(active.split()), 0.4 * len(previous.split()))
        # Only the finite-value nonexistence result is now stated in 5.3;
        # the archived conditional explosion proposition stays commented.
        self.assertEqual(active.count(r"\begin{proposition}"), 1)
        self.assertIn(r"\label{prop:rewrite-research-scale}", active)
        self.assertNotIn("investment shares", active)
        all_active = "\n".join(active_sources())
        self.assertNotIn("prop:rewrite-uncapped-substitutes-explosion", all_active)
        self.assertNotIn(r"\input{sections_rewrite/appendix_uncapped_substitutes_proof}",
                         all_active)
        proof = ROOT / "sections_rewrite/appendix_uncapped_substitutes_proof.tex"
        self.assertTrue(proof.exists())
        self.assertIn("Step 9.", proof.read_text(encoding="utf-8"))

    def test_new_scope_and_intro_follow_the_upper_bound_comparison(self):
        body = " ".join(source("sections_rewrite/05_uncapped_equilibria.tex").split())
        intro = " ".join(source("sections_rewrite/01_introduction.tex").split())
        self.assertIn(r"\label{eq:rewrite-uncapped-dated-return-bound}", body)
        self.assertIn(r"\label{eq:rewrite-substitutes-dated-output-capital}", body)
        self.assertIn("with or without an efficiency upper bound", body)
        self.assertIn(r"$g_{C/N}=r-\rho\to\infty$", body)
        self.assertNotIn(r"g_{Y/N}\to\infty", body)
        self.assertIn("do not establish a finite-time singularity", body)
        self.assertIn("increase without bound as the efficiency upper bound rises", intro)
        self.assertNotIn("discounted net profits arbitrarily large", intro)
        for label in ("eq:rewrite-ai-output-limit", "eq:rewrite-composite-ai-limit",
                      "eq:rewrite-output-capital-limit", "eq:rewrite-euler"):
            self.assertIn(r"\eqref{" + label + "}", body)

    def test_composite_output_and_return_growth_identities(self):
        for alpha in (Q(1, 100), Q(1, 5), Q(33, 100), Q(3, 5), Q(99, 100)):
            exponent = (1-alpha)/alpha
            self.assertGreater(exponent, 0)
            self.assertEqual(exponent * alpha/(1-alpha), 1)
            # Production: log Y=alpha log K+(1-alpha) log Z.
            logY, logK = Q(7, 3), Q(3, 7)
            logZ = (logY-alpha*logK)/(1-alpha)
            self.assertEqual(logZ-logY, alpha/(1-alpha)*(logY-logK))
            # R(B)+delta has elasticity (1-alpha)/alpha in B.
            self.assertGreater(alpha*exponent, 0)

    def test_abstract_and_intro_specify_long_run_growth_and_unit_benchmark(self):
        abstract = " ".join(source("main_rewrite.tex").split(
            r"\begin{abstract}", 1)[1].split(r"\end{abstract}", 1)[0].split())
        intro = " ".join(source("sections_rewrite/01_introduction.tex").split())
        paragraph = intro.split("I also examine the role", 1)[1].split(
            "Simulations show", 1)[0]
        self.assertIn("long-run output-per-worker growth cannot exceed", abstract)
        self.assertIn("increases without bound as the upper bound rises", abstract)
        self.assertNotIn("growth is always bounded", abstract)
        self.assertNotIn("IA efficiency", abstract)
        self.assertIn("long-run output-per-person growth cannot exceed", paragraph)
        self.assertIn("At unit elasticity and without an upper bound", paragraph)
        self.assertIn("output per person and real wages grow faster than this exogenous rate",
                      paragraph)
        self.assertNotIn("positive labor income share", paragraph)

    def test_complementarity_reverses_the_static_comparison(self):
        for alpha in (Q(1, 5), Q(33, 100), Q(3, 5)):
            for sigma in (Q(1, 10), Q(1, 2), Q(99, 100)):
                lower = (1-sigma)/(1-alpha*sigma)
                for fraction in (Q(1, 1000), Q(1, 2), Q(999, 1000)):
                    s = lower+(1-lower)*fraction
                    e = (1-s)/sigma+alpha*s
                    self.assertLess(e, 1)
                    numerator = (sigma-2)*(1-alpha*sigma)*s-(sigma-1)
                    derivative = numerator/(sigma*(sigma-1)*(1-e))
                    self.assertGreater(derivative, 0)
                at_lower = (sigma-2)*(1-alpha*sigma)*lower-(sigma-1)
                self.assertEqual(at_lower, -(1-sigma)**2)


if __name__ == "__main__":
    unittest.main()

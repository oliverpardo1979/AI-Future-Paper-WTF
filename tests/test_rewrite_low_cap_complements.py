"""Algebra and scope checks for the low-cap complementarity argument.

These are not simulations or an equilibrium-existence certificate.
"""
from fractions import Fraction as Q
import re
import unittest

from test_rewrite_proposition_structure import source


class LowCapComplementarity(unittest.TestCase):
    def test_necessary_property_is_separate_from_existence_proposition(self):
        body = source("sections_rewrite/04_equilibrium_regimes.tex")
        proposition = re.search(
            r"\\begin\{proposition\}.*?\\end\{proposition\}", body, re.S
        ).group()
        self.assertEqual(len(re.findall(r"\\item\b", proposition)), 4)
        reference = r"\ref{prop:rewrite-low-cap-complements}"
        self.assertIn(reference, body)
        self.assertNotIn(reference, proposition)
        appendix = source("sections_rewrite/appendix.tex")
        self.assertIn(r"\label{prop:rewrite-low-cap-complements}", appendix)

    def test_appendix_proofs_follow_statement_order(self):
        def expand(path):
            return re.sub(
                r"\\input\{([^}]+)\}",
                lambda match: expand(match[1] + ".tex"),
                source(path),
            )

        # Only the proofs section, before the numerical appendices.
        appendix = re.split(
            r"\\section\{", source("sections_rewrite/appendix.tex")
        )[1]
        appendix = re.sub(
            r"\\input\{([^}]+)\}",
            lambda match: expand(match[1] + ".tex"),
            appendix,
        )
        headings = re.findall(
            r"\\begin\{proof\}\[Proof of (Lemma|Proposition)~\\ref\{([^}]+)\}\]",
            appendix,
        )
        self.assertEqual(headings, [
            ("Lemma", "lem:rewrite-monopoly-choice"),
            ("Lemma", "lem:rewrite-developer-verification"),
            ("Proposition", "prop:rewrite-equilibrium-regimes"),
            ("Proposition", "prop:rewrite-uncapped-complements-bounds"),
            ("Proposition", "cond:rewrite-uncapped-complements-limits"),
            ("Proposition", "prop:rewrite-uncapped-unit-bgp"),
            ("Proposition", "prop:rewrite-research-scale"),
            ("Proposition", "prop:rewrite-low-cap-complements"),
        ])

    def test_proof_bounds_average_growth_without_assuming_ratio_convergence(self):
        proof = source("sections_rewrite/appendix.tex").split(
            r"\label{proof:rewrite-low-cap-complements}", 1
        )[1].split(r"\end{proof}", 1)[0]
        self.assertIn(r"C_t\geq(\rho-n)K_t", proof)
        self.assertIn(r"\limsup_{t\to\infty}\frac1t", proof)
        self.assertIn(r"$X/(AL)\to0$", proof)
        self.assertIn("not a proof of equilibrium existence", proof)
        self.assertIn(r"Proposition~\ref{prop:rewrite-equilibrium-regimes}", proof)
        self.assertNotIn("Step 1 above", proof)
        for label in ("eq:rewrite-household-budget", "eq:rewrite-household-tvc",
                      "eq:rewrite-euler", "eq:rewrite-frontier-share-map"):
            self.assertIn(r"\eqref{" + label + "}", proof)

    def test_return_output_and_service_bounds_with_exact_arithmetic(self):
        omega_x, rho, n, gamma, delta = Q(1, 5), Q(4, 100), Q(1, 100), Q(1, 100), Q(5, 100)
        for alpha in (Q(1, 5), Q(1, 3), Q(1, 2)):
            theta = (1-alpha)/alpha
            self.assertEqual(theta.denominator, 1)
            for sigma in (Q(1, 2), Q(2, 3), Q(3, 4)):
                power, share_power = sigma/(sigma-1), -1/(sigma-1)
                self.assertEqual(power.denominator, 1)
                self.assertEqual(share_power.denominator, 1)
                cap = Q(1, 10)/((1-alpha)**2 * omega_x**int(power))
                yk_cap = ((1-alpha)**2 * cap * omega_x**int(power))**int(theta)
                return_cap = alpha*yk_cap-delta
                self.assertLess(return_cap-rho, gamma)
                lower_share = (1-sigma)/(1-alpha*sigma)
                for b_fraction in (Q(1, 10), Q(1, 2), Q(1)):
                    b = b_fraction*cap
                    for fraction in (Q(1, 100), Q(1, 2), Q(99, 100)):
                        s = lower_share+(1-lower_share)*fraction
                        e = (1-s)/sigma+alpha*s
                        yk = (b*(1-alpha)*omega_x**int(power)
                              *(1-e)*s**int(share_power))**int(theta)
                        self.assertLessEqual(yk, yk_cap)
                        self.assertLessEqual(b*(1-alpha)*s*(1-e), cap*(1-alpha)**2)
                        # C >= (rho-n)K bounds Y/C by yk_cap/(rho-n).
                        for wealth_fraction in (Q(1, 10), Q(1, 2), Q(1)):
                            k_over_c = wealth_fraction/(rho-n)
                            self.assertLessEqual(yk*k_over_c, yk_cap/(rho-n))


if __name__ == "__main__":
    unittest.main()

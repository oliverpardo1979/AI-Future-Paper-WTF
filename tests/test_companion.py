"""Checks for the new manuscript; no transition simulations or file exports."""
from collections import Counter
from pathlib import Path
import re
import sys
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from define_positive_ai_branch import (  # noqa: E402
    PositiveAIBenchmarkParameters,
    balanced_growth_seed,
    canonical_seed_residuals,
)
from test_rewrite_proposition_structure import active_sources  # noqa: E402


class CompanionManuscript(unittest.TestCase):
    def test_labels_references_and_proof_are_self_contained(self):
        text = "\n".join(active_sources("main_companion.tex"))
        labels = re.findall(r"\\label\{([^}]+)\}", text)
        self.assertFalse([k for k, n in Counter(labels).items() if n > 1])
        refs = re.findall(r"\\(?:eqref|ref|pageref)\*?\{([^}]+)\}", text)
        self.assertFalse(set(refs) - set(labels))
        self.assertNotIn("eq:rewrite-", text)
        self.assertEqual(text.count(r"\begin{proposition}"), 1)
        self.assertIn(r"\begin{proof}[Proof of Proposition~\ref{prop:companion-bgp}]", text)
        for suffix in ("initial", "household-tvc", "developer-tvc"):
            self.assertIn("eq:companion-eq-" + suffix, labels)
        for suffix in ("developer-verification", "household-verification"):
            self.assertIn("eq:companion-" + suffix, labels)
        bib = (ROOT / "references.bib").read_text(encoding="utf-8")
        keys = set(re.findall(r"@\w+\{([^,]+),", bib))
        citations = re.findall(r"\\cite\w*\{([^}]+)\}", text)
        self.assertFalse({k.strip() for group in citations for k in group.split(",")} - keys)

    def test_calibration_uses_current_not_legacy_values(self):
        original = (ROOT / "sections_rewrite/05_quantitative_equilibria.tex").read_text(encoding="utf-8")
        companion = (ROOT / "sections_companion/04_calibration.tex").read_text(encoding="utf-8")
        expected = {r"\alpha": "0.33", r"\delta": "0.05", r"\rho": "0.04",
                    "n": "0.003", r"\gamma": "0.01", r"\omega_X": "0.20",
                    r"\omega_L": "0.80", r"\eta": "0.20"}
        for symbol, value in expected.items():
            pattern = re.escape("$" + symbol + "$") + r"\s*&\s*" + re.escape(value) + r"\s*&"
            self.assertRegex(original, pattern)
            self.assertRegex(companion, pattern)
        self.assertIn("I do not transfer that timing target", companion)
        self.assertIn(r"$\sigma$ & 1", companion)
        self.assertIn(r"$\chi$ & Free, $>0$", companion)

    def test_reference_result_matches_existing_equilibrium(self):
        p = PositiveAIBenchmarkParameters()
        s = balanced_growth_seed(p)
        self.assertLess(canonical_seed_residuals(p, s)["max_abs_equilibrium_residual"], 5e-12)
        self.assertAlmostEqual(s.output_growth - p.population_growth, 0.01086666666666667)
        self.assertAlmostEqual(s.net_interest_rate, 0.05086666666666667)
        self.assertAlmostEqual(100*(s.output_growth - p.population_growth - p.labor_productivity_growth),
                               0.08666666666666667)

    def test_analytical_sensitivity_matches_existing_code(self):
        # Finite differences audit derivatives, not calibrated scenario ranges.
        step = 1e-5
        for eta, omega in ((0.10, 0.10), (0.20, 0.20), (0.30, 0.40)):
            total = 0.003 + 0.01
            expected = [omega*(1-omega)*total/(1-eta-omega)**2,
                        eta*(1-eta)*total/(1-eta-omega)**2]
            def growth(e, w):
                p = PositiveAIBenchmarkParameters(eta=e, omega_x=w)
                self.assertLessEqual((1-p.alpha)*w, 0.5)
                self.assertLess(e+w, 1)
                return balanced_growth_seed(p).output_growth-p.population_growth
            numerical = [(growth(eta+step, omega)-growth(eta-step, omega))/(2*step),
                         (growth(eta, omega+step)-growth(eta, omega-step))/(2*step)]
            np.testing.assert_allclose(numerical, expected, rtol=5e-9, atol=1e-12)

    def test_chi_changes_levels_not_rates_or_ratios(self):
        cases = [balanced_growth_seed(PositiveAIBenchmarkParameters(chi=x))
                 for x in (0.01, 1.0, 1.4378)]
        for s in cases[1:]:
            for name in ("output_growth", "capability_growth", "net_interest_rate",
                         "inference_share", "research_share", "consumption_share",
                         "capital_output_ratio"):
                self.assertAlmostEqual(getattr(s, name), getattr(cases[0], name))
            self.assertNotAlmostEqual(s.capability, cases[0].capability)

    def test_separate_manuscripts_and_publication_paths(self):
        original = (ROOT / "main_rewrite.tex").read_text(encoding="utf-8")
        self.assertNotIn("sections_companion", original)
        self.assertIn(r"\input{sections_rewrite/appendix_uncapped_unit}", original)
        body = (ROOT / "sections_rewrite/05_uncapped_equilibria.tex").read_text(encoding="utf-8")
        uncapped_bgp = body.split(r"\label{subsec:rewrite-uncapped-unit-bgp}")[1].split(
            r"\label{subsec:rewrite-uncapped}")[0]
        # The author removed the two closing paragraphs of Section 5.2,
        # including this citation; the separate manuscript is preserved.
        self.assertNotIn(r"\citep{pardo2026companion}", uncapped_bgp)
        self.assertNotIn("This is balanced growth, not a steady state in levels", uncapped_bgp)
        self.assertNotIn("With any finite upper bound, the characterized", uncapped_bgp)
        workflow = (ROOT / ".github/workflows/pages.yml").read_text(encoding="utf-8")
        self.assertIn("main_rewrite.tex\n            main_companion.tex", workflow)
        self.assertIn("sections_companion/**", workflow)
        self.assertIn("how-much-can-recursive-ai-self-improvement-raise-economic-growth.pdf", workflow)


if __name__ == "__main__":
    unittest.main()

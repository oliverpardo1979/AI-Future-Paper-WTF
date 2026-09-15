"""Guard the scope of the approved September 15 Overleaf integration."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SECTIONS = ROOT / "sections_rewrite"


def active_source(filename):
    source = (SECTIONS / filename).read_text(encoding="utf-8")
    return re.sub(r"(?<!\\)%[^\n]*", "", source)


class OverleafIntegrationTests(unittest.TestCase):
    def test_single_research_scale_result(self):
        source = active_source("05_uncapped_equilibria.tex")
        proposition = source.split(
            r"\label{prop:rewrite-research-scale}", 1
        )[1].split(r"\end{proposition}", 1)[0]
        self.assertIn(r"0<\alpha <\eta<1", proposition)
        self.assertIn(r"[0,T]", proposition)
        self.assertNotIn(r"\item", proposition)
        self.assertNotIn("infinite-horizon equilibrium", proposition)

    def test_proof_matches_the_single_result(self):
        source = active_source("appendix.tex")
        self.assertEqual(source.count(r"\label{proof:rewrite-research-scale}"), 1)
        proof = source.split(r"\label{proof:rewrite-research-scale}", 1)[1]
        proof = proof.split(r"\end{proof}", 1)[0]
        self.assertIn(r"\label{eq:rewrite-research-burst-payoff}", proof)
        self.assertIn(r"\eta>\alpha", proof)
        self.assertIn("discount factor above and away from zero", proof)
        self.assertIn(r"Each finite $\mathcal M$", proof)
        self.assertNotIn("Part (i)", proof)
        self.assertNotIn("Part (ii)", proof)
        self.assertNotIn("nonexistence conclusion", proof)

    def test_broader_proof_is_preserved_but_inactive(self):
        source = (SECTIONS / "appendix.tex").read_text(encoding="utf-8")
        archive = source.split("% BEGIN PRESERVED BROADER RESEARCH-SCALE PROOF", 1)[1]
        archive = archive.split("% END PRESERVED BROADER RESEARCH-SCALE PROOF", 1)[0]
        self.assertIn("The exponent satisfies $p<1$", archive)
        self.assertIn("To obtain the infinite-horizon nonexistence conclusion", archive)
        self.assertTrue(all(line.startswith("%") for line in archive.splitlines()[1:]))
        self.assertNotIn("Besides the two cases", active_source("appendix.tex"))

    def test_design_and_parameter_table_do_not_cite_removed_part(self):
        design = active_source("08_rsi_design.tex")
        table = active_source("parameter_tables.tex")
        obsolete = r"\ref{prop:rewrite-research-scale}(i)"
        self.assertNotIn(obsolete, design + table)
        self.assertIn(r"\mathcal B(1.5)<\overline B<\mathcal B(1.1)", design)
        self.assertIn("The following two subsections differ only", design)
        self.assertIn(r"Setting $\chi=0$ rules out improvements", design)


if __name__ == "__main__":
    unittest.main()

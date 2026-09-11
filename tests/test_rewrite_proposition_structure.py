"""Source checks for the unified proposition and its proof.

These tests check manuscript organization and references, not equilibrium
existence or numerical transition accuracy. Algebraic checks are in
test_rewrite_finite_frontier.py.
"""
from collections import Counter
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


def source(path):
    text = (ROOT / path).read_text(encoding="utf-8")
    return re.sub(r"(?<!\\)%[^\n]*", "", text)


def active_sources(path="main_rewrite.tex", visited=None):
    visited = set() if visited is None else visited
    if path in visited:
        return []
    visited.add(path)
    text = source(path)
    result = [text]
    for name in re.findall(r"\\(?:input|include)\{([^}]+)\}", text):
        child = name if name.endswith(".tex") else name + ".tex"
        result.extend(active_sources(child, visited))
    return result


class UnifiedPropositionStructure(unittest.TestCase):
    def test_four_cases_share_one_proposition(self):
        body = source("sections_rewrite/04_equilibrium_regimes.tex")
        propositions = re.findall(
            r"\\begin\{proposition\}.*?\\end\{proposition\}", body, re.S
        )
        self.assertEqual(len(propositions), 1)
        unified = propositions[0]
        self.assertIn(r"\label{prop:rewrite-equilibrium-regimes}", unified)
        self.assertEqual(len(re.findall(r"\\item\b", unified)), 4)
        self.assertIn(r"ref=\theproposition(\roman*)", unified)
        labels = [
            "prop:rewrite-capped-complements-existence",
            "prop:rewrite-capped-unit-existence",
            "prop:rewrite-capped-substitutes-labor-existence",
            "prop:rewrite-capped-substitutes-existence",
        ]
        positions = [unified.index(r"\label{" + label + "}") for label in labels]
        self.assertEqual(positions, sorted(positions))
        unit_case = unified[positions[1]:positions[2]]
        # The identity may appear in prose or inside the displayed system.
        self.assertIn(r"s_X=\omega_X", unit_case)
        self.assertIn(r"$0<\sigma<1$ and $\overline B>\mathcal B(\sigma)$", unified)
        self.assertIn("nonempty open set", unified)
        self.assertIn(r"$0<\overline B<\infty$", unified)
        self.assertIn(
            r"\label{def:rewrite-equilibrium}", source("sections_rewrite/03_model.tex")
        )

    def test_growth_definitions_and_unit_frontier_scope(self):
        body = source("sections_rewrite/04_equilibrium_regimes.tex")
        self.assertIn(r"$g_{Y/N}$ as the growth rate of output per worker", body)
        self.assertIn(r"$g_w$ as the real-wage growth rate", body)
        self.assertIn(r"$\sigma=1$ & Any finite $\overline B>0$", body)

    def test_table_stays_in_main_text_and_coordinates_move_to_proof(self):
        body = source("sections_rewrite/04_equilibrium_regimes.tex")
        proof = source("sections_rewrite/appendix_finite_frontier.tex")
        self.assertIn(r"\label{tab:rewrite-finite-existence}", body)
        self.assertIn(r"\label{fig:rewrite-frontier-regimes}", body)
        self.assertNotIn(r"\label{tab:rewrite-finite-existence}", proof)
        for label in (
            "eq:rewrite-unit-terminal-capital",
            "eq:rewrite-labor-local-initial",
            "eq:rewrite-ai-local-initial",
        ):
            self.assertNotIn(r"\label{" + label + "}", body)
            self.assertIn(r"\label{" + label + "}", proof)
        heading = r"\begin{proof}[Proof of Proposition~\ref{prop:rewrite-equilibrium-regimes}]"
        self.assertEqual(proof.count(heading), 1)
        unified_proof = proof.split(heading, 1)[1].split(r"\end{proof}", 1)[0]
        self.assertEqual(len(re.findall(r"\\textit\{Step [1-5]\.", unified_proof)), 5)
        self.assertIn(r"\label{eq:rewrite-finite-existence-tvcs}", unified_proof)
        self.assertIn("The preimage of each open neighborhood", unified_proof)

    def test_regime_figure_includes_only_proven_complementary_region(self):
        body = source("sections_rewrite/04_equilibrium_regimes.tex")
        figure = next(
            block for block in re.findall(
                r"\\begin\{figure\}.*?\\end\{figure\}", body, re.S
            ) if r"\label{fig:rewrite-frontier-regimes}" in block
        )
        self.assertIn(r"$0<\sigma<1$", figure)
        self.assertIn(r"$\overline B>\mathcal B(\sigma)$", figure)
        # These scope qualifications are in the surrounding text, not
        # necessarily repeated in the figure caption.
        normalized_body = " ".join(body.split())
        self.assertIn(
            r"The omission of the case where $\sigma<1$ and $\overline B < \mathcal B(\sigma)$",
            normalized_body,
        )
        self.assertIn("the existence proof does not cover it", normalized_body)
        for label in (
            "prop:rewrite-capped-complements-existence",
            "prop:rewrite-capped-substitutes-labor-existence",
            "prop:rewrite-capped-substitutes-existence",
        ):
            self.assertIn(r"\ref{" + label + "}", figure)
        self.assertEqual(figure.count("plot[smooth] coordinates"), 2)

    def test_wage_result_and_proof_are_together_in_appendix(self):
        body = source("sections_rewrite/04_equilibrium_regimes.tex")
        appendix = source("sections_rewrite/appendix_finite_frontier.tex")
        self.assertNotIn(r"\subsection{Wages and labor's income share}", body)
        for label in (
            "prop:rewrite-output-wage-wedge",
            "eq:rewrite-output-wage-wedge",
            "eq:rewrite-labor-share-decline-rate",
            "eq:rewrite-wage-premium-share-decline",
        ):
            self.assertNotIn(r"\label{" + label + "}", body)
            self.assertIn(r"\label{" + label + "}", appendix)
        self.assertLess(
            appendix.index(r"\label{prop:rewrite-output-wage-wedge}"),
            appendix.index(r"\label{proof:rewrite-output-wage-wedge}"),
        )
        self.assertIn(r"\ref{prop:rewrite-output-wage-wedge}", body)
        quantitative = source("sections_rewrite/05_quantitative_equilibria.tex")
        self.assertIn(r"\ref{prop:rewrite-output-wage-wedge}", quantitative)

    def test_active_references_resolve_once(self):
        text = "\n".join(active_sources())
        labels = Counter(re.findall(r"\\label\{([^}]+)\}", text))
        refs = set(re.findall(r"\\(?:eqref|ref)\*?\{([^}]+)\}", text))
        refs.update(re.findall(r"\\hyperref\[([^]]+)\]", text))
        self.assertEqual({label: count for label, count in labels.items() if count > 1}, {})
        self.assertEqual(refs - labels.keys(), set())


if __name__ == "__main__":
    unittest.main()

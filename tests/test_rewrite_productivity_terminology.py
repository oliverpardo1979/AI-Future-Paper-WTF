"""The name of B changes, not its meaning or the algorithm's identifiers."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ProductivityTerminologyTests(unittest.TestCase):
    def test_efficiency_is_retained_only_as_a_conceptual_bridge(self):
        files = [ROOT / 'main_rewrite.tex', *sorted((ROOT / 'sections_rewrite').rglob('*.tex'))]
        matches = []
        for path in files:
            text = path.read_text(encoding='utf-8')
            matches.extend((path.name, match.group()) for match in
                           re.finditer(r'AI(?:\s+|-)efficiency', text))
        self.assertEqual(matches, [('03_model.tex', 'AI efficiency')])

    def test_definition_and_literature_bridge(self):
        text = (ROOT / 'sections_rewrite/03_model.tex').read_text(encoding='utf-8')
        self.assertIn('AI productivity: AI services obtained per unit of compute', text)
        self.assertIn(r'\emph{AI efficiency}', text)
        self.assertIn(r'\emph{algorithmic efficiency}', text)
        self.assertIn(r'\citep{hernandezbrown2020,erdilbesiroglu2022}', text)
        self.assertIn('X=BU.', text)
        self.assertIn(r'\dot B=\chi(BM)^\eta\psi(B)', text)
        self.assertIn('The parameter \\(\\chi\\) shifts research productivity.', text)
        self.assertIn('$A$ efficiency units', text)

    def test_legacy_equation_labels_are_unchanged(self):
        text = (ROOT / 'sections_rewrite/05_uncapped_equilibria.tex').read_text(encoding='utf-8')
        self.assertIn(r'\label{eq:rewrite-uncapped-unit-efficiency-growth}', text)
        self.assertIn(r'\eqref{eq:rewrite-uncapped-unit-efficiency-growth}', text)


if __name__ == '__main__':
    unittest.main()

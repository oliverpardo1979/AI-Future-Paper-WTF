"""Compare revised short-run scales with the pre-change renderer, without writes."""
import ast
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'.python-packages'), str(ROOT/'scripts')]
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np
import calibrate_rewrite_ai_price as renderer
from simulate_rewrite_illustrative_rsi import make_design


class DistributionScales(unittest.TestCase):
    def test_only_initial_a_and_c_change(self):
        source = subprocess.check_output([
            'git', 'show', '27356d9:scripts/calibrate_rewrite_ai_price.py'], cwd=ROOT).decode()
        original = next(n for n in ast.parse(source).body
                        if isinstance(n, ast.FunctionDef) and n.name == 'render_comparison_views')
        namespace = dict(vars(renderer))
        exec(compile(ast.Module(body=[original], type_ignores=[]), '<original renderer>', 'exec'), namespace)
        baseline = namespace['render_comparison_views']

        def capture(function, design):
            figures = {}
            def save(fig, path, **kwargs):
                if Path(path).suffix == '.pdf':
                    figures[Path(path).name] = [dict(
                        ylim=ax.get_ylim(), xlim=ax.get_xlim(),
                        lines=[(np.asarray(line.get_xdata()), np.asarray(line.get_ydata()))
                               for line in ax.lines]) for ax in fig.axes]
            with patch.object(Figure, 'savefig', save), patch.object(renderer, 'write_json'), \
                    patch.dict(namespace, write_json=lambda *args: None):
                function(design, show_price_target=False)
            plt.close('all')
            return figures

        for chi in (7.5, 1.5):
            design = make_design(chi)
            before = capture(baseline, design)
            after = capture(renderer.render_comparison_views, design)
            self.assertEqual(before.keys(), after.keys())
            for filename in before:
                for i, (old, new) in enumerate(zip(before[filename], after[filename])):
                    with self.subTest(chi=chi, figure=filename, panel=i):
                        self.assertEqual(old['xlim'], new['xlim'])
                        changed = 'ai_distribution' in filename and i in (0, 2)
                        lines = old['lines'][:4] + old['lines'][5:] if changed else old['lines']
                        self.assertEqual(len(lines), len(new['lines']))
                        for (x, y), (nx, ny) in zip(lines, new['lines']):
                            np.testing.assert_array_equal(x, nx)
                            np.testing.assert_array_equal(y, ny)
                        if changed:
                            lo, hi = new['ylim']
                            values = np.concatenate([y for _, y in new['lines'][:4]])
                            self.assertLessEqual(lo, values.min())
                            self.assertGreaterEqual(hi, values.max())
                            self.assertLess(hi-lo, (old['ylim'][1]-old['ylim'][0])/4)
                            self.assertGreater(lo, .5) if i == 0 else self.assertLess(hi, .1)
                        else:
                            self.assertEqual(old['ylim'], new['ylim'])


if __name__ == '__main__':
    unittest.main()

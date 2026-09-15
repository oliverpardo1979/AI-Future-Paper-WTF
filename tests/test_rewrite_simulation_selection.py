"""Editorial selection preserves all data and the reproduction route."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import re
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import reproduce_rewrite_results as reproduce


def quantitative_text(full=False, legacy=False):
    main = (ROOT / 'main_rewrite.tex').read_text(encoding='utf-8')
    section = main.split(r'\input{sections_rewrite/05_uncapped_equilibria}')[1]
    section = section.split(r'\input{sections_rewrite/06_conclusion}')[0]
    flags = {'showfullpricebenchmark': full, 'showlegacysimulations': legacy}
    stack, active, output = [], True, []
    def expand(path):
        text = (ROOT / (path + '.tex')).read_text(encoding='utf-8')
        return re.sub(r'\\input\{([^}]+)\}', lambda m: expand(m[1]), text)
    for line in section.splitlines():
        line = line.strip()
        if line.startswith(r'\if'):
            stack.append((active, flags[line[3:]]))
            active = active and stack[-1][1]
        elif line == r'\else':
            active = stack[-1][0] and not stack[-1][1]
        elif line == r'\fi':
            active = stack.pop()[0]
        elif active and line.startswith(r'\input'):
            output.append(expand(re.search(r'\{([^}]+)\}', line)[1]))
    if stack:
        raise AssertionError('Unclosed editorial conditional')
    return '\n'.join(output)


class SimulationSelection(unittest.TestCase):
    def test_one_parameter_table_covers_both_calibrations(self):
        text = quantitative_text()
        self.assertEqual(text.count(r'\begin{table}'), 1)
        self.assertNotIn('rewriteParameterTable', text)
        self.assertIn('{tab:rewrite-rsi-parameters}', text)
        self.assertNotIn('{tab:rewrite-rsi-half-parameters}', text)
        self.assertNotIn('{tab:rewrite-research-share-parameters}', text)
        self.assertIn('7.616305 (central)', text)
        self.assertIn('1.4378 (slow)', text)
        self.assertLess(text.index(r'\begin{table}'),
                        text.index(r'\subsection{Central illustrative scenario}'))
        table = (ROOT/'sections_rewrite/rsi_parameters.tex').read_text(encoding='utf-8')
        self.assertNotIn(r'\input', table)
        for old in ('parameter_tables.tex', 'rsi_half_decline_parameters.tex',
                    'rsi_research_share_parameters.tex', 'rsi_activation_parameters.tex'):
            self.assertFalse((ROOT/'sections_rewrite'/old).exists())
            self.assertTrue((ROOT/'sections_rewrite/preserved'/old).exists())

    def test_unified_values_match_both_saved_calibrations(self):
        table = (ROOT/'sections_rewrite/rsi_parameters.tex').read_text(encoding='utf-8')
        rows = dict(re.findall(r'^\$([^$]+)\$ & (.*?) &', table, re.M))
        self.assertEqual(len(rows), 15)
        def rounded_value(segment, actual):
            token = re.match(r'[\d,]+(?:\.\d+)?', segment.strip())[0].replace(',', '')
            decimals = len(token.split('.')[1]) if '.' in token else 0
            self.assertLessEqual(abs(float(token)-actual), .5*10**(-decimals)+1e-10)
        mapping = {r'\alpha':'alpha', r'\delta':'depreciation', r'\rho':'discount',
                   'n':'population_growth', r'\gamma':'labor_productivity_growth',
                   r'\eta':'eta', r'\omega_X':'omega_x'}
        for index, folder in enumerate(('rsi_activation_half_decline', 'rsi_research_share_2023')):
            manifest = json.loads((ROOT/'numerical_rewrite'/folder/'paths_manifest.json').read_text())
            for symbol, field in mapping.items():
                rounded_value(rows[symbol], manifest['parameters'][field])
            rounded_value(rows[r'\omega_L'], 1-manifest['parameters']['omega_x'])
            for j, field in enumerate(('initial_labor_productivity', 'initial_population')):
                rounded_value(rows['A_0,N_0'].split(';')[j], manifest['parameters'][field])
            rounded_value(rows[r'\chi'].split(r';\newline ')[index], manifest['parameters']['chi'])
            rounded_value(rows[r'\overline B'], manifest['frontier'])
            rounded_value(rows['B_0'], manifest['initial_capability'])
            p = manifest['parameters']
            rounded_value(rows['K_0/Y_0'], p['alpha']/(p['discount']+p['labor_productivity_growth']+p['depreciation']))
            for j, sigma in enumerate((.9, 1., 1.1, 1.5)):
                rounded_value(rows[r'\sigma'].split(';')[j], sigma)
                key = 'sigma_' + f'{sigma:.2f}'.replace('.', '_')
                rounded_value(rows['K_0'].split(';')[j], manifest['initial_capital_by_sigma'][key])

    def test_default_order_and_six_retained_figures(self):
        main = (ROOT / 'main_rewrite.tex').read_text()
        self.assertIn(r'\showfullpricebenchmarkfalse', main)
        self.assertIn(r'\showlegacysimulationsfalse', main)
        text = quantitative_text()
        headings = re.findall(r'\\subsection\{([^}]+)\}', text)
        self.assertEqual(headings, [
            'Experimental design and initial conditions',
            'Central illustrative scenario',
            'Sensitivity: a slow transition',
            'Interpretation and limitations',
        ])
        figures = re.findall(r'\\includegraphics\[[^]]*\]\{([^}]+)\}', text)
        self.assertEqual(len(figures), 6)
        self.assertTrue(all('rsi_activation_half_decline_' in p for p in figures[:3]))
        self.assertTrue(all('rsi_research_share_2023_' in p for p in figures[3:]))
        self.assertTrue(all((ROOT / p).exists() for p in figures))

    def test_full_price_benchmark_can_be_reactivated(self):
        text = quantitative_text(full=True)
        self.assertEqual(text.count(r'\begin{figure}'), 9)
        for suffix in ('accumulation_growth', 'growth_returns', 'ai_distribution'):
            self.assertIn('equilibrium_rsi_activation_' + suffix + '_windows.pdf', text)
        self.assertIn(r'\label{eq:rewrite-rsi-price-target}', text)

    def test_only_chi_differs_and_reported_timing_matches_saved_data(self):
        folders = [ROOT / 'numerical_rewrite' / name for name in (
            'rsi_research_share_2023', 'rsi_activation_half_decline')]
        manifests = [json.loads((p / 'paths_manifest.json').read_text()) for p in folders]
        first, second = manifests
        self.assertEqual({k:v for k,v in first['parameters'].items() if k != 'chi'},
                         {k:v for k,v in second['parameters'].items() if k != 'chi'})
        self.assertNotEqual(first['parameters']['chi'], second['parameters']['chi'])
        for field in ('frontier', 'initial_capital_by_sigma', 'initial_capability'):
            self.assertEqual(first[field], second[field], field)
        for p, manifest in zip(folders, manifests):
            digest = hashlib.sha256((p / 'equilibrium_paths.csv').read_bytes()).hexdigest()
            self.assertEqual(digest, manifest['csv_sha256'])
        self.assertAlmostEqual(first['sigma_1_50_transition_dates']['T50'], 220.5497042, places=6)
        self.assertAlmostEqual(second['sigma_1_50_transition_dates']['T50'], 46.7960891, places=6)

    def test_default_driver_runs_only_the_two_displayed_calibrations(self):
        with patch.object(sys, 'argv', ['reproduce', '--skip-tests']), \
             patch.object(reproduce, 'run') as run, contextlib.redirect_stdout(io.StringIO()):
            reproduce.main()
        commands = [c.args[0] for c in run.call_args_list]
        calibrations = [c for c in commands if any('scripts/calibrate_' in x for x in c)]
        self.assertEqual(len(calibrations), 2)
        self.assertIn('scripts/calibrate_rewrite_research_share_central.py', calibrations[0])
        self.assertIn('scripts/calibrate_rewrite_research_share_low.py', calibrations[1])
        self.assertFalse(any('rsi_activation' in c for c in commands))

    def test_legacy_driver_retains_full_price_command(self):
        with patch.object(sys, 'argv', ['reproduce', '--skip-tests', '--include-legacy']), \
             patch.object(reproduce, 'run') as run, contextlib.redirect_stdout(io.StringIO()):
            reproduce.main()
        self.assertTrue(any(c.args[0][-1] == 'rsi_activation' for c in run.call_args_list))

    def test_central_target_is_illustrative_not_an_observed_estimate(self):
        text = quantitative_text()
        self.assertIn('not an observed estimate', text)
        self.assertIn(r'$0.183\%$', text)
        self.assertIn(r'$0.182916\%$', text)
        self.assertIn('not an additional calibration target', text)
        self.assertIn(r'$0.1544\%$', text)
        self.assertIn(r'$3.0091\%$', text)
        self.assertNotIn('Principal calibration: research expenditure', text)
        comparison = json.loads((ROOT / 'numerical_rewrite/rsi_research_share_2025/'
                                 'published_comparison.json').read_text())
        moment = comparison['rsi_activation_half_decline']['first_year']['share']
        self.assertAlmostEqual(100 * moment, .1829, places=4)
        proxy = 45.23 / 29298.013
        self.assertAlmostEqual(100 * proxy, .1544, places=4)
        self.assertAlmostEqual(10000 * (moment - proxy), 2.8536871, places=6)

    def test_appendix_and_replication_follow_display_order(self):
        appendix = (ROOT / 'sections_rewrite/appendix_rsi_activation.tex').read_text()
        self.assertLess(appendix.index('rsi_half_decline_accuracy'),
                        appendix.index('rsi_research_share_accuracy'))
        self.assertLess(appendix.index('python scripts/calibrate_rewrite_research_share_central.py'),
                        appendix.index('python scripts/calibrate_rewrite_research_share_low.py'))
        guide = (ROOT / 'REPLICATION.md').read_text()
        self.assertLess(guide.index('## Central illustrative scenario'),
                        guide.index('## Slow-transition sensitivity'))


if __name__ == '__main__':
    unittest.main()

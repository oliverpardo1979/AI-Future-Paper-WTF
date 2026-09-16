"""Read-only checks for the September 16 figure-by-figure editorial revision.

No equilibrium is recomputed. Existing admission records, source hashes,
reported numbers, analytical limits and preservation of figures are checked.
Run from any directory: python scripts/check_rewrite_rsi_exposition.py
"""
import csv
import re
import subprocess

from report_rewrite_illustrative_rsi import ROOT, KEYS, admitted_data

BASE = '76b3062'


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT).decode('utf-8')


def check():
    high, low = [admitted_data(n) for n in ('rsi_chi_7_5', 'rsi_chi_1_5')]
    texts = []
    for file, prefix in [('12_rsi_high_productivity.tex', 'rsi-half'),
                         ('13_rsi_low_productivity.tex', 'rsi-research')]:
        path = 'sections_rewrite/' + file
        text = (ROOT/path).read_text(encoding='utf-8')
        old = git('show', BASE + ':' + path)
        pattern = r'\\begin\{figure\}.*?\\end\{figure\}'
        figures = re.findall(pattern, text, re.S)
        assert len(figures) == 3
        assert figures == re.findall(pattern, old, re.S), 'A figure or caption changed'
        previous_end = 0
        for figure, suffix in zip(figures, ('accumulation', 'prices', 'distribution')):
            start = text.index(figure)
            label = 'fig:rewrite-' + prefix + '-' + suffix
            before = text[previous_end:start]
            assert r'\ref{' + label + '}' in before
            assert 'upper' in before and 'lower' in before
            previous_end = start + len(figure)
        percentages = re.findall(r'(\d+(?:\.\d+)?)\\%', text)
        assert all(re.fullmatch(r'\d+\.\d', value) for value in percentages), percentages
        texts.append(text)

    for d in (high, low):
        spec = d['spec']
        assert spec['empirical_target'] is None
        gamma = spec['parameters']['labor_productivity_growth']
        for key in KEYS:
            s = d['summary']['scenarios'][key]['snapshots']
            start = s['0.0']
            pre = d['figures']['pre_event_bgp'][key]
            assert start['capital_effective_labor_growth'] < 0
            assert start['consumption_effective_labor'] > pre['consumption']
            assert abs(start['net_interest'] - 0.05) < 1e-12
            for row in s.values():
                assert abs(row['output_per_person_growth'] -
                           row['output_effective_labor_growth'] - gamma) < 1e-12
                assert abs(sum(row[f] for f in ('labor_income_share',
                    'profit_output_share', 'inference_output_share',
                    'research_output_share')) + spec['parameters']['alpha'] - 1) < 1e-10

    with (high['folder']/'equilibrium_paths.csv').open(newline='') as source:
        assert all(float(row['profit_output_share']) > 0 for row in csv.DictReader(source))

    # Figure-derived percentages explicitly used in the revised narrative.
    expected = [
        (high, 'sigma_0_90', '0.0', 'output_effective_labor_growth', '0.6'),
        (high, 'sigma_1_50', '0.0', 'ai_services_effective_labor_growth', '80.8'),
        (high, 'sigma_1_50', '0.0', 'output_effective_labor_growth', '3.5'),
        (high, 'sigma_1_50', '0.0', 'research_output_share', '3.1'),
        (high, 'sigma_1_50', '0.0', 'profit_output_share', '0.2'),
        (high, 'sigma_1_50', '10.0', 'labor_income_share', '53.0'),
        (high, 'sigma_1_50', '10.0', 'net_interest', '7.8'),
        (high, 'sigma_1_50', '500.0', 'output_effective_labor_growth', '2.2'),
        (high, 'sigma_1_50', '500.0', 'wage_growth', '2.5'),
        (high, 'sigma_1_50', '500.0', 'net_interest', '7.2'),
        (high, 'sigma_1_50', '500.0', 'labor_income_share', '0.2'),
        (low, 'sigma_0_90', '0.0', 'output_effective_labor_growth', '0.1'),
        (low, 'sigma_1_50', '0.0', 'output_effective_labor_growth', '0.5'),
        (low, 'sigma_1_50', '0.0', 'ai_services_effective_labor_growth', '11.6'),
        (low, 'sigma_1_50', '0.0', 'research_output_share', '0.6'),
        (low, 'sigma_1_50', '0.0', 'profit_output_share', '2.7'),
        (low, 'sigma_1_50', '0.0', 'labor_income_share', '61.9'),
        (low, 'sigma_1_50', '10.0', 'labor_income_share', '60.1'),
        (low, 'sigma_1_50', '10.0', 'net_interest', '5.5'),
        (low, 'sigma_1_50', '500.0', 'output_effective_labor_growth', '3.2'),
        (low, 'sigma_1_50', '500.0', 'output_per_person_growth', '4.2'),
        (low, 'sigma_1_50', '500.0', 'wage_growth', '3.1'),
        (low, 'sigma_1_50', '500.0', 'net_interest', '8.2'),
        (low, 'sigma_1_50', '500.0', 'labor_income_share', '2.3'),
    ]
    combined = '\n'.join(texts)
    for d, key, time, field, value in expected:
        actual = d['summary']['scenarios'][key]['snapshots'][time][field]
        assert f'{100*actual:.1f}' == value, (field, actual, value)
        assert value + r'\%' in combined, value
    for d, annual, price, halfway in [(high, '0.2', '39.6', '47'),
                                     (low, '0.1', '9.4', '213')]:
        assert f"{100*d['annual']['scenarios']['sigma_1_00']['first_year']['share']:.1f}" == annual
        assert f"{100*(1-d['summary']['scenarios']['sigma_1_00']['target_window_price_ratio']):.1f}" == price
        assert f"{d['summary']['sigma_1_50_transition_dates']['T50']:.0f}" == halfway

    assert high['figures']['analytical_limits'] == low['figures']['analytical_limits']
    limits = high['figures']['analytical_limits']['sigma_1_50']
    for field, value in [('output_effective_labor_growth', '2.1'),
                         ('wage_growth', '2.4'), ('net_interest', '7.1'),
                         ('inference_output_share', '44.9'),
                         ('profit_output_share', '22.1')]:
        assert f'{100*limits[field]:.1f}' == value
    assert limits['labor_income_share'] == limits['research_output_share'] == 0
    assert f"{limits['ai_service_price']:.5f}" == '0.00110'
    hp = dict(high['spec']['parameters']); lp = dict(low['spec']['parameters'])
    assert hp.pop('chi') == 7.5 and lp.pop('chi') == 1.5 and hp == lp
    for field in ('frontier', 'initial_capability', 'initial_stocks_by_sigma'):
        assert high['spec'][field] == low['spec'][field]

    protected = ['main_rewrite.tex', 'references.bib', 'sections_rewrite/03_model.tex',
        'sections_rewrite/04_equilibrium_regimes.tex', 'sections_rewrite/08_rsi_design.tex',
        'numerical_rewrite', 'figures_rewrite',
        'sections_rewrite/rsi_chi_7_5_results.tex',
        'sections_rewrite/rsi_chi_1_5_results.tex',
        'scripts/report_rewrite_illustrative_rsi.py',
        'scripts/simulate_rewrite_illustrative_rsi.py']
    assert not git('diff', BASE, '--name-only', '--', *protected).strip()
    table = 'sections_rewrite/rsi_parameters.tex'
    assert (ROOT/table).read_text(encoding='utf-8') == git('show', BASE+':'+table).replace('\\fi\n', '')
    print(f'PASS: {len(expected)} snapshot values, annual outcomes, dates, limits,')
    print('all 8 existing admission records and hashes; 6 unchanged figure blocks;')
    print('unchanged simulation inputs, data, figures, model and generated digests.')


if __name__ == '__main__':
    check()

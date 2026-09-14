"""Audit initial K/Y against saved paths and PWT; never solve a dynamic BVP.

Run with --pwt PATH to regenerate the frozen PWT extract from the official
PWT 11.0 Stata download. Without that option, use the checked-in extract.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / '.python-packages'), str(ROOT / 'scripts')]
from define_positive_ai_branch import PositiveAIBenchmarkParameters
from solve_near_unit_ai_bvp import solve_monopoly_static_block

DATA = ROOT / 'empirical/capital_output'
OUTPUT = ROOT / 'numerical_rewrite/initial_capital_output_audit.json'
SIGMAS = (.9, 1., 1.1, 1.5)
DIRECTORIES = ('', 'ramsey_start', 'price_calibrated',
               'price_calibrated_low_ai_high_cap', 'near_terminal',
               'slow_transition')
YEARS = (2019, 2021, 2023)
FIELDS = ('countrycode', 'country', 'year', 'cn', 'cgdpo', 'pl_n', 'pl_gdpo')
SOURCE_URL = 'https://dataverse.nl/api/access/datafile/554030'


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def csv_sha256(path):
    """Normalize line endings so source checks survive Git on Windows/Linux."""
    return hashlib.sha256(path.read_bytes().replace(b'\r\n', b'\n')).hexdigest()


def extract_pwt(path):
    import pandas as pd
    with pd.io.stata.StataReader(path) as reader:
        labels = reader.variable_labels()
        frame = reader.read(convert_categoricals=False)
    assert 'Capital stock at current PPPs' in labels['cn']
    assert 'Capital services' in labels['ck']
    assert 'Output-side real GDP at current PPPs' in labels['cgdpo']
    assert not frame.duplicated(['countrycode', 'year']).any()
    selected = frame.loc[frame.year.isin(YEARS), list(FIELDS)].copy()
    # Promote before arithmetic: the original Stata variables include float32.
    selected[['cn', 'cgdpo', 'pl_n', 'pl_gdpo']] = selected[
        ['cn', 'cgdpo', 'pl_n', 'pl_gdpo']].astype('float64')
    selected.sort_values(['year', 'countrycode']).to_csv(
        DATA / 'pwt110_capital_output_extract.csv', index=False)
    metadata = {
        'title': 'Penn World Table 11.0', 'doi': '10.34894/FABVLR',
        'download_url': SOURCE_URL, 'retrieved': '2026-09-14',
        'raw_file_sha256': sha256(path),
        'license': 'CC BY 4.0', 'rows_full_dataset': len(frame),
        'years_extracted': YEARS, 'rows_extracted': len(selected),
        'source_variable_labels': {key: labels[key] for key in (*FIELDS, 'ck')},
        'attribution': 'Feenstra, Inklaar and Timmer (2015), AER 105(10), 3150-3182',
    }
    (DATA / 'source.json').write_text(json.dumps(metadata, indent=2) + '\n')


def empirical_comparison():
    import pandas as pd
    file = DATA / 'pwt110_capital_output_extract.csv'
    frame = pd.read_csv(file)
    assert not frame.duplicated(['countrycode', 'year']).any()
    result = []
    for year in YEARS:
        all_rows = frame.loc[frame.year.eq(year)].copy()
        values = all_rows[['cn', 'cgdpo', 'pl_n', 'pl_gdpo']]
        valid = values.notna().all(axis=1) & values.gt(0).all(axis=1)
        sample = all_rows.loc[valid].copy()
        assert len(all_rows) == 185 and len(sample) == 180
        sample['capital_current_usd'] = sample.cn * sample.pl_n
        sample['output_current_usd'] = sample.cgdpo * sample.pl_gdpo
        usa = sample.loc[sample.countrycode.eq('USA')].iloc[0]
        result.append({
            'year': year, 'countries_available': len(all_rows),
            'countries_used': len(sample),
            'excluded_missing': sorted(all_rows.loc[~valid, 'countrycode']),
            'share_of_available_pwt_ppp_output': float(sample.cgdpo.sum()/all_rows.cgdpo.sum()),
            'sum_capital_current_usd_millions': float(sample.capital_current_usd.sum()),
            'sum_output_current_usd_millions': float(sample.output_current_usd.sum()),
            'sample_current_price_ratio': float(sample.capital_current_usd.sum()/sample.output_current_usd.sum()),
            'sample_ppp_ratio': float(sample.cn.sum()/sample.cgdpo.sum()),
            'usa_current_price_ratio': float(usa.capital_current_usd/usa.output_current_usd),
            'usa_ppp_ratio': float(usa.cn/usa.cgdpo),
        })
    return {'source_extract_sha256': csv_sha256(file), 'observations': result}


def initial_static(audit, sigma):
    p = PositiveAIBenchmarkParameters(**audit['parameters'])
    capital = audit['initial_capital']
    block = solve_monopoly_static_block(
        math.log(capital), math.log(audit['initial_capability']),
        math.log(p.initial_labor_productivity*p.initial_population), sigma, p)
    output = math.exp(block.log_output)
    return capital/output, output, p.alpha*output/capital-p.depreciation


def simulation_comparison():
    rows = []
    for directory in DIRECTORIES:
        folder = ROOT / 'numerical_rewrite' / directory
        csv_file = folder / 'equilibrium_paths.csv'
        with csv_file.open() as stream:
            initial = [r for r in csv.DictReader(stream) if float(r['time']) == 0]
        assert len(initial) == 4
        by_sigma = {float(r['sigma']): r for r in initial}
        assert set(by_sigma) == set(SIGMAS)
        for sigma in SIGMAS:
            audit_path = folder / ('sigma_'+f'{sigma:.2f}'.replace('.', '_')+'_audit.json')
            audit = json.loads(audit_path.read_text())
            assert audit['equilibrium_certified']
            ratio, output, interest = initial_static(audit, sigma)
            saved = by_sigma[sigma]
            saved_ratio = float(saved['capital_effective_labor'])/float(saved['output_effective_labor'])
            interest_ratio = audit['parameters']['alpha']/(float(saved['net_interest'])+audit['parameters']['depreciation'])
            # Only verifies stored numbers; 1e-9 allows CSV rounding and root arithmetic.
            assert math.isclose(ratio, saved_ratio, rel_tol=1e-9)
            assert math.isclose(ratio, interest_ratio, rel_tol=1e-9)
            p = audit['parameters']
            pre_ratio = p['alpha']/(p['discount']+p['labor_productivity_growth']+p['depreciation'])
            pre_output = audit['initial_capital']**p['alpha'] * (
                p['initial_labor_productivity']*p['initial_population'])**(1-p['alpha'])
            rows.append({
                'scenario': directory or 'main', 'sigma': sigma,
                'K0': audit['initial_capital'], 'B0': audit['initial_capability'],
                'Y0': output, 'K0_Y0_years': ratio, 'r0': interest,
                'saved_csv_ratio': saved_ratio, 'return_identity_ratio': interest_ratio,
                'no_ai_steady_state_ratio_years': pre_ratio,
                'output_change_from_no_ai_same_stocks': output/pre_output-1,
                'audit_file': audit_path.relative_to(ROOT).as_posix(),
                'path_file': csv_file.relative_to(ROOT).as_posix(),
                'path_sha256': csv_sha256(csv_file),
            })
    distant_path = ROOT / 'numerical_rewrite/initial_financing_sensitivity.json'
    distant = json.loads(distant_path.read_text())
    ratio, output, interest = initial_static(distant, distant['sigma'])
    slow = next(row for row in rows if row['scenario']=='slow_transition' and row['sigma']==1.5)
    # chi differs but is absent from the dated production/pricing block.
    assert math.isclose(ratio, slow['K0_Y0_years'], rel_tol=1e-9)
    rows.append({'scenario': 'initial_financing_distant', 'sigma': 1.5,
                 'K0': distant['initial_capital'], 'B0': distant['initial_capability'],
                 'Y0': output, 'K0_Y0_years': ratio, 'r0': interest,
                 'audit_file': distant_path.relative_to(ROOT).as_posix()})
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pwt', type=Path)
    args = parser.parse_args()
    if args.pwt:
        extract_pwt(args.pwt)
    result = {
        'model_units': 'years; date-zero stock divided by instantaneous output at an annual rate',
        'csv_hash_convention': 'SHA256 with CRLF normalized to LF; raw Stata hash is byte-for-byte',
        'pwt_current_price_formula': 'sum(cn*pl_n)/sum(cgdpo*pl_gdpo)',
        'pwt_ppp_formula': 'sum(cn)/sum(cgdpo)',
        'empirical': empirical_comparison(), 'simulations': simulation_comparison(),
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result['empirical'], indent=2))
    for row in result['simulations']:
        print(row['scenario'], row['sigma'], f"K0/Y0 = {row['K0_Y0_years']:.6f}")


if __name__ == '__main__':
    main()

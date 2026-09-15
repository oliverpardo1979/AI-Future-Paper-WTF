"""Reproduce the central illustrative first-year M/Y target of 0.183%.

Retain the previously price-calibrated chi: it already matches the new target
at its quoted precision. The historical price record remains unchanged. No
claim of independent empirical identification or exact root matching is made.
--verify-existing recomputes the annual moments from hash-checked, admitted
checkpoints; the default also runs the existing solves and equilibrium audits.
"""
import argparse
from dataclasses import replace
import hashlib
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'.python-packages'), str(ROOT/'scripts')]
from calibrate_rewrite_ai_price import calibrated_design, finish, log_price_ratio, write_json
from calibrate_rewrite_research_share import checked_moment
from simulate_rewrite_finite_frontier import SIGMAS, key, load_solution, run, validate_solution_design

TARGET_SHARE = 0.00183
# Half of 0.001 percentage points: precision of the author's 0.183% target.
TARGET_TOLERANCE = 0.000005
RECORD = 'research_share_target.json'


def make_design():
    return replace(calibrated_design('rsi_activation_half_decline'),
        initial_stock_reference='Existing-AI fixed-B pre-RSI BGP at each elasticity; '
        'K0/Y0=3.30 and B0=0.01 Bbar. Chi retained from the historical price '
        'calibration to approximate an illustrative first-year M/Y target of '
        '0.183% at sigma=1; fixed across the other three elasticities.')


def validate_target(solution):
    moment = checked_moment(solution)
    error = moment['share'] - TARGET_SHARE
    if abs(error) >= TARGET_TOLERANCE:
        raise RuntimeError('Research target no longer matched at quoted precision; review chi.')
    return dict(matched_share=moment['share'], error_basis_points=1e4*error)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evaluate(design):
    """Read-only audit of the selected moment and its numerical provenance."""
    out, cache = design.output_directory, design.cache_directory
    paths = json.loads((out/'paths_manifest.json').read_text())
    figures = json.loads((out/'figure_manifest.json').read_text())
    event = json.loads((out/'activation_audit.json').read_text())
    csv_hash = digest(out/'equilibrium_paths.csv')
    if not (event['passes'] and figures['all_scenarios_admitted']
            and paths['csv_sha256'] == figures['data_sha256'] == csv_hash
            and figures['activation_audit_sha256'] == digest(out/'activation_audit.json')):
        raise RuntimeError('Unverified or changed export; rerun the equilibrium audit.')
    moments = {}
    for sigma in SIGMAS:
        name = key(sigma)
        audit = json.loads((out/f'{name}_audit.json').read_text())
        checkpoint = cache/audit['checkpoint_filename']
        if not (audit['equilibrium_certified'] and audit['early_window_checks']['passes']
                and audit['checkpoint_sha256'] == paths['checkpoint_sha256'][name]
                == digest(checkpoint)):
            raise RuntimeError(f'Unverified equilibrium checkpoint for {name}.')
        stages = {}
        for stage in ('base', 'refined', 'long'):
            sol = load_solution(cache/f'{name}_{stage}.npz')
            validate_solution_design(sol, design, sigma)
            stages[stage] = checked_moment(sol)
        gap = max(abs(math.log(stages[a]['share']/stages[b]['share']))
                  for a, b in (('base', 'refined'), ('refined', 'long'), ('base', 'long')))
        if gap >= 2e-5:
            raise RuntimeError(f'Annual research share is horizon-sensitive for {name}.')
        moments[name] = dict(first_year=stages['long'], second_year=checked_moment(sol, 1.),
            horizon_stages=stages, maximum_horizon_log_change=gap,
            checkpoint_sha256=digest(checkpoint),
            implied_price_ratio_27_months=math.exp(log_price_ratio(sol)))
        if sigma == 1.:
            matched = validate_target(sol)
    return dict(status='numerically_admitted_approximate_calibration',
        target_share=TARGET_SHARE, target_years=1., calibration_sigma=1.,
        target_definition='Integral of M over the first year divided by integral of Y.',
        target_is_observed=False, target_exactly_matched=False,
        selection='Author-selected illustrative target; retain the historical chi '
                  'because its achieved annual ratio rounds to 0.183%.',
        chi=design.parameters.chi, chi_held_fixed_across_sigmas=True,
        target_tolerance_basis_points=1e4*TARGET_TOLERANCE,
        numerical_tolerances_unchanged=True, price_is_current_target=False,
        historical_price_calibration_sha256=digest(out/'calibration.json'),
        csv_sha256=csv_hash, scenarios=moments, **matched)


def publish(verify_existing=False):
    design = make_design()
    if not verify_existing:
        for sigma in SIGMAS:
            run(sigma, design)
        write_json(design.output_directory/RECORD,
                   dict(status='awaiting_equilibrium_checks', chi=design.parameters.chi))
        finish(design, calibration_validator=validate_target,
               calibration_filename=RECORD, retain_price_outcome_marker=True)
    payload = evaluate(design)
    write_json(design.output_directory/RECORD, payload)
    path = design.output_directory/'figure_manifest.json'
    manifest = json.loads(path.read_text())
    if manifest.get('price_target') is not None:
        manifest['price_outcome_marker'] = manifest['price_target']
    manifest['price_target'] = None
    manifest['active_calibration_record'] = RECORD
    write_json(path, manifest)
    print(json.dumps({k: payload[k] for k in ('status', 'chi', 'target_share',
        'matched_share', 'error_basis_points', 'target_tolerance_basis_points')}, indent=2))
    return payload


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify-existing', action='store_true')
    publish(parser.parse_args().verify_existing)

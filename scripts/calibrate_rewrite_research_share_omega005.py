"""Standalone omega_X=0.05 experiment; does not edit the manuscript.

Retain the paper's cap RULE (1.1 times the sigma=1.5 threshold), B0/Bbar=1%,
pre-RSI fixed-efficiency BGP at each sigma, and every equilibrium admission
gate. Match integral M / integral Y over year one to 0.0664% at sigma=1.
The four-regime figures are exported by the existing paper renderer only
after all four trajectories pass its existing checks.

After installing requirements-rewrite.txt, run from the repository root:
  python scripts/calibrate_rewrite_research_share_omega005.py
The saved calibration is reused. To refit it explicitly, use --calibrate;
--sigma 0.9 (or 1, 1.1, 1.5) solves an individual case; --finish reaudits
and renders all cases. Numerical checkpoints remain in tmp/; committed
CSV, audit JSON and figures retain hashes linking the displayed results.
This experiment was developed from base commit 05ff8c2, with the associated
marginal-revenue precision fix. Use this script's repository revision,
not the base commit alone, to reproduce it.
"""
from dataclasses import asdict, replace
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / '.python-packages'), str(ROOT / 'scripts')]
import numpy as np
from scipy.optimize import brentq
from analyze_axm_finite_cap_bvp import critical_capability_frontier, terminal_point
from calibrate_rewrite_ai_price import make_design as price_design, finish, write_json
from calibrate_rewrite_research_share import checked_moment, TARGET_LOG_TOLERANCE
from calibrate_rewrite_research_share_low import SOURCE
from simulate_rewrite_finite_frontier import (
    SIGMAS, PARAMETERS, key, design_initial_stocks, fixed_efficiency_bgp,
    load_solution, save_solution, validate_solution_design, run,
)
from solve_axm_global_finite_cap_bvp import solve_global_finite_cap_bvp

NAME = 'rsi_research_share_omega005'
TARGET_SHARE = 0.000664
OUTPUT = ROOT / 'numerical_rewrite' / NAME
RECORD = OUTPUT / 'calibration.json'


def make_design(chi):
    p = replace(PARAMETERS, omega_x=0.05, chi=float(chi))
    cap = 1.1 * critical_capability_frontier(1.5, p)
    return replace(price_design(chi, 'rsi_activation'), name=NAME, parameters=p,
        frontier=cap, initial_capability=0.01 * cap,
        output_directory=OUTPUT, cache_directory=ROOT/'tmp'/f'rewrite_bvp_{NAME}',
        initial_stock_reference=(
            'Existing AI with omega_X=0.05 before and after unexpected RSI activation. '
            'Bbar=1.10 times the sigma=1.50 threshold, B0/Bbar=0.01. '
            'Each sigma inherits its own fixed-B pre-RSI BGP capital with K0/Y0=3.30. '
            'Chi matches integral_0^1 M / integral_0^1 Y = 0.000664 at sigma=1 '
            'and is held fixed across the four elasticities. No manuscript edits.'))


def calibrate():
    path = OUTPUT / 'calibration_trials.json'
    trials = json.loads(path.read_text()) if path.exists() else []

    def objective(log_chi):
        chi = math.exp(float(log_chi))
        for row in trials:
            if math.isclose(chi, row['chi'], rel_tol=8*np.finfo(float).eps, abs_tol=0):
                chi = row['chi']
                break
        design = make_design(chi)
        tag = hashlib.sha256(float(chi).hex().encode()).hexdigest()[:16]
        checkpoint = design.cache_directory/'calibration_trials'/f'chi_{tag}.npz'
        print(f'Calibration trial: chi={chi:.10g}', flush=True)
        if checkpoint.exists():
            sol = load_solution(checkpoint)
        else:
            k0, b0 = design_initial_stocks(design, 1.)
            sol = solve_global_finite_cap_bvp(
                terminal_point(1., design.frontier, design.parameters),
                design.parameters, k0, b0, continuation_steps=32, nodes=221,
                tolerance=2e-7, boundary_tolerance=1e-10, maximum_nodes=40000)
            save_solution(sol, checkpoint)
        validate_solution_design(sol, design, 1.)
        moment = checked_moment(sol)
        residual = math.log(moment['share']/TARGET_SHARE)
        row = dict(chi=chi, annual_research_share=moment['share'],
            log_target_residual=residual, quadrature_log_gap=moment['quadrature_log_gap'],
            checkpoint=checkpoint.relative_to(ROOT).as_posix(),
            checkpoint_sha256=hashlib.sha256(checkpoint.read_bytes()).hexdigest(),
            maximum_rms_residual=float(np.max(sol.raw.rms_residuals)), horizon=sol.horizon)
        trials[:] = [t for t in trials if t['chi'] != chi]
        trials.append(row)
        write_json(path, trials)
        print(f'chi={chi:.10g}: first-year M/Y={100*moment["share"]:.9g}%', flush=True)
        return residual

    # This geometric search is a numerical bracket, not a parameter restriction.
    # Start below the old low-chi calibration, then take the first ascending
    # crossing. Do not assert uniqueness over every positive research productivity.
    low = math.log(PARAMETERS.chi/8)
    fl = objective(low)
    for _ in range(12):
        if fl < 0:
            break
        low -= math.log(2)
        fl = objective(low)
    else:
        raise RuntimeError('No lower search endpoint below the target; no figures exported.')
    high = low + math.log(2)
    for _ in range(14):
        fh = objective(high)
        if fh >= 0:
            break
        if fh <= fl:
            raise RuntimeError('Research share turned down before reaching target; inspect feasibility.')
        low, fl = high, fh
        high += math.log(2)
    else:
        raise RuntimeError('Target not bracketed; no figures exported.')
    root = brentq(objective, low, high, xtol=2e-6, rtol=1e-10)
    residual = objective(root)
    if abs(residual) >= TARGET_LOG_TOLERANCE:
        raise RuntimeError('Calibration mismatch exceeds the existing research-target tolerance.')
    selected = min(trials, key=lambda r: abs(r['log_target_residual']))
    design = make_design(selected['chi'])
    sol = load_solution(ROOT/selected['checkpoint'])
    validate_solution_design(sol, design, 1.)
    save_solution(sol, design.cache_directory/f'{key(1.)}_base.npz')
    write_json(RECORD, dict(status='awaiting_equilibrium_checks', chi=design.parameters.chi,
        target_share=TARGET_SHARE, calibration_sigma=1., target_years=1.,
        target_definition='Integral of M over year one divided by integral of Y over year one.',
        source=SOURCE, rounded_source_ratio=18.46/27811.517,
        target_interpretation='User-requested rounded 2023 US proxy, not measured autonomous RSI.',
        selection='First ascending target crossing in the documented low-chi search.',
        root_log_chi_tolerance=2e-6, target_log_tolerance=TARGET_LOG_TOLERANCE,
        parameters=asdict(design.parameters), frontier=design.frontier,
        frontier_rule='1.1 * threshold(sigma=1.5, omega_X=0.05)',
        initial_capability=design.initial_capability,
        initial_stocks_by_sigma={key(s):list(design_initial_stocks(design,s)) for s in SIGMAS},
        source_code_base_commit='05ff8c2', trial=selected, document_modified=False))
    return design


def current_design():
    if not RECORD.exists():
        return calibrate()
    return make_design(json.loads(RECORD.read_text())['chi'])


def finish_experiment(design):
    def validate_moment(unit):
        moments = {}
        for sigma in SIGMAS:
            stages = {}
            for suffix in ('base','refined','long'):
                sol = load_solution(design.cache_directory/f'{key(sigma)}_{suffix}.npz')
                validate_solution_design(sol, design, sigma)
                stages[suffix] = checked_moment(sol)
            gap = max(abs(math.log(v['share']/stages['long']['share'])) for v in stages.values())
            if gap >= TARGET_LOG_TOLERANCE:
                raise RuntimeError(f'Annual research moment remains horizon-sensitive for sigma={sigma}.')
            sol = load_solution(design.cache_directory/f'{key(sigma)}_long.npz')
            moments[key(sigma)] = dict(first_year=stages['long'], second_year=checked_moment(sol,1.),
                horizon_stages=stages, maximum_horizon_log_change=gap)
        first = checked_moment(unit)
        if abs(math.log(first['share']/TARGET_SHARE)) >= TARGET_LOG_TOLERANCE:
            raise RuntimeError('Refined target changed; recalibration needed.')
        write_json(OUTPUT/'annual_moments.json', dict(target_share=TARGET_SHARE,
            target_sigma=1., scenarios=moments))
        return dict(matched_share=first['share'], error_basis_points=1e4*(first['share']-TARGET_SHARE),
            moment_log_change_after_two_horizon_extensions=moments[key(1.)]['maximum_horizon_log_change'])
    finish(design, calibration_validator=validate_moment)
    print(json.dumps(json.loads(RECORD.read_text()), indent=2), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--calibrate', action='store_true')
    parser.add_argument('--sigma', type=float, choices=SIGMAS)
    parser.add_argument('--finish', action='store_true')
    args = parser.parse_args()
    if args.calibrate:
        calibrate()
    elif args.sigma is not None:
        run(args.sigma, current_design())
    elif args.finish:
        finish_experiment(current_design())
    else:
        d = current_design()
        for s in SIGMAS:
            run(s, d)
        finish_experiment(d)

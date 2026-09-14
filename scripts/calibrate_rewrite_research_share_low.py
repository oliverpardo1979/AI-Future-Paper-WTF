"""Publish the low (2023 US) research-share calibration using the existing BVP.

The author permits an approximate empirical match. Select the nearest already
explored candidate on the increasing low-chi branch; retain every original
equilibrium and stability gate. The high-target results remain untouched.
"""
from dataclasses import asdict, replace
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'.python-packages'),str(ROOT/'scripts')]
from calibrate_rewrite_research_share import checked_moment, SOURCE as HIGH_SOURCE
from calibrate_rewrite_ai_price import (
    make_design as price_design, write_json, log_price_ratio,
    finish as finish_comparison,
)
from simulate_rewrite_finite_frontier import (
    key, design_initial_stocks, load_solution, save_solution,
    validate_solution_design, run,
    SIGMAS,
)
from analyze_axm_finite_cap_bvp import terminal_point
from solve_axm_global_finite_cap_bvp import solve_global_finite_cap_bvp

NAME='rsi_research_share_2023'
TARGET_SHARE=18.46/27811.517
SOURCE=dict(HIGH_SOURCE,year=2023,research_compute_billion_usd=18.46,
    nominal_gdp_billion_usd=27811.517,
    limitations=HIGH_SOURCE['limitations'][:-1]+[
        'The 2023 value is the lowest dated proxy previously discussed, not a lower confidence bound.',
        'The ratio does not measure the current level of research spending.'])


def select_candidate():
    """A finite, archived candidate set; no new identification claim."""
    path=ROOT/'numerical_rewrite/rsi_research_share_2025/feasibility_diagnostic.json'
    diagnostic=json.loads(path.read_text())
    candidates=[r for r in diagnostic['trials'] if r['chi']<=diagnostic['local_peak_chi']]
    row=min(candidates,key=lambda r:abs(r['annual_research_share']-TARGET_SHARE))
    return row,hashlib.sha256(path.read_bytes()).hexdigest()


def make_design(chi):
    return replace(price_design(chi,'rsi_activation'),name=NAME,sigmas=SIGMAS,
        output_directory=ROOT/'numerical_rewrite'/NAME,
        cache_directory=ROOT/'tmp'/f'rewrite_bvp_{NAME}',
        initial_stock_reference='Existing-AI fixed-B pre-RSI BGP for each elasticity; '
            'K0/Y0=3.30 and B0=0.01 Bbar. RSI becomes available unexpectedly. '
            'Only K0 and B0 are inherited; C0, q0 and M0 are endogenous. '
            'Chi approximates the annual 2023 US research-compute/GDP proxy at sigma=1 '
            'and is held fixed for sigma=0.90, 1.10 and 1.50.')


def prepare_unit(design, row):
    """Preserve the already verified unit-elastic calibration checkpoint."""
    cache=design.cache_directory
    base_path=cache/f'{key(1.)}_base.npz'
    if not base_path.exists():
        archived=ROOT/row['checkpoint'].replace('\\','/')
        if archived.exists():
            if hashlib.sha256(archived.read_bytes()).hexdigest()!=row['checkpoint_sha256']:
                raise ValueError('Archived candidate has changed since the search.')
            base=load_solution(archived)
        else:
            k0,b0=design_initial_stocks(design,1.)
            base=solve_global_finite_cap_bvp(terminal_point(1.,design.frontier,design.parameters),
                design.parameters,k0,b0,continuation_steps=32,nodes=221,
                tolerance=2e-7,boundary_tolerance=1e-10,maximum_nodes=40000)
        validate_solution_design(base,design,1.)
        save_solution(base,base_path)
    base=load_solution(base_path)
    validate_solution_design(base,design,1.)
    return base


def publish():
    row,selection_hash=select_candidate()
    design=make_design(row['chi'])
    output,cache=design.output_directory,design.cache_directory
    base=prepare_unit(design,row)
    original_moment=checked_moment(base)
    for sigma in SIGMAS:
        run(sigma,design)

    moments={}
    def validate_moment(solution):
        first=checked_moment(solution)
        change=abs(math.log(first['share']/original_moment['share']))
        if change>=2e-5:
            raise RuntimeError('Annual research share is not stable across horizon extensions.')
        if abs(first['share']-TARGET_SHARE)>1e-4:
            raise RuntimeError('Candidate is no longer within one basis point of the target.')
        for sigma in SIGMAS:
            sol=load_solution(cache/f'{key(sigma)}_long.npz')
            one,two=checked_moment(sol),checked_moment(sol,1.)
            initial=checked_moment(load_solution(cache/f'{key(sigma)}_base.npz'))
            delta=abs(math.log(one['share']/initial['share']))
            if delta>=2e-5:
                raise RuntimeError(f'Annual moment is not stable for sigma={sigma}.')
            moments[key(sigma)]=dict(first_year=one,second_year=two,
                annual_share_growth=two['share']/one['share']-1,
                moment_log_change_after_two_horizon_extensions=delta,
                untargeted_price_ratio_27_months=math.exp(log_price_ratio(sol)))
        return dict(refined_matched_share=first['share'],
                    moment_log_change_after_two_horizon_extensions=change)

    # The existing four-regime pipeline checks original equations, both TVCs,
    # horizon stability and global developer support before exporting figures.
    # No price-target check is used: prices are untargeted in this exercise.
    calibration_path=output/'calibration.json'
    if not calibration_path.exists():
        write_json(calibration_path,dict(status='awaiting_equilibrium_checks',chi=row['chi']))
    finish_comparison(design,calibration_validator=validate_moment)
    checkpoint=cache/f'{key(1.)}_long.npz'
    solution=load_solution(checkpoint)
    first,second=checked_moment(solution),checked_moment(solution,1.)
    moment_change=abs(math.log(first['share']/original_moment['share']))
    report=json.loads((output/f'{key(1.)}_audit.json').read_text())
    report['settings']['base_tolerance']=2e-7
    write_json(output/f'{key(1.)}_audit.json',report)
    write_json(output/'annual_moments.json',dict(target_share=TARGET_SHARE,
        target_sigma=1.,scenarios=moments,
        csv_sha256=hashlib.sha256((output/'equilibrium_paths.csv').read_bytes()).hexdigest()))
    manifest=json.loads((output/'figure_manifest.json').read_text())
    figure_hashes={}
    for view in manifest['two_window_views']:
        for ext in ('pdf','png'):
            path=ROOT/'figures_rewrite'/f'{view["filename"]}.{ext}'
            figure_hashes[path.relative_to(ROOT).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
    payload=dict(status='numerically_admitted_approximate_calibration',sigmas=list(SIGMAS),
        calibration_sigma=1.,chi_held_fixed_across_sigmas=True,
        initial_stocks_by_sigma={key(s):list(design_initial_stocks(design,s)) for s in SIGMAS},
        parameters=asdict(design.parameters),chi=design.parameters.chi,
        frontier=design.frontier,initial_stocks=list(design_initial_stocks(design,1.)),
        source=SOURCE,target_share=TARGET_SHARE,target_years=1.,first_year=first,
        second_year=second,matched_share=first['share'],
        target_exactly_matched=False,empirical_tolerance_basis_points=1.,
        error_basis_points=1e4*(first['share']-TARGET_SHARE),
        relative_shortfall=1-first['share']/TARGET_SHARE,
        numerical_tolerances_unchanged=True,
        moment_log_change_after_two_horizon_extensions=moment_change,
        untargeted_price_ratio_27_months=math.exp(log_price_ratio(solution)),
        selection='Nearest archived candidate on the examined increasing low-chi branch.',
        selection_diagnostic_sha256=selection_hash,
        checkpoint_sha256=hashlib.sha256(checkpoint.read_bytes()).hexdigest(),
        csv_sha256=hashlib.sha256((output/'equilibrium_paths.csv').read_bytes()).hexdigest(),
        figure_sha256=figure_hashes)
    write_json(output/'calibration.json',payload)
    print(json.dumps({k:payload[k] for k in ('status','chi','target_share','matched_share',
        'error_basis_points','second_year','untargeted_price_ratio_27_months',
        'moment_log_change_after_two_horizon_extensions')},indent=2),flush=True)
    return design


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sigma',type=float,choices=SIGMAS,
        help='Solve one elasticity; final publication still requires all four.')
    args=parser.parse_args()
    if args.sigma is None:
        publish()
    else:
        selected,_=select_candidate()
        design=make_design(selected['chi'])
        if args.sigma==1.:
            prepare_unit(design,selected)
        run(args.sigma,design)

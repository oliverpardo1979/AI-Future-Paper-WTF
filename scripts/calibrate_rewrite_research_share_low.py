"""Publish the low (2023 US) research-share calibration using the existing BVP.

The author permits an approximate empirical match. Select the nearest already
explored candidate on the increasing low-chi branch; retain every original
equilibrium and stability gate. The high-target results remain untouched.
"""
from dataclasses import asdict, replace
import hashlib
import json
import math
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'.python-packages'),str(ROOT/'scripts')]
import numpy as np
from calibrate_rewrite_research_share import checked_moment, SOURCE as HIGH_SOURCE
from calibrate_rewrite_ai_price import (
    make_design as price_design, write_json, extend, log_price_ratio,
    audit_rsi_activation, render_comparison_views, summarize,
)
from simulate_rewrite_finite_frontier import (
    key, design_initial_stocks, load_solution, save_solution,
    validate_solution_design, run, export_paths,
)
from analyze_axm_finite_cap_bvp import terminal_point
from solve_axm_global_finite_cap_bvp import (
    solve_global_finite_cap_bvp, audit_counterfactual_developer_sufficiency,
)
from audit_rewrite_equilibria import finalize, independent_residuals
from plot_rewrite_equilibria import render

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
    return replace(price_design(chi,'rsi_activation'),name=NAME,sigmas=(1.,),
        output_directory=ROOT/'numerical_rewrite'/NAME,
        cache_directory=ROOT/'tmp'/f'rewrite_bvp_{NAME}',
        initial_stock_reference='Unchanged existing-AI fixed-B pre-RSI BGP at sigma=1; '
            'K0/Y0=3.30 and B0=0.01 Bbar. RSI becomes available unexpectedly. '
            'Only K0 and B0 are inherited; C0, q0 and M0 are endogenous. '
            'Chi approximates the annual 2023 US research-compute/GDP proxy.')


def publish():
    row,selection_hash=select_candidate()
    design=make_design(row['chi'])
    output,cache=design.output_directory,design.cache_directory
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
    original_moment=checked_moment(base)
    run(1.,design)
    extend(1.,design)
    report=finalize(design)[0]
    checkpoint=cache/f'{key(1.)}_long.npz'
    solution=load_solution(checkpoint)
    checks=[independent_residuals(solution,h,np.linspace(.001,10.,801))
        for h in (.0003,.0001)]
    optimality=audit_counterfactual_developer_sufficiency(solution,time_points=161,
        capability_points=161,sample_times=np.linspace(0.,10.,161))
    early=bool(optimality['developer_sufficiency_gate_passes'] and all(
        c['maximum_ode_residual']<1e-6 and c['maximum_research_foc_residual']<1e-9
        and c['maximum_monopoly_foc_residual']<1e-9 for c in checks))
    first,second=checked_moment(solution),checked_moment(solution,1.)
    moment_change=abs(math.log(first['share']/original_moment['share']))
    if not (report['equilibrium_certified'] and early and moment_change<2e-5):
        raise RuntimeError('Equilibrium or moment-stability checks failed; no publication.')
    # An empirical mismatch is reported, never passed off as solver error.
    # One basis point is stricter than the author's allowance of a few bp.
    if abs(first['share']-TARGET_SHARE)>1e-4:
        raise RuntimeError('Candidate is no longer within one basis point of the target.')
    report['early_window_checks']=dict(passes=early,independent_residuals=checks,
        concavity=optimality)
    report['settings']['base_tolerance']=2e-7
    write_json(output/f'{key(1.)}_audit.json',report)
    audit_rsi_activation(design)
    export_paths(500.,4001,design,additional_times=np.r_[np.linspace(0.,10.,1001),2.25])
    render(design,reference_sigma=1.)
    render_comparison_views(design,show_price_target=False,reference_sigma=1.)
    summarize(design)
    manifest=json.loads((output/'figure_manifest.json').read_text())
    figure_hashes={}
    for view in manifest['two_window_views']:
        for ext in ('pdf','png'):
            path=ROOT/'figures_rewrite'/f'{view["filename"]}.{ext}'
            figure_hashes[path.relative_to(ROOT).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
    payload=dict(status='numerically_admitted_approximate_calibration',sigmas=[1.],
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
    publish()

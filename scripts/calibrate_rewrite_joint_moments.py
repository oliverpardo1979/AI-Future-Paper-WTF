"""Separate, provisional US-reference calibration; never alters paper scenarios.

Default: audit the source snapshots and compute static compatibility.
--fit: fit omega_X and chi at sigma=1 conditional on each existing Bbar.
No research-spend fit, no paper edits and no new plots are performed here.
All BVP calls and admission gates are reused from the existing implementation.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import asdict, replace
import csv
import hashlib
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'.python-packages'), str(ROOT/'scripts')]
import numpy as np
from scipy.optimize import brentq
from simulate_rewrite_finite_frontier import (
    PARAMETERS, FRONTIER, RAMSEY_START_STEADY_STATE, SimulationDesign,
    key, save_solution, load_solution, validate_solution_design, run,
)
from analyze_axm_finite_cap_bvp import terminal_point
from solve_axm_global_finite_cap_bvp import (
    solve_global_finite_cap_bvp, reconstruct_levels,
    audit_counterfactual_developer_sufficiency,
)
from calibrate_rewrite_ai_price import log_price_ratio, extend, write_json
from audit_rewrite_equilibria import finalize, independent_residuals
from solve_near_unit_ai_bvp import solve_monopoly_static_block

DATA = ROOT/'empirical'/'joint_calibration'


def revenue_floor(sigma, alpha=PARAMETERS.alpha):
    """Strict revenue/Y lower bound from positive marginal revenue, sigma<1."""
    if not math.isfinite(sigma) or sigma <= 0 or not 0 < alpha < 1:
        raise ValueError('Require sigma>0 and 0<alpha<1.')
    return ((1-alpha)*(1-sigma)/(1-alpha*sigma) if sigma < 1 else 0.0)


def omega_from_unit_share(share, alpha=PARAMETERS.alpha):
    if not math.isfinite(alpha) or not 0 < alpha < 1:
        raise ValueError('Require 0<alpha<1.')
    if not math.isfinite(share) or not 0 < share < 1-alpha:
        raise ValueError('The revenue share must be strictly between 0 and 1-alpha.')
    return share/(1-alpha)


def load_references():
    reference = json.loads((DATA/'reference_moments.json').read_text(encoding='utf-8'))
    gdp = json.loads((DATA/'sources/world_bank_gdp_2026-09-14.json').read_text(encoding='utf-8-sig'))
    if gdp[0]['pages'] != 1 or len(gdp[1]) != gdp[0]['total']:
        raise ValueError('Incomplete GDP response.')
    lookup = {(r['countryiso3code'], int(r['date'])): r['value'] for r in gdp[1]}
    if len(lookup) != len(gdp[1]):
        raise ValueError('Duplicate GDP country/year.')
    comparisons = []
    for row in reference['annual_us_estimates_usd_billion']:
        denominator = lookup.get(('USA', row['year']))
        if denominator is None or denominator <= 0:
            raise ValueError('Missing same-country, same-year nominal GDP.')
        share = row['services_revenue']*1e9/denominator
        comparisons.append(dict(**row, gdp_usd=denominator, revenue_gdp_share=share,
                                implied_unit_omega=omega_from_unit_share(share)))
    target = next(r for r in comparisons if r['year'] == reference['revenue_reference_year'])
    return reference, comparisons, target


def source_audit():
    reference, comparisons, target = load_references()
    with (DATA/'sources/epoch_revenue_2026-09-14.csv').open(encoding='utf-8-sig', newline='') as f:
        revenue = list(csv.DictReader(f))
    with (DATA/'sources/epoch_compute_2026-09-14.csv').open(encoding='utf-8-sig', newline='') as f:
        compute = list(csv.DictReader(f))
    annual = [r for r in revenue if r['Period type'] == 'Year' and r['Period revenue']]
    projected = [r['Id'] for r in compute if r['Report date'] and r['Date']
                 and r['Report date'] < r['Date']]
    # Forecast/report dates do not establish realized annual expenditure.
    duplicates = [k for k,v in Counter(r['Id'] for r in compute).items() if v > 1]
    discrepancies = [r['Id'] for r in compute if r['Inference compute spend']
                     and r['Category'] == 'Inference cloud compute'
                     and float(r['Amount']) != float(r['Inference compute spend'])]
    quarter_flags = [r['Id'] for r in revenue if r['Company'] == 'xAI'
                     and r['Period type'] == 'Quarter']
    static_stress=[]
    for sigma in (.9,.99,.999):
        for omega in (.001,omega_from_unit_share(target['revenue_gdp_share']),.1,.2):
            record=dict(sigma=sigma,omega_X=omega,K=5.94,B=1.7,AL=1.)
            try:
                block=solve_monopoly_static_block(math.log(5.94),math.log(1.7),0.,sigma,
                                                 replace(PARAMETERS,omega_x=omega))
                record.update(foc_log_residual=block.monopoly_foc_log_residual,
                    passes_foc_check=abs(block.monopoly_foc_log_residual)<1e-9)
            except (FloatingPointError,RuntimeError,ValueError) as error:
                record.update(passes_foc_check=False,error=f'{type(error).__name__}: {error}')
            static_stress.append(record)
    payload = dict(
        status='source_and_structural_audit_not_equilibrium_simulation',
        geography='US reference; not a worldwide total', comparisons=comparisons,
        revenue_rows=len(revenue), compute_rows=len(compute),
        period_type_counts=dict(Counter(r['Period type'] or 'unspecified' for r in revenue)),
        annual_revenue_rows=[{k:r[k] for k in ('Id','Company','Date','Period revenue','Scope','Source type','Source 1')}
                             for r in annual],
        forecasts_or_partial_year_reports=projected, duplicate_compute_ids=duplicates,
        compute_amount_field_disagreements=discrepancies,
        excluded_quarterly_records_requiring_unit_review=quarter_flags,
        quarterly_issue='xAI record IDs say 43M/59M/107M; Period revenue fields are four times those numbers. No automatic correction or aggregation.',
        source_limitations=[
            'Epoch covers selected companies, not the world sector; reports are not independently audited statements.',
            'Several original company financial reports are behind paywalls; retain as secondary evidence only.',
            'Do not sum annualized, annual, quarterly, company and product-level revenue records.',
            'Research cost notes mix forecasts, training and amortized expenses; not a homogeneous flow M.',
            'PIIE services revenue and training spending share common imputation assumptions.',
            'GDP mapping is an external calibration convention; it does not reconcile every intermediate-input or R&D-capitalization convention.',
        ],
        sigma_compatibility=[dict(sigma=s, strict_revenue_share_floor=revenue_floor(s),
                                  passes_necessary_static_condition=target['revenue_gdp_share'] > revenue_floor(s))
                             for s in (.9, .99, .999, 1., 1.1, 1.5)],
        unit_elastic_inference_check=dict(
            model_inference_to_revenue=target['revenue_gdp_share'],
            source_assumed_inference_to_revenue=1/1.5,
            implication='These cannot both be fitted at sigma=1 by changing chi or B0; this is a structural/proxy mismatch, not an optimizer failure.'),
        source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in sorted((DATA/'sources').iterdir()) if p.is_file()},
        research_target_independent=False,
        identified_parameter_count=None,
        nonunit_static_stress=static_stress,
        nonunit_static_stress_scope='Diagnostic points, not trajectories. Failures near zero marginal revenue must be resolved before any affected dynamic fit; no tolerances are relaxed.',
    )
    write_json(DATA/'source_audit.json', payload)
    return payload


def make_joint_design(chi, frontier, initial_fraction=.01):
    _, _, target = load_references()
    omega = omega_from_unit_share(target['revenue_gdp_share'])
    if not math.isfinite(frontier) or frontier <= 0 or not 0 < initial_fraction < 1:
        raise ValueError('Require positive finite Bbar and 0<B0/Bbar<1.')
    # Full-precision scenario fingerprint prevents reuse across changed inputs.
    tag = hashlib.sha256(json.dumps([frontier, initial_fraction, omega]).encode()).hexdigest()[:12]
    name = 'joint_us_proxy_'+tag
    return SimulationDesign(
        name=name, sigmas=(1.,), parameters=replace(PARAMETERS, omega_x=omega, chi=float(chi)),
        frontier=frontier, initial_capital=RAMSEY_START_STEADY_STATE.capital,
        initial_capability=initial_fraction*frontier,
        output_directory=ROOT/'numerical_rewrite'/'joint_us_proxy'/tag,
        cache_directory=ROOT/'tmp'/'rewrite_bvp_joint_us_proxy'/tag, display_horizon=500.,
        initial_stock_reference=(
            'No-AI Ramsey capital with global-paper macro parameters; B0/Bbar is assumed, '
            'not fitted. US 2024 estimated AI services/GDP is an external reference. '
            'All jump variables are solved by the existing equilibrium BVP.'),
    )


def fit_unit(frontier, initial_fraction=.01):
    reference, _, target = load_references()
    price = reference['price']
    template = make_joint_design(1., frontier, initial_fraction)
    trials = []

    def objective(log_chi):
        chi = math.exp(float(log_chi))
        design = make_joint_design(chi, frontier, initial_fraction)
        tag = hashlib.sha256(float(chi).hex().encode()).hexdigest()[:16]
        path = design.cache_directory/'trials'/f'{tag}.npz'
        print(f'Joint reference Bbar={frontier:.6g}, B0/Bbar={initial_fraction:g}, chi={chi:.9g}', flush=True)
        if path.exists():
            sol = load_solution(path)
            validate_solution_design(sol, design, 1.)
        else:
            sol = solve_global_finite_cap_bvp(
                terminal_point(1., frontier, design.parameters), design.parameters,
                design.initial_capital, design.initial_capability,
                continuation_steps=32, nodes=221, tolerance=2e-7,
                boundary_tolerance=1e-10, maximum_nodes=40000)
            save_solution(sol, path)
        residual = log_price_ratio(sol, price['years'])-math.log(price['ratio'])
        trials.append(dict(chi=chi, price_ratio=price['ratio']*math.exp(residual),
                           log_price_residual=residual, checkpoint=str(path.relative_to(ROOT))))
        write_json(template.output_directory/'calibration_trials.json', trials)
        print(f'  price ratio={trials[-1]["price_ratio"]:.9g}', flush=True)
        return residual

    lo = math.log(PARAMETERS.chi)
    hi = lo+math.log(2.)
    fl, fh = objective(lo), objective(hi)
    for _ in range(16):
        if fl*fh <= 0:
            break
        if fl > 0 and fh > 0:
            hi += math.log(2.)
            fh = objective(hi)
        else:
            lo -= math.log(2.)
            fl = objective(lo)
    else:
        raise RuntimeError('Search bracket exhausted; no fit or equilibrium claim.')
    root = brentq(objective, lo, hi, xtol=2e-6, rtol=1e-10)
    residual = objective(root)
    if abs(residual) > 2e-5:
        raise RuntimeError('Price residual exceeds the existing calibration gate.')
    design = make_joint_design(math.exp(root), frontier, initial_fraction)
    payload = dict(
        status='fitted_candidate_pending_equilibrium_admission', design=design.name,
        parameters=asdict(design.parameters), frontier=frontier,
        initial_capital=design.initial_capital, initial_capability=design.initial_capability,
        empirical_reference=target, price_reference=price,
        fitted_parameters=['omega_X', 'chi'], conditioned_on=['eta','sigma=1','Bbar','B0','macro parameters'],
        fit_is_global_identification=False,
        interpretation='Two conditional moment matches; no claim of global identification or estimated monopoly RSI productivity.',
        research_moment_fitted=False, trials=trials,
        numerical_settings=dict(log_chi_xtol=2e-6, price_log_residual_gate=2e-5,
                                reason='Same tolerances and admission workflow as the existing price calibration.'),
    )
    write_json(design.output_directory/'calibration.json', payload)
    run(1., design)
    extend(1., design)
    report = finalize(design)[0]
    sol = load_solution(design.cache_directory/f'{key(1.)}_long.npz')
    early = [independent_residuals(sol, h, np.linspace(.001,10.,801)) for h in (.0003,.0001)]
    optimality = audit_counterfactual_developer_sufficiency(
        sol, time_points=161, capability_points=161, sample_times=np.linspace(0.,10.,161))
    passes = bool(report['equilibrium_certified'] and optimality['developer_sufficiency_gate_passes']
                  and all(x['maximum_ode_residual']<1e-6 and x['maximum_research_foc_residual']<1e-9
                          and x['maximum_monopoly_foc_residual']<1e-9 for x in early))
    final_ratio = math.exp(log_price_ratio(sol, price['years']))
    passes = passes and abs(math.log(final_ratio/price['ratio'])) < 2e-5
    report.update(early_window_checks=early, early_optimality=optimality,
                  equilibrium_certified=passes, status='numerically_admitted' if passes else 'not_admitted')
    write_json(design.output_directory/f'{key(1.)}_audit.json', report)
    payload.update(status=report['status'], final_price_ratio=final_ratio,
                   checkpoint_sha256=report['checkpoint_sha256'])
    if passes:
        # No trajectory export. These are moments of the admitted solution only.
        v = reconstruct_levels(np.array([0.]), sol.raw.sol(0.)[:,None], sol)
        revenue_share = (1-PARAMETERS.alpha)*float(v['ai_ces_share'][0])
        m_share = math.exp(float(v['log_research_compute'][0]-v['log_output'][0]))
        payload['admitted_moments'] = dict(revenue_output_share=revenue_share,
            price_ratio=final_ratio, initial_research_output_share=m_share,
            initial_research_revenue_ratio=m_share/revenue_share,
            initial_inference_revenue_ratio=revenue_share)
    write_json(design.output_directory/'calibration.json', payload)
    if not passes:
        raise RuntimeError('Full equilibrium admission failed; no numerical path exported.')
    print(json.dumps(payload['admitted_moments']), flush=True)
    return payload


def local_log_sensitivity(moment_function, positive_parameters, steps=(1e-3,3e-4,1e-4)):
    """Report local sensitivity at several steps; never assert identification.

    Log coordinates remove units; central differences are checked across steps.
    The function must return positive moments of independently admitted paths.
    Singular values and their stability matter; counting moments is insufficient.
    """
    x = np.asarray(positive_parameters, dtype=float)
    if x.ndim != 1 or x.size == 0 or not np.all(np.isfinite(x)) or np.any(x<=0):
        raise ValueError('Parameters must be positive and finite.')
    def evaluate(z):
        y = np.asarray(moment_function(z), dtype=float)
        if y.ndim != 1 or y.size == 0 or not np.all(np.isfinite(y)) or np.any(y<=0):
            raise ValueError('Log moments must be positive and finite.')
        return np.log(y)
    evaluate(x)
    results = []
    for h in steps:
        if not math.isfinite(h) or h <= 0:
            raise ValueError('Positive finite difference step required.')
        columns=[]
        for j in range(len(x)):
            shift=np.zeros(len(x)); shift[j]=h
            columns.append((evaluate(x*np.exp(shift))-evaluate(x*np.exp(-shift)))/(2*h))
        jacobian=np.column_stack(columns)
        singular=np.linalg.svd(jacobian, compute_uv=False)
        # Standard floating-point rank diagnostic, not an empirical strength test.
        tolerance=np.finfo(float).eps*max(jacobian.shape)*singular[0]
        results.append(dict(step=h, jacobian=jacobian.tolist(), singular_values=singular.tolist(),
                            floating_point_rank=int(np.sum(singular>tolerance)),
                            parameter_count=len(x)))
    return dict(scope='local diagnostics only; not global identification', checks=results)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fit', action='store_true')
    parser.add_argument('--frontier', type=float, default=FRONTIER)
    parser.add_argument('--initial-fraction', type=float, default=.01)
    args=parser.parse_args()
    audit=source_audit()
    print(json.dumps(dict(comparisons=audit['comparisons'], sigma_compatibility=audit['sigma_compatibility'])), flush=True)
    if args.fit:
        fit_unit(args.frontier, args.initial_fraction)


if __name__=='__main__':
    main()

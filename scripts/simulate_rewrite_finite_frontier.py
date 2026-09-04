"""Four agreed capped-model BVPs; export only after equilibrium admission.

The inherited uncapped unit BGP supplies K0 and B0, never C0, q0, or a
terminal restriction. Cached splines are technical candidates, not figures.
Run each sigma separately to retain reproducible intermediate diagnostics.
"""
from dataclasses import asdict
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import sys
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.python-packages'))
sys.path.insert(0, str(ROOT / 'scripts'))
import numpy as np
from scipy.interpolate import PPoly
from analyze_axm_finite_cap_bvp import (
    critical_capability_frontier, terminal_point, terminal_linearization,
)
from define_positive_ai_branch import PositiveAIBenchmarkParameters, balanced_growth_seed
from solve_near_unit_ai_bvp import elasticity_coordinate, solve_monopoly_static_block
from solve_axm_global_finite_cap_bvp import (
    GlobalFiniteCapBVP, GlobalContinuationStage, solve_global_finite_cap_bvp,
    refine_global_horizon, audit_global_solution, compare_global_solutions,
    audit_counterfactual_developer_sufficiency, reconstruct_levels,
    dated_raw_dynamics, _solution_payload,
)

SIGMAS = (0.9, 1.0, 1.1, 1.5)
PARAMETERS = PositiveAIBenchmarkParameters()
FRONTIER = 1.1 * critical_capability_frontier(1.5, PARAMETERS)
OUT = ROOT / 'numerical_rewrite'
CACHE = ROOT / 'tmp' / 'rewrite_bvp'


def key(sigma):
    return f'sigma_{sigma:.2f}'.replace('.', '_')


def real_wage_growth(static, sigma, capital_growth, capability_growth,
                     effective_labor_growth, output_growth, population_growth):
    """Recover ``g_w`` exactly from the static equilibrium block.

    Since ``w=(1-alpha)(1-s_X)Y/L`` and ``L=N``, wage growth equals
    per-person output growth plus the growth of ``1-s_X``.  The CES share
    identity supplies the latter without numerically differentiating a
    plotted series.
    """
    xk, xb = static.ai_services_log_gradient[:2]
    ai_services_growth = (
        xk * capital_growth
        + xb * capability_growth
        + (1.0 - xk) * effective_labor_growth
    )
    labor_share_growth = (
        -elasticity_coordinate(sigma)
        * static.ai_ces_share
        * (ai_services_growth - effective_labor_growth)
    )
    return output_growth - population_growth + labor_share_growth


def save_solution(solution, filename):
    """Save numerical arrays without executable/pickled Python objects."""
    CACHE.mkdir(parents=True, exist_ok=True)
    raw = solution.raw
    metadata = dict(sigma=solution.terminal.sigma_xl, frontier=solution.terminal.frontier,
                    parameters=asdict(solution.parameters), initial_capital=solution.initial_capital,
                    initial_capability=solution.initial_capability,
                    initial_effective_labor_scale=solution.initial_effective_labor_scale,
                    horizon=solution.horizon, niter=raw.niter,
                    stages=[asdict(s) for s in solution.stages])
    np.savez_compressed(filename, metadata=json.dumps(metadata), x=raw.x,
                        coefficients=raw.sol.c, spline_x=raw.sol.x,
                        spline_axis=raw.sol.axis,
                        rms_residuals=raw.rms_residuals)


def load_solution(filename):
    with np.load(filename, allow_pickle=False) as saved:
        m = json.loads(str(saved['metadata']))
        p = PositiveAIBenchmarkParameters(**m['parameters'])
        t = terminal_point(m['sigma'], m['frontier'], p)
        # solve_bvp stores a vector-valued PPoly with axis=1. Its canonical
        # coefficients must not be reinterpreted as an axis=0 interpolant.
        axis = int(saved['spline_axis']) if 'spline_axis' in saved else 1
        raw = SimpleNamespace(sol=PPoly.construct_fast(saved['coefficients'].copy(),
                              saved['spline_x'].copy(), axis=axis),
                              x=saved['x'].copy(), rms_residuals=saved['rms_residuals'].copy(),
                              niter=m['niter'], success=True)
        return GlobalFiniteCapBVP(raw, t, terminal_linearization(t, p), p,
                                 m['initial_capital'], m['initial_capability'],
                                 m['initial_effective_labor_scale'], m['horizon'],
                                 tuple(GlobalContinuationStage(**v) for v in m['stages']))


def run(sigma):
    if sigma not in SIGMAS:
        raise ValueError('Use one of the four agreed elasticities.')
    p = PARAMETERS
    seed = balanced_growth_seed(p)
    terminal = terminal_point(sigma, FRONTIER, p)
    OUT.mkdir(exist_ok=True)
    CACHE.mkdir(parents=True, exist_ok=True)
    name = key(sigma)
    base_path, refined_path = CACHE/f'{name}_base.npz', CACHE/f'{name}_refined.npz'
    print(f'{name}: frontier={FRONTIER:.12g}; regime={terminal.regime}', flush=True)
    if base_path.exists():
        base = load_solution(base_path)
        terminal = base.terminal
        if asdict(base.parameters) != asdict(p) or terminal.frontier != FRONTIER:
            raise ValueError('Cached parameters differ from the agreed design.')
    else:
        base = solve_global_finite_cap_bvp(terminal, p, seed.capital, seed.capability,
                                         continuation_steps=32, nodes=221,
                                         tolerance=2e-6, maximum_nodes=20000)
        save_solution(base, base_path)
    print(f'{name}: base solved, T={base.horizon:.2f}; refining', flush=True)
    if refined_path.exists():
        refined = load_solution(refined_path)
        refined.terminal = terminal
    else:
        refined = refine_global_horizon(base, base.horizon+500,
                                       nodes=401, tolerance=1e-8,
                                       boundary_tolerance=1e-10, maximum_nodes=40000)
        save_solution(refined, refined_path)
    print(f'{name}: refined; auditing equations and developer optimality', flush=True)
    audit = audit_global_solution(refined)
    comparison = compare_global_solutions(base, refined)
    sufficiency = audit_counterfactual_developer_sufficiency(
        refined, time_points=81, capability_points=101)
    payload = _solution_payload(refined, audit, horizon_comparison=comparison,
                                counterfactual_sufficiency=sufficiency)
    payload['parameters'] = asdict(p)
    payload['initial_stock_reference'] = 'uncapped unit-elastic BGP, not a capped BGP'
    payload['status'] = 'numerically_admitted' if payload['equilibrium_certified'] else 'not_admitted'
    payload['settings'] = dict(base_tolerance=2e-6, refined_tolerance=1e-8,
                               horizon_extension=500, continuation_steps=32)
    (OUT/f'{name}_audit.json').write_text(json.dumps(payload, indent=2, allow_nan=False)+'\n',
                                         encoding='utf-8')
    print(f'{name}: {payload["status"]}; {sufficiency}', flush=True)
    return payload


def export_paths(horizon, points):
    """Refuse a partial or uncertified comparison; never extrapolate splines."""
    solutions = []
    checkpoint_hashes = {}
    for sigma in SIGMAS:
        path = OUT/f'{key(sigma)}_audit.json'
        if not path.exists() or not json.loads(path.read_text())['equilibrium_certified']:
            raise RuntimeError(f'No admitted equilibrium for sigma={sigma}; no figure export.')
        report = json.loads(path.read_text())
        checkpoint = CACHE/report['checkpoint_filename']
        if hashlib.sha256(checkpoint.read_bytes()).hexdigest() != report['checkpoint_sha256']:
            raise RuntimeError('The checkpoint has changed since its equilibrium audit.')
        sol = load_solution(checkpoint)
        if horizon > sol.horizon:
            raise ValueError('Display horizon exceeds a solved and audited horizon.')
        solutions.append(sol)
        checkpoint_hashes[key(sigma)] = report['checkpoint_sha256']
    rows = []
    times = np.linspace(0, horizon, points)
    for sol in solutions:
        p, sigma = sol.parameters, sol.terminal.sigma_xl
        bounded = sol.raw.sol(times)
        v = reconstruct_levels(times, bounded, sol)
        raw = bounded + sol.terminal.terminal_growth*times[None, :]
        rates = dated_raw_dynamics(times, raw, sol.terminal, p, sol.initial_effective_labor_scale)
        for j, time in enumerate(times):
            # Differentiate the static FOC to obtain the actual output growth.
            al = math.log(sol.initial_effective_labor_scale)+(p.population_growth+p.labor_productivity_growth)*time
            static = solve_monopoly_static_block(v['log_capital'][j], v['log_capability'][j], al, sigma, p)
            psi = math.exp(v['log_remaining_frontier_share'][j])
            gb = rates[1,j]*psi  # d logit(B/Bbar)/dt = g_B / psi.
            yk, yb = static.output_log_gradient[:2]
            # The supplied gradient is with respect to (log K, log B, log C,
            # log q). Homogeneity gives the missing log(AL) derivative 1-yk.
            gy = float(yk*rates[0,j] + yb*gb + (1-yk)*(
                                        p.population_growth+p.labor_productivity_growth))
            gw = real_wage_growth(
                static, sigma, rates[0,j], gb,
                p.population_growth+p.labor_productivity_growth,
                gy, p.population_growth,
            )
            sx = v['ai_ces_share'][j]
            revenue = (1-p.alpha)*sx
            u = math.exp(v['log_inference_compute'][j]-v['log_output'][j])
            m = math.exp(v['log_research_compute'][j]-v['log_output'][j])
            rows.append(dict(sigma=sigma, time=time,
                output_effective_labor=math.exp(v['log_output'][j]-al),
                output_per_person_growth=gy-p.population_growth,
                wage_growth=gw,
                wage_productivity=(1-p.alpha)*(1-sx)*math.exp(v['log_output'][j]-al),
                net_interest=v['net_interest_rate'][j], labor_income_share=(1-p.alpha)*(1-sx),
                ai_revenue_output_share=revenue, capability_frontier_ratio=1-psi,
                consumption_effective_labor=math.exp(v['log_consumption'][j]-al),
                capital_effective_labor=math.exp(v['log_capital'][j]-al),
                inference_revenue_share=u/revenue, research_revenue_share=m/revenue,
                profit_revenue_share=1-(u+m)/revenue))
    with (OUT/'equilibrium_paths.csv').open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    manifest = dict(horizon=horizon, points_per_scenario=points,
                    checkpoint_sha256=checkpoint_hashes,
                    csv_sha256=hashlib.sha256((OUT/'equilibrium_paths.csv').read_bytes()).hexdigest())
    (OUT/'paths_manifest.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sigma', type=float)
    parser.add_argument('--export-horizon', type=float)
    parser.add_argument('--points', type=int, default=1201)
    parser.add_argument('--verify-long-horizon', action='store_true')
    args = parser.parse_args()
    if args.verify_long_horizon:
        for sigma in SIGMAS:
            source = load_solution(CACHE/f'{key(sigma)}_refined.npz')
            target = CACHE/f'{key(sigma)}_long.npz'
            if not target.exists():
                longer = refine_global_horizon(source, source.horizon+500,
                                                nodes=601, tolerance=1e-9,
                                                boundary_tolerance=1e-11)
                save_solution(longer, target)
            print(f'{key(sigma)}: second horizon extension saved', flush=True)
    elif args.export_horizon is not None:
        export_paths(args.export_horizon, args.points)
    elif args.sigma is not None:
        run(args.sigma)
    else:
        parser.error('Choose --sigma or --export-horizon.')

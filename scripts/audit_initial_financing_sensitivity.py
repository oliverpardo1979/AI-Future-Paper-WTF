"""Reproduce the distant-initial-stock financing sensitivity reported in the paper."""
from dataclasses import asdict, replace
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".python-packages"))
sys.path.insert(0, str(ROOT / "scripts"))
import numpy as np

from analyze_axm_finite_cap_bvp import critical_capability_frontier, terminal_point
from audit_rewrite_equilibria import independent_residuals, terminal_support_bound
from audit_rewrite_hamiltonian_support import audit_support
from define_positive_ai_branch import PositiveAIBenchmarkParameters, balanced_growth_seed
from simulate_rewrite_finite_frontier import load_solution, save_solution
from solve_axm_global_finite_cap_bvp import (
    audit_global_solution,
    compare_global_solutions,
    raw_to_terminal_coordinates,
    reconstruct_levels,
    refine_global_horizon,
    solve_global_finite_cap_bvp,
)

SIGMA = 1.5
BASE_PARAMETERS = PositiveAIBenchmarkParameters()
PARAMETERS = replace(BASE_PARAMETERS, chi=1.4223)
FRONTIER = 1.1 * critical_capability_frontier(SIGMA, PARAMETERS)
INITIAL = balanced_growth_seed(BASE_PARAMETERS)
CACHE = ROOT / "tmp" / "rewrite_financing_sensitivity"
OUTPUT = ROOT / "numerical_rewrite" / "initial_financing_sensitivity.json"


def crossing_time(times, values, target):
    distance = values-target
    hits = np.flatnonzero(distance[:-1]*distance[1:] <= 0)
    if not hits.size:
        return None
    j = int(hits[0])
    return float(times[j]+(target-values[j])*(times[j+1]-times[j])
                 /(values[j+1]-values[j]))


def solve(fresh=False):
    CACHE.mkdir(parents=True, exist_ok=True)
    paths = {name: CACHE/f"sigma_1_50_{name}.npz"
             for name in ("base", "refined", "long")}
    if fresh:
        for path in paths.values():
            path.unlink(missing_ok=True)
    terminal = terminal_point(SIGMA, FRONTIER, PARAMETERS)
    if paths["base"].exists():
        base = load_solution(paths["base"])
    else:
        base = solve_global_finite_cap_bvp(
            terminal, PARAMETERS, INITIAL.capital, INITIAL.capability,
            continuation_steps=32, nodes=221, tolerance=2e-6,
            boundary_tolerance=1e-10, maximum_nodes=40000,
        )
        save_solution(base, paths["base"])
    if paths["refined"].exists():
        refined = load_solution(paths["refined"])
    else:
        refined = refine_global_horizon(
            base, base.horizon+500, nodes=401, tolerance=1e-8,
            boundary_tolerance=1e-10, maximum_nodes=40000,
        )
        save_solution(refined, paths["refined"])
    if paths["long"].exists():
        long = load_solution(paths["long"])
    else:
        long = refine_global_horizon(
            refined, refined.horizon+500, nodes=601, tolerance=1e-9,
            boundary_tolerance=1e-11,
        )
        save_solution(long, paths["long"])
    for candidate in (base, refined, long):
        if (asdict(candidate.parameters) != asdict(PARAMETERS)
                or candidate.terminal.frontier != FRONTIER
                or candidate.terminal.sigma_xl != SIGMA):
            raise ValueError("A financing-sensitivity checkpoint uses a different design.")
        # Reloading reconstructs an equal terminal object for each checkpoint,
        # while the horizon comparator deliberately requires common identity.
        candidate.terminal = terminal
    return base, refined, long, paths


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fresh", action="store_true")
    args = parser.parse_args()
    base, refined, solution, paths = solve(args.fresh)
    audit = audit_global_solution(solution)
    comparisons = {
        "base_to_refined": compare_global_solutions(base, refined, common_window=500),
        "refined_to_long": compare_global_solutions(refined, solution, common_window=500),
    }
    residuals = [independent_residuals(solution, step) for step in (.003, .001)]
    supports = []
    for dates, states in ((81, 101), (321, 241)):
        support = audit_support(solution, dates, states)
        supports.append({key: value for key, value in support.items() if key != "checks"})
    bound = terminal_support_bound(solution)
    raw = (solution.raw.sol(solution.horizon)
           + solution.terminal.terminal_growth*solution.horizon)
    terminal_coordinates = raw_to_terminal_coordinates(
        solution.horizon, raw, solution.terminal, solution.parameters,
        solution.initial_effective_labor_scale,
    )
    terminal_gap = float(np.max(np.abs(
        terminal_coordinates-solution.terminal.coordinates)))

    values = reconstruct_levels(np.array([0.0]), solution.raw.sol(0.0)[:, None], solution)
    revenue_output = float((1-PARAMETERS.alpha)*values["ai_ces_share"][0])
    inference_output = math.exp(values["log_inference_compute"][0]-values["log_output"][0])
    research_output = math.exp(values["log_research_compute"][0]-values["log_output"][0])
    composition = {
        "inference_revenue_share": inference_output/revenue_output,
        "research_revenue_share": research_output/revenue_output,
        "profit_revenue_share": 1-(inference_output+research_output)/revenue_output,
        "ai_revenue_output_share": revenue_output,
        "inference_output_share": inference_output,
        "research_output_share": research_output,
        "profit_output_share": revenue_output-inference_output-research_output,
    }

    times = np.linspace(0, 500, 10001)
    values = reconstruct_levels(times, solution.raw.sol(times), solution)
    labor_share = (1-PARAMETERS.alpha)*(1-values["ai_ces_share"])
    initial_share = float(labor_share[0])
    terminal_share = solution.terminal.labor_income_share
    transitions = {}
    for fraction in (.1, .5, .9):
        target = initial_share+fraction*(terminal_share-initial_share)
        transitions[f"T{int(100*fraction)}"] = crossing_time(times, labor_share, target)

    residual_gate = all(
        item["maximum_ode_residual"] < 1e-6
        and item["maximum_research_foc_residual"] < 1e-9
        and item["maximum_monopoly_foc_residual"] < 1e-9
        for item in residuals
    )
    support_gate = (
        all(item["support_diagnostic_passes"]
            and item["maximum_own_gap"] < 1e-10
            and item["maximum_tail_derivative_ratio"] <= 1
            for item in supports)
        and bound["terminal_capability_above_cutoff"]
        and bound["terminal_margin"] > 0
    )
    comparison = comparisons["refined_to_long"]
    admitted = bool(
        audit["dated_candidate_accepted"] and residual_gate and support_gate
        and comparison["maximum_initial_jump_change"] < 2e-5
        and comparison["maximum_common_window_coordinate_change"] < 2e-5
        and terminal_gap < 1e-4
    )
    result = {
        "purpose": "initial-stock and developer-financing sensitivity",
        "parameters": asdict(PARAMETERS),
        "sigma": SIGMA,
        "frontier": FRONTIER,
        "initial_capital": INITIAL.capital,
        "initial_capability": INITIAL.capability,
        "initial_capability_frontier_ratio": INITIAL.capability/FRONTIER,
        "transition_definition": (
            "fraction of the labor-share decline from date zero to its analytical limit"
        ),
        "transition_dates": transitions,
        "date_zero_composition": composition,
        "audit": audit,
        "independent_dated_checks": residuals,
        "horizon_comparisons": comparisons,
        "global_hamiltonian_support": supports,
        "analytical_support_continuation": bound,
        "maximum_terminal_coordinate_gap": terminal_gap,
        "equilibrium_certified": admitted,
        "checkpoint_sha256": hashlib.sha256(paths["long"].read_bytes()).hexdigest(),
    }
    if not admitted or abs(transitions["T50"]-50) > .1:
        raise RuntimeError("The financing sensitivity failed admission or timing calibration.")
    OUTPUT.write_text(json.dumps(result, indent=2, allow_nan=False)+"\n", encoding="utf-8")
    print(json.dumps({
        "equilibrium_certified": admitted,
        "transition_dates": transitions,
        "date_zero_composition": composition,
    }, indent=2))


if __name__ == "__main__":
    main()

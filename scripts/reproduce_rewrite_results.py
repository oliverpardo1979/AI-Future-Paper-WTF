"""Reproduce the numerical equilibrium results used by ``main_rewrite.tex``.

The script deliberately stops at the first failed test, solve, or audit. A
partial set of trajectories must never be exported as the paper's comparison.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
SIGMAS = (0.9, 1.0, 1.1, 1.5)
DESIGN_SIGMAS = {
    'main': SIGMAS,
    'slow': SIGMAS,
    'near_terminal': SIGMAS,
}
DESIGNS = tuple(DESIGN_SIGMAS)
TEST_FILES = (
    "test_finite_cap_bvp.py",
    "test_global_finite_cap_bvp.py",
    "test_rewrite_finite_frontier.py",
    "test_rewrite_simulation_design.py",
    "test_near_unit_ai_bvp.py",
)


def run(arguments: list[str]) -> None:
    """Run one visible, fail-fast reproduction stage from the repository root."""
    display = " ".join(arguments)
    print(f"\n>>> {display}", flush=True)
    subprocess.run(arguments, cwd=ROOT, check=True)


def remove_generated_checkpoints() -> None:
    """Remove only this workflow's untracked BVP checkpoints."""
    removed = 0
    cache_designs = {
        'rewrite_bvp': SIGMAS,
        'rewrite_bvp_slow': SIGMAS,
        'rewrite_bvp_near_terminal': DESIGN_SIGMAS['near_terminal'],
    }
    for cache_name, sigmas in cache_designs.items():
        cache = ROOT / "tmp" / cache_name
        for sigma in sigmas:
            key = f"sigma_{sigma:.2f}".replace(".", "_")
            for suffix in ("base", "refined", "long"):
                path = cache / f"{key}_{suffix}.npz"
                if path.exists():
                    path.unlink()
                    removed += 1
    print(f"Removed {removed} generated equilibrium checkpoint(s).", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fresh",
        action="store_true",
        help="discard only the generated rewrite BVP checkpoints before solving",
    )
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="skip the regression suites (use only after an unchanged successful run)",
    )
    parser.add_argument("--export-horizon", type=float, default=500.0)
    parser.add_argument("--slow-export-horizon", type=float, default=4000.0)
    parser.add_argument("--points", type=int, default=1201)
    args = parser.parse_args()

    if args.export_horizon <= 0 or args.slow_export_horizon <= 0 or args.points < 2:
        parser.error("Both export horizons must be positive and --points must be at least 2.")

    if args.fresh:
        remove_generated_checkpoints()

    python = sys.executable
    if not args.skip_tests:
        for test_file in TEST_FILES:
            run(
                [
                    python,
                    "-m",
                    "unittest",
                    "discover",
                    "-s",
                    "tests",
                    "-p",
                    test_file,
                    "-v",
                ]
            )

    horizons = {
        'main': args.export_horizon,
        'slow': args.slow_export_horizon,
        'near_terminal': args.export_horizon,
    }
    for design in DESIGNS:
        for sigma in DESIGN_SIGMAS[design]:
            run(
                [
                    python,
                    "scripts/simulate_rewrite_finite_frontier.py",
                    "--design",
                    design,
                    "--sigma",
                    str(sigma),
                ]
            )

        run(
            [
                python,
                "scripts/simulate_rewrite_finite_frontier.py",
                "--design",
                design,
                "--verify-long-horizon",
            ]
        )
        if design in ('main', 'slow'):
            for dates, states in ((81, 101), (321, 241)):
                run(
                    [
                        python,
                        "scripts/audit_rewrite_hamiltonian_support.py",
                        "--design",
                        design,
                        "--sigma",
                        "1.5",
                        "--time-points",
                        str(dates),
                        "--capability-points",
                        str(states),
                    ]
                )
        run([python, "scripts/audit_rewrite_equilibria.py", "--design", design])
        run(
            [
                python,
                "scripts/simulate_rewrite_finite_frontier.py",
                "--design",
                design,
                "--export-horizon",
                str(horizons[design]),
                "--points",
                str(args.points),
            ]
        )
        run([python, "scripts/plot_rewrite_equilibria.py", "--design", design])

    financing_command = [python, "scripts/audit_initial_financing_sensitivity.py"]
    if args.fresh:
        financing_command.append("--fresh")
    run(financing_command)
    print(
        "\nReproduction complete: the main, slow-transition, and near-terminal "
        "comparisons passed admission and their audited data and figures were "
        "regenerated.",
        flush=True,
    )


if __name__ == "__main__":
    main()

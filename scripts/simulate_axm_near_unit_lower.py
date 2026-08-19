from __future__ import annotations

import csv
import math
import sys
from dataclasses import replace
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import simulate_axm_equilibrium as core


SIGMA_XL = 0.90
SIGMA_HM = 2.0
HORIZONS = (5000.0, 5300.0, 5600.0)
TOLERANCE = 1e-6
NODES = 401
STEP = 2.0
OUT = ROOT / "numerical_axm"


def write_csv(path: Path, rows: list[dict[str, float | str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    reference = replace(core.Parameters(), sigma_xl=1.0, sigma_hm=2.0)
    seed = core.fixed_share_guess(
        reference,
        (1.0, 1.0, 1.0),
        horizon=1.0,
        mesh=np.asarray([0.0]),
    )
    stocks = (math.exp(float(seed[0, 0])), 1.0, 1.0)
    parameters = replace(
        core.Parameters(), sigma_xl=SIGMA_XL, sigma_hm=SIGMA_HM
    )
    all_rows: list[dict[str, float | str]] = []
    summaries: list[dict[str, float | str]] = []
    for horizon in HORIZONS:
        solution, targets = core.solve_equilibrium(
            parameters,
            stocks,
            horizon=horizon,
            nodes=NODES,
            tolerance=TOLERANCE,
        )
        scenario = f"near_unit_sigma_xl_090_hm_2_T_{horizon:g}"
        rows = core.evaluate_solution(
            scenario,
            solution,
            parameters,
            horizon,
            step=STEP,
            initial_population=stocks[2],
        )
        diagnostics = core.path_diagnostics(rows, parameters)
        max_rms = float(np.max(solution.rms_residuals))
        max_eq = max(
            float(value)
            for key, value in diagnostics.items()
            if key.startswith("max_abs_")
        )
        if not solution.success or max_rms > TOLERANCE * (1.0 + 1e-8):
            raise RuntimeError(
                f"{scenario}: solver failure or RMS {max_rms:.3e}"
            )
        if max_eq > 2e-5:
            raise RuntimeError(f"{scenario}: equation residual {max_eq:.3e}")
        tagged = [
            {
                "alpha": parameters.alpha,
                "eta": parameters.eta,
                "sigma_xl": SIGMA_XL,
                "sigma_hm": SIGMA_HM,
                "horizon": horizon,
                "solver_tolerance": TOLERANCE,
                **row,
            }
            for row in rows
        ]
        all_rows.extend(tagged)
        terminal = rows[-1]
        summaries.append(
            {
                "scenario": scenario,
                "alpha": parameters.alpha,
                "eta": parameters.eta,
                "sigma_xl": SIGMA_XL,
                "sigma_hm": SIGMA_HM,
                "horizon": horizon,
                "solver_success": int(bool(solution.success)),
                "mesh_nodes": int(solution.x.size),
                "max_rms_residual": max_rms,
                "max_equilibrium_residual": max_eq,
                "initial_log_consumption": rows[0]["log_consumption"],
                "initial_log_shadow_value": rows[0]["log_shadow_value"],
                "terminal_output_per_capita_growth": terminal[
                    "output_per_capita_growth"
                ],
                "terminal_net_interest_rate": terminal[
                    "net_capital_return"
                ],
                "terminal_aggregate_labor_share": terminal[
                    "aggregate_labor_share"
                ],
                "terminal_ai_share": terminal["ai_share"],
                "terminal_consumption_share": terminal[
                    "consumption_share"
                ],
                "terminal_shadow_object": targets["terminal_shadow_object"],
                "terminal_shadow_target": targets["terminal_shadow_target"],
            }
        )
        print(
            f"PASS T={horizon:g} nodes={solution.x.size} "
            f"RMS={max_rms:.3e} maxeq={max_eq:.3e}"
        )
    write_csv(OUT / "near_unit_sigma090_horizon_paths.csv", all_rows)
    write_csv(OUT / "near_unit_sigma090_horizon_summary.csv", summaries)


if __name__ == "__main__":
    main()

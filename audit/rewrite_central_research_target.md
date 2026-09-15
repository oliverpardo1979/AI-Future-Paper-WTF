# Central illustrative research-share target (2026-09-14)

The author selected first-year M/Y=0.183% at sigma=1. This is an illustrative
target, not an exact empirical observation. The ratio is integral(M,0,1)
divided by integral(Y,0,1), not M0/Y0 or an average of instantaneous ratios.

## Selection and provenance

The existing chi=7.616304576019883 delivers 0.182915940777111%, a discrepancy
of -0.008405922289 basis points. It rounds to the requested 0.183%. Half the
rounding interval is 0.05 basis points; this is a target-precision criterion,
not a relaxed equilibrium tolerance. No chi retuning was necessary.

Chi was originally found from the 40% price decline over 27 months. The
research target was selected after examining this result, not independently
estimated. `calibration.json` retains that original search; the new
`research_share_target.json` stores the current target, achieved annual
moments and checkpoint/CSV provenance. The price decline is now an outcome,
including the diamond in the price panel. Its geometry is unchanged.

## Checks executed

Ran `calibrate_rewrite_research_share_central.py --verify-existing`:

- Verified hashes linking all four long checkpoints, existing admission
  audits, activation continuity and the plotted CSV.
- Recomputed first-year M/Y on base, refined and long horizons at all four
  sigmas, with 64/128 Gauss-Legendre quadrature nodes. Quadrature log gaps
  remain below 1e-8 and horizon changes below 2e-5.
- Recomputed second-year M/Y and the implied 27-month price changes.
- Passed 28 regression tests (central target, simulation selection,
  historical half-decline calibration, and slow sensitivity).

This execution reused the admitted equilibrium paths; it did not rerun the
full developer-support audit or solve new trajectories. The default new
driver retains that full-solve/audit route for replication. The historical
price driver remains available. No equation or economic parameter changed.

The central and slow CSVs, checkpoints and figure files are unchanged.
Title, abstract, introduction and analytical sections are unchanged. The
paper, parameter table, numerical appendix and replication guide now agree
on the illustrative research target and on the source of the retained chi.

# RSI activation with half the observed percentage price decline

This folder accompanies [The Future of Growth and Human Labor Under Recursive
AI Self-Improvement](https://oliverpardo1979.github.io/AI-Future-Paper-WTF/paper/the-future-of-growth-and-human-labor-under-recursive-ai-self-improvement.pdf),
compiled from `main_rewrite.tex`, subsection "A slower decline in the AI-service price".

## What changes

Only the price target and the fitted chi change relative to `../rsi_activation/`.
At sigma=1, target `p_X(2.25)/p_X(0)=0.60`: a 40% decline, half the
rounded observed 80% decline. This is not half the log change, half the
annual rate, or half of chi. It is an illustrative sensitivity, not a new
empirical observation or an identified effect of market structure.

Keep omega_X=0.10, eta=0.20, Bbar=1360.9921392415592, B0=0.01*Bbar,
the four sigmas 0.90, 1.00, 1.10, 1.50, and the original annual conventions.
AI already exists before unexpected RSI activation. Each economy starts
on its fixed-B BGP, with K0/Y0=3.30 and r0=0.05. These initial stocks are
identical to the 80%-decline exercise. Post-event C and q are re-solved.

## Reproduction

Install the root `requirements-rewrite.txt`, then run from the repository root:

```text
python scripts/calibrate_rewrite_ai_price.py --variant rsi_activation_half_decline
python -m unittest discover -s tests -p test_rewrite_rsi_half_decline.py -v
```

For separate stages, append `--calibrate-only`, then `--sigma 0.9`,
`--sigma 1`, `--sigma 1.1`, `--sigma 1.5`, and finally `--finish`.
The existing collocation BVP, two horizon extensions, independent residuals,
optimality checks, TVCs, admission tolerances, and event audit are unchanged.
No export is allowed unless all four paths pass the complete workflow.

Files follow the original folder's schema: calibration and trials,
pre-event references, per-sigma equilibrium audits, Hamiltonian support
audits, activation audit, admitted path CSV, plot manifests, and summary.
The final comparison is in `comparison_to_full_decline.json`. It records
the parameter/stock checks and binds both sets of results to their data hashes.
Git preserves JSON/CSV line endings so byte-level hashes survive checkouts.

Figures use the same four lines, panels, normalizations, and time windows
as the original exercise. Their vertical scales may differ to preserve
legibility; exact comparisons are in the summary rather than inferred
from differently scaled panels. The earlier simulations are not overwritten.

# RSI activation with existing AI

This folder accompanies [The Future of Growth and Human Labor Under Recursive
AI Self-Improvement](https://oliverpardo1979.github.io/AI-Future-Paper-WTF/paper/the-future-of-growth-and-human-labor-under-recursive-ai-self-improvement.pdf),
compiled from `main_rewrite.tex`.

## Economic experiment

AI production services already exist before time zero. The production
weight is 0.10 on both sides of an unexpected activation of RSI. Before
the event, research is unavailable (chi=0, M=0), so B stays fixed. Each
sigma starts on the corresponding fixed-B BGP with K/Y=3.30 and r=0.05.
Only predetermined stocks are inherited: post-event consumption and the
shadow value are selected by the positive-chi BVP. The pre-event BGP is a
controlled reference, not an assertion that historical AI efficiency was
constant or that RSI actually began in January 2024.

The upper bound, initial B, eta, omega_X, four sigmas, annual conventions,
post-event equilibrium equations, and admission tolerances follow the
agreed lower-weight design. Initial capital differs across sigmas, and
chi is refitted at sigma=1 to p_X(2.25)/p_X(0)=0.20, then held fixed.
No old trajectory is overwritten or relabeled as an RSI-activation path.

## Reproduce

From the repository root, using the dependencies in `requirements-rewrite.txt`:

```text
python scripts/calibrate_rewrite_ai_price.py --variant rsi_activation
python -m unittest discover -s tests -p test_rewrite_rsi_activation.py -v
```

For separate stages, use `--calibrate-only`, then `--sigma 0.9`, `--sigma 1`,
`--sigma 1.1`, `--sigma 1.5`, and finally `--finish`. The default
`scripts/reproduce_rewrite_results.py` runs this comparison; use
`--include-legacy` to reproduce the earlier comparisons too.

## Files and checks

- `calibration.json`: exact parameters, initial capital by sigma, price
  target, source/proxy qualifications, and final match.
- `calibration_trials.json`: scalar search diagnostics; trial BVPs are not
  exported as equilibrium trajectories.
- `pre_rsi_reference.json`: the four analytical fixed-B references.
- `sigma_*_audit.json`: equation, feasibility, horizon, TVC and developer
  optimality checks for the post-event trajectories.
- `sigma_1_50*_support_*.json`: counterfactual Hamiltonian-support audits
  used when the stronger global-concavity criterion fails.
- `activation_audit.json`: pre-event Euler/resource/static equations,
  continuity of K, B, Y, X, U, w, r and p_X at the event, and the
  endogenous consumption and research jumps. Its 1e-9 log tolerance
  checks identical static equations at inherited stocks, relative to the
  final BVP boundary tolerance of 1e-11.
- `equilibrium_paths.csv`: admitted post-event paths, not calibration trials.
- `paths_manifest.json`, `figure_manifest.json`: checkpoint/data hashes,
  analytic limits, figure fields and time windows. The first two years
  before activation in the window figures are the analytical pre-RSI BGP;
  the discontinuity at zero in growth rates or spending is not interpolated
  into a fictitious transition interval.
- `summary.json`: exact observations used to write the paper.

Exports require all four post-event paths to pass the unchanged admission
workflow, the final refined price target, and the event audit. The code
does not pass through chi=0 or omega_X=0 to seed the post-event BVP.
Numerical admission uses analytical long-run continuations and numerical
optimality checks; it is not an interval-arithmetic existence proof.

The earlier simulations remain stored in their original folders. Set
`\showlegacysimulationstrue` in `main_rewrite.tex` to restore their section
and numerical appendix; set it to `\showlegacysimulationsfalse` to display
this exercise. The switch changes the PDF only, not any model or data file.

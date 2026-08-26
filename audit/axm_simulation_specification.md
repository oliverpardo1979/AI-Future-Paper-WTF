# Master specification for the A--B model simulations

## Status and scope

This document records the numerical contract for the A--B implementation. It
fixes the economic system, notation, state vector, terminal restrictions, and
acceptance tests. The core migration is complete: the Python solver evaluates
labor productivity as `A(t)=A0*exp(gamma_A*t)`, treats `B` as AI capability,
and uses effective production labor `A*L`. Descriptive public fields such as
`log_capability` retain their names and now unambiguously mean `log(B)`.

The reported simulations continue to use `A0=1` and `gamma_A=0`. The script
`scripts/check_axm_ab_regression.py` reconstructs sampled dated allocations
and rates from the previously audited unit-elasticity, complementarity, and
gross-substitutes files frozen at commit `d019192`, with a maximum absolute
difference of zero. It also
checks exact positive-`gamma_A` balanced paths for the automated benchmark and
the `sigma_HM=1` extension. Thus the migration reorganizes notation and adds
the exogenous productivity path without changing the model when labor
productivity is held fixed.

The broader near-unit grid, rescaled-time diagnostic, and boundary-Jacobian
conditioning test below remain implementation extensions. The currently
reported points `sigma_XL` in `{0.90,1.00,1.10}` have been re-solved and
accepted under their existing horizon and common-window audits.

## 1. Notation contract

| Economic object | New paper notation | Current code/output name | Required migrated name |
|---|---:|---|---|
| Labor productivity | \(A\) | absent | `labor_productivity`, `log_labor_productivity` |
| AI capability | \(B\) | `A`, `capability`, `log_capability` | `capability`, `log_capability` |
| Effective production labor | \(AL\) | `L` | `effective_production_labor` |
| AI production services | \(X=BU\) | `X=A*U` | `ai_production_services` |
| Inference compute | \(U\) | `inference_compute` | unchanged |
| AI research services | \(BM\) | `A*M` | `ai_research_services` |
| Research compute | \(M\) | `research_compute` | unchanged |
| Human research | \(H\) | `human_research` | unchanged |
| Capability flow | \(\dot B\) | `capability_flow` | unchanged semantic name |
| Capability growth | \(g_B=\dot B/B\) | `capability_growth` | unchanged semantic name |
| Shadow value of capability | \(q\) | `shadow_value` | `shadow_value_capability` |

Internal descriptive names such as `log_capability` already have the correct
economic meaning and need not be replaced. Symbolic labels, CSV metadata, audit
equations, and documentation must use \(B\), not \(A\), for capability.

The following substitutions are identities, not changes in the model:

\[
 A_{\mathrm{old}}\mapsto B,\qquad
 X=A_{\mathrm{old}}U\mapsto X=BU,\qquad
 A_{\mathrm{old}}M\mapsto BM,\qquad
 qA_{\mathrm{old}}\mapsto qB.
\]

A blind text substitution is prohibited because \(A\) now has the distinct
meaning of labor productivity.

## 2. Primitives and exogenous paths

The initial conditions are

\[
 K(0)=K_0,\qquad B(0)=B_0,\qquad
 A(0)=A_0,\qquad N(0)=N_0,
\]

with

\[
 \frac{\dot A}{A}=\gamma_A,\qquad
 \frac{\dot N}{N}=n.
\]

The numerical state vector contains the four endogenous variables

\[
 y=(\log K,\log B,\log C,\log q)'.
\]

The solver evaluates \(A_t=A_0e^{\gamma_A t}\) and
\(N_t=N_0e^{nt}\) analytically. The baseline compatibility experiment uses
\(A_0=1\) and \(\gamma_A=0\).

## 3. Dated static equilibrium: automated-research benchmark

In the benchmark, \(H=0\) and \(L=N\). For
\(\varphi=(\sigma_{XL}-1)/\sigma_{XL}\),

\[
 Z=\left[\omega_L(AL)^\varphi+\omega_XX^\varphi\right]^{1/\varphi},
 \qquad Y=K^\alpha Z^{1-\alpha},
\]

with the continuous Cobb--Douglas limit at \(\sigma_{XL}=1\). The static
equations are

\[
 s_X=\frac{\omega_XX^\varphi}
 {\omega_L(AL)^\varphi+\omega_XX^\varphi},
 \qquad
 e_X=\frac{1-s_X}{\sigma_{XL}}+\alpha s_X,
\]

\[
 p_X=(1-\alpha)s_X\frac{Y}{X},\qquad
 p_X(1-e_X)=\frac1B,\qquad X=BU,
\]

\[
 r=\alpha\frac YK-\delta,\qquad
 w=(1-\alpha)(1-s_X)\frac YL,
\]

and

\[
 \dot B=\chi(BM)^\eta,\qquad
 q\chi\eta B(BM)^{\eta-1}=1.
\]

For positive \((K,B,A,N,q)\), the monopoly equation selects the unique
positive service supply established in the paper. The research condition gives
a unique positive \(M\).

## 4. Dated static equilibrium: human-research extension

Labor clearing is

\[
 N=L+H.
\]

For \(\varrho_{HM}=(\sigma_{HM}-1)/\sigma_{HM}\),

\[
 E=\left[\omega_HH^{\varrho_{HM}}
 +\omega_M(BM)^{\varrho_{HM}}\right]^{1/\varrho_{HM}},
 \qquad \dot B=\chi E^\eta.
\]

The unit expenditure of \(E\) is

\[
 P_E=\left[\omega_H^{\sigma_{HM}}w^{1-\sigma_{HM}}
 +\omega_M^{\sigma_{HM}}(1/B)^{1-\sigma_{HM}}
 \right]^{1/(1-\sigma_{HM})},
\]

with its Cobb--Douglas limit when \(\sigma_{HM}=1\). The scale condition and
conditional demands are

\[
 q\chi\eta E^{\eta-1}=P_E,
\]

\[
 H=\omega_H^{\sigma_{HM}}(P_E/w)^{\sigma_{HM}}E,
 \qquad
 BM=\omega_M^{\sigma_{HM}}(BP_E)^{\sigma_{HM}}E.
\]

The intratemporal map solves labor clearing jointly with final production,
the monopoly equation, research cost minimization, and research scale. It then
recovers \(L,H,U,M,X,E,Z,Y,r,w,p_X,P_E,s_X,s_M\). The selected numerical root
must be interior and must satisfy the monopoly second-order condition.

## 5. Canonical dynamic system

After solving the dated static map, the benchmark uses

\[
 \frac{\dot K}{K}=\frac{Y-C-U-M}{K}-\delta,
 \qquad
 \frac{\dot B}{B}=\frac{\chi(BM)^\eta}{B},
\]

\[
 \frac{\dot C}{C}=n+\alpha\frac YK-\delta-\rho,
\]

\[
 \frac{\dot q}{q}=\alpha\frac YK-\delta
 -\frac{X}{qB^2}-\eta\frac{\dot B}{B}.
\]

The human-research extension replaces the capability equation with
\(\dot B=\chi E^\eta\) and the last equation with

\[
 \frac{\dot q}{q}=\alpha\frac YK-\delta
 -\frac{X}{qB^2}-\eta s_M\frac{\dot B}{B}.
\]

These are the only four endogenous differential equations. Neither the static
root solver nor detrending introduces an additional economic condition.

## 6. Unit elasticity

Define

\[
 \beta=(1-\alpha)\omega_X,\qquad
 \lambda=(1-\alpha)\omega_L,\qquad
 \nu=\frac\beta\lambda,\qquad
 G=n+\gamma_A.
\]

At \(\sigma_{XL}=1\),

\[
 Y^{1-\beta}=K^\alpha(AL)^\lambda(\beta^2B)^\beta,
 \qquad \frac UY=\beta^2,
\]

and a balanced path with positive limiting \(K/Y,C/Y,L/N\) satisfies

\[
 g_Y=G+\nu g_B.
\]

Let

\[
 \bar s=\begin{cases}
 \omega_M,&\sigma_{HM}=1,\\
 1,&H=0\text{ or }\sigma_{HM}>1\text{ with }Bw\to\infty,
 \end{cases}
 \qquad
 D(\bar s)=1-\eta\bar s(1+\nu).
\]

The candidate capability growth rate is

\[
 g_B^*=\frac{\eta(n+\bar s\gamma_A)}{D(\bar s)},
 \qquad
 g_Y^*=G+\nu g_B^*.
\]

For \(\sigma_{HM}=1\), this is an exact interior balanced path. For
\(\sigma_{HM}>1\), it describes the limiting automated-research candidate on
which \(H/N\to0\). The automated benchmark uses \(\bar s=1\).

Define the per-capita output growth rate

\[
 \gamma^*=g_Y^*-n=\gamma_A+\nu g_B^*.
\]

The candidate output shares and prices are

\[
 u^*=\beta^2,\qquad
 k^*=\frac{\alpha}{\rho+\delta+\gamma^*},\qquad
 i^*=(g_Y^*+\delta)k^*,
\]

\[
 m^*=\frac{\beta^2\eta\bar s g_B^*}
 {\rho-n+(1-\eta\bar s)g_B^*},\qquad
 c^*=1-u^*-i^*-m^*.
\]

The remaining growth rates are

\[
 g_U=g_M=g_Y^*,\quad g_X=g_Y^*+g_B^*,\quad
 g_q=g_Y^*-g_B^*,\quad g_w=\gamma^*.
\]

When \(\sigma_{HM}=1\), the exact production-labor fraction is

\[
 \ell^*\equiv\frac LN
 =\frac{\lambda\omega_M}
 {\lambda\omega_M+m^*\omega_H},
\]

and \(g_H=n\). When \(\sigma_{HM}>1\),

\[
 g_H=n-(\sigma_{HM}-1)
 \left[\gamma_A+(1+\nu)g_B^*\right].
\]

The unit-elastic fixed-horizon terminal ratios are

\[
 \frac{C(T)}{Y(T)}=c^*,\qquad
 \frac{q(T)B(T)}{Y(T)}
 =\frac{m^*}{\eta\bar s g_B^*}.
\]

For the automated benchmark, the preferred local terminal restriction is the
projection onto the two unstable left eigenvectors of the normalized
four-dimensional system. The ratio restrictions remain a transparent
finite-horizon approximation and a regression check.

### Local saddle calculations

For \(H=0\), the Jacobian evaluated at the current Table 2 calibration has
eigenvalues

\[
 \operatorname{eig}(J^*)=
 \{-0.098971,-0.003194,0.040391,0.149290\}.
\]

The determinant of the state block of Euclidean-normalized stable
eigenvectors is \(0.6037\).

For the exact \(\sigma_{HM}=1\) interior balanced path, implicit
differentiation of the labor allocation and research block gives, at
\(\gamma_A=0\),

\[
 J_{HM=1}^*=\begin{pmatrix}
  0.0401778& 0.0417493&-0.2070996&-0.0001158\\
 -0.0001628&-0.0024661& 0&0.0006575\\
 -0.0561020& 0.0140298&0&-0.0000264\\
 -0.0676956& 0.0399367&0&0.0303825
 \end{pmatrix}.
\]

Its eigenvalues are

\[
 \{-0.08967,-0.002945,0.03100,0.12971\}.
\]

The determinant of the state block of Euclidean-normalized stable
eigenvectors is \(0.6097\). The exact Cobb--Douglas human-research path
therefore has the same two-state, two-jump saddle structure as the automated
benchmark. For \(\sigma_{HM}>1\), the limiting static allocation approaches
the automated benchmark; the limiting Jacobian must be checked numerically as
part of the migrated solver rather than copied at finite dates.

## 7. Complementarity in final production

For \(\sigma_{XL}<1\), define the limiting technological share

\[
 \bar s_X=\frac{1-\sigma_{XL}}{1-\alpha\sigma_{XL}}.
\]

On the regular complementary-input limit,

\[
 \frac{X}{AL}\to\bar x,\qquad
 \frac{Z}{AL}\to\bar z,\qquad
 g_Y=g_K=g_X=g_C=G.
\]

Output per person and the real wage grow at \(\gamma_A\), while

\[
 r\to\rho+\gamma_A,\qquad
 \frac KY\to\frac{\alpha}{\rho+\gamma_A+\delta}.
\]

If \(\sigma_{HM}=1\),

\[
 \bar g_B=
 \frac{n+\omega_M\gamma_A}{1+\eta^{-1}-\omega_M},
 \quad
 g_U=g_M=G-\bar g_B,
 \quad
 g_H=n-\bar g_B,
\]

\[
 g_q=G-2\bar g_B,\qquad
 g_{BM}=G,\qquad g_E=\bar g_B/\eta.
\]

If \(\sigma_{HM}>1\),

\[
 \bar g_B=\eta G,\qquad
 g_U=g_M=(1-\eta)G,\qquad
 g_q=(1-2\eta)G,
\]

\[
 g_{BM}=G,\qquad g_E=G,\qquad
 g_H=G-\sigma_{HM}(\eta G+\gamma_A).
\]

In both cases, the terminal ratios used by fixed-horizon collocation are

\[
 \frac{C(T)}{Y(T)}=1-
 \frac{\alpha(G+\delta)}{\rho+\gamma_A+\delta},
\]

\[
 \frac{X(T)}{q(T)B(T)^2}
 =\rho-n+(2-\eta\bar s)\bar g_B.
\]

Setting \(\gamma_A=0\) reproduces the existing formulas exactly.

## 8. Gross substitution and the finite boundary

For \(\sigma_{XL}>1\), no finite-rate balanced-growth terminal condition may
be imposed on the AI-dominated branch. The solver uses

\[
 z_T=\frac{Y(T)}{K(T)}
\]

as an artificial boundary and treats \(T\) as unknown. The leading singular
ratios are unchanged by exogenous labor productivity because \(AL\) is
asymptotically negligible relative to \(X\):

\[
 \frac{C(T)}{Y(T)}\to
 1-(1-\alpha)^2-\alpha+\theta h
 -\frac{\eta(1-\alpha)^2}{1+\theta-\eta},
\]

\[
 \frac{q(T)B(T)}{K(T)}\to
 \frac{(1-\alpha)^2}{\eta\alpha},
 \qquad \frac{Y(T)}{K(T)}=z_T.
\]

The migrated implementation must recheck, rather than assume, that
\(Bw\to\infty\), \(s_M\to1\), and every non-imposed singular ratio converges
as \(z_T\) increases.

## 9. Near-unit continuation

Define

\[
 \varphi=\frac{\sigma_{XL}-1}{\sigma_{XL}},\qquad
 d=\log\frac{X}{AL},\qquad h=\varphi d,
\]

and, for the automated benchmark,

\[
 \nu_X=g_X^*-(n+\gamma_A)
 =\frac{\eta(n+\gamma_A)}{\omega_L-\eta}.
\]

The first experiment grid is

\[
 \sigma_{XL}\in
 \{0.90,0.95,0.98,0.99,1,1.01,1.02,1.05,1.10\}.
\]

Each saved path must include \(d,h\), and the slow time

\[
 \tau=|\varphi|\nu_Xt.
\]

Horizons must increase with \(1/|\sigma_{XL}-1|\). Equal calendar horizons
are useful for common-window comparisons but are not evidence that two
near-unit paths share the same tail.

## 10. Numerical methods by regime

1. Solve the unit-elastic path first.
2. Continue in \(\sigma_{XL}\) with adaptive parameter steps.
3. For \(\sigma_{XL}\leq1\), use fixed-horizon collocation and repeat at
   increasing independent horizons.
4. For \(\sigma_{XL}>1\), use finite-boundary continuation in \(z_T\) and
   compare paths on common pre-terminal windows.
5. Monitor the smallest singular value or condition number of the discretized
   boundary-value Jacobian. Solver success and a small residual are not enough
   when this Jacobian is nearly singular.
6. Use pseudo-arclength continuation if ordinary parameter continuation reaches
   a fold.
7. Preserve log states and detrending. Evaluate the final CES with stable
   `log1p`/`expm1` expressions or its expansion when \(|h|\) is small.

## 11. Regression invariant

Before generating any new economic result, the migrated code must be run with

\[
 A_0=1,\qquad\gamma_A=0,\qquad B_0=A_{0,\mathrm{old}}.
\]

After relabeling columns, the migrated static allocations, four differential
equations, initial jumps, transition paths, terminal ratios, figures, and
tables must agree with the currently audited outputs within their stated
solver tolerances. Any discrepancy larger than tolerance is an economic or
timing change and must be explained before proceeding.

## 12. Acceptance gates

Every reported path must pass all of the following checks:

- positivity and interiority, with the correct KKT condition at an admitted
  corner;
- final production, service identities, research technology, and labor
  clearing;
- factor prices, monopoly first- and second-order conditions, and research
  first-order conditions;
- the resource constraint and consolidated payment identity;
- the four canonical differential equations, reconstructed independently from
  the saved path;
- stability of \(C_0\) and \(q_0\) across horizons or finite boundaries;
- stability on every common reported time window;
- terminal restrictions and non-imposed asymptotic ratios;
- conditioning of the boundary-value derivative;
- the \(1/|\sigma_{XL}-1|\) separation diagnostic around unit elasticity;
- exact recovery of the current audited paths when \(\gamma_A=0\).

## 13. Implementation status

1. **Complete:** rename capability symbols in the paper, appendix, audits, and
   public output metadata without changing the equations.
2. **Complete:** add the exogenous \(A_t\) path and replace production labor by
   \(A_tL_t\).
3. **Complete in the common solver:** implement the automated benchmark \(H=0\)
   and verify its exact balanced path at positive \(\gamma_A\).
4. **Complete:** reproduce and re-audit the reported \(\gamma_A=0\) benchmark
   outputs.
5. **Complete:** migrate the \(\sigma_{HM}=1\) human-research case and verify its
   exact positive-\(\gamma_A\) balanced path.
6. **Complete for the reported paths:** migrate the \(\sigma_{HM}>1\) extension
   and re-solve the complementary, unit-elasticity, and gross-substitutes
   exercises.
7. **Partly complete:** re-solve and audit the near-unit points 0.90, 1.00, and
   1.10. The denser grid, slow-time diagnostic, and explicit Jacobian
   conditioning measure remain to be implemented.
8. **Complete for the currently reported exercises:** regenerate their tables,
   figures, audit reports, and manifests only after the applicable gates pass.

# The Davidson route: persistent investment and uncapped explosion

Research note, 2026-09-12. Starting commit: 53bdf57.

The persistent-investment result below is now incorporated in Proposition 5,
with its proof in the existing proofs appendix. The original proposition and
proof are preserved in `audit/archive/` (see its README). This revision
preserves the model, notation, calibrated parameters, simulation code and
figures; only the relevant manuscript discussion and PDF are updated. No new
transition simulation is computed. The results below are analytical statements about
technology, feasibility and necessary equilibrium conditions, not newly
constructed equilibrium trajectories.

## What the literature contributes

[Davidson, Halperin, Houlden and Korinek (July 2026)](https://basilhalperin.com/papers/singularities.pdf),
Section 3.2, equations (23)-(28) and Proposition 1.*, establish explosive
growth through combined technological and capital-accumulation feedback.
Their benchmark fixes saving and factor-allocation shares. Their Appendix A
uses comparison systems to address depreciation. Pages 21-22 discuss
endogenous saving and refer to Trammell and Korinek; the fixed-saving
qualification is therefore not their final word on optimal behavior.

[Trammell and Korinek](https://philiptrammell.com/static/egtai_new.pdf),
Section 2.1, the paragraph "Saving", use an Euler equation to show why optimal
saving need not neutralize superexponential growth in their setting.
Their displayed example has double-exponential consumption growth, not a
finite-time singularity. It does not by itself verify our monopolist's research
choice. Our proof below is an adaptation of the feedback/comparison method,
not a direct application of their theorem or a change to our saving rule.

## 1. A return bound that holds before AI dominates

Assume sigma > 1, positive capital, AI efficiency and effective labor, and
the static production and monopoly conditions of the paper. Define, only
within this note,

\[
 s=s_X,\qquad \theta=\frac{1-\alpha}{\alpha},\qquad
 d=\left[(1-\alpha)^2\omega_X^{\sigma/(\sigma-1)}\right]^\theta>0.
\]

The existing function is therefore
\(\mathcal R(B)=\alpha dB^\theta-\delta\). The exact static identity proved
in the current Proposition 5 appendix is

\[
 \frac YK=\left[
 \omega_X^{\sigma/(\sigma-1)}B(1-\alpha)
 \left(1-\frac{1-s}{\sigma}-\alpha s\right)
 s^{-1/(\sigma-1)}\right]^\theta.
\]

Let
\[
 f(s)=\left(1-\frac{1-s}{\sigma}-\alpha s\right)s^{-1/(\sigma-1)}.
\]
Its logarithmic derivative has the sign of
\[
 N(s)=(\sigma-2)(1-\alpha\sigma)s-(\sigma-1).
\]
This function is affine in s, and
\[
 N(0)=-(\sigma-1)<0,\qquad
 N(1)=-[1-\alpha+\alpha(\sigma-1)^2]<0.
\]
Thus f is strictly decreasing on (0,1), with f(1)=1-alpha. It follows that

\[
 \boxed{\frac{Y_t}{K_t}\geq d B_t^\theta,
 \qquad r_t\geq\mathcal R(B_t).}
 \tag{D1}
\]

Both inequalities are strict for 0 < s_X < 1; equality is the limiting
case s_X -> 1. This is an actual dated inequality, not an interchange of
the upper-bound limit and the long-run limit. It does not assume
B -> infinity or AI dominance. If B is later shown to diverge along a
global path, D1 implies r -> infinity on that path, but D1 alone says
nothing about whether the endpoint is finite.

## 2. A cleaner conditional nonexistence statement

**Claim.** Let sigma > 1, no upper bound on B, 0 < alpha < 1,
0 < eta < 1, chi > 0, delta >= 0, positive CES weights summing to one,
and nondecreasing positive effective
labor AL, as in the paper. No globally defined feasible path satisfying
the static monopoly conditions can maintain both

\[
 \frac{\dot K+\delta K}{Y}\geq\iota>0,
 \qquad\frac MY\geq\mu>0
 \quad\hbox{for every }t\geq t_0.
 \tag{D2}
\]

Here iota and mu are lower bounds on *gross* capital-investment and research
shares, not new model parameters or imposed equilibrium saving rules.
Feasibility includes C,U,M >= 0, K,B > 0, the resource constraint and the
uncapped research law. Classical continuously differentiable paths suffice.
Every equilibrium is feasible, so D2 also excludes an equilibrium with those
two persistent investment floors.

Unlike the archived Proposition 5, this claim requires no convergence of C/Y or
M/Y, no regularity of their logarithmic derivatives, no limit of s_X, no
assumption that B diverges, and no initial AI-efficiency threshold. Shares
can vary or oscillate. In particular, C/Y need not stay away from zero.

### Proof

Suppose for contradiction that such a path exists for all t >= t0.
All bounds below concern this proposed global path, not an assumed
finite-time explosion.

**First, research makes B eventually exceed every finite level.** For
sigma > 1 the CES also supplies the independent labor lower bound

\[
 Y\geq c_L K^\alpha(AL)^{1-\alpha},\qquad
 c_L=\omega_L^{\sigma(1-\alpha)/(\sigma-1)}>0.
\]

Since AL(t) >= AL(t0), the capital-investment floor gives

\[
 \dot K\geq\iota c_L K^\alpha[AL(t_0)]^{1-\alpha}-\delta K.
\]

If delta > 0, K cannot cross below

\[
 K_{\min}=\min\left\{K(t_0),
 \left(\frac{\iota c_L[AL(t_0)]^{1-\alpha}}{\delta}
 \right)^{1/(1-\alpha)}\right\}>0.
\]

For delta = 0, take K_min = K(t0). Consequently Y is bounded below by
a positive constant Y_min, and M >= mu Y_min. The research law implies

\[
 B_t^{1-\eta}\geq B_{t_0}^{1-\eta}
 +(1-\eta)\chi(\mu Y_{\min})^\eta(t-t_0).
 \tag{D3}
\]

Thus B would tend to infinity if the path were global. This divergence is
derived, not assumed. Nondecreasing AL suffices; positive population or
technology growth is not essential to this step.

**Second, sufficiently high B makes depreciation negligible relative to
the investment floor.** Put z=Y/K. By D1 and D3, there is a finite t1
after which delta/z <= iota/2. Therefore

\[
 \dot K\geq(\iota/2)Y>0,\qquad
 \chi\mu^\eta B^\eta Y^\eta\leq\dot B
 \leq\chi B^\eta Y^\eta.
 \tag{D4}
\]

The upper bound uses M <= Y, which follows from feasibility and positive
gross capital investment. The factor 1/2 is only a convenient proof margin;
any fixed margin strictly between zero and one gives the same conclusion.
It is not a calibration choice or a numerical tolerance.

**Third, capital and AI efficiency reinforce one another.** Because dot B > 0,
we may use B as the independent variable along this path. Use the lower bound
on dot K and the *upper* bound on dot B in D4:

\[
 \frac{\mathrm d K^\eta}{\mathrm dB}
 =\frac{\eta K^{\eta-1}\dot K}{\dot B}
 \geq\frac{\eta\iota}{2\chi} B^{-\eta}z^{1-\eta}
 \geq\frac{\eta\iota d^{1-\eta}}{2\chi}
 B^{(1-\alpha-\eta)/\alpha}.
 \tag{D5}
\]

Dividing two lower bounds would be invalid; the upper research bound in D4
is essential here. Since (1-eta)/alpha > 0, integration yields

\[
 K^\eta\geq K_1^\eta+
 H\left[B^{(1-\eta)/\alpha}-B_1^{(1-\eta)/\alpha}\right],
 \qquad
 H=\frac{\eta\iota\alpha d^{1-\eta}}{2\chi(1-\eta)}>0,
 \tag{D6}
\]

where K1=K(t1) and B1=B(t1). At sufficiently large B,
K^eta >= (H/2) B^{(1-eta)/alpha}. Substituting into the *lower* research
bound gives

\[
 \boxed{\dot B\geq c B^{1/\alpha},\qquad
 c=\frac{\chi\mu^\eta d^\eta H}{2}>0.}
 \tag{D7}
\]

The exponent is greater than one because alpha < 1. This is the cumulative
feedback: the research exponent eta/alpha combines with the capital response
(1-eta)/alpha to give 1/alpha. The calculation is valid below, at and above
eta=alpha, provided 0 < eta < 1. The coefficient depends on eta and vanishes
as eta approaches zero; this argument does not cover eta=0.

**Finally, D7 contradicts an infinite horizon.** For a sufficiently late t2,

\[
 \frac{\mathrm d}{\mathrm dt} B^{1-1/\alpha}
 \leq-(1/\alpha-1)c,
\]
so the positive quantity on the left must reach zero no later than

\[
 t_2+\frac{B(t_2)^{1-1/\alpha}}{(1/\alpha-1)c}<\infty.
\]

This contradicts positive finite B at every finite date. The scalar
integration is the Osgood/comparison step, as in the literature, with all
coefficients obtained from the present model. This proves the claim.

## 3. The technological class is not empty

One can analytically construct feasible allocation rules that satisfy D2.
For example, let gross capital investment and research each equal
(alpha/4)Y, and set

\[
 C=Y-U-\frac\alpha2Y.
\]

Static monopoly pricing implies U/Y=(1-alpha)s_X(1-e_X)<1-alpha.
Thus C/Y > alpha/2 > 0. Solve the two stock laws with these allocation
rules and the unique static monopoly choice at each date. Their smooth
positive solution exists locally for every positive K0,B0, but by the
claim cannot remain globally finite.

For these constant-share rules the finite maximal endpoint is a stock
explosion, not a consumption-positivity boundary. To see this, suppose B
were bounded on a finite interval. The bound Z <= AL+X gives
Y <= K^alpha[(AL)^(1-alpha)+X^(1-alpha)]. Since X=BU and U<=Y,

\[
 Y\leq K^\alpha(AL)^{1-\alpha}+K^\alpha(BY)^{1-\alpha}.
\]

At each date at least one term is >= Y/2. Hence

\[
 Y\leq\max\{2K^\alpha(AL)^{1-\alpha},
                2^{1/\alpha}KB^\theta\}.
\]

Bounded B and AL on a finite interval therefore bound Y by a constant
times 1+K. Gronwall bounds K; the stock vector field then extends unless
B is unbounded. Under these allocation rules B is increasing, so B must
diverge at the finite endpoint. The constant-share equations give exactly

\[
 \frac{\mathrm dK^\eta}{\mathrm dB}
 =\frac{\eta}{\chi(\alpha/4)^\eta}
 \left(\frac\alpha4-\frac\delta z\right)
 z^{1-\eta}B^{-\eta}.
\]

For large B, D1 makes the bracket positive and bounded away from zero;
integration as in D6 gives K -> infinity. D1 then gives Y,r -> infinity,
and the consumption floor gives C -> infinity. Thus technological
feasibility permits a finite-time explosion for each 0 < eta < 1 and
each sigma > 1, including eta < alpha.

These allocation rules need NOT solve the household and developer's
dynamic problems. They are an existence construction for an explosive
technological path up to its maximal endpoint, NOT an equilibrium or a
simulation to present as an equilibrium. No such trajectory has been plotted
or added to the paper's numerical results.

## 4. What optimality contributes, and what remains missing

The household Euler equation gives
\[
 \frac{\dot C}{C}=n+r-\rho\geq n+\mathcal R(B)-\rho.
\]
This is consistent with the saving argument in Trammell and Korinek, but
does not by itself supply both investment floors in D2. Household saving
finances two distinct uses: capital accumulation and the developer's
research. A claim about saving cannot silently become a lower bound on
each use separately.

For the developer, differentiating the research FOC and substituting the
uncapped costate equation gives the exact necessary condition

\[
 (1-\eta)\frac{\dot M}{M}
 =r-\eta\chi U B^{\eta-1}M^{\eta-1},
\]
or, equivalently, for the proof variable P=M^(1-eta),
\[
 \dot P=rP-\eta\chi U B^{\eta-1}.
 \tag{D8}
\]

Write D_t=exp(-integral_0^t r_v dv). The research FOC implies
P=chi eta q B^eta. Since B is nondecreasing, the developer TVC
D_t q_t B_t -> 0 implies D_t P_t -> 0. Integrating D8 gives

\[
 \boxed{M_t^{1-\eta}=\eta\chi\int_t^\infty
 \exp\left(-\int_t^s r_v\,\mathrm dv\right)
 U_sB_s^{\eta-1}\,\mathrm ds.}
 \tag{D9}
\]

This equation ties current research to future discounted inference-cost
savings. It is a necessary implication of the FOC, costate equation and
TVC, not a new behavioral rule or a sufficient global-optimality theorem.
The positive right side implies M_t > 0 for a finite-valued interior
candidate with positive future inference use. Pointwise positivity does
not establish M_t/Y_t >= mu > 0 uniformly as t grows.

Crucially, r >= R(B) is a *lower* bound on the discount rate. On its own,
it supplies an upper bound on discount factors, not the lower bound on
the integral needed to prove a research-share floor. Future U and B must
be analyzed jointly with discounting. This is the missing incentive step,
not an omitted direct application of Davidson's technology theorem.

The new claim gives the following necessary restriction on any globally
finite equilibrium: its gross capital-investment and research shares
cannot BOTH have strictly positive liminf. If gross capital investment is
nonnegative, at least one of those liminf must be zero. This does not prove
that an equilibrium with vanishing or intermittently small shares exists.
It identifies the alternatives an unconditional nonexistence proof must
exclude. For eta > alpha the independent unbounded-profit argument already
excludes a finite-valued developer optimum, without D2. For eta <= alpha,
general nonexistence is not established by this note.

## 5. Precisely what Section 4 supplies

The function R(B) in D1 is exactly Section 4's return function. Its static
derivation can be strengthened from a limit as s_X -> 1 to the dated lower
bound D1. This avoids exchanging a limit of capped equilibria with an
uncapped trajectory. It is a key ingredient of Steps 2-3 above. Crossing
the Section 4 threshold B(sigma) also implies r > rho+gamma and hence
consumption-per-person growth > gamma through the Euler equation. It does
not by itself imply the same instantaneous growth comparison for output.

Section 4's AI-dominated construction gives, for each fixed finite Bbar,

\[
 \overline g=n+\mathcal R(\overline B)-\rho>n+\gamma,\qquad
 M\longrightarrow
 \left[\frac{\overline g\,\overline B^{1-\eta}}{\chi}\right]^{1/\eta}.
\]

The exact references are `eq:rewrite-substitutes-terminal-growth` and
`eq:rewrite-ai-terminal-values` in `appendix_finite_frontier.tex`.
Since Y grows at a positive limiting rate and M has a finite positive
limit, M/Y -> 0. The capital-investment share instead satisfies

\[
 \frac{\dot K+\delta K}{Y}\longrightarrow
 \frac{\alpha[n+\mathcal R(\overline B)-\rho+\delta]}
 {\mathcal R(\overline B)+\delta}
 =\alpha-\frac{\alpha(\rho-n)}{\mathcal R(\overline B)+\delta}.
\]

It is strictly between zero and alpha and tends to alpha as Bbar -> infinity.
Thus the existing equilibria do supply an eventual positive capital-investment
share for each bound, but cannot supply a positive uniform research-share floor:
their limiting research share is zero for EVERY finite bound. This is not a
counterexample to the uncapped theorem, since their research law includes psi.
Nor does it prove vanishing research shares in the uncapped economy.

The incentive difference can be seen without a limit interchange. For either
research law define P=M^(1-eta)=chi eta q B^eta psi(B). Differentiation gives

\[
 \dot P=rP-\chi\eta U B^{\eta-1}\psi(B).
\]

The psi derivative in the FOC cancels its counterpart in the costate equation.
The TVC argument used for D9 still applies since 0 < psi <= 1, and gives

\[
 M_t^{1-\eta}=\chi\eta\int_t^\infty
 \exp\left(-\int_t^s r_v\,dv\right)
 U_s B_s^{\eta-1}\psi(B_s)\,ds.
\]

In the uncapped economy psi is identically one; near a finite bound it
approaches zero. This explains why copying terminal research allocations
across the two problems is not an optimality argument. The upper-bound
limit at a fixed date would additionally require control of endogenous
prices, values and initial states. Section 4 only constructs local initial
stock neighborhoods depending on Bbar; it gives no common-initial-state,
uniform-in-Bbar compactness or value bound.

The outstanding task is therefore specific: derive restrictions on investment
shares (possibly averaged over time) from the household Euler/TVC conditions,
the developer's PV identity, and feasibility. An inference of the form
"r is large, therefore both uses receive positive shares" skips the allocation
between research and physical capital. D1 is a lower bound on r and thus an
upper bound on discount factors; a lower bound on research's PV requires
additional control of the future inference flow. These observations locate
the remaining step; they are not a proof that the step is impossible.

## Adoption and verification

The new condition replaces the original Proposition 5's asymptotic regularity
conditions. Section 5.3 now distinguishes the claim excluding persistent
positive investment shares from the stronger, still unproved claim that no
equilibrium exists at all for eta <= alpha. It also includes D1, D9 and the
Section 4 investment limits. The old asymptotic result and its exact algebra
tests are retained as archived research material, not active manuscript text.

Next: use D8-D9 together with household optimality and the resource constraint
to investigate vanishing or intermittent investment shares. The lower-bound
approach may extend to time-averaged investment, but no such extension is
claimed here. The result is not uniform as sigma -> 1: d can become extremely
small. It predicts no date for an economic transition.

Reproduce the algebra checks (not equilibrium simulations) from the repo root:

```powershell
python -B -X utf8 -m unittest discover -s tests -p test_rewrite_davidson_route.py -v
```

The tests check the exact derivative signs, static return bound, feedback
exponents and integral coefficient on both sides of eta=alpha, feasibility
of the analytical constant-share rule, and the transformed research Euler
identity. Numerical checks supplement but do not replace the proof.

Initial verification on 2026-09-12: all seven original tests passed. The
research present-value identity was additionally checked against the existing
analytical unit-elastic equilibrium, where it reproduces the research level.
This is a check of the identity, not an application of the explosion claim
to sigma=1. The tested derivative/return grids include alpha=0.01, 0.2, 0.33,
0.6, 0.99 and sigma=1.0001, 1.001, 1.01, 1.5, 2, 4, 100 (as applicable).
Exact feedback checks use eta=alpha/2, alpha, (1+alpha)/2 for alpha=0.2, 0.33,
0.6. No numerical blow-up trajectory was used as evidence for the theorem.
The adoption adds source checks of the new proposition, analytical checks of
the capped investment/research limits, and the research-FOC/costate cancellation
with and without the psi factor.

Final adoption verification on 2026-09-12: all 62 tests in the eight-module
targeted suite passed, including all 10 tests in `test_rewrite_davidson_route`.
The suite covers the preserved companion/unit-elastic results, finite-bound
algebra and linearizations, complementary case, positive-AI branch, archived
asymptotic result, new comparison proof, and active references. These tests
are algebra/source checks, not a substitute for the written existence or
nonexistence proofs and not new equilibrium transition simulations.

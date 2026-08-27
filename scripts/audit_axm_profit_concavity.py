"""Common optimality checks for nonunit final-production elasticities.

After the developer has optimized AI-service sales, let ``pi_t(B)`` denote
operating profit before research expenditure. The envelope theorem gives
``pi_B=X/B**2``. Hence ``pi_t`` is concave at a dated allocation exactly when
the elasticity of optimal service supply with respect to capability is no
larger than two.

This module evaluates that condition from the CES service share. It also
recovers the largest share reachable from a lower capability bound without
calling the equilibrium solver. The calculation is used as an admission gate;
a positive pointwise monopoly second-order condition alone is not enough to
establish global optimality of the developer's dynamic policy.
"""

from __future__ import annotations

import math


def inverse_demand_elasticity(
    share: float, sigma_xl: float, alpha: float
) -> float:
    """Return ``e_X`` in the paper's inverse-demand notation."""

    return (1.0 - share) / sigma_xl + alpha * share


def service_capability_elasticity(
    share: float, sigma_xl: float, alpha: float
) -> float:
    """Return ``d log X*(B) / d log B`` at a dated optimum."""

    inverse_sigma = 1.0 / sigma_xl
    inverse_elasticity = inverse_demand_elasticity(
        share, sigma_xl, alpha
    )
    soc_denominator = (
        inverse_elasticity * (1.0 - inverse_elasticity)
        + (alpha - inverse_sigma)
        * (1.0 - inverse_sigma)
        * share
        * (1.0 - share)
    )
    if soc_denominator <= 0.0:
        raise ValueError("The pointwise monopoly second-order condition fails.")
    return (1.0 - inverse_elasticity) / soc_denominator


def _log_ces_ratio_from_share(
    share: float, sigma_xl: float, omega_x: float
) -> tuple[float, float]:
    """Return ``(log(X/AL), log(Z/AL))`` from the CES share."""

    if not 0.0 < share < 1.0:
        raise ValueError("The CES share must be strictly between zero and one.")
    if sigma_xl == 1.0:
        raise ValueError("This recovery is only needed away from unit elasticity.")
    omega_l = 1.0 - omega_x
    varphi = (sigma_xl - 1.0) / sigma_xl
    log_ratio = (
        math.log(share)
        - math.log1p(-share)
        + math.log(omega_l)
        - math.log(omega_x)
    ) / varphi
    left = math.log(omega_l)
    right = math.log(omega_x) + varphi * log_ratio
    maximum = max(left, right)
    log_composite = (
        maximum
        + math.log(math.exp(left - maximum) + math.exp(right - maximum))
    ) / varphi
    return log_ratio, log_composite


def _log_marginal_revenue_component(
    share: float,
    sigma_xl: float,
    alpha: float,
    omega_x: float,
) -> float:
    """Return the share-dependent part of log marginal revenue."""

    log_ratio, log_composite = _log_ces_ratio_from_share(
        share, sigma_xl, omega_x
    )
    inverse_elasticity = inverse_demand_elasticity(
        share, sigma_xl, alpha
    )
    if inverse_elasticity >= 1.0:
        return -math.inf
    return (
        math.log(share)
        + (1.0 - alpha) * log_composite
        - log_ratio
        + math.log1p(-inverse_elasticity)
    )


def share_at_lower_capability(
    *,
    current_share: float,
    log_current_capability: float,
    log_lower_capability: float,
    sigma_xl: float,
    alpha: float,
    omega_x: float,
) -> float:
    """Recover the service share at the same date and a lower ``B``.

    For ``sigma_xl<1``, optimal service supply rises with capability while the
    CES service share falls. The monopoly first-order condition therefore
    supplies a monotone scalar equation for the counterfactual share at the
    lower capability bound. Only that branch is needed for the complementary
    paths admitted by the paper.
    """

    if not sigma_xl < 1.0:
        raise ValueError("The lower-capability recovery requires sigma_xl < 1.")
    if log_lower_capability > log_current_capability + 1.0e-12:
        raise ValueError("The proposed capability bound exceeds current B.")
    if math.isclose(
        log_lower_capability, log_current_capability, abs_tol=1.0e-13
    ):
        return current_share

    target = (
        log_current_capability
        + _log_marginal_revenue_component(
            current_share, sigma_xl, alpha, omega_x
        )
        - log_lower_capability
    )

    lower = current_share
    upper = 1.0 - 1.0e-13

    def residual(share: float) -> float:
        return (
            _log_marginal_revenue_component(
                share, sigma_xl, alpha, omega_x
            )
            - target
        )

    if residual(lower) > 1.0e-11 or residual(upper) < 0.0:
        raise RuntimeError("Could not bracket the counterfactual service share.")
    for _ in range(180):
        midpoint = 0.5 * (lower + upper)
        if residual(midpoint) < 0.0:
            lower = midpoint
        else:
            upper = midpoint
    return 0.5 * (lower + upper)


def maximum_service_capability_elasticity(
    *,
    lower_share: float,
    upper_share: float,
    sigma_xl: float,
    alpha: float,
) -> dict[str, float]:
    """Maximize the rational elasticity exactly over a share interval.

    The numerator is linear and the denominator quadratic in the CES share.
    The derivative therefore has at most two interior roots. Evaluating those
    roots and the interval endpoints avoids an arbitrary numerical grid.
    """

    if not 0.0 <= lower_share <= upper_share < 1.0:
        raise ValueError("Invalid CES-share interval.")
    inverse_sigma = 1.0 / sigma_xl
    slope = alpha - inverse_sigma
    numerator_0 = 1.0 - inverse_sigma
    numerator_1 = inverse_sigma - alpha
    denominator_0 = inverse_sigma * (1.0 - inverse_sigma)
    denominator_1 = slope * (2.0 - 3.0 * inverse_sigma)
    denominator_2 = -slope * (alpha + 1.0 - 2.0 * inverse_sigma)

    derivative_0 = (
        numerator_1 * denominator_0
        - numerator_0 * denominator_1
    )
    derivative_1 = -2.0 * numerator_0 * denominator_2
    derivative_2 = -numerator_1 * denominator_2

    candidates = [lower_share, upper_share]
    if abs(derivative_2) <= 1.0e-15:
        if abs(derivative_1) > 1.0e-15:
            candidates.append(-derivative_0 / derivative_1)
    else:
        discriminant = (
            derivative_1 * derivative_1
            - 4.0 * derivative_2 * derivative_0
        )
        if discriminant >= 0.0:
            root = math.sqrt(discriminant)
            candidates.extend(
                [
                    (-derivative_1 - root) / (2.0 * derivative_2),
                    (-derivative_1 + root) / (2.0 * derivative_2),
                ]
            )

    admissible = [
        value
        for value in candidates
        if lower_share <= value <= upper_share
    ]
    values = [
        (service_capability_elasticity(value, sigma_xl, alpha), value)
        for value in admissible
        if inverse_demand_elasticity(value, sigma_xl, alpha) < 1.0
    ]
    maximum, maximizing_share = max(values)
    return {
        "maximum_service_capability_elasticity": maximum,
        "maximizing_share": maximizing_share,
        "profit_concavity_margin": 2.0 - maximum,
    }

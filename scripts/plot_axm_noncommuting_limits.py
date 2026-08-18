"""Numerical illustration of the non-commuting final-production limits.

The experiment holds production labor fixed and varies the log AI-service to
labor ratio.  It evaluates the paper's CES aggregate exactly for elasticities
on both sides of one.  This is a technology experiment, not an equilibrium
path: the model determines endogenously how fast X/L changes over calendar
time.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np
import scipy  # noqa: F401  # Load the audited dependency before the core path shim.
from PIL import Image, ImageDraw

import simulate_axm_equilibrium as core


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "numerical_axm" / "noncommuting_limits_technology.csv"
FIGURE_PATH = ROOT / "figures_axm" / "axm_noncommuting_limits.png"

SIGMAS = (0.90, 0.95, 1.00, 1.05, 1.10)
LOG_RATIOS = np.linspace(0.0, 80.0, 321)
PARAMETERS = core.Parameters()

LABELS = {
    0.90: "elasticity = 0.90",
    0.95: "elasticity = 0.95",
    1.00: "elasticity = 1.00",
    1.05: "elasticity = 1.05",
    1.10: "elasticity = 1.10",
}
PALETTE = {
    0.90: core.mechanism.COLORS["blue"],
    0.95: core.mechanism.COLORS["olive"],
    1.00: core.mechanism.COLORS["ink"],
    1.05: core.mechanism.COLORS["gold"],
    1.10: core.mechanism.COLORS["orange"],
}
LINE_WIDTHS = {0.90: 5, 0.95: 4, 1.00: 5, 1.05: 4, 1.10: 5}


def logsumexp_pair(left: float, right: float) -> float:
    maximum = max(left, right)
    return maximum + math.log(
        math.exp(left - maximum) + math.exp(right - maximum)
    )


def logistic(value: float) -> float:
    if value >= 0.0:
        negative = math.exp(-value)
        return 1.0 / (1.0 + negative)
    positive = math.exp(value)
    return positive / (1.0 + positive)


def technology_values(sigma: float, log_ratio: float) -> dict[str, float]:
    omega_x = PARAMETERS.omega_x
    alpha = PARAMETERS.alpha
    if math.isclose(sigma, 1.0):
        log_composite = omega_x * log_ratio
        ai_share = omega_x
    else:
        rho = (sigma - 1.0) / sigma
        labor_term = math.log1p(-omega_x)
        ai_term = math.log(omega_x) + rho * log_ratio
        log_composite = logsumexp_pair(labor_term, ai_term) / rho
        ai_share = logistic(ai_term - labor_term)
    log_cobb_douglas = omega_x * log_ratio
    return {
        "log_ai_labor_ratio": log_ratio,
        "log_composite_relative_to_unit": log_composite - log_cobb_douglas,
        "ai_share": ai_share,
        "production_labor_payment_share": (1.0 - alpha) * (1.0 - ai_share),
        "gross_ai_service_payment_share": (1.0 - alpha) * ai_share,
    }


def build_rows() -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for sigma in SIGMAS:
        for log_ratio in LOG_RATIOS:
            rows.append(
                {
                    "sigma_xl": sigma,
                    "alpha": PARAMETERS.alpha,
                    "omega_x": PARAMETERS.omega_x,
                    **technology_values(sigma, float(log_ratio)),
                }
            )
    return rows


def validate_rows(rows: list[dict[str, float]]) -> None:
    maximum_payment_error = max(
        abs(
            row["production_labor_payment_share"]
            + row["gross_ai_service_payment_share"]
            - (1.0 - PARAMETERS.alpha)
        )
        for row in rows
    )
    if maximum_payment_error > 1e-13:
        raise RuntimeError(
            f"The noncapital payment identity fails by {maximum_payment_error:.3e}."
        )
    at_zero = [
        row for row in rows if math.isclose(row["log_ai_labor_ratio"], 0.0)
    ]
    if max(abs(row["ai_share"] - PARAMETERS.omega_x) for row in at_zero) > 1e-13:
        raise RuntimeError("The CES shares do not coincide at X/L=1.")
    unit_rows = [row for row in rows if math.isclose(row["sigma_xl"], 1.0)]
    if max(abs(row["ai_share"] - PARAMETERS.omega_x) for row in unit_rows) > 1e-13:
        raise RuntimeError("The unit-elasticity AI share is not constant.")


def write_rows(rows: list[dict[str, float]]) -> None:
    DATA_PATH.parent.mkdir(exist_ok=True)
    with DATA_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def draw_marker(
    draw: ImageDraw.ImageDraw,
    x: float,
    y: float,
    color: str,
    radius: int = 6,
) -> None:
    draw.ellipse(
        (x - radius, y - radius, x + radius, y + radius),
        fill="white",
        outline=color,
        width=3,
    )


def draw_figure(rows: list[dict[str, float]]) -> None:
    width, height = 2400, 1780
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    title_font = core.mechanism.load_font(48, bold=True)
    subtitle_font = core.mechanism.load_font(27)
    panel_font = core.mechanism.load_font(29, bold=True)
    axis_font = core.mechanism.load_font(22)
    legend_font = core.mechanism.load_font(23)

    draw.text(
        (120, 55),
        "Near-unit elasticities: finite-input similarity and limiting divergence",
        fill=core.mechanism.COLORS["ink"],
        font=title_font,
    )
    draw.text(
        (120, 120),
        "Exact CES technology experiment; the horizontal axis is ln(X/L), not calendar time",
        fill=core.mechanism.COLORS["muted"],
        font=subtitle_font,
    )

    legend_y = 185
    legend_x = 160
    for sigma in SIGMAS:
        color = PALETTE[sigma]
        draw.line(
            (legend_x, legend_y + 10, legend_x + 55, legend_y + 10),
            fill=color,
            width=LINE_WIDTHS[sigma],
        )
        draw_marker(draw, legend_x + 28, legend_y + 10, color, radius=5)
        draw.text(
            (legend_x + 68, legend_y - 4),
            LABELS[sigma],
            fill=core.mechanism.COLORS["ink"],
            font=legend_font,
        )
        legend_x += 420

    panels = (
        (
            "Log composite ratio, ln[Z(sigma)/Z(1)]",
            "log_composite_relative_to_unit",
            (-15.0, 50.0),
            lambda value: f"{value:.0f}",
        ),
        (
            "Elasticity of the composite with respect to AI services, s_X",
            "ai_share",
            (0.0, 1.0),
            lambda value: f"{100.0 * value:.0f}%",
        ),
        (
            "Production-labor payment / output, wL/Y",
            "production_labor_payment_share",
            (0.0, 0.67),
            lambda value: f"{100.0 * value:.0f}%",
        ),
        (
            "Gross AI-service payment / output, p_X X/Y",
            "gross_ai_service_payment_share",
            (0.0, 0.67),
            lambda value: f"{100.0 * value:.0f}%",
        ),
    )
    boxes = (
        (110, 300, 1160, 950),
        (1240, 300, 2290, 950),
        (110, 1030, 1160, 1680),
        (1240, 1030, 2290, 1680),
    )
    grouped = {
        sigma: [row for row in rows if math.isclose(row["sigma_xl"], sigma)]
        for sigma in SIGMAS
    }

    for (panel_title, field, (y_min, y_max), formatter), box in zip(panels, boxes):
        left, top, right, bottom = box
        plot_left, plot_top = left + 125, top + 75
        plot_right, plot_bottom = right - 35, bottom - 95
        draw.text(
            (left, top),
            panel_title,
            fill=core.mechanism.COLORS["ink"],
            font=panel_font,
        )
        y_ticks = (
            (-15.0, 0.0, 15.0, 30.0, 45.0, 50.0)
            if field == "log_composite_relative_to_unit"
            else np.linspace(y_min, y_max, 5)
        )
        for tick in y_ticks:
            y_pixel = plot_bottom - (tick - y_min) / (y_max - y_min) * (
                plot_bottom - plot_top
            )
            draw.line(
                (plot_left, y_pixel, plot_right, y_pixel),
                fill=core.mechanism.COLORS["grid"],
                width=2,
            )
            label = formatter(float(tick))
            bounds = draw.textbbox((0, 0), label, font=axis_font)
            draw.text(
                (plot_left - 14 - (bounds[2] - bounds[0]), y_pixel - 12),
                label,
                fill=core.mechanism.COLORS["muted"],
                font=axis_font,
            )
        for tick in (0.0, 20.0, 40.0, 60.0, 80.0):
            x_pixel = plot_left + tick / 80.0 * (plot_right - plot_left)
            draw.line(
                (x_pixel, plot_bottom, x_pixel, plot_bottom + 8),
                fill=core.mechanism.COLORS["ink"],
                width=2,
            )
            label = f"{tick:.0f}"
            bounds = draw.textbbox((0, 0), label, font=axis_font)
            draw.text(
                (x_pixel - (bounds[2] - bounds[0]) / 2, plot_bottom + 14),
                label,
                fill=core.mechanism.COLORS["muted"],
                font=axis_font,
            )
        axis_label = "ln(X/L)"
        bounds = draw.textbbox((0, 0), axis_label, font=axis_font)
        draw.text(
            (
                (plot_left + plot_right - (bounds[2] - bounds[0])) / 2,
                plot_bottom + 50,
            ),
            axis_label,
            fill=core.mechanism.COLORS["muted"],
            font=axis_font,
        )
        draw.line(
            (plot_left, plot_top, plot_left, plot_bottom),
            fill=core.mechanism.COLORS["ink"],
            width=3,
        )
        draw.line(
            (plot_left, plot_bottom, plot_right, plot_bottom),
            fill=core.mechanism.COLORS["ink"],
            width=3,
        )
        for sigma in SIGMAS:
            series = grouped[sigma]
            points = []
            for row in series:
                x_value = row["log_ai_labor_ratio"]
                y_value = row[field]
                x_pixel = plot_left + x_value / 80.0 * (plot_right - plot_left)
                y_pixel = plot_bottom - (y_value - y_min) / (y_max - y_min) * (
                    plot_bottom - plot_top
                )
                points.append((x_pixel, y_pixel))
            draw.line(points, fill=PALETTE[sigma], width=LINE_WIDTHS[sigma])
            for index in (0, 80, 160, 240, 320):
                draw_marker(draw, *points[index], PALETTE[sigma])

    FIGURE_PATH.parent.mkdir(exist_ok=True)
    image.save(FIGURE_PATH)


def main() -> None:
    rows = build_rows()
    validate_rows(rows)
    write_rows(rows)
    draw_figure(rows)
    print(
        f"Wrote {DATA_PATH.relative_to(ROOT)} and {FIGURE_PATH.relative_to(ROOT)} "
        f"from {len(rows):,} exact CES evaluations.",
        flush=True,
    )


if __name__ == "__main__":
    main()

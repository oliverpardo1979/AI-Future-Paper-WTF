"""Plot the audited unit-elastic AI-adoption experiment.

The script verifies the accepted simulation manifest and its source hashes
before drawing two paper figures with Pillow.  The first figure reports the
macroeconomic transition.  The second reports growth, capability, the shadow
value of capability, and the consolidated income decomposition.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Callable

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
RESULT_DIR = ROOT / "numerical_axm"
FIGURE_DIR = ROOT / "figures_axm"
PATH_FILE = RESULT_DIR / "ai_adoption_unit_elasticity_paths.csv"
SUMMARY_FILE = RESULT_DIR / "ai_adoption_unit_elasticity_summary.csv"
MANIFEST_FILE = RESULT_DIR / "ai_adoption_unit_elasticity_audit_manifest.json"
MACRO_FILE = FIGURE_DIR / "axm_ai_adoption_macro.png"
MECHANISM_FILE = FIGURE_DIR / "axm_ai_adoption_mechanism_distribution.png"
DISTRIBUTION_FILE = FIGURE_DIR / "axm_ai_adoption_income_shares.png"

AI_COLOR = "#205493"
NO_AI_COLOR = "#66717E"
BGP_COLOR = "#C69214"
INK = "#22272E"
MUTED = "#66717E"
GRID = "#D9DEE5"
WHITE = "#FFFFFF"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_manifest() -> dict[str, object]:
    with MANIFEST_FILE.open("r", encoding="utf-8") as handle:
        manifest = json.load(handle)
    if manifest.get("accepted") is not True:
        raise ValueError("The AI-adoption audit manifest is not accepted.")
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, dict):
        raise ValueError("The audit manifest has no artifact map.")
    expected = {
        "paths": PATH_FILE,
        "summary": SUMMARY_FILE,
    }
    for key, path in expected.items():
        record = artifacts.get(key)
        if not isinstance(record, dict):
            raise ValueError(f"Missing manifest record for {key}.")
        if sha256_file(path).lower() != str(record.get("sha256", "")).lower():
            raise ValueError(f"Hash mismatch for {path}.")
        if path.stat().st_size != int(record.get("bytes", -1)):
            raise ValueError(f"Size mismatch for {path}.")
    return manifest


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"No observations found in {path}.")
    return rows


def number(row: dict[str, str], field: str) -> float:
    value = float(row[field])
    if not math.isfinite(value):
        raise ValueError(f"Non-finite {field}.")
    return value


def font(size: int, *, bold: bool = False) -> ImageFont.ImageFont:
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(name, size=size)


def text_right(
    draw: ImageDraw.ImageDraw,
    xy: tuple[float, float],
    value: str,
    *,
    fill: str,
    text_font: ImageFont.ImageFont,
) -> None:
    bounds = draw.textbbox((0, 0), value, font=text_font)
    draw.text(
        (xy[0] - (bounds[2] - bounds[0]), xy[1]),
        value,
        fill=fill,
        font=text_font,
    )


def text_center(
    draw: ImageDraw.ImageDraw,
    xy: tuple[float, float],
    value: str,
    *,
    fill: str,
    text_font: ImageFont.ImageFont,
) -> None:
    bounds = draw.textbbox((0, 0), value, font=text_font)
    draw.text(
        (xy[0] - (bounds[2] - bounds[0]) / 2, xy[1]),
        value,
        fill=fill,
        font=text_font,
    )


def patterned_line(
    draw: ImageDraw.ImageDraw,
    points: list[tuple[float, float]],
    *,
    fill: str,
    width: int,
    pattern: tuple[float, ...] | None = None,
) -> None:
    if len(points) < 2:
        return
    if pattern is None:
        draw.line(points, fill=fill, width=width, joint="curve")
        return
    pattern_index = 0
    remaining = pattern[0]
    drawing = True
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        dx, dy = x1 - x0, y1 - y0
        segment = math.hypot(dx, dy)
        if segment <= 0.0:
            continue
        used = 0.0
        while used < segment - 1.0e-9:
            step = min(remaining, segment - used)
            f0 = used / segment
            f1 = (used + step) / segment
            start = (x0 + dx * f0, y0 + dy * f0)
            end = (x0 + dx * f1, y0 + dy * f1)
            if drawing:
                draw.line((start, end), fill=fill, width=width)
            used += step
            remaining -= step
            if remaining <= 1.0e-9:
                pattern_index = (pattern_index + 1) % len(pattern)
                remaining = pattern[pattern_index]
                drawing = pattern_index % 2 == 0


def draw_header(
    draw: ImageDraw.ImageDraw,
    title: str,
    subtitle: str,
    *,
    show_scenario_legend: bool,
) -> None:
    draw.text((105, 42), title, fill=INK, font=font(50, bold=True))
    draw.text((105, 105), subtitle, fill=MUTED, font=font(29))
    if show_scenario_legend:
        legend_y = 166
        patterned_line(
            draw,
            [(110, legend_y + 13), (175, legend_y + 13)],
            fill=AI_COLOR,
            width=7,
        )
        draw.text(
            (190, legend_y),
            "AI adoption: ωₓ = 0.20",
            fill=INK,
            font=font(31),
        )
        patterned_line(
            draw,
            [(755, legend_y + 13), (820, legend_y + 13)],
            fill=NO_AI_COLOR,
            width=5,
            pattern=(16.0, 10.0),
        )
        draw.text(
            (835, legend_y),
            "No-AI counterfactual: ωₓ = 0",
            fill=INK,
            font=font(31),
        )


def draw_line_panel(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    rows: list[dict[str, str]],
    *,
    title: str,
    subtitle: str,
    series: tuple[tuple[str, str, tuple[float, ...] | None, int], ...],
    y_ticks: tuple[float, ...],
    y_formatter: Callable[[float], str],
    log_scale: bool = False,
    x_max: float = 250.0,
    x_ticks: tuple[float, ...] | None = None,
) -> None:
    left, top, right, bottom = box
    panel_title_font = font(36, bold=True)
    panel_subtitle_font = font(25)
    tick_font = font(27)
    draw.text((left, top), title, fill=INK, font=panel_title_font)
    draw.text((left, top + 46), subtitle, fill=MUTED, font=panel_subtitle_font)
    plot_left = left + 112
    plot_right = right - 28
    plot_top = top + 96
    plot_bottom = bottom - 72

    def transform(value: float) -> float:
        if log_scale:
            if value <= 0.0:
                raise ValueError(f"Log-scale panel received {value}.")
            return math.log(value)
        return value

    transformed_ticks = [transform(value) for value in y_ticks]
    y_min, y_max = min(transformed_ticks), max(transformed_ticks)
    if y_max <= y_min:
        raise ValueError("The y-axis requires at least two distinct ticks.")

    def y_pixel(value: float) -> float:
        transformed = transform(value)
        return plot_bottom - (transformed - y_min) / (y_max - y_min) * (
            plot_bottom - plot_top
        )

    for tick in y_ticks:
        y = y_pixel(tick)
        draw.line((plot_left, y, plot_right, y), fill=GRID, width=2)
        text_right(
            draw,
            (plot_left - 14, y - 14),
            y_formatter(tick),
            fill=MUTED,
            text_font=tick_font,
        )
    draw.line((plot_left, plot_top, plot_left, plot_bottom), fill=INK, width=3)
    draw.line((plot_left, plot_bottom, plot_right, plot_bottom), fill=INK, width=3)

    if x_ticks is None:
        x_ticks = (0.0, 50.0, 100.0, 150.0, 200.0, 250.0)
    if any(tick < 0.0 or tick > x_max for tick in x_ticks):
        raise ValueError("Every x-axis tick must lie within the plotted range.")
    for tick in x_ticks:
        x = plot_left + tick / x_max * (plot_right - plot_left)
        draw.line((x, plot_bottom, x, plot_bottom + 8), fill=INK, width=2)
        text_center(
            draw,
            (x, plot_bottom + 13),
            f"{tick:.0f}",
            fill=MUTED,
            text_font=tick_font,
        )
    text_center(
        draw,
        ((plot_left + plot_right) / 2, plot_bottom + 45),
        "Years since adoption",
        fill=MUTED,
        text_font=tick_font,
    )

    for field, color, pattern, width in series:
        points: list[tuple[float, float]] = []
        for row in rows:
            time = number(row, "time")
            if time > x_max + 1.0e-12:
                continue
            value = number(row, field)
            x = plot_left + time / x_max * (plot_right - plot_left)
            points.append((x, y_pixel(value)))
        patterned_line(
            draw,
            points,
            fill=color,
            width=width,
            pattern=pattern,
        )
        if points:
            x, y = points[-1]
            draw.ellipse(
                (x - 5, y - 5, x + 5, y + 5),
                fill=color,
                outline=WHITE,
                width=2,
            )


def draw_macro(rows: list[dict[str, str]]) -> None:
    image = Image.new("RGB", (2400, 1800), WHITE)
    draw = ImageDraw.Draw(image)
    draw_header(
        draw,
        "Macroeconomic transition after AI adoption",
        "Both economies start from the no-AI balanced-growth path; σₓₗ = 1",
        show_scenario_legend=True,
    )
    boxes = (
        (105, 250, 1170, 985),
        (1280, 250, 2345, 985),
        (105, 1035, 1170, 1770),
        (1280, 1035, 2345, 1770),
    )
    level_ticks = (0.5, 1.0, 2.0, 5.0, 10.0, 20.0)
    common_series = lambda ai, no_ai: (
        (ai, AI_COLOR, None, 7),
        (no_ai, NO_AI_COLOR, (16.0, 10.0), 5),
    )
    draw_line_panel(
        draw,
        boxes[0],
        rows,
        title="A. Output per person",
        subtitle="Common date-zero no-AI index; logarithmic vertical scale",
        series=common_series("ai_output_pc_index", "no_ai_output_pc_index"),
        y_ticks=level_ticks,
        y_formatter=lambda value: f"{value:g}",
        log_scale=True,
    )
    draw_line_panel(
        draw,
        boxes[1],
        rows,
        title="B. Consumption per person",
        subtitle="Common date-zero no-AI index; logarithmic vertical scale",
        series=common_series(
            "ai_consumption_pc_index", "no_ai_consumption_pc_index"
        ),
        y_ticks=level_ticks,
        y_formatter=lambda value: f"{value:g}",
        log_scale=True,
    )
    draw_line_panel(
        draw,
        boxes[2],
        rows,
        title="C. Real wage",
        subtitle="Common date-zero no-AI index; logarithmic vertical scale",
        series=common_series("ai_wage_index", "no_ai_wage_index"),
        y_ticks=level_ticks,
        y_formatter=lambda value: f"{value:g}",
        log_scale=True,
    )
    draw_line_panel(
        draw,
        boxes[3],
        rows,
        title="D. Net interest rate",
        subtitle="Annual percent; 3,000-year audit; dotted line: analytical BGP",
        series=(
            ("ai_net_interest", AI_COLOR, None, 7),
            ("no_ai_net_interest", NO_AI_COLOR, (16.0, 10.0), 5),
            ("ai_bgp_net_interest", BGP_COLOR, (4.0, 7.0), 5),
        ),
        y_ticks=(0.0500, 0.0502, 0.0504, 0.0506, 0.0508, 0.0510),
        y_formatter=lambda value: f"{100.0 * value:.3f}",
        x_max=3000.0,
        x_ticks=(0.0, 1000.0, 2000.0, 3000.0),
    )
    FIGURE_DIR.mkdir(exist_ok=True)
    image.save(MACRO_FILE, dpi=(220, 220))


def draw_mechanism(rows: list[dict[str, str]]) -> None:
    image = Image.new("RGB", (2400, 1700), WHITE)
    draw = ImageDraw.Draw(image)
    draw_header(
        draw,
        "Growth and the value of AI capability",
        "Audited equilibrium transition after adoption; σₓₗ = 1",
        show_scenario_legend=False,
    )
    boxes = (
        (105, 220, 1170, 875),
        (1280, 220, 2345, 875),
        (105, 925, 2345, 1670),
    )
    draw_line_panel(
        draw,
        boxes[0],
        rows,
        title="A. Growth of output per person",
        subtitle="Annual percent; focused 0.004-percentage-point range",
        series=(
            ("ai_output_pc_growth", AI_COLOR, None, 7),
            ("no_ai_output_pc_growth", NO_AI_COLOR, (16.0, 10.0), 5),
        ),
        y_ticks=(0.009995, 0.010000, 0.010010, 0.010020, 0.010030, 0.010040),
        y_formatter=lambda value: f"{100.0 * value:.4f}",
    )
    draw_line_panel(
        draw,
        boxes[1],
        rows,
        title="B. AI capability",
        subtitle="B/B₀; logarithmic vertical scale",
        series=(("ai_capability_index", AI_COLOR, None, 7),),
        y_ticks=(1.000, 1.005, 1.010, 1.015, 1.020, 1.025, 1.030),
        y_formatter=lambda value: f"{value:.3f}",
        log_scale=True,
    )
    draw_line_panel(
        draw,
        boxes[2],
        rows,
        title="C. Value of AI capability",
        subtitle="qB/Y, percent; focused vertical scale",
        series=(("ai_shadow_capability_to_output", AI_COLOR, None, 7),),
        y_ticks=(0.4835, 0.4837, 0.4839, 0.4841, 0.4843, 0.4845, 0.4847),
        y_formatter=lambda value: f"{100.0 * value:.2f}",
    )
    FIGURE_DIR.mkdir(exist_ok=True)
    image.save(MECHANISM_FILE, dpi=(220, 220))


def draw_distribution(rows: list[dict[str, str]]) -> None:
    """Draw all dated output shares and a focused inset for M/Y."""

    for row in rows:
        total = sum(
            number(row, field)
            for field in (
                "ai_gross_capital_share",
                "ai_labor_share",
                "ai_profit_share",
                "ai_inference_share",
                "ai_research_share",
            )
        )
        if abs(total - 1.0) > 1.0e-10:
            raise ValueError(f"Dated output shares do not sum to one at t={row['time']}.")

    image = Image.new("RGB", (2400, 1250), WHITE)
    draw = ImageDraw.Draw(image)
    draw.text(
        (105, 42),
        "Distribution of output after AI adoption",
        fill=INK,
        font=font(50, bold=True),
    )
    draw.text(
        (105, 105),
        "AI equilibrium path; σₓₗ = 1; every component is divided by Y",
        fill=MUTED,
        font=font(29),
    )

    series = (
        ("ai_labor_share", "wL/Y", "#205493", None, 7),
        ("ai_gross_capital_share", "(r + δ)K/Y", "#424A55", (20.0, 8.0), 6),
        ("ai_profit_share", "Π/Y", "#C69214", None, 6),
        ("ai_inference_share", "U/Y", "#D2601A", (4.0, 7.0), 6),
        ("ai_research_share", "M/Y", "#667A2C", None, 6),
        ("no_ai_labor_share", "No-AI wL/Y", "#7C8794", (16.0, 10.0), 5),
    )
    legend_positions = (
        (110, 166),
        (430, 166),
        (840, 166),
        (1080, 166),
        (1300, 166),
        (1530, 166),
    )
    for (_, label, color, pattern, width), (x, y) in zip(series, legend_positions):
        patterned_line(
            draw,
            [(x, y + 13), (x + 62, y + 13)],
            fill=color,
            width=width,
            pattern=pattern,
        )
        draw.text((x + 75, y), label, fill=INK, font=font(27))

    plot_left, plot_right = 225, 2250
    plot_top, plot_bottom = 255, 1090
    y_min, y_max = 0.0, 0.70
    for tick in (0.0, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70):
        y = plot_bottom - (tick - y_min) / (y_max - y_min) * (
            plot_bottom - plot_top
        )
        draw.line((plot_left, y, plot_right, y), fill=GRID, width=2)
        text_right(
            draw,
            (plot_left - 16, y - 14),
            f"{100.0 * tick:.0f}",
            fill=MUTED,
            text_font=font(27),
        )
    draw.line((plot_left, plot_top, plot_left, plot_bottom), fill=INK, width=3)
    draw.line((plot_left, plot_bottom, plot_right, plot_bottom), fill=INK, width=3)
    for tick in (0.0, 50.0, 100.0, 150.0, 200.0, 250.0):
        x = plot_left + tick / 250.0 * (plot_right - plot_left)
        draw.line((x, plot_bottom, x, plot_bottom + 8), fill=INK, width=2)
        text_center(
            draw,
            (x, plot_bottom + 14),
            f"{tick:.0f}",
            fill=MUTED,
            text_font=font(27),
        )
    text_center(
        draw,
        ((plot_left + plot_right) / 2, plot_bottom + 49),
        "Years since adoption",
        fill=MUTED,
        text_font=font(27),
    )
    draw.text((105, 210), "Percent of output", fill=MUTED, font=font(24))

    def main_point(row: dict[str, str], field: str) -> tuple[float, float]:
        time = number(row, "time")
        share = number(row, field)
        x = plot_left + time / 250.0 * (plot_right - plot_left)
        y = plot_bottom - (share - y_min) / (y_max - y_min) * (
            plot_bottom - plot_top
        )
        return x, y

    for field, _, color, pattern, width in series:
        points = [main_point(row, field) for row in rows]
        patterned_line(
            draw,
            points,
            fill=color,
            width=width,
            pattern=pattern,
        )

    endpoint_labels = (
        ("no_ai_labor_share", "67.0", "#7C8794", -27),
        ("ai_labor_share", "53.6", "#205493", -27),
        ("ai_gross_capital_share", "33.0", "#424A55", -27),
        ("ai_profit_share", "11.60", "#C69214", -27),
        ("ai_inference_share", "1.796", "#D2601A", -32),
    )
    for field, label, color, offset in endpoint_labels:
        x, y = main_point(rows[-1], field)
        text_right(
            draw,
            (x - 10, y + offset),
            label,
            fill=color,
            text_font=font(24, bold=True),
        )

    # M/Y is too small to read on the common percentage-point scale.  Keep it
    # in the main panel and also show the same dated series in basis points.
    inset_left, inset_top, inset_right, inset_bottom = 1320, 470, 2150, 790
    draw.rectangle(
        (inset_left, inset_top, inset_right, inset_bottom),
        fill=WHITE,
        outline="#AEB7C2",
        width=3,
    )
    draw.text(
        (inset_left + 24, inset_top + 18),
        "Research compute, M/Y",
        fill=INK,
        font=font(26, bold=True),
    )
    draw.text(
        (inset_left + 24, inset_top + 52),
        "Basis points of output; focused scale",
        fill=MUTED,
        font=font(21),
    )
    inner_left = inset_left + 105
    inner_right = inset_right - 30
    inner_top = inset_top + 98
    inner_bottom = inset_bottom - 55
    inset_y_min, inset_y_max = 0.05, 0.15
    for tick in (0.06, 0.08, 0.10, 0.12, 0.14):
        y = inner_bottom - (tick - inset_y_min) / (inset_y_max - inset_y_min) * (
            inner_bottom - inner_top
        )
        draw.line((inner_left, y, inner_right, y), fill=GRID, width=1)
        text_right(
            draw,
            (inner_left - 12, y - 10),
            f"{tick:.2f}",
            fill=MUTED,
            text_font=font(19),
        )
    draw.line((inner_left, inner_top, inner_left, inner_bottom), fill=INK, width=2)
    draw.line((inner_left, inner_bottom, inner_right, inner_bottom), fill=INK, width=2)
    for tick in (0.0, 125.0, 250.0):
        x = inner_left + tick / 250.0 * (inner_right - inner_left)
        text_center(
            draw,
            (x, inner_bottom + 12),
            f"{tick:.0f}",
            fill=MUTED,
            text_font=font(19),
        )
    inset_points: list[tuple[float, float]] = []
    for row in rows:
        time = number(row, "time")
        basis_points = 10_000.0 * number(row, "ai_research_share")
        x = inner_left + time / 250.0 * (inner_right - inner_left)
        y = inner_bottom - (
            basis_points - inset_y_min
        ) / (inset_y_max - inset_y_min) * (inner_bottom - inner_top)
        inset_points.append((x, y))
    patterned_line(draw, inset_points, fill="#667A2C", width=5)

    FIGURE_DIR.mkdir(exist_ok=True)
    image.save(DISTRIBUTION_FILE, dpi=(220, 220))


def main() -> None:
    verify_manifest()
    rows = read_rows(PATH_FILE)
    display_rows = [row for row in rows if number(row, "display_window") == 1.0]
    if len(display_rows) < 100:
        raise ValueError("The display window is too sparse for the figures.")
    times = [number(row, "time") for row in display_rows]
    if any(right <= left for left, right in zip(times, times[1:])):
        raise ValueError("Display times are not strictly increasing.")
    draw_macro(rows)
    draw_mechanism(display_rows)
    draw_distribution(display_rows)
    print(f"Wrote {MACRO_FILE.relative_to(ROOT)}")
    print(f"Wrote {MECHANISM_FILE.relative_to(ROOT)}")
    print(f"Wrote {DISTRIBUTION_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

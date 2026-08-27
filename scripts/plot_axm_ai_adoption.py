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

AI_COLOR = "#205493"
NO_AI_COLOR = "#66717E"
INK = "#22272E"
MUTED = "#66717E"
GRID = "#D9DEE5"
WHITE = "#FFFFFF"
LIGHT = "#F5F7FA"

SHARE_COMPONENTS = (
    ("gross_capital", "Gross capital", "#424A55"),
    ("labor", "Labor", "#205493"),
    ("profit", "AI profit", "#C69214"),
    ("inference", "Inference compute", "#D2601A"),
    ("research", "Research compute", "#667A2C"),
)


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

    for tick in (0.0, 50.0, 100.0, 150.0, 200.0, 250.0):
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
        subtitle="Annual percent; focused vertical scale",
        series=common_series("ai_net_interest", "no_ai_net_interest"),
        y_ticks=(0.04999, 0.05000, 0.05001, 0.05002, 0.05003, 0.05004),
        y_formatter=lambda value: f"{100.0 * value:.3f}",
    )
    FIGURE_DIR.mkdir(exist_ok=True)
    image.save(MACRO_FILE, dpi=(220, 220))


def draw_distribution_panel(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    path_rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
) -> None:
    left, top, right, bottom = box
    draw.text((left, top), "D. Distribution of output", fill=INK, font=font(36, bold=True))
    draw.text(
        (left, top + 46),
        "Percent of output; bars sum to 100%",
        fill=MUTED,
        font=font(25),
    )
    legend_font = font(22)
    legend_positions = (
        (left + 15, top + 85),
        (left + 340, top + 85),
        (left + 610, top + 85),
        (left + 15, top + 119),
        (left + 390, top + 119),
    )
    for (_, label, color), (x, y) in zip(SHARE_COMPONENTS, legend_positions):
        draw.rectangle((x, y + 3, x + 23, y + 26), fill=color, outline=INK, width=1)
        draw.text((x + 32, y), label, fill=INK, font=legend_font)

    initial = path_rows[0]
    bgp = next(row for row in summary_rows if row["point"] == "AI BGP")
    bars = (
        (
            "No AI",
            {
                "gross_capital": number(initial, "no_ai_gross_capital_share"),
                "labor": number(initial, "no_ai_labor_share"),
                "profit": 0.0,
                "inference": 0.0,
                "research": 0.0,
            },
        ),
        (
            "AI at adoption",
            {
                "gross_capital": number(initial, "ai_gross_capital_share"),
                "labor": number(initial, "ai_labor_share"),
                "profit": number(initial, "ai_profit_share"),
                "inference": number(initial, "ai_inference_share"),
                "research": number(initial, "ai_research_share"),
            },
        ),
        (
            "AI BGP",
            {
                "gross_capital": number(initial, "ai_gross_capital_share"),
                "labor": number(bgp, "ai_labor_share"),
                "profit": number(bgp, "ai_profit_share"),
                "inference": number(bgp, "ai_inference_share"),
                "research": number(bgp, "ai_research_share"),
            },
        ),
    )
    plot_left = left + 105
    plot_right = right - 35
    plot_top = top + 175
    plot_bottom = bottom - 126
    for tick in (0.0, 0.25, 0.50, 0.75, 1.0):
        y = plot_bottom - tick * (plot_bottom - plot_top)
        draw.line((plot_left, y, plot_right, y), fill=GRID, width=2)
        text_right(
            draw,
            (plot_left - 14, y - 13),
            f"{100*tick:.0f}",
            fill=MUTED,
            text_font=font(25),
        )
    draw.line((plot_left, plot_top, plot_left, plot_bottom), fill=INK, width=3)
    draw.line((plot_left, plot_bottom, plot_right, plot_bottom), fill=INK, width=3)
    centers = (
        plot_left + 0.17 * (plot_right - plot_left),
        plot_left + 0.50 * (plot_right - plot_left),
        plot_left + 0.83 * (plot_right - plot_left),
    )
    bar_width = 175
    component_colors = {key: color for key, _, color in SHARE_COMPONENTS}
    for center, (label, shares) in zip(centers, bars):
        cumulative = 0.0
        for key, _, _ in SHARE_COMPONENTS:
            share = shares[key]
            lower = plot_bottom - cumulative * (plot_bottom - plot_top)
            upper = plot_bottom - (cumulative + share) * (plot_bottom - plot_top)
            if share > 0.0:
                draw.rectangle(
                    (center - bar_width / 2, upper, center + bar_width / 2, lower),
                    fill=component_colors[key],
                    outline=WHITE,
                    width=2,
                )
            if share >= 0.065:
                text_center(
                    draw,
                    (center, (upper + lower) / 2 - 14),
                    f"{100*share:.1f}",
                    fill=WHITE,
                    text_font=font(25, bold=True),
                )
            cumulative += share
        if abs(cumulative - 1.0) > 1.0e-10:
            raise ValueError(f"Distribution bar does not sum to one: {label}")
        text_center(
            draw,
            (center, plot_bottom + 18),
            label,
            fill=INK,
            text_font=font(24),
        )
    initial_u = 100.0 * bars[1][1]["inference"]
    initial_m = 100.0 * bars[1][1]["research"]
    bgp_u = 100.0 * bars[2][1]["inference"]
    bgp_m = 100.0 * bars[2][1]["research"]
    draw.text(
        (left + 40, bottom - 72),
        f"Small shares — adoption: U/Y={initial_u:.3f}%, M/Y={initial_m:.4f}%; "
        f"AI BGP: U/Y={bgp_u:.3f}%, M/Y={bgp_m:.4f}%",
        fill=MUTED,
        font=font(21),
    )


def draw_mechanism(
    rows: list[dict[str, str]], summary_rows: list[dict[str, str]]
) -> None:
    image = Image.new("RGB", (2400, 1800), WHITE)
    draw = ImageDraw.Draw(image)
    draw_header(
        draw,
        "Growth, AI capability, and the distribution of output",
        "Audited equilibrium transition after adoption; σₓₗ = 1",
        show_scenario_legend=False,
    )
    boxes = (
        (105, 250, 1170, 985),
        (1280, 250, 2345, 985),
        (105, 1035, 1170, 1770),
        (1280, 1035, 2345, 1770),
    )
    draw_line_panel(
        draw,
        boxes[0],
        rows,
        title="A. Growth of output per person",
        subtitle="Annual percent; blue AI, gray dashed no AI; focused scale",
        series=(
            ("ai_output_pc_growth", AI_COLOR, None, 7),
            ("no_ai_output_pc_growth", NO_AI_COLOR, (16.0, 10.0), 5),
        ),
        y_ticks=(0.009995, 0.010000, 0.010010, 0.010020, 0.010030, 0.010040),
        y_formatter=lambda value: f"{100.0 * value:.3f}",
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
    draw_distribution_panel(draw, boxes[3], rows, summary_rows)
    FIGURE_DIR.mkdir(exist_ok=True)
    image.save(MECHANISM_FILE, dpi=(220, 220))


def main() -> None:
    verify_manifest()
    rows = read_rows(PATH_FILE)
    summary_rows = read_rows(SUMMARY_FILE)
    display_rows = [row for row in rows if number(row, "display_window") == 1.0]
    if len(display_rows) < 100:
        raise ValueError("The display window is too sparse for the figures.")
    times = [number(row, "time") for row in display_rows]
    if any(right <= left for left, right in zip(times, times[1:])):
        raise ValueError("Display times are not strictly increasing.")
    draw_macro(display_rows)
    draw_mechanism(display_rows, summary_rows)
    print(f"Wrote {MACRO_FILE.relative_to(ROOT)}")
    print(f"Wrote {MECHANISM_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

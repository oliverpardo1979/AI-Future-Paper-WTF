"""Plot the consolidated output decomposition along the three benchmark paths.

This is a read-only post-processing script.  It does not call a solver and it
does not modify any numerical CSV.  Before plotting, it verifies the acceptance
status and every file hash recorded in the three regime-specific audit
manifests.  The six plotted shares are reconstructed from dated prices and
quantities rather than copied from the summary table.

The gross-complements and unit-elasticity panels use the complete primary
sigma_HM=2 candidate paths.  The gross-substitutes panel uses the audited
z_T=128 finite-boundary path only through Y/K <= 5, matching the transition
window used elsewhere in the paper.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]

from PIL import Image, ImageDraw, ImageFont


RESULT_DIR = ROOT / "numerical_axm"
FIGURE_DIR = ROOT / "figures_axm"
OUTPUT_PATH = FIGURE_DIR / "axm_distributional_decomposition_paths.png"

MANIFESTS = (
    RESULT_DIR / "complements_audit_manifest.json",
    RESULT_DIR / "unit_elasticity_audit_manifest.json",
    RESULT_DIR / "high_sigma_sigma150_validated_audit_manifest.json",
)

COMPLEMENTS_PATH = RESULT_DIR / "complements_transition_paths.csv"
UNIT_PATH = RESULT_DIR / "equilibrium_transition_paths.csv"
SUBSTITUTES_PATH = (
    RESULT_DIR / "high_sigma_sigma150_z128_validated_boundary_paths.csv"
)

COMPONENTS = (
    ("gross_capital", "Gross capital payment, (r + δ)K/Y", "#424A55"),
    ("production_labor", "Production labor, wL/Y", "#205493"),
    ("research_labor", "Research labor, wH/Y", "#A44870"),
    ("distributed_profit", "Distributed profit, Π/Y", "#C69214"),
    ("inference_compute", "Inference compute, U/Y", "#D2601A"),
    ("research_compute", "Research compute, M/Y", "#667A2C"),
)

INK = "#22272E"
MUTED = "#66717E"
GRID = "#D9DEE5"
LIGHT = "#F5F7FA"
WHITE = "#FFFFFF"
ACCOUNTING_TOLERANCE = 1.0e-10
NONNEGATIVITY_TOLERANCE = 1.0e-12


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def hashed_entries(value: object) -> Iterable[dict[str, object]]:
    """Yield all manifest objects that declare a path and SHA-256 hash."""

    if isinstance(value, dict):
        if "path" in value and "sha256" in value:
            yield value
        for child in value.values():
            yield from hashed_entries(child)
    elif isinstance(value, list):
        for child in value:
            yield from hashed_entries(child)


def verify_manifests() -> set[Path]:
    """Require accepted manifests and verify all hashes they record."""

    declared_paths: set[Path] = set()
    for manifest_path in MANIFESTS:
        if not manifest_path.exists():
            raise FileNotFoundError(manifest_path)
        with manifest_path.open("r", encoding="utf-8") as handle:
            manifest = json.load(handle)
        accepted = manifest.get("accepted", manifest.get("overall_accepted"))
        if accepted is not True:
            raise ValueError(f"Audit manifest does not record PASS: {manifest_path}")
        for entry in hashed_entries(manifest):
            # Audit manifests are written on Windows.  Normalize their
            # separators so the same accepted artifacts can be verified on
            # POSIX systems as well.
            relative = Path(str(entry["path"]).replace("\\", "/"))
            candidate = (ROOT / relative).resolve()
            if not candidate.exists():
                raise FileNotFoundError(candidate)
            expected = str(entry["sha256"]).lower()
            observed = sha256_file(candidate).lower()
            if observed != expected:
                raise ValueError(
                    f"Hash differs from accepted manifest for {candidate}: "
                    f"expected {expected}, observed {observed}."
                )
            if "bytes" in entry and candidate.stat().st_size != int(entry["bytes"]):
                raise ValueError(f"File size differs from manifest for {candidate}.")
            declared_paths.add(candidate)

    required = {
        COMPLEMENTS_PATH.resolve(),
        UNIT_PATH.resolve(),
        SUBSTITUTES_PATH.resolve(),
    }
    missing = required.difference(declared_paths)
    if missing:
        raise ValueError(
            "The accepted manifests do not cover every plotted CSV: "
            + ", ".join(str(path) for path in sorted(missing))
        )
    return declared_paths


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"No observations found in {path}.")
    return rows


def numeric(row: dict[str, str], field: str) -> float:
    value = float(row[field])
    if not math.isfinite(value):
        raise ValueError(f"Non-finite {field} in scenario {row.get('scenario', '')}.")
    return value


def reconstruct_shares(row: dict[str, str]) -> dict[str, float]:
    """Reconstruct all six shares from dated log levels and factor prices."""

    log_y = numeric(row, "log_output")
    gross_capital = numeric(row, "gross_capital_return") * math.exp(
        numeric(row, "log_capital") - log_y
    )
    production_labor = math.exp(
        numeric(row, "log_wage")
        + numeric(row, "log_production_labor")
        - log_y
    )
    research_labor = math.exp(
        numeric(row, "log_wage")
        + numeric(row, "log_human_research")
        - log_y
    )
    inference_compute = math.exp(
        numeric(row, "log_inference_compute") - log_y
    )
    research_compute = math.exp(
        numeric(row, "log_automated_research") - log_y
    )
    gross_ai_revenue = math.exp(
        numeric(row, "log_ai_price")
        + numeric(row, "log_ai_services")
        - log_y
    )
    distributed_profit = (
        gross_ai_revenue
        - inference_compute
        - research_labor
        - research_compute
    )
    return {
        "gross_capital": gross_capital,
        "production_labor": production_labor,
        "research_labor": research_labor,
        "distributed_profit": distributed_profit,
        "inference_compute": inference_compute,
        "research_compute": research_compute,
    }


def crosscheck_saved_fields(
    row: dict[str, str], shares: dict[str, float]
) -> float:
    """Cross-check the reconstruction against independent saved ratios."""

    errors = [
        abs(shares["production_labor"] - numeric(row, "production_labor_share")),
        abs(
            shares["production_labor"]
            + shares["research_labor"]
            - numeric(row, "aggregate_labor_share")
        ),
        abs(shares["inference_compute"] - numeric(row, "inference_share")),
        abs(shares["research_compute"] - numeric(row, "research_resource_share")),
    ]
    operating_profit = (
        shares["distributed_profit"]
        + shares["research_labor"]
        + shares["research_compute"]
    )
    errors.append(abs(operating_profit - numeric(row, "ai_profit_share")))
    return max(errors)


def prepare_path(
    rows: list[dict[str, str]],
    *,
    selector,
    name: str,
) -> tuple[list[dict[str, object]], dict[str, float]]:
    selected = [row for row in rows if selector(row)]
    if len(selected) < 12:
        raise ValueError(f"Too few selected observations for {name}.")
    selected.sort(key=lambda row: numeric(row, "time"))
    times = [numeric(row, "time") for row in selected]
    if any(right <= left for left, right in zip(times[:-1], times[1:])):
        raise ValueError(f"Times are not strictly increasing for {name}.")

    plotted: list[dict[str, object]] = []
    max_accounting_error = 0.0
    max_crosscheck_error = 0.0
    minimum_share = math.inf
    max_research_labor = 0.0
    for row in selected:
        shares = reconstruct_shares(row)
        accounting_error = abs(sum(shares.values()) - 1.0)
        max_accounting_error = max(max_accounting_error, accounting_error)
        max_crosscheck_error = max(
            max_crosscheck_error, crosscheck_saved_fields(row, shares)
        )
        minimum_share = min(minimum_share, *shares.values())
        max_research_labor = max(max_research_labor, shares["research_labor"])
        plotted.append({"time": numeric(row, "time"), **shares})

    if max_accounting_error > ACCOUNTING_TOLERANCE:
        raise ValueError(
            f"{name} accounting error {max_accounting_error:.3e} exceeds "
            f"{ACCOUNTING_TOLERANCE:.1e}."
        )
    if max_crosscheck_error > ACCOUNTING_TOLERANCE:
        raise ValueError(
            f"{name} saved-field cross-check error {max_crosscheck_error:.3e} "
            f"exceeds {ACCOUNTING_TOLERANCE:.1e}."
        )
    if minimum_share < -NONNEGATIVITY_TOLERANCE:
        raise ValueError(f"{name} contains a negative share: {minimum_share:.3e}.")
    return plotted, {
        "observations": float(len(plotted)),
        "start": times[0],
        "end": times[-1],
        "max_accounting_error": max_accounting_error,
        "max_crosscheck_error": max_crosscheck_error,
        "minimum_share": minimum_share,
        "max_research_labor": max_research_labor,
    }


def load_font(size: int, *, bold: bool = False) -> ImageFont.ImageFont:
    candidates: tuple[str | Path, ...] = (
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
        Path(
            "C:/Windows/Fonts/DejaVuSans-Bold.ttf"
            if bold
            else "C:/Windows/Fonts/DejaVuSans.ttf"
        ),
        Path(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            if bold
            else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        ),
    )
    for candidate in candidates:
        try:
            return ImageFont.truetype(str(candidate), size=size)
        except OSError:
            continue
    style = "bold" if bold else "regular"
    raise RuntimeError(
        "Could not load DejaVu Sans. Install its "
        f"{style} font file to reproduce the canonical chart layout."
    )


def nice_time_ticks(end: float) -> list[float]:
    target_step = end / 5.0
    magnitude = 10.0 ** math.floor(math.log10(target_step))
    normalized = target_step / magnitude
    if normalized <= 1.0:
        step = magnitude
    elif normalized <= 2.0:
        step = 2.0 * magnitude
    elif normalized <= 5.0:
        step = 5.0 * magnitude
    else:
        step = 10.0 * magnitude
    ticks = []
    value = 0.0
    while value <= end + 1.0e-9:
        ticks.append(value)
        value += step
    if end - ticks[-1] > 0.18 * step:
        ticks.append(end)
    return ticks


def decimate(rows: list[dict[str, object]], width: int) -> list[dict[str, object]]:
    """Retain the first and last row mapped to each output x pixel."""

    start = float(rows[0]["time"])
    end = float(rows[-1]["time"])
    buckets: dict[int, list[dict[str, object]]] = {}
    for row in rows:
        bucket = round((float(row["time"]) - start) / (end - start) * width)
        buckets.setdefault(bucket, []).append(row)
    result: list[dict[str, object]] = []
    for bucket in sorted(buckets):
        group = buckets[bucket]
        result.append(group[0])
        if len(group) > 1:
            result.append(group[-1])
    return result


def draw_legend_item(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    label: str,
    color: str,
    font: ImageFont.ImageFont,
) -> None:
    draw.rounded_rectangle((x, y + 2, x + 38, y + 34), radius=3, fill=color)
    draw.text((x + 54, y), label, fill=INK, font=font)


def draw_panel(
    draw: ImageDraw.ImageDraw,
    rows: list[dict[str, object]],
    *,
    top: int,
    panel_label: str,
    title: str,
    detail: str,
) -> None:
    plot_left, plot_right = 245, 2280
    plot_top, plot_bottom = top + 104, top + 390
    panel_font = load_font(40, bold=True)
    detail_font = load_font(36)
    axis_font = load_font(36)

    draw.text((105, top), f"{panel_label}. {title}", fill=INK, font=panel_font)
    draw.text((105, top + 50), detail, fill=MUTED, font=detail_font)

    for percent in (0, 25, 50, 75, 100):
        y = plot_bottom - percent / 100.0 * (plot_bottom - plot_top)
        draw.line((plot_left, y, plot_right, y), fill=GRID, width=2)
        label = f"{percent}%"
        bbox = draw.textbbox((0, 0), label, font=axis_font)
        draw.text(
            (
                plot_left - 16 - (bbox[2] - bbox[0]),
                y - (bbox[3] - bbox[1]) / 2,
            ),
            label,
            fill=MUTED,
            font=axis_font,
        )

    start = float(rows[0]["time"])
    end = float(rows[-1]["time"])
    sampled = decimate(rows, plot_right - plot_left)
    lower = [0.0 for _ in sampled]
    for component_index, (field, _label, color) in enumerate(COMPONENTS):
        if component_index == len(COMPONENTS) - 1:
            # Closure has already been validated at 1e-10.  Pin the plotted
            # envelope to exactly 100 percent so floating-point noise cannot
            # create a ragged white hairline along the upper border.
            upper = [100.0 for _ in sampled]
        else:
            upper = [
                lower[index] + 100.0 * float(row[field])
                for index, row in enumerate(sampled)
            ]
        top_points = [
            (
                plot_left
                + (float(row["time"]) - start) / (end - start)
                * (plot_right - plot_left),
                plot_bottom
                - upper[index] / 100.0 * (plot_bottom - plot_top),
            )
            for index, row in enumerate(sampled)
        ]
        bottom_points = [
            (
                plot_left
                + (float(row["time"]) - start) / (end - start)
                * (plot_right - plot_left),
                plot_bottom
                - lower[index] / 100.0 * (plot_bottom - plot_top),
            )
            for index, row in enumerate(sampled)
        ]
        draw.polygon(top_points + list(reversed(bottom_points)), fill=color)
        if component_index < len(COMPONENTS) - 1:
            draw.line(top_points, fill=WHITE, width=2, joint="curve")
        lower = upper

    draw.line((plot_left, plot_top, plot_left, plot_bottom), fill=INK, width=3)
    draw.line((plot_left, plot_top, plot_right, plot_top), fill=INK, width=2)
    draw.line((plot_left, plot_bottom, plot_right, plot_bottom), fill=INK, width=3)
    for tick in nice_time_ticks(end):
        x = plot_left + (tick - start) / (end - start) * (plot_right - plot_left)
        draw.line((x, plot_bottom, x, plot_bottom + 8), fill=INK, width=2)
        label = f"{tick:,.0f}"
        bbox = draw.textbbox((0, 0), label, font=axis_font)
        draw.text(
            (x - (bbox[2] - bbox[0]) / 2, plot_bottom + 14),
            label,
            fill=MUTED,
            font=axis_font,
        )
    axis_label = "Model time (years)"
    bbox = draw.textbbox((0, 0), axis_label, font=axis_font)
    draw.text(
        ((plot_left + plot_right - (bbox[2] - bbox[0])) / 2, plot_bottom + 55),
        axis_label,
        fill=MUTED,
        font=axis_font,
    )


def draw_figure(
    paths: list[tuple[str, str, str, list[dict[str, object]]]],
) -> None:
    width, height = 2400, 2030
    image = Image.new("RGB", (width, height), WHITE)
    draw = ImageDraw.Draw(image)
    title_font = load_font(49, bold=True)
    subtitle_font = load_font(36)
    legend_font = load_font(36)

    draw.text(
        (105, 48),
        "Consolidated decomposition of final output along numerical paths",
        fill=INK,
        font=title_font,
    )
    draw.text(
        (105, 112),
        "Six dated components sum to 100%; research-input elasticity = 2 in every panel",
        fill=MUTED,
        font=subtitle_font,
    )
    draw.text(
        (105, 151),
        "Each panel uses its own actual model-time horizon; horizontal positions are not comparable across panels.",
        fill=MUTED,
        font=subtitle_font,
    )

    legend_positions = (
        (105, 196),
        (1235, 196),
        (105, 245),
        (1235, 245),
        (105, 294),
        (1235, 294),
    )
    for (_field, label, color), (x, y) in zip(COMPONENTS, legend_positions):
        draw_legend_item(draw, x, y, label, color, legend_font)

    for top, (panel_label, title, detail, rows) in zip(
        (365, 900, 1435), paths
    ):
        draw_panel(
            draw,
            rows,
            top=top,
            panel_label=panel_label,
            title=title,
            detail=detail,
        )

    FIGURE_DIR.mkdir(exist_ok=True)
    image.save(OUTPUT_PATH, dpi=(220, 220))


def main() -> None:
    verify_manifests()
    complements, complements_diagnostics = prepare_path(
        read_rows(COMPLEMENTS_PATH),
        selector=lambda row: row["scenario"]
        == "axm_complements_sigma_xl_075_hm_2",
        name="gross complements",
    )
    unit, unit_diagnostics = prepare_path(
        read_rows(UNIT_PATH),
        selector=lambda row: row["scenario"] == "axm_sigma_xl_1_hm_2",
        name="unit elasticity",
    )
    substitutes, substitutes_diagnostics = prepare_path(
        read_rows(SUBSTITUTES_PATH),
        selector=lambda row: numeric(row, "output_capital_ratio") <= 5.0,
        name="gross substitutes",
    )

    paths = [
        (
            "A",
            "Gross complements: final-production elasticity = 0.75",
            f"Full candidate-path approximation, 0-{complements_diagnostics['end']:,.0f} years",
            complements,
        ),
        (
            "B",
            "Unit elasticity: final-production elasticity = 1.00",
            f"Full candidate-path approximation, 0-{unit_diagnostics['end']:,.0f} years",
            unit,
        ),
        (
            "C",
            "Gross substitutes: final-production elasticity = 1.50",
            "Conditional finite-boundary approximation while Y/K is at most 5, about 0-1,665 years",
            substitutes,
        ),
    ]
    diagnostics = [
        complements_diagnostics,
        unit_diagnostics,
        substitutes_diagnostics,
    ]
    draw_figure(paths)

    for name, item in zip(
        ("gross complements", "unit elasticity", "gross substitutes"),
        diagnostics,
    ):
        print(
            f"{name}: n={int(item['observations']):,}, "
            f"t=[{item['start']:.3f}, {item['end']:.3f}], "
            f"max accounting error={item['max_accounting_error']:.3e}, "
            f"max cross-check error={item['max_crosscheck_error']:.3e}, "
            f"max wH/Y={100.0 * item['max_research_labor']:.4f}%"
        )
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()

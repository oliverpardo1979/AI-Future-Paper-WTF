"""Create phone-readable charts for the bilingual social-media thread.

The script does not solve the model. It reads the same audited equilibrium
paths used by the paper figures and refuses to plot them if their provenance
checks fail.
"""
import csv
import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".python-packages"))
sys.path.insert(0, str(ROOT / "scripts"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, PercentFormatter

from simulate_rewrite_finite_frontier import MAIN_DESIGN, key


STYLES = {
    0.9: ("#677748", (0, (5, 2)), 2.2),
    1.0: ("#414141", "-", 2.2),
    1.1: ("#bd8620", (0, (1, 1.8)), 2.2),
    1.5: ("#24618c", "-", 4.0),
}

LANGUAGE = {
    "en": {
        "years": "Years",
        "source": (
            "Equilibrium paths. Same parameters and initial stocks; "
            "only the AI–labor substitution elasticity varies."
        ),
        "output": {
            "title": "With sufficient substitution, growth can shift\nto a higher regime",
            "subtitle": "Annual growth of output per person",
            "bottleneck": "Labor bottleneck\n≈ 1.0%",
            "ai": "AI-dominated\n≈ 3.2%",
        },
        "wage": {
            "title": "Real wages can grow faster—not slower",
            "subtitle": "Annual growth of the real wage",
            "bottleneck": "Labor bottleneck\n≈ 1.0%",
            "ai": "AI-dominated\n≈ 2.5%",
        },
        "labor": {
            "title": "Yet labor’s share of income can vanish",
            "subtitle": (
                "Workers become richer in absolute terms while losing "
                "relative economic weight"
            ),
            "bottleneck": "Labor bottleneck\n≈ 50–54%",
            "ai": "AI-dominated\n≈ 0%",
        },
    },
    "es": {
        "years": "Años",
        "source": (
            "Trayectorias de equilibrio. Mismos parámetros y condiciones iniciales; "
            "solo varía la elasticidad de sustitución entre IA y trabajo."
        ),
        "output": {
            "title": "Con suficiente sustitución, el crecimiento puede pasar\na otro régimen",
            "subtitle": "Crecimiento anual del producto por persona",
            "bottleneck": "Cuello de botella laboral\n≈ 1,0%",
            "ai": "Dominado por la IA\n≈ 3,2%",
        },
        "wage": {
            "title": "Los salarios reales pueden crecer más, no menos",
            "subtitle": "Crecimiento anual del salario real",
            "bottleneck": "Cuello de botella laboral\n≈ 1,0%",
            "ai": "Dominado por la IA\n≈ 2,5%",
        },
        "labor": {
            "title": "Pero la participación laboral en el ingreso\npuede desaparecer",
            "subtitle": (
                "Los trabajadores se enriquecen en términos absolutos mientras "
                "pierden peso económico relativo"
            ),
            "bottleneck": "Cuello de botella laboral\n≈ 50–54%",
            "ai": "Dominado por la IA\n≈ 0%",
        },
    },
}


def load_audited_paths():
    """Load the paper's main equilibrium paths after provenance checks."""
    design = MAIN_DESIGN
    output = design.output_directory
    cache = design.cache_directory
    manifest_path = output / "paths_manifest.json"
    csv_path = output / "equilibrium_paths.csv"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    if manifest.get("design") != design.name:
        raise ValueError("The path manifest belongs to a different simulation design.")
    if hashlib.sha256(csv_path.read_bytes()).hexdigest() != manifest["csv_sha256"]:
        raise ValueError("The equilibrium-path CSV has changed since its audited export.")

    for sigma in design.sigmas:
        report = json.loads(
            (output / f"{key(sigma)}_audit.json").read_text(encoding="utf-8")
        )
        if report.get("design") != design.name or not report["equilibrium_certified"]:
            raise ValueError(f"sigma={sigma} is not a certified main-design equilibrium.")
        checkpoint = cache / report["checkpoint_filename"]
        checkpoint_hash = hashlib.sha256(checkpoint.read_bytes()).hexdigest()
        if checkpoint_hash != report["checkpoint_sha256"]:
            raise ValueError(f"The audited checkpoint for sigma={sigma} has changed.")
        if manifest["checkpoint_sha256"][key(sigma)] != checkpoint_hash:
            raise ValueError(f"CSV and audit disagree for sigma={sigma}.")

    rows = list(csv.DictReader(csv_path.open(encoding="utf-8")))
    data = {
        sigma: [
            {field: float(value) for field, value in row.items()}
            for row in rows
            if float(row["sigma"]) == sigma
        ]
        for sigma in design.sigmas
    }
    if any(not rows_for_sigma for rows_for_sigma in data.values()):
        raise ValueError("The audited CSV omits a scenario needed by the thread.")
    return data


def plot_one(data, language, chart, field, output_path):
    copy = LANGUAGE[language]
    chart_copy = copy[chart]

    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "axes.titleweight": "bold",
            "axes.edgecolor": "#888888",
            "pdf.fonttype": 42,
        }
    )
    fig, axis = plt.subplots(figsize=(12, 6.75), facecolor="#fbfaf7")
    axis.set_facecolor("#fbfaf7")

    for sigma, series in data.items():
        color, linestyle, linewidth = STYLES[sigma]
        axis.plot(
            [row["time"] for row in series],
            [row[field] for row in series],
            color=color,
            linestyle=linestyle,
            linewidth=linewidth,
            label=fr"$\sigma={sigma:.2f}$",
            zorder=4 if sigma == 1.5 else 3,
        )

    horizon = data[1.0][-1]["time"]
    axis.set_xlim(0, horizon)
    axis.set_xticks([0, 100, 200, 300, 400, 500])
    axis.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:,.0f}"))
    axis.yaxis.set_major_formatter(PercentFormatter(1, decimals=1))
    axis.tick_params(axis="both", labelsize=14, length=4, colors="#4b4b4b")
    axis.grid(axis="y", color="#dedbd4", linewidth=1.0, zorder=0)
    axis.spines[["top", "right"]].set_visible(False)
    axis.spines[["left", "bottom"]].set_color("#8b8984")
    axis.set_xlabel(copy["years"], fontsize=16, labelpad=10)

    if chart == "output":
        axis.set_ylim(0, 0.07)
        bottleneck_y, ai_y = 0.0102, 0.0324
    elif chart == "wage":
        axis.set_ylim(0, 0.046)
        bottleneck_y, ai_y = 0.0102, 0.0249
    else:
        axis.set_ylim(0, 0.60)
        bottleneck_y, ai_y = 0.525, 0.012

    title_lines = chart_copy["title"].count("\n") + 1
    subtitle_y = 0.855 - 0.065 * (title_lines - 1)
    axes_top = 0.73 - 0.065 * (title_lines - 1)
    fig.text(
        0.075,
        0.94,
        chart_copy["title"],
        fontsize=22,
        linespacing=1.05,
        weight="bold",
        color="#202020",
        va="top",
    )
    fig.text(0.075, subtitle_y, chart_copy["subtitle"], fontsize=16, color="#555555")

    axis.legend(
        ncol=4,
        loc="upper left",
        bbox_to_anchor=(-0.01, 1.16),
        frameon=False,
        fontsize=14,
        handlelength=3.0,
        columnspacing=1.7,
    )

    box = dict(boxstyle="round,pad=0.45", facecolor="#fbfaf7", edgecolor="#c7c3ba")
    axis.annotate(
        chart_copy["bottleneck"],
        xy=(horizon, bottleneck_y),
        xytext=(-105, 25 if chart != "labor" else 0),
        textcoords="offset points",
        ha="right",
        va="center",
        fontsize=14,
        color="#414141",
        bbox=box,
    )
    axis.annotate(
        chart_copy["ai"],
        xy=(horizon, ai_y),
        xytext=(-18, 34 if chart != "labor" else 35),
        textcoords="offset points",
        ha="right",
        va="center",
        fontsize=14,
        weight="bold",
        color="#24618c",
        bbox=box,
    )

    fig.text(0.075, 0.035, copy["source"], fontsize=10.5, color="#696969")
    fig.subplots_adjust(left=0.09, right=0.96, bottom=0.16, top=axes_top)
    fig.savefig(output_path, dpi=160, facecolor=fig.get_facecolor())
    plt.close(fig)


def main():
    data = load_audited_paths()
    output_directory = ROOT / "social_media" / "anthropic_econ_scenarios"
    output_directory.mkdir(parents=True, exist_ok=True)
    charts = {
        "output": "output_per_person_growth",
        "wage": "wage_growth",
        "labor": "labor_income_share",
    }
    for language in LANGUAGE:
        for chart, field in charts.items():
            plot_one(
                data,
                language,
                chart,
                field,
                output_directory / f"{language}_{chart}.png",
            )
    print(f"Created {len(LANGUAGE) * len(charts)} charts in {output_directory}")


if __name__ == "__main__":
    main()

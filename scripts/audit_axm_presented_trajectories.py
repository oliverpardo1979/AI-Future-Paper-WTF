"""Enforce the paper-wide equilibrium admission rule for trajectory figures."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SECTION_FILES = (
    ROOT / "main_axm.tex",
    ROOT / "sections_axm" / "01_introduction.tex",
    ROOT / "sections_axm" / "02_literature.tex",
    ROOT / "sections_axm" / "03_model.tex",
    ROOT / "sections_axm" / "04_growth_regimes.tex",
    ROOT / "sections_axm" / "06_conclusion.tex",
    ROOT / "sections_axm" / "appendix.tex",
)
OUTPUT = ROOT / "numerical_axm" / "presented_trajectory_admission_manifest.json"

ADMITTED_FIGURES = {
    "figures_axm/axm_complements_macro_prices.png": "complement_equilibrium",
    "figures_axm/axm_complements_factor_shares_automation.png": (
        "complement_equilibrium"
    ),
    "figures_axm/axm_complements_research_resources.png": (
        "complement_equilibrium"
    ),
    "figures_axm/axm_ai_adoption_macro.png": "unit_adoption_equilibrium",
    "figures_axm/axm_ai_adoption_mechanism_distribution.png": (
        "unit_adoption_equilibrium"
    ),
    "figures_axm/axm_ai_adoption_income_shares.png": (
        "unit_adoption_equilibrium"
    ),
    "figures_axm/axm_near_unit_equilibrium_paths.png": (
        "near_unit_admitted_equilibria"
    ),
}

REJECTED_FIGURES = {
    "figures_axm/axm_equilibrium_growth_rates.png": (
        "finite-horizon human-research candidate"
    ),
    "figures_axm/axm_equilibrium_factor_shares.png": (
        "finite-horizon human-research candidate"
    ),
    "figures_axm/axm_research_technology_comparison.png": (
        "finite-horizon human-research candidate"
    ),
    "figures_axm/axm_unit_elasticity_feedback_diagnostic.png": (
        "transformation of rejected candidate paths"
    ),
    "figures_axm/high_sigma_validated_transition_rates.png": (
        "finite-boundary pre-singular candidate"
    ),
    "figures_axm/high_sigma_validated_production_allocation.png": (
        "finite-boundary pre-singular candidate"
    ),
    "figures_axm/high_sigma_validated_research_allocation.png": (
        "finite-boundary pre-singular candidate"
    ),
    "figures_axm/high_sigma_validated_asymptotic_ratios.png": (
        "finite-boundary pre-singular diagnostic"
    ),
    "figures_axm/high_sigma_validated_boundary_convergence.png": (
        "finite-boundary pre-singular diagnostic"
    ),
    "figures_axm/axm_distributional_decomposition_paths.png": (
        "mixed equilibrium and non-equilibrium paths"
    ),
}

REJECTED_TABLE_LABELS = {
    "tab:axm-near-unit-continuity-audit": (
        "finite-window nonunit candidate paths"
    ),
    "tab:axm-high-sigma-convergence": (
        "finite-boundary pre-singular candidate paths"
    ),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(relative: str) -> dict[str, object]:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def run_audit() -> dict[str, object]:
    manuscript = "\n".join(
        path.read_text(encoding="utf-8") for path in SECTION_FILES
    )
    complement = load_json("numerical_axm/complements_audit_manifest.json")
    adoption = load_json(
        "numerical_axm/ai_adoption_unit_elasticity_audit_manifest.json"
    )
    near_unit = load_json(
        "numerical_axm/near_unit_equilibrium_status_audit.json"
    )

    rejected_references = {
        path: reason
        for path, reason in REJECTED_FIGURES.items()
        if path in manuscript
    }
    rejected_table_references = {
        label: reason
        for label, reason in REJECTED_TABLE_LABELS.items()
        if label in manuscript
    }
    missing_admitted_references = sorted(
        path for path in ADMITTED_FIGURES if path not in manuscript
    )
    near_values = near_unit.get("exported_path", {}).get("sigma_xl_values")
    gates = {
        "complement_audit_accepted": complement.get("accepted") is True,
        "adoption_audit_accepted": adoption.get("accepted") is True,
        "near_unit_audit_accepted": near_unit.get("accepted") is True,
        "near_unit_exports_only_admitted_sigmas": near_values == [0.99, 1.0],
        "no_rejected_trajectory_figure_is_referenced": not rejected_references,
        "no_rejected_trajectory_table_is_referenced": (
            not rejected_table_references
        ),
        "all_admitted_trajectory_figures_are_referenced": (
            not missing_admitted_references
        ),
    }
    return {
        "accepted": all(gates.values()),
        "rule": (
            "Every presented model trajectory must satisfy dated equilibrium "
            "conditions, admissibility, numerical robustness, a terminal regime "
            "derived for the same parameters, sufficient optimality conditions, "
            "and both transversality conditions."
        ),
        "admitted_figures": ADMITTED_FIGURES,
        "rejected_figures": REJECTED_FIGURES,
        "rejected_references_found": rejected_references,
        "rejected_table_references_found": rejected_table_references,
        "missing_admitted_references": missing_admitted_references,
        "gates": gates,
        "inputs": {
            str(path.relative_to(ROOT)).replace("\\", "/"): sha256(path)
            for path in SECTION_FILES
        },
    }


def main() -> None:
    result = run_audit()
    OUTPUT.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if not bool(result["accepted"]):
        raise SystemExit("Presented-trajectory equilibrium audit failed.")


if __name__ == "__main__":
    main()

"""Regression test for the paper-wide equilibrium trajectory admission rule."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = (
    ROOT / "numerical_axm" / "presented_trajectory_admission_manifest.json"
)
GROSS_SUBSTITUTES_AUDIT = (
    ROOT / "numerical_axm" / "gross_substitutes_status_audit.json"
)


class PresentedTrajectoryAdmissionTests(unittest.TestCase):
    def test_only_admitted_equilibrium_trajectories_are_presented(self) -> None:
        audit = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertTrue(audit["accepted"])
        self.assertTrue(all(audit["gates"].values()))
        self.assertEqual(audit["rejected_references_found"], {})
        self.assertEqual(audit["rejected_table_references_found"], {})
        self.assertEqual(audit["missing_admitted_references"], [])

    def test_gross_substitutes_diagnostic_is_never_admitted(self) -> None:
        audit = json.loads(
            GROSS_SUBSTITUTES_AUDIT.read_text(encoding="utf-8")
        )
        self.assertTrue(audit["audit_passed"])
        self.assertFalse(audit["trajectory_admitted"])
        self.assertTrue(all(audit["gates"].values()))
        self.assertEqual(audit["presented_sigma_xl_values"], [0.99, 1.0])
        self.assertFalse(
            audit["developer_global_optimality"]["concavity_gate_available"]
        )


if __name__ == "__main__":
    unittest.main()

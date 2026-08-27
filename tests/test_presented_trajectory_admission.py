"""Regression test for the paper-wide equilibrium trajectory admission rule."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = (
    ROOT / "numerical_axm" / "presented_trajectory_admission_manifest.json"
)


class PresentedTrajectoryAdmissionTests(unittest.TestCase):
    def test_only_admitted_equilibrium_trajectories_are_presented(self) -> None:
        audit = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertTrue(audit["accepted"])
        self.assertTrue(all(audit["gates"].values()))
        self.assertEqual(audit["rejected_references_found"], {})
        self.assertEqual(audit["rejected_table_references_found"], {})
        self.assertEqual(audit["missing_admitted_references"], [])


if __name__ == "__main__":
    unittest.main()

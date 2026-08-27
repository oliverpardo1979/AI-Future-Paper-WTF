"""Regression tests for the audited near-unit BGP perturbation exercise."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULT_DIR = ROOT / "numerical_axm"
MANIFEST_PATH = RESULT_DIR / "near_unit_bgp_perturbation_audit_manifest.json"
PATH_FILE = RESULT_DIR / "near_unit_bgp_perturbation_paths.csv"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


class NearUnitBGPPerturbationOutputTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        with PATH_FILE.open("r", encoding="utf-8", newline="") as handle:
            cls.rows = list(csv.DictReader(handle))

    def test_manifest_accepts_every_numerical_gate_and_binds_path(self) -> None:
        self.assertTrue(self.manifest["accepted"])
        self.assertTrue(all(self.manifest["gates"].values()))
        relative = str(PATH_FILE.relative_to(ROOT)).replace("\\", "/")
        self.assertEqual(
            sha256(PATH_FILE), self.manifest["files"][relative]["sha256"]
        )

    def test_scenarios_share_unit_bgp_predetermined_stocks(self) -> None:
        initial = [row for row in self.rows if float(row["time"]) == 0.0]
        self.assertEqual(
            sorted(float(row["sigma_xl"]) for row in initial),
            [0.99, 1.0, 1.01],
        )
        expected_log_capital = math.log(
            float(self.manifest["parameters"]["initial_capital"])
        )
        expected_log_capability = math.log(
            float(self.manifest["parameters"]["initial_capability"])
        )
        for row in initial:
            self.assertAlmostEqual(
                float(row["log_capital"]), expected_log_capital, places=12
            )
            self.assertAlmostEqual(
                float(row["log_capability"]), expected_log_capability, places=12
            )

    def test_unit_case_remains_exactly_on_analytical_bgp(self) -> None:
        unit = [row for row in self.rows if float(row["sigma_xl"]) == 1.0]
        self.assertTrue(unit)
        self.assertLess(
            max(abs(float(row["log_output_relative_to_unit_bgp"])) for row in unit),
            2.0e-9,
        )
        self.assertLess(
            max(abs(float(row["log_wage_relative_to_unit_bgp"])) for row in unit),
            2.0e-9,
        )

    def test_display_window_is_complete_and_equations_close(self) -> None:
        display_horizon = float(self.manifest["display_horizon"])
        for sigma_xl in (0.99, 1.0, 1.01):
            scenario = [
                row for row in self.rows if float(row["sigma_xl"]) == sigma_xl
            ]
            self.assertEqual(float(scenario[0]["time"]), 0.0)
            self.assertEqual(float(scenario[-1]["time"]), display_horizon)
        self.assertLess(
            max(abs(float(row["accounting_residual"])) for row in self.rows),
            1.0e-12,
        )
        self.assertLess(
            max(abs(float(row["monopoly_foc_log_residual"])) for row in self.rows),
            2.0e-11,
        )
        self.assertGreater(
            min(float(row["monopoly_soc_margin"]) for row in self.rows), 0.0
        )

    def test_paths_are_locally_close_but_not_identical_on_longer_dates(self) -> None:
        lookup = {
            (float(row["sigma_xl"]), float(row["time"])): row
            for row in self.rows
        }
        for sigma_xl in (0.99, 1.01):
            initial_gap = abs(
                float(lookup[(sigma_xl, 0.0)]["log_output_relative_to_unit_bgp"])
            )
            later_gap = abs(
                float(
                    lookup[(sigma_xl, 2500.0)][
                        "log_output_relative_to_unit_bgp"
                    ]
                )
            )
            self.assertLess(initial_gap, 0.02)
            self.assertGreater(later_gap, 0.05)


if __name__ == "__main__":
    unittest.main()

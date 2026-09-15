"""The illustrative M/Y target preserves the admitted equilibrium paths."""
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'.python-packages'), str(ROOT/'scripts')]
import calibrate_rewrite_research_share_central as central


class CentralResearchTarget(unittest.TestCase):
    def test_units_and_quoted_precision(self):
        self.assertAlmostEqual(100*central.TARGET_SHARE, .183)
        self.assertAlmostEqual(1e4*central.TARGET_TOLERANCE, .05)

    @unittest.skipUnless(all((ROOT/'tmp/rewrite_bvp_rsi_activation_half_decline'/
        f'{central.key(s)}_{stage}.npz').exists()
        for s in central.SIGMAS for stage in ('base', 'refined', 'long')),
        'Regenerate the four BVP checkpoints first')
    def test_candidate_matches_without_changing_chi(self):
        design = central.make_design()
        report = central.evaluate(design)
        self.assertEqual(design.parameters.chi, 7.616304576019883)
        self.assertAlmostEqual(report['matched_share']*100, .182915940777111)
        self.assertEqual(f"{report['matched_share']*100:.3f}", '0.183')
        self.assertAlmostEqual(report['error_basis_points'], -.0084059222889)
        self.assertEqual(len(report['scenarios']), 4)
        self.assertFalse(report['target_is_observed'])
        for moment in report['scenarios'].values():
            self.assertLess(moment['maximum_horizon_log_change'], 2e-5)
            self.assertLess(moment['first_year']['share'], 1.)

    def test_reject_target_miss_instead_of_relaxing_equilibrium_checks(self):
        with patch.object(central, 'checked_moment', return_value={'share': .00184}):
            with self.assertRaises(RuntimeError):
                central.validate_target(None)

    def test_price_marker_is_an_outcome_and_legacy_record_is_preserved(self):
        out = central.make_design().output_directory
        manifest = json.loads((out/'figure_manifest.json').read_text())
        self.assertIsNone(manifest['price_target'])
        self.assertEqual(manifest['active_calibration_record'], central.RECORD)
        historical = json.loads((out/'calibration.json').read_text())
        self.assertEqual(historical['target_price_ratio'], .6)
        record = json.loads((out/central.RECORD).read_text())
        self.assertEqual(record['historical_price_calibration_sha256'],
                         central.digest(out/'calibration.json'))
        self.assertFalse(record['price_is_current_target'])


if __name__ == '__main__':
    unittest.main()

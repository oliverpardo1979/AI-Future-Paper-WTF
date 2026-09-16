"""Offline regression checks for the literature inventory and publication."""

import json
import shutil
import unittest
import uuid
from pathlib import Path
from unittest.mock import patch

import build_literature_database as db


class LiteratureDatabaseTests(unittest.TestCase):
    def test_current_and_historical_corpora_are_distinct(self):
        locations = {
            "current": ["sections_rewrite/02_literature.tex:10"],
            "companion": ["main_companion.tex:20"],
            "old": ["sections_axm/model.tex:30", "sections/model.tex:40"],
        }
        current = db.finalize_entry({"citation_key": "current"}, locations)
        companion = db.finalize_entry({"citation_key": "companion"}, locations)
        old = db.finalize_entry({"citation_key": "old"}, locations)
        self.assertEqual(current["cited_in_rewrite"], "yes")
        self.assertEqual(current["cited_in_axm"], "no")
        self.assertEqual(companion["cited_in_companion"], "yes")
        self.assertEqual(old["cited_in_rewrite"], "no")
        self.assertEqual(old["cited_in_axm"], "yes")
        self.assertEqual(old["cited_in_legacy"], "yes")

    def test_inventory_covers_every_bib_entry_and_source_citation(self):
        manual = json.loads(db.MANUAL_PATH.read_text(encoding="utf-8"))
        cache = json.loads(db.CACHE_PATH.read_text(encoding="utf-8"))
        locations = db.citation_locations(db.ROOT)
        entries = [db.normalize_bib_entry(e) for e in db.parse_bibtex(db.BIB_PATH)]
        entries += [dict(e) for e in manual["additions"]]
        finished = []
        audits = db.load_attribution_reviews()
        for entry in entries:
            entry = db.enrich_entry(entry, cache, refresh=False)
            db.merge_nonempty(entry, manual["overrides"].get(entry["citation_key"], {}), True)
            db.apply_review_context(entry, manual, audits)
            finished.append(db.finalize_entry(entry, locations))
        report = db.validation_report(finished, locations, "test")
        for field in ("cited_keys_missing_from_database", "duplicate_citation_keys",
                      "duplicate_dois", "incomplete_structured_reviews", "missing_document_url"):
            self.assertFalse(report[field], (field, report[field]))
        by_key = {entry["citation_key"]: entry for entry in finished}
        self.assertFalse(set(manual.get("connection_reviews", {})) - set(by_key))
        for key in ("bresnahantrajtenberg1995", "bresnahanbrynjolfssonhitt2002",
                    "brynjolfssonliraymond2025", "ngaipissarides2007", "bea2018grossoutput"):
            self.assertEqual(by_key[key]["cited_in_rewrite"], "yes")
            self.assertEqual(by_key[key]["abstract_type"], "editorial_summary")

    def test_metadata_matching_is_not_treated_as_original_reading(self):
        entry = db.finalize_entry({"citation_key": "metadata", "verification_status": "doi_metadata_matched"}, {})
        self.assertEqual(entry["reading_status"], "lectura no documentada")
        entry = {"citation_key": "blocked"}
        audits = {"blocked": {"pages": "No verificadas", "version": "v1", "verdict": "Pendiente: acceso", "note": "No certificar la atribución", "confidence": "Low"}}
        db.apply_review_context(entry, {}, audits)
        self.assertEqual(entry["reading_status"], "texto completo pendiente")

    def test_discussed_connections_and_limits_are_recorded(self):
        manual = json.loads(db.MANUAL_PATH.read_text(encoding="utf-8"))
        reviews = manual["connection_reviews"]
        for key in ("davidsonetal2026", "jonestonetti2026", "korinekmckelvey2026",
                    "sastryetal2024", "jones2026future", "autorkausik2026", "liuwan2026"):
            for field in ("connection_themes", "suggested_sections", "reviewed_passages", "integration_note"):
                self.assertTrue(reviews[key][field], (key, field))
        self.assertIn("inference compute", reviews["davidsonetal2026"]["terminology"])
        self.assertIn("training and R&D compute", reviews["korinekmckelvey2026"]["terminology"])
        self.assertIn("5.3", reviews["davidsonetal2026"]["integration_note"])
        self.assertIn("por sí sola", reviews["ngaisamaniego2011"]["integration_note"])

    def test_davidson_deferred_sources_are_registered_without_false_verification(self):
        manual = json.loads(db.MANUAL_PATH.read_text(encoding="utf-8"))
        by_key = {e["citation_key"]: e for e in manual["additions"]}
        keys = ("altman2025gentle", "epoch2026trends", "goldiemirhoseini2024alphachip",
                "hanson2000growth", "howhitfill2025experiments", "chatgptjones2026explosive",
                "krugman1998formalism", "nesov2025slowdown", "openai2025futureqa",
                "roodman2020outside", "sandbergmanheim2021value", "whitfilletal2025horizon",
                "yudkowsky2013microeconomics")
        for key in keys:
            self.assertIn(key, by_key)
            self.assertNotEqual(by_key[key]["reading_status"], "pasajes originales revisados")
        self.assertIn("ChatGPT", by_key["chatgptjones2026explosive"]["authors"])

    def test_browser_exposes_connections_and_reading_status(self):
        template = (db.OUT_DIR / "browser_template.html").read_text(encoding="utf-8")
        for control in ("connection", "reading", "priority", "reset"):
            self.assertIn('id="' + control + '"', template)
        self.assertIn("reading_status", template)
        self.assertIn("reviewed_passages", template)

    def test_public_outputs_are_identical_to_validated_local_files(self):
        temporary_root = db.ROOT / "tmp"
        temporary_root.mkdir(exist_ok=True)
        # TemporaryDirectory's mode 0700 can produce an inaccessible ACL in
        # the Windows sandbox. Use the normal inherited ACL for this fixture.
        temporary = temporary_root / ("literature-test-" + uuid.uuid4().hex)
        temporary.mkdir()
        self.assertEqual(temporary.resolve().parent, temporary_root.resolve())
        try:
            source = temporary / "source"
            public = temporary / "public"
            source.mkdir()
            names = ("literature_browser.html", "literature_database.json",
                     "literature_database.csv", "validation_report.json")
            for name in names:
                (source / name).write_text("Checked UTF-8: revisión " + name, encoding="utf-8")
            with patch.object(db, "OUT_DIR", source):
                db.publish_outputs(public)
            self.assertEqual((source / names[0]).read_bytes(), (public / "index.html").read_bytes())
            for name in names[1:]:
                self.assertEqual((source / name).read_bytes(), (public / name).read_bytes())
        finally:
            shutil.rmtree(temporary)


if __name__ == "__main__":
    unittest.main()

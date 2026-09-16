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
        for entry in entries:
            entry = db.enrich_entry(entry, cache, refresh=False)
            db.merge_nonempty(entry, manual["overrides"].get(entry["citation_key"], {}), True)
            finished.append(db.finalize_entry(entry, locations))
        report = db.validation_report(finished, locations, "test")
        for field in ("cited_keys_missing_from_database", "duplicate_citation_keys",
                      "duplicate_dois", "incomplete_structured_reviews", "missing_document_url"):
            self.assertFalse(report[field], (field, report[field]))
        by_key = {entry["citation_key"]: entry for entry in finished}
        for key in ("bresnahantrajtenberg1995", "bresnahanbrynjolfssonhitt2002",
                    "brynjolfssonliraymond2025", "ngaipissarides2007", "bea2018grossoutput"):
            self.assertEqual(by_key[key]["cited_in_rewrite"], "yes")
            self.assertEqual(by_key[key]["abstract_type"], "editorial_summary")

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

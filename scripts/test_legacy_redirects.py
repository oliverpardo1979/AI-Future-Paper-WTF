"""Check that publication redirects preserve the historical source files."""

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from build_legacy_redirects import build, CURRENT_PDF, CURRENT_SITE, PAPER_PATH


class LegacyRedirectTests(unittest.TestCase):
    def test_redirects_and_archive_preservation(self):
        with TemporaryDirectory(prefix="legacy-redirect-test-", dir=Path(__file__).resolve().parent) as directory:
            root = Path(directory)
            source, output = root / "docs", root / "site"
            (source / "paper").mkdir(parents=True)
            old_pdf = b"%PDF-1.4 historical draft"
            (source / PAPER_PATH).write_bytes(old_pdf)
            (source / "index.html").write_text("Historical homepage", encoding="utf-8")
            companion = source / "paper/companion.pdf"
            companion.write_bytes(b"%PDF-1.4 companion")
            build(source, output)
            self.assertEqual((source / PAPER_PATH).read_bytes(), old_pdf)
            self.assertEqual((source / "index.html").read_text(), "Historical homepage")
            self.assertEqual((output / "paper/companion.pdf").read_bytes(), companion.read_bytes())
            self.assertTrue((output / PAPER_PATH).is_dir())
            for page, target in [(output / "index.html", CURRENT_SITE),
                                 (output / PAPER_PATH / "index.html", CURRENT_PDF)]:
                html = page.read_text(encoding="utf-8")
                self.assertIn(f'content="0; url={target}"', html)
                self.assertIn(f'rel="canonical" href="{target}"', html)
                self.assertIn('content="noindex, follow"', html)
                self.assertIn(f'<a href="{target}">', html)
            self.assertTrue((output / ".nojekyll").exists())
            with self.assertRaises(FileExistsError):
                build(source, output)
            for unsafe in [source, source / "nested", root]:
                with self.assertRaises(ValueError):
                    build(source, unsafe)


if __name__ == "__main__":
    unittest.main()

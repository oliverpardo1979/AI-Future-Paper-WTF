"""Check audit coverage and cached-file integrity, not the truth of attributions."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "audit/related_literature_2026-09-13"
CACHE = ROOT / "tmp/related_literature_audit_2026-09-13"


def main():
    manuscript = (ROOT / "sections_rewrite/02_literature.tex").read_text(encoding="utf-8")
    keys = {key.strip() for group in re.findall(r"\\cite\w*\{([^}]+)\}", manuscript)
            for key in group.split(",")}
    manifest = json.loads((AUDIT / "source_manifest.json").read_text(encoding="utf-8"))
    review = json.loads((AUDIT / "attribution_review.json").read_text(encoding="utf-8"))["sources"]
    report = (AUDIT / "README.md").read_text(encoding="utf-8")
    if len({row["key"] for row in review}) != len(review):
        raise ValueError("Duplicate review keys")
    if keys != {row["key"] for row in review}:
        raise ValueError("Review does not cover exactly the manuscript citations")
    if keys != {row["citation_key"] for row in manifest}:
        raise ValueError("Manifest does not cover exactly the manuscript citations")
    for row in review:
        if f'`{row["key"]}`' not in report:
            raise ValueError(f'Missing report entry: {row["key"]}')
        for field in ("pages", "version", "verdict", "claim", "note", "confidence"):
            if not row.get(field):
                raise ValueError(f'Missing {field}: {row["key"]}')
    checked = 0
    for row in manifest:
        if row["status"] != "downloaded_not_yet_audited":
            continue
        key = row["citation_key"]
        data = (CACHE / f"{key}.pdf").read_bytes()
        if not data.lstrip().startswith(b"%PDF-"):
            raise ValueError(f"Not a PDF: {key}")
        if hashlib.sha256(data).hexdigest() != row["sha256"]:
            raise ValueError(f"Hash changed: {key}")
        pages = json.loads((CACHE / f"{key}.pages.json").read_text(encoding="utf-8"))
        if len(pages) != row["pdf_pages"]:
            raise ValueError(f"Page count changed: {key}")
        if sum(len(page["text"]) for page in pages) != row["text_characters"]:
            raise ValueError(f"Extraction changed: {key}")
        checked += 1
    print(json.dumps({
        "citation_keys": len(keys), "review_entries": len(review),
        "verified_local_pdf_hashes": checked,
        "full_text_reading_pending": [row["key"] for row in review
                                      if row["verdict"].startswith("Pendiente:")],
        "result": "Mechanical coverage and integrity checks passed; not a truth test."
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

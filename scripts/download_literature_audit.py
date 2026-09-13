"""Cache cited full texts for a manual attribution audit; never certifies a claim.

PDFs and page text remain in ignored tmp/. The audit manifest records provenance,
not copyrighted full text. Downloads use public URLs and no authentication.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import urllib.request

from pypdf import PdfReader
from build_literature_database import parse_bibtex

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "tmp" / "related_literature_audit_2026-09-13"
AUDIT = ROOT / "audit" / "related_literature_2026-09-13"


def references():
    text = (ROOT / "sections_rewrite/02_literature.tex").read_text(encoding="utf-8")
    keys = set(k for group in re.findall(r"\\cite\w*\{([^}]+)\}", text)
               for k in group.split(","))
    return [e for e in parse_bibtex(ROOT / "references.bib") if e["citation_key"] in keys]


def urls(entry, overrides):
    key = entry["citation_key"]
    candidates = list(overrides.get(key, []))
    doi, url = entry.get("doi", ""), entry.get("url", "")
    if doi.startswith("10.3386/w"):
        number = doi.rsplit("/", 1)[1]
        candidates.append(f"https://www.nber.org/system/files/working_papers/{number}/{number}.pdf")
    if "arxiv.org/abs/" in url:
        candidates.append(url.replace("/abs/", "/pdf/"))
    if url.lower().endswith(".pdf"):
        candidates.append(url)
    return list(dict.fromkeys(candidates))


def extract(key, path):
    reader = PdfReader(path)
    pages = [{"pdf_page": i + 1, "text": p.extract_text() or ""}
             for i, p in enumerate(reader.pages)]
    (CACHE / f"{key}.pages.json").write_text(json.dumps(pages, ensure_ascii=False), encoding="utf-8")
    (CACHE / f"{key}.txt").write_text(
        "\n\n".join(f"=== PDF PAGE {p['pdf_page']} ===\n{p['text']}" for p in pages), encoding="utf-8")
    return {"pdf_pages": len(pages), "text_characters": sum(len(p["text"]) for p in pages),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def fetch(entry, overrides, old, refresh):
    key = entry["citation_key"]
    row = dict(entry)
    path = CACHE / f"{key}.pdf"
    if path.exists() and not refresh:
        row.update(old.get(key, {}))
        row.update(extract(key, path))
        row["status"] = "downloaded_not_yet_audited"
        return row
    row["attempts"] = []
    for url in urls(entry, overrides):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/pdf,*/*"})
            with urllib.request.urlopen(request, timeout=25) as response:
                data = response.read(40 * 1024 * 1024)
                resolved = response.url
            if not data.lstrip().startswith(b"%PDF-"):
                raise ValueError("Response is not a PDF")
            path.write_bytes(data)
            row.update(extract(key, path))
            row.update(status="downloaded_not_yet_audited", fulltext_url=url,
                       resolved_url=resolved, retrieved_at=datetime.now(timezone.utc).isoformat())
            return row
        except Exception as exc:
            row["attempts"].append({"url": url, "error": str(exc)})
    row["status"] = "full_text_not_downloaded"
    return row


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--keys", nargs="*")
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()
    CACHE.mkdir(parents=True, exist_ok=True)
    AUDIT.mkdir(parents=True, exist_ok=True)
    overrides_path = AUDIT / "download_urls.json"
    overrides = json.loads(overrides_path.read_text(encoding="utf-8")) if overrides_path.exists() else {}
    manifest = AUDIT / "source_manifest.json"
    old = {r["citation_key"]: r for r in json.loads(manifest.read_text(encoding="utf-8"))} if manifest.exists() else {}
    entries = references()
    chosen = [e for e in entries if not args.keys or e["citation_key"] in args.keys]
    with ThreadPoolExecutor(max_workers=5) as pool:
        futures = {pool.submit(fetch, e, overrides, old, args.refresh): e for e in chosen}
        for future in as_completed(futures):
            row = future.result()
            old[row["citation_key"]] = row
            print(row["citation_key"], row["status"], row.get("pdf_pages", ""), flush=True)
            manifest.write_text(json.dumps([old[e["citation_key"]] for e in entries if e["citation_key"] in old], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

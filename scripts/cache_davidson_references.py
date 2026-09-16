"""Cache public originals identified in Davidson et al.; not a claim audit."""
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import download_literature_audit as downloader

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "audit/davidson_references_2026-09-16"
downloader.CACHE = ROOT / "tmp/davidson_references_2026-09-16"


def main():
    downloader.CACHE.mkdir(parents=True, exist_ok=True)
    urls = json.loads((AUDIT / "download_urls.json").read_text(encoding="utf-8"))
    manifest = AUDIT / "source_manifest.json"
    old = {r["citation_key"]: r for r in json.loads(manifest.read_text(encoding="utf-8"))} if manifest.exists() else {}

    def fetch(key):
        row = downloader.fetch({"citation_key": key}, urls, old, False)
        print(key, row["status"], row.get("pdf_pages", ""), flush=True)
        return row

    with ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(fetch, urls))
    manifest.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

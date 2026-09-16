"""Cache public original papers for the Jones/top-five bibliographic review.

Reuse the existing downloader; no copyrighted PDFs are placed in tracked files.
Downloaded text is evidence for manual review, not a certification of claims.
"""
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import download_literature_audit as downloader

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / 'audit' / 'jones_top5_2026-09-16'
downloader.CACHE = ROOT / 'tmp' / 'jones_top5_2026-09-16'
downloader.CACHE.mkdir(parents=True, exist_ok=True)
urls = json.loads((AUDIT / 'download_urls.json').read_text(encoding='utf-8'))
target = AUDIT / 'source_manifest.json'
old = {r['citation_key']: r for r in json.loads(target.read_text(encoding='utf-8'))} if target.exists() else {}
with ThreadPoolExecutor(max_workers=4) as pool:
    pending = [key for key in urls if not (
        old.get(key, {}).get('status') == 'downloaded_not_yet_audited'
        and (downloader.CACHE / f'{key}.pages.json').exists()
    )]
    jobs = [pool.submit(downloader.fetch, {'citation_key': key}, urls, old, False) for key in pending]
    for job in as_completed(jobs):
        row = job.result()
        old[row['citation_key']] = row
        print(row['citation_key'], row['status'], row.get('pdf_pages', ''), flush=True)
target.write_text(json.dumps(list(old.values()), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

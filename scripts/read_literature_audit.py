"""Print complete cached pages, or locate passages for manual reading."""
import argparse
import json
from pathlib import Path
import re

parser = argparse.ArgumentParser()
parser.add_argument("key")
parser.add_argument("--pages", nargs="*", type=int)
parser.add_argument("--find")
parser.add_argument("--context", type=int, default=650)
args = parser.parse_args()
cache = Path(__file__).resolve().parents[1] / "tmp/related_literature_audit_2026-09-13"
pages = json.loads((cache / f"{args.key}.pages.json").read_text(encoding="utf-8"))
for page in pages:
    if args.pages and page["pdf_page"] not in args.pages:
        continue
    text = page["text"]
    if args.find:
        matches = list(re.finditer(args.find, text, re.I))
        if not matches:
            continue
        print(f"=== {args.key} PDF PAGE {page['pdf_page']} ===")
        spans = []
        for match in matches:
            start, end = max(0, match.start()-args.context), min(len(text), match.end()+args.context)
            if spans and start <= spans[-1][1]:
                spans[-1] = (spans[-1][0], max(end, spans[-1][1]))
            else:
                spans.append((start, end))
        for start, end in spans:
            print(text[start:end], "\n")
    else:
        print(f"=== {args.key} PDF PAGE {page['pdf_page']} ===\n{text}\n")

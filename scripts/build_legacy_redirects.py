"""Retire the published draft without modifying historical manuscript files.

GitHub Pages serves index.html in a directory. Replacing the PDF only in
the deployment artifact with a directory of the same name lets the old
PDF URL lead to an HTML redirect, then to the maintained PDF. The source
PDF and all other archive files remain unchanged in this repository.
"""

import argparse
from html import escape
from pathlib import Path
import shutil


CURRENT_SITE = "https://oliverpardo1979.github.io/ai-growth-and-labor/"
PAPER_PATH = Path("paper/the-future-of-growth-and-human-labor-under-recursive-ai-self-improvement.pdf")
CURRENT_PDF = CURRENT_SITE + PAPER_PATH.as_posix()


def redirect_page(destination):
    url = escape(destination, quote=True)
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex, follow">
  <link rel="canonical" href="{url}">
  <meta http-equiv="refresh" content="0; url={url}">
  <title>Paper moved</title>
</head>
<body>
  <p>This paper has moved. <a href="{url}">Open the current version.</a></p>
</body>
</html>
'''


def build(source, output):
    source = Path(source).resolve()
    output = Path(output).resolve()
    # Never overwrite an existing directory or operate on the source tree.
    if output == source or source in output.parents or output in source.parents:
        raise ValueError("The output must be separate from the archived docs directory.")
    if not (source / PAPER_PATH).is_file():
        raise FileNotFoundError(source / PAPER_PATH)
    shutil.copytree(source, output)
    (output / "index.html").write_text(redirect_page(CURRENT_SITE), encoding="utf-8")
    legacy_pdf = output / PAPER_PATH
    legacy_pdf.unlink()  # Only the fresh deployment copy, never the archive.
    legacy_pdf.mkdir()
    (legacy_pdf / "index.html").write_text(redirect_page(CURRENT_PDF), encoding="utf-8")
    (output / ".nojekyll").touch()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    build(Path(__file__).resolve().parents[1] / "docs", args.output)

"""Read the previous Section 5.3 separately from the active manuscript."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
START = "% BEGIN COMMENTED PREVIOUS SECTION 5.3 (2026-09-13)\n"
END = "% END COMMENTED PREVIOUS SECTION 5.3"


def preserved_section_53():
    text = (ROOT / "sections_rewrite/05_uncapped_equilibria.tex").read_text(
        encoding="utf-8")
    block = text.split(START, 1)[1].split(END, 1)[0]
    # The two archive-description lines are not part of the preserved text.
    lines = block.splitlines()[2:]
    if not lines or not all(line == "%" or line.startswith("% ") for line in lines):
        raise AssertionError("The previous subsection must remain fully commented")
    return "\n".join("" if line == "%" else line[2:] for line in lines) + "\n"

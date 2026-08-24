#!/usr/bin/env python3
"""Sync the .qmd's orientation diagrams into the committed .ipynb notebooks.

Why this instead of a full `quarto convert` rebuild (which is what the sibling
data-analysis repo does): this course's `exercises_solutions.ipynb` is committed
WITH executed outputs, and both notebooks here were produced by
`quarto render --to ipynb`, whose markdown differs cosmetically from
`quarto convert` (pandoc-style `-----` rules, `1.  ` list numbering, hard-wrapped
prose). Rebuilding would rewrite every markdown cell in a notebook students open
in Colab. This script touches only the cells that gain a diagram.

For each `<!-- diagram: slug -->` block in the .qmd it finds the heading that
diagram sits under, locates the same heading in the notebook, and inserts the
pre-rendered PNG at the matching spot: after the heading and its prose, before
the next heading or the end of that markdown cell. Colab's markdown engine has
no mermaid support, so the notebooks get an <img>, not a fence (see
scripts/diagrams.py).

Re-running replaces what it inserted last time rather than stacking copies.

Usage:  python3 scripts/add-diagrams-to-notebooks.py
Requires: mermaid-cli (`mmdc`) only when a diagram's PNG is missing.
"""
import json
import re
from pathlib import Path

from diagrams import mermaid_to_image

ROOT = Path(__file__).resolve().parent.parent

TARGETS = [
    ("exercises.qmd", "exercises.ipynb"),
    ("exercises_solutions.qmd", "exercises_solutions.ipynb"),
]

HEADING = re.compile(r"^#{1,6} ")
BLOCK = re.compile(r"<!-- diagram: ([a-z0-9-]+) -->\n```\{mermaid\}\n(.*?)\n```", re.S)


def parse_qmd(path):
    """Return [(slug, mermaid_body, anchor_heading, occurrence)] in file order."""
    text = path.read_text()
    lines = text.splitlines()
    found = []
    seen = {}  # heading -> how many times we've passed it
    heading = None
    i = 0
    while i < len(lines):
        ln = lines[i]
        if HEADING.match(ln):
            heading = ln
            seen[heading] = seen.get(heading, 0) + 1
        elif ln.startswith("<!-- diagram: "):
            m = BLOCK.match("\n".join(lines[i:]))
            if m and heading:
                body = "\n".join(x for x in m.group(2).split("\n")
                                 if not x.lstrip().startswith("%%|")).strip("\n")
                found.append((m.group(1), body, heading, seen[heading]))
        i += 1
    return found


def strip_existing(text, slug):
    pat = re.compile(r"<!-- diagram: " + re.escape(slug) + r" -->\n<div align=\"center\">.*?</div>\n\n?")
    return pat.sub("", text)


def insert_into_cell(text, heading, img_html, slug, nth):
    """Place the diagram after the nth `heading` in this cell and its prose,
    before the next heading of any level."""
    lines = text.split("\n")
    start = [i for i, ln in enumerate(lines) if ln == heading][nth]
    i = start + 1
    while i < len(lines) and not HEADING.match(lines[i]):
        i += 1
    while i > start + 1 and lines[i - 1].strip() == "":
        i -= 1
    block = [""] if i > start + 1 else []
    block += [f"<!-- diagram: {slug} -->", img_html, ""]
    return "\n".join(lines[:i] + block + lines[i:])


def apply(qmd, ipynb):
    diagrams = parse_qmd(ROOT / qmd)
    nb_path = ROOT / ipynb
    nb = json.loads(nb_path.read_text())

    placed = 0
    for slug, body, heading, occurrence in diagrams:
        img = mermaid_to_image(body)
        count = 0
        for cell in nb["cells"]:
            if cell["cell_type"] != "markdown":
                continue
            text = strip_existing("".join(cell["source"]), slug)
            hits = [ln for ln in text.split("\n") if ln == heading]
            if not hits:
                cell["source"] = text.splitlines(keepends=True)
                continue
            if count + len(hits) < occurrence:
                count += len(hits)
                cell["source"] = text.splitlines(keepends=True)
                continue
            text = insert_into_cell(text, heading, img, slug, occurrence - count - 1)
            cell["source"] = text.splitlines(keepends=True)
            placed += 1
            break
        else:
            raise SystemExit(f"{ipynb}: no markdown cell holds occurrence "
                             f"{occurrence} of {heading!r} (diagram {slug})")

    nb_path.write_text(json.dumps(nb, indent=1))
    print(f"{ipynb}: {placed} diagrams in place")


def main():
    for qmd, ipynb in TARGETS:
        apply(qmd, ipynb)


if __name__ == "__main__":
    main()

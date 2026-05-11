"""
convert_to_notebooks.py
Converts each project .py script into a proper Jupyter .ipynb notebook.
Run this if your submission requires .ipynb format.

Usage:
    python convert_to_notebooks.py

Requires: pip install nbformat
"""

import nbformat
import os
import re

SRC_DIR = os.path.join(os.path.dirname(__file__), "notebooks")
OUT_DIR = SRC_DIR   # place .ipynb alongside .py files

SCRIPTS = [
    "project1_supermarket_sales.py",
    "project2_student_performance.py",
    "project3_weather_analysis.py",
    "project4_healthcare_covid.py",
    "project5_finance_stocks.py",
]


def py_to_notebook(py_path: str, ipynb_path: str) -> None:
    with open(py_path, "r", encoding="utf-8") as f:
        source = f.read()

    nb = nbformat.v4.new_notebook()
    cells = []

    # Split on section separators (── ... ──) into logical blocks
    # Each block becomes one code cell; docstring at top becomes a markdown cell
    lines = source.split("\n")

    # First cell: extract the module docstring as a Markdown cell
    if lines[0].startswith('"""'):
        doc_lines = []
        i = 1
        while i < len(lines) and not lines[i].startswith('"""'):
            doc_lines.append(lines[i])
            i += 1
        md_source = "\n".join(doc_lines).strip()
        # Convert plain text to markdown heading
        title_match = re.match(r"Project\s+\d+\s+[—–-]+\s+(.+)", md_source.split("\n")[0])
        if title_match:
            md_source = f"# {md_source.split(chr(10))[0]}\n\n" + \
                        "\n".join(md_source.split("\n")[1:])
        cells.append(nbformat.v4.new_markdown_cell(md_source))
        remaining = "\n".join(lines[i + 1:])
    else:
        remaining = source

    # Split remaining code on the ── separator comment lines into cells
    blocks = re.split(r"\n# ── .+ ─+\n", remaining)
    separators = re.findall(r"# ── (.+?) ─+", remaining)

    for idx, block in enumerate(blocks):
        block = block.strip()
        if not block:
            continue
        # Add a markdown header cell before each code block (from separator)
        if idx > 0 and idx - 1 < len(separators):
            header = separators[idx - 1].strip()
            # Turn into a clean markdown heading
            cells.append(nbformat.v4.new_markdown_cell(f"## {header}"))
        cells.append(nbformat.v4.new_code_cell(block))

    nb.cells = cells
    nb.metadata["kernelspec"] = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    }
    nb.metadata["language_info"] = {"name": "python", "version": "3.9.0"}

    with open(ipynb_path, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)
    print(f"  [CONVERTED] {os.path.basename(py_path)} → {os.path.basename(ipynb_path)}")


if __name__ == "__main__":
    try:
        import nbformat
    except ImportError:
        print("Install nbformat first:  pip install nbformat")
        raise SystemExit(1)

    print("\nConverting project scripts to Jupyter notebooks ...\n")
    for script in SCRIPTS:
        src = os.path.join(SRC_DIR, script)
        out = os.path.join(OUT_DIR, script.replace(".py", ".ipynb"))
        if os.path.exists(src):
            py_to_notebook(src, out)
        else:
            print(f"  [SKIP] {script} not found")
    print("\nDone. Open any .ipynb file in Jupyter Lab / Notebook.\n")

#!/usr/bin/env python3
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
REPORTS = DOCS / "reports"

PAGES = [
    ROOT / "data/scans/scan_20260508.md",
    *sorted((ROOT / "data/analyses").glob("*_20260508.md")),
]


def inline(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(
        r"\[([^\]]+)\]\((https?://[^)]+)\)",
        r'<a href="\2" target="_blank" rel="noopener">\1</a>',
        escaped,
    )
    return escaped


def is_table_separator(line: str) -> bool:
    stripped = line.strip().strip("|").strip()
    return bool(stripped) and all(set(part.strip()) <= {"-", ":"} for part in stripped.split("|"))


def split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def markdown_to_html(markdown: str) -> str:
    lines = markdown.splitlines()
    out: list[str] = []
    i = 0
    in_list = False

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            close_list()
            i += 1
            continue

        if stripped.startswith("|") and i + 1 < len(lines) and is_table_separator(lines[i + 1]):
            close_list()
            headers = split_table_row(stripped)
            out.append('<div class="table-wrap detail-table"><table><thead><tr>')
            out.extend(f"<th>{inline(cell)}</th>" for cell in headers)
            out.append("</tr></thead><tbody>")
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = split_table_row(lines[i])
                out.append("<tr>")
                out.extend(f"<td>{inline(cell)}</td>" for cell in cells)
                out.append("</tr>")
                i += 1
            out.append("</tbody></table></div>")
            continue

        if stripped.startswith("#"):
            close_list()
            level = len(stripped) - len(stripped.lstrip("#"))
            text = stripped[level:].strip()
            level = min(level, 4)
            out.append(f"<h{level}>{inline(text)}</h{level}>")
            i += 1
            continue

        if stripped == "---":
            close_list()
            out.append("<hr>")
            i += 1
            continue

        if stripped.startswith("- "):
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{inline(stripped[2:])}</li>")
            i += 1
            continue

        close_list()
        out.append(f"<p>{inline(stripped)}</p>")
        i += 1

    close_list()
    return "\n".join(out)


def page_title(path: Path, markdown: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def render_page(path: Path) -> None:
    markdown = path.read_text(encoding="utf-8")
    title = page_title(path, markdown)
    body = markdown_to_html(markdown)
    output = REPORTS / f"{path.stem}.html"
    output.write_text(
        f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <link rel="stylesheet" href="../assets/site.css">
</head>
<body>
  <header class="detail-header">
    <a class="back-link" href="../index.html">← 返回总览</a>
    <p class="eyebrow">Detailed Report</p>
    <h1>{html.escape(title)}</h1>
    <p class="summary">由 <code>{html.escape(path.relative_to(ROOT).as_posix())}</code> 生成。</p>
  </header>
  <main class="detail-layout">
    <article class="detail-content">
{body}
    </article>
  </main>
</body>
</html>
""",
        encoding="utf-8",
    )


def main() -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    for page in PAGES:
        render_page(page)


if __name__ == "__main__":
    main()

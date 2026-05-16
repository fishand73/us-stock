#!/usr/bin/env python3
from __future__ import annotations

import html
import re
from dataclasses import dataclass, field
from datetime import date as DateCls
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
REPORTS = DOCS / "reports"
DATES_DIR = DOCS / "dates"
SCANS = ROOT / "data/scans"
ANALYSES = ROOT / "data/analyses"

WEEKDAYS = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

SCAN_NAME = re.compile(r"^scan_(\d{8})\.md$")
DATE_TAIL = re.compile(r"_(\d{8})\.md$")
THEME_PATTERNS = [
    re.compile(r"^\s*\*\*主题过滤\*\*\s*[：:]\s*(.+)$", re.MULTILINE),
    re.compile(r"^\s*\*\*筛选主题\*\*\s*[：:]\s*(.+)$", re.MULTILINE),
    re.compile(r"^\s*\*\*主题\*\*\s*[：:]\s*(.+)$", re.MULTILINE),
    re.compile(r"^\s*\*\*筛选\*\*\s*[：:]\s*(.+)$", re.MULTILINE),
]


# ---------- Markdown inline helpers ----------

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


def strip_inline_markup(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return text


def is_table_separator(line: str) -> bool:
    stripped = line.strip().strip("|").strip()
    return bool(stripped) and all(set(part.strip()) <= {"-", ":"} for part in stripped.split("|"))


def split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def slugify(text: str, used: dict[str, int]) -> str:
    plain = strip_inline_markup(text).strip().lower()
    plain = re.sub(r"[^\w一-鿿\s-]", "", plain, flags=re.UNICODE)
    plain = re.sub(r"\s+", "-", plain)
    plain = re.sub(r"-+", "-", plain).strip("-")
    if not plain:
        plain = "section"
    if plain in used:
        used[plain] += 1
        return f"{plain}-{used[plain]}"
    used[plain] = 0
    return plain


def markdown_to_html(markdown: str) -> tuple[str, list[tuple[int, str, str]]]:
    lines = markdown.splitlines()
    out: list[str] = []
    headings: list[tuple[int, str, str]] = []
    slug_used: dict[str, int] = {}
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
            header_cells = split_table_row(stripped)
            out.append('<div class="table-wrap detail-table"><table><thead><tr>')
            out.extend(f"<th>{inline(cell)}</th>" for cell in header_cells)
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
            if level in (2, 3):
                slug = slugify(text, slug_used)
                headings.append((level, strip_inline_markup(text), slug))
                out.append(f'<h{level} id="{html.escape(slug)}">{inline(text)}</h{level}>')
            else:
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
    return "\n".join(out), headings


# ---------- Discovery ----------

@dataclass
class Doc:
    path: Path
    ymd: str
    date_iso: str
    kind: str            # scan | analysis | strategy
    ticker: str
    title: str
    snippet: str
    output_rel: str      # filename inside reports/


@dataclass
class DateBundle:
    ymd: str
    date_iso: str
    weekday: str
    theme: str = ""
    scan: Doc | None = None
    analyses: list[Doc] = field(default_factory=list)
    strategies: list[Doc] = field(default_factory=list)
    highlights_rel: str | None = None  # path under docs/ if any


def fmt_iso(ymd: str) -> str:
    return f"{ymd[:4]}-{ymd[4:6]}-{ymd[6:8]}"


def weekday_zh(ymd: str) -> str:
    d = DateCls(int(ymd[:4]), int(ymd[4:6]), int(ymd[6:8]))
    return WEEKDAYS[d.weekday()]


def first_title(markdown: str, fallback: str) -> str:
    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return strip_inline_markup(stripped[2:]).strip()
        if stripped.startswith("## "):
            return strip_inline_markup(stripped[3:]).strip()
    return fallback


def extract_snippet(markdown: str, max_len: int = 130) -> str:
    for line in markdown.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            continue
        if stripped.startswith("---"):
            continue
        if stripped.startswith("|"):
            continue
        if stripped.startswith(">"):
            continue
        if stripped.startswith("- "):
            continue
        if re.match(r"^\d+\.\s", stripped):
            continue
        cleaned = strip_inline_markup(stripped)
        # Skip short bold key-value metadata lines like "**日期**：2026-05-08"
        if re.match(r"^\*\*[^*]+\*\*\s*[：:]", stripped) and len(cleaned) < 60:
            continue
        if len(cleaned) > max_len:
            cleaned = cleaned[:max_len].rstrip() + "…"
        return cleaned
    return ""


def extract_theme(markdown: str) -> str:
    for pattern in THEME_PATTERNS:
        m = pattern.search(markdown)
        if m:
            value = strip_inline_markup(m.group(1).strip())
            return value.rstrip("。 ").strip()
    return ""


def classify(filename: str) -> tuple[str, str, str] | None:
    m = SCAN_NAME.match(filename)
    if m:
        return "scan", "", m.group(1)
    tail = DATE_TAIL.search(filename)
    if not tail:
        return None
    ymd = tail.group(1)
    stem = filename[: tail.start()]
    if not stem:
        return None
    if "strategy" in stem.lower() or stem.lower().startswith("portfolio"):
        ticker = re.split(r"_strategy", stem, maxsplit=1)[0] or stem
        return "strategy", ticker, ymd
    if re.fullmatch(r"[A-Z][A-Z0-9]*", stem):
        return "analysis", stem, ymd
    return None


def load_doc(path: Path) -> Doc | None:
    info = classify(path.name)
    if not info:
        return None
    kind, ticker, ymd = info
    text = path.read_text(encoding="utf-8")
    fallback = path.stem
    title = first_title(text, fallback)
    snippet = extract_snippet(text)
    return Doc(
        path=path,
        ymd=ymd,
        date_iso=fmt_iso(ymd),
        kind=kind,
        ticker=ticker,
        title=title,
        snippet=snippet,
        output_rel=f"{path.stem}.html",
    )


def discover() -> list[DateBundle]:
    bundles: dict[str, DateBundle] = {}

    def get_bundle(ymd: str) -> DateBundle:
        if ymd not in bundles:
            bundles[ymd] = DateBundle(ymd=ymd, date_iso=fmt_iso(ymd), weekday=weekday_zh(ymd))
        return bundles[ymd]

    if SCANS.is_dir():
        for path in sorted(SCANS.glob("scan_*.md")):
            doc = load_doc(path)
            if doc and doc.kind == "scan":
                bundle = get_bundle(doc.ymd)
                bundle.scan = doc
                bundle.theme = extract_theme(path.read_text(encoding="utf-8"))

    if ANALYSES.is_dir():
        for path in sorted(ANALYSES.glob("*.md")):
            doc = load_doc(path)
            if not doc:
                continue
            bundle = get_bundle(doc.ymd)
            if doc.kind == "analysis":
                bundle.analyses.append(doc)
            elif doc.kind == "strategy":
                bundle.strategies.append(doc)

    for bundle in bundles.values():
        bundle.analyses.sort(key=lambda d: d.ticker)
        bundle.strategies.sort(key=lambda d: (d.ticker.lower(), d.path.name))
        highlights = DATES_DIR / f"{bundle.date_iso}-highlights.html"
        if highlights.exists():
            bundle.highlights_rel = highlights.name

    return sorted(bundles.values(), key=lambda b: b.ymd, reverse=True)


# ---------- Rendering ----------

def render_toc(headings: list[tuple[int, str, str]]) -> str:
    if not headings:
        return ""
    items: list[str] = []
    for level, text, slug in headings:
        cls = "toc-l3" if level == 3 else "toc-l2"
        items.append(
            f'<li><a class="{cls}" href="#{html.escape(slug)}">{html.escape(text)}</a></li>'
        )
    return (
        '<aside class="toc" aria-label="目录">'
        '<h2>本页目录</h2>'
        f'<ul>{"".join(items)}</ul>'
        '</aside>'
    )


THEME_BOOTSTRAP = """    (function () {
      try {
        var k = "us-stock-theme";
        var s = localStorage.getItem(k);
        var t = s || (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
        document.documentElement.dataset.theme = t;
      } catch (e) {}
    })();"""


def page_shell(title: str, body: str, css_rel: str, js_rel: str) -> str:
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <link rel="stylesheet" href="{css_rel}">
  <script>
{THEME_BOOTSTRAP}
  </script>
  <script defer src="{js_rel}"></script>
</head>
<body>
  <button class="theme-toggle" type="button" data-theme-toggle aria-pressed="false" aria-label="切换主题">☾ 深色</button>
{body}
</body>
</html>
"""


def render_report(doc: Doc) -> None:
    markdown = doc.path.read_text(encoding="utf-8")
    body_html, headings = markdown_to_html(markdown)
    toc = render_toc(headings)
    rel_source = doc.path.relative_to(ROOT).as_posix()
    body = f"""  <header class="detail-header">
    <a class="back-link" href="../dates/{doc.date_iso}.html">← 返回 {doc.date_iso}</a>
    <p class="eyebrow">{html.escape(_kind_label(doc.kind))} · {doc.date_iso}</p>
    <h1>{html.escape(doc.title)}</h1>
    <p class="summary">由 <code>{html.escape(rel_source)}</code> 生成。</p>
  </header>
  <main class="detail-layout">
    <article class="detail-content">
{body_html}
    </article>
{toc}
  </main>"""
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / doc.output_rel).write_text(
        page_shell(doc.title, body, "../assets/site.css", "../assets/site.js"),
        encoding="utf-8",
    )


def _kind_label(kind: str) -> str:
    return {"scan": "Daily Scan", "analysis": "Deep Dive", "strategy": "Strategy"}.get(kind, "Report")


def render_date_page(bundle: DateBundle) -> None:
    n_scan = 1 if bundle.scan else 0
    n_analyses = len(bundle.analyses)
    n_strategies = len(bundle.strategies)

    sections: list[str] = []

    if bundle.highlights_rel:
        sections.append(
            '<section class="band">'
            '<div class="highlights-callout">'
            '<p><strong>当日还有一份手工点评</strong>：发布结论 · 执行分层 · 速览表。</p>'
            f'<a class="date-link" href="{html.escape(bundle.highlights_rel)}">查看手工点评</a>'
            '</div>'
            '</section>'
        )

    if bundle.scan:
        sections.append(
            '<section class="band">'
            '<h2>市场扫描</h2>'
            f'<a class="big-card" href="../reports/{html.escape(bundle.scan.output_rel)}">'
            f'<h3>{html.escape(bundle.scan.title)}</h3>'
            f'<p>{html.escape(bundle.scan.snippet)}</p>'
            '</a>'
            '</section>'
        )

    if bundle.analyses:
        cards = "".join(_render_doc_card(d) for d in bundle.analyses)
        sections.append(
            '<section class="band">'
            f'<h2>深度分析 <span class="signal-count">{n_analyses}</span></h2>'
            f'<div class="ticker-grid">{cards}</div>'
            '</section>'
        )

    if bundle.strategies:
        cards = "".join(_render_doc_card(d) for d in bundle.strategies)
        sections.append(
            '<section class="band">'
            f'<h2>交易策略 <span class="signal-count">{n_strategies}</span></h2>'
            f'<div class="ticker-grid">{cards}</div>'
            '</section>'
        )

    metrics = (
        '<dl class="metrics" aria-label="当日统计">'
        f'<div><dt>Scan</dt><dd>{n_scan}</dd></div>'
        f'<div><dt>深度分析</dt><dd>{n_analyses}</dd></div>'
        f'<div><dt>策略</dt><dd>{n_strategies}</dd></div>'
        f'<div><dt>主题</dt><dd style="font-size:14px;line-height:1.3;">{html.escape(bundle.theme or "—")}</dd></div>'
        '</dl>'
    )

    body = f"""  <header class="masthead">
    <div>
      <a class="back-link" href="../index.html">← 返回首页</a>
      <p class="eyebrow">Daily Overview · {bundle.weekday}</p>
      <h1>{bundle.date_iso} 美股报告</h1>
      <p class="summary">{html.escape(bundle.theme) if bundle.theme else "当日 scan、深度分析与交易策略汇总。"}</p>
    </div>
    {metrics}
  </header>
  <main class="section-stack">
{chr(10).join(sections)}
  </main>"""

    DATES_DIR.mkdir(parents=True, exist_ok=True)
    (DATES_DIR / f"{bundle.date_iso}.html").write_text(
        page_shell(
            f"{bundle.date_iso} 美股报告",
            body,
            "../assets/site.css",
            "../assets/site.js",
        ),
        encoding="utf-8",
    )


def _render_doc_card(doc: Doc) -> str:
    label = doc.ticker.upper() if doc.ticker else doc.title
    meta = _kind_label(doc.kind)
    snippet = html.escape(doc.snippet) if doc.snippet else ""
    return (
        f'<a class="ticker-card" href="../reports/{html.escape(doc.output_rel)}">'
        f'<span class="ticker-meta">{html.escape(meta)}</span>'
        f'<span class="ticker-code">{html.escape(label)}</span>'
        f'<span class="ticker-snippet">{snippet}</span>'
        '</a>'
    )


def render_index(bundles: list[DateBundle]) -> None:
    total_analyses = sum(len(b.analyses) for b in bundles)
    total_strategies = sum(len(b.strategies) for b in bundles)
    total_scans = sum(1 for b in bundles if b.scan)

    cards: list[str] = []
    for idx, bundle in enumerate(bundles):
        latest = (
            '<span class="badge badge-bull">最新</span>'
            if idx == 0
            else ""
        )
        meta_items: list[str] = []
        if bundle.scan:
            meta_items.append('<li><strong>1</strong> Scan</li>')
        if bundle.analyses:
            meta_items.append(f'<li><strong>{len(bundle.analyses)}</strong> 深度分析</li>')
        if bundle.strategies:
            meta_items.append(f'<li><strong>{len(bundle.strategies)}</strong> 策略</li>')
        theme = (
            html.escape(bundle.theme)
            if bundle.theme
            else "当日 scan、深度分析与交易策略汇总。"
        )
        cards.append(
            f'<a class="date-card" href="dates/{bundle.date_iso}.html">'
            f'<header>'
            f'<div><time datetime="{bundle.date_iso}">{bundle.date_iso}</time>'
            f'<span class="weekday">{bundle.weekday}</span></div>'
            f'{latest}'
            f'</header>'
            f'<p class="theme">{theme}</p>'
            f'<ul class="date-meta">{"".join(meta_items)}</ul>'
            f'<div class="date-actions"><span class="date-link">查看当日</span></div>'
            f'</a>'
        )

    body = f"""  <header class="masthead">
    <div>
      <p class="eyebrow">US Equity AI Workflow</p>
      <h1>美股 AI 分析日报</h1>
      <p class="summary">每日由 <code>/scan</code> · <code>/analyze</code> · <code>/strategy</code> 三个 skill 串联产出的市场扫描、个股研究与交易计划。按日期归档，最新在上。</p>
    </div>
    <dl class="metrics" aria-label="累计统计">
      <div><dt>报告日数</dt><dd>{len(bundles)}</dd></div>
      <div><dt>Scan 报告</dt><dd>{total_scans}</dd></div>
      <div><dt>深度分析</dt><dd>{total_analyses}</dd></div>
      <div><dt>交易策略</dt><dd>{total_strategies}</dd></div>
    </dl>
  </header>
  <main>
    <section class="band">
      <div class="band-toolbar">
        <h2>每日报告</h2>
        <p class="summary" style="font-size:13px;margin:0;">点击卡片查看当日详情</p>
      </div>
      <div class="date-list">
{chr(10).join(cards)}
      </div>
    </section>
    <section class="band">
      <p class="disclaimer">本站为个人研究整理，不构成投资建议。所有交易计划都应结合账户风险、实时价格和最新公告重新确认。</p>
    </section>
  </main>"""

    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "index.html").write_text(
        page_shell("美股 AI 分析日报", body, "assets/site.css", "assets/site.js"),
        encoding="utf-8",
    )


def main() -> None:
    bundles = discover()
    REPORTS.mkdir(parents=True, exist_ok=True)
    DATES_DIR.mkdir(parents=True, exist_ok=True)

    for bundle in bundles:
        for doc in [bundle.scan, *bundle.analyses, *bundle.strategies]:
            if doc:
                render_report(doc)
        render_date_page(bundle)

    render_index(bundles)


if __name__ == "__main__":
    main()

---
name: us-stock-workflow
description: Use this skill for this repository's AI-assisted US stock analysis workflow, including market scans, ticker analysis, and trade strategy generation. Trigger when the user asks to scan US stocks, analyze a ticker, generate a long or short strategy, update reports, or work with this repo's watchlist, analyses, scans, templates, or GitHub Pages output.
---

# US Stock Workflow

This repository is a Markdown-driven US stock analysis workflow. It supports:

- Market scans: use the instructions in `references/commands/scan.md`.
- Ticker analysis: use the instructions in `references/commands/analyze.md`.
- Trade strategy generation: use the instructions in `references/commands/strategy.md`.

## Operating Rules

- Follow `AGENTS.md`, `CLAUDE.md`, `config/settings.md`, and the relevant template in `templates/`.
- Treat `references/commands` as the canonical command source. It is a symlink to `.claude/commands`, which is also used by OpenCode.
- Always use the current date in market-data queries.
- Verify prices from at least two sources before writing analysis or strategy output.
- Mark stale market data as `[stale: as of <date>]`.
- Keep prices in USD and tickers uppercase.
- Do not expose or commit sensitive data from `data/portfolio.md`.

## Publishing

When adding or updating published reports, run:

```bash
python3 scripts/build_pages.py
```

If a new report date is added, update the hardcoded `PAGES` list in `scripts/build_pages.py` so the HTML report is generated.

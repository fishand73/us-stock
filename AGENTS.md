# Repository Guidelines

## Project Structure & Module Organization

This repository stores an AI-assisted US stock analysis workflow. Source material is Markdown, organized by purpose:

- `CLAUDE.md`: project overview, slash-command workflow, and output conventions.
- `config/settings.md`: trading, scan, and analysis preferences that should guide generated reports.
- `templates/analysis_template.md`: canonical format for company deep dives.
- `templates/strategy_template.md`: canonical format for trade plans.
- `data/watchlist.md`: active ticker watchlist.
- `data/analyses/`: saved ticker analyses and strategies, named by ticker and date.
- `data/scans/`: market scan outputs, named by scan date.

## Build, Test, and Development Commands

There is no application build or automated test suite in this repository. Work directly with Markdown files.

Useful local checks:

- `rg "TICKER|YYYY" templates data`: find unfilled placeholders before finalizing an output.
- `rg --files`: list tracked content paths quickly.
- `git diff -- AGENTS.md data/ templates/ config/`: review edits when this directory is inside a Git repository.

## Coding Style & Naming Conventions

Use Markdown with clear headings, concise bullets, and tables where they improve scanability. Keep dates in `YYYY-MM-DD` format and all prices in USD. Use ticker symbols in uppercase.

Follow existing file naming patterns:

- Analysis: `data/analyses/TICKER_YYYYMMDD.md`
- Strategy: `data/analyses/TICKER_strategy_YYYYMMDD.md`
- Scan: `data/scans/scan_YYYYMMDD.md`

Preserve the terminology in `CLAUDE.md`: risk levels are `Low`, `Medium`, `High`, or `Extreme`; sentiment labels range from `Strongly Bearish` to `Strongly Bullish`; conviction scores use `1-10`.

## Testing Guidelines

Before adding or updating analysis content, manually verify that the report follows the relevant template, includes current source context, and has no placeholder fields. Check that linked strategy files exist and that watchlist entries match the latest analysis names and dates.

## Commit & Pull Request Guidelines

No Git history is available in this checkout, so no established commit convention can be inferred. Use short, imperative commit messages such as `Add NVDA analysis for 2026-05-08` or `Update scan preferences`.

Pull requests should summarize changed tickers or templates, list data sources used for new market claims, mention affected dates, and include screenshots only when rendered Markdown formatting is important.

## Security & Configuration Tips

Do not commit account balances, broker credentials, API keys, or personally identifying financial information. Keep personal risk preferences in `config/settings.md` generic enough to share safely.

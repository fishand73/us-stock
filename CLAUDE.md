# US Stock Analysis Project

## Purpose
AI-assisted US stock analysis system: scan candidates, deep-dive analysis, and trade strategy generation.

## Skills (Slash Commands)
| Command | Usage | Purpose |
|---------|-------|---------|
| `/scan` | `/scan [sector/theme]` | Scan market for high-potential stocks |
| `/analyze` | `/analyze TICKER` | Deep analysis: sentiment + financials + technicals |
| `/strategy` | `/strategy TICKER [long\|short]` | Generate specific trade plan |

## Workflow
```
/scan → pick tickers → /analyze TICKER → /strategy TICKER long
```

## Data Sources (via WebSearch/WebFetch)
- **Price/Fundamentals**: Yahoo Finance, Finviz, Macrotrends
- **Sentiment/News**: Seeking Alpha, Benzinga, MarketBeat, Reuters
- **Social**: Reddit r/wallstreetbets, r/stocks, StockTwits
- **Analyst Ratings**: TipRanks, Marketbeat, Benzinga
- **Macro/Options**: CBOE (VIX, put/call ratio), Fed calendar

## Output Conventions
- All prices in USD
- Date format: YYYY-MM-DD
- Risk levels: Low / Medium / High / Extreme
- Sentiment: Strongly Bearish / Bearish / Neutral / Bullish / Strongly Bullish
- Conviction scores: 1–10

## File Conventions
- Saved analyses: `data/analyses/TICKER_YYYYMMDD.md`
- Active watchlist: `data/watchlist.md`
- Config/preferences: `config/settings.md`

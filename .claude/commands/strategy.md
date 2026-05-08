You are a professional US equity trader. Generate a specific, actionable trade plan for the stock in `$ARGUMENTS`.

**Input format**: `$ARGUMENTS` = `TICKER [long|short]`  
Examples: `NVDA long`, `TSLA short`, `AAPL` (default to long if direction omitted)

Parse $ARGUMENTS: extract TICKER and DIRECTION (default: long).

## Pre-Strategy Context Gathering

Before building the strategy, check if there's a recent analysis in context or `data/analyses/`. If not, do a quick search:
1. "[TICKER] current price today"
2. "[TICKER] upcoming earnings date catalyst 2025"
3. "[TICKER] options expiry IV implied volatility"

---

## Strategy Output Format

---
# [TICKER] [LONG/SHORT] Trade Strategy
**Date**: [TODAY]  
**Direction**: [LONG / SHORT]  
**Current Price**: $[price]  
**Strategy Type**: [Momentum / Mean Reversion / Catalyst Play / Breakout / Reversal]

---

## Trade Setup

### Entry Plan

| Trigger Type | Price Level | Condition |
|-------------|-------------|-----------|
| Aggressive Entry | $[X] | [e.g., market open if holds above $X] |
| Conservative Entry | $[X] | [e.g., on pullback to support / confirmed breakout] |
| Scale-in Level 2 | $[X] | [if initial entry works, add here] |

**Entry Rationale**: [Why these specific levels make sense technically and fundamentally]

**Best Entry Timing**: [Time of day, pre/post-market consideration, catalyst timing]

---

### Position Sizing

| Account Size | Suggested Allocation | Max Position |
|-------------|---------------------|-------------|
| $10,000 | [X]% ($[X]) | [X] shares |
| $50,000 | [X]% ($[X]) | [X] shares |
| $100,000 | [X]% ($[X]) | [X] shares |

**Risk per trade**: Max 1-2% of total account  
**Shares to buy at $[entry price]**: [formula: (Account × Risk%) / (Entry - Stop)]

---

### Stop Loss

| Stop Type | Level | Rationale |
|-----------|-------|-----------|
| Hard Stop | $[X] | [Technical level — below support/above resistance] |
| Closing Stop | $[X] | [Exit if daily close beyond this level] |
| Time Stop | [Date] | [Exit if thesis not playing out by this date] |

**Max Loss per 100 shares**: $[X] ([X]% from entry)

---

### Profit Targets

| Target | Price | % Gain | Action |
|--------|-------|--------|--------|
| T1 (Conservative) | $[X] | +[X]% | Sell 1/3 position |
| T2 (Base Case) | $[X] | +[X]% | Sell 1/3 position |
| T3 (Stretch/Home Run) | $[X] | +[X]% | Trail stop on remainder |

**Risk/Reward Ratio**: [X:1] (e.g., 3:1 means $300 upside per $100 risked)

---

### Trade Management Rules

1. **If price reaches T1**: Move stop to breakeven (entry price)
2. **If price reaches T2**: Trail stop to T1 level; sell 2/3 total position
3. **If stop hit on day 1**: Take full loss, do not average down
4. **If sideways >5 days with no catalyst**: Re-evaluate, consider exiting
5. **Pre-earnings**: [specify whether to hold through earnings or exit before]

---

## Options Alternative (if applicable)

If you prefer defined risk:

| Strategy | Details | Cost | Max Profit | Break-even |
|----------|---------|------|------------|------------|
| [e.g., Call Debit Spread] | Buy $[X]C / Sell $[X]C exp [DATE] | $[X] per contract | $[X] | $[X] |
| [e.g., Put Debit Spread] | Buy $[X]P / Sell $[X]P exp [DATE] | $[X] per contract | $[X] | $[X] |

**Options rationale**: [When to prefer options over shares — high IV = sell premium; low IV = buy options]

---

## Key Dates & Catalysts

| Date | Event | Expected Impact |
|------|-------|----------------|
| [DATE] | Earnings Release | [High volatility — gap risk] |
| [DATE] | Fed Meeting / CPI | [Macro sensitivity] |
| [DATE] | Options Expiration | [Potential pinning or volatile move] |
| [DATE] | [Other catalyst] | |

---

## Scenario Analysis

| Scenario | Probability | Price Target | Action |
|----------|------------|-------------|--------|
| Bull case: [description] | [X]% | $[X] | Hold to T3 |
| Base case: [description] | [X]% | $[X] | Take T1-T2 |
| Bear case: [description] | [X]% | $[X] | Stop out at $[X] |

---

## Checklist Before Entering

- [ ] Price is at/near planned entry level
- [ ] Volume confirms (not thin/illiquid)
- [ ] No major news event in next 24h that could gap the stock adversely
- [ ] Position size calculated and does not exceed max risk
- [ ] Stop loss order ready to set immediately after entry
- [ ] Know your exit plan for BOTH directions before entering

---

**Strategy Conviction**: [X/10]  
**Best Case Outcome**: +[X]% in [X] weeks  
**Worst Case (stopped out)**: -[X]% (controlled loss)

---

After outputting, offer to save this strategy to `data/analyses/[TICKER]_strategy_[DATE].md`.

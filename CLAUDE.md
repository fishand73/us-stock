# 美股分析项目

## 目的
AI 辅助的美股分析体系：扫描候选标的、深度多维分析、生成交易策略。

## Skills（斜杠命令）
| 命令 | 用法 | 用途 |
|------|------|------|
| `/scan` | `/scan [行业/主题]` | 扫描市场，挖掘高潜力股票 |
| `/analyze` | `/analyze TICKER` | 深度分析：舆情 + 基本面 + 技术面 |
| `/strategy` | `/strategy TICKER [long\|short]` | 生成具体交易计划 |

## 工作流
```
/scan → 挑选 ticker → /analyze TICKER → /strategy TICKER long
```

## 数据源（通过 WebSearch / WebFetch 获取）
- **价格 / 基本面**：Yahoo Finance、Finviz、Macrotrends
- **舆情 / 新闻**：Seeking Alpha、Benzinga、MarketBeat、Reuters
- **社交平台**：Reddit r/wallstreetbets、r/stocks、StockTwits
- **分析师评级**：TipRanks、Marketbeat、Benzinga
- **宏观 / 期权**：CBOE（VIX、Put/Call 比率）、美联储日历

## 输出约定
- 所有价格均使用 USD
- 日期格式：YYYY-MM-DD
- 风险等级：低 / 中 / 高 / 极高
- 舆情倾向：极度看跌 / 看跌 / 中性 / 看涨 / 极度看涨
- 信念分：1–10

## 文件命名约定
- 已保存的分析：`data/analyses/TICKER_YYYYMMDD.md`
- 当前自选股：`data/watchlist.md`
- 配置 / 偏好：`config/settings.md`

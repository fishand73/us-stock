# 仓库说明

## 这个仓库是什么

AI 辅助的美股分析工作流。以 Markdown 驱动：扫描候选标的、深度分析、生成交易策略。双语（英文 + 中文）—— 自选股和分析报告中两种语言混用。

## 关键目录

- `CLAUDE.md` —— 斜杠命令工作流、数据源、输出约定
- `config/settings.md` —— 影响报告输出形态的交易/扫描/分析偏好
- `templates/` —— `analysis_template.md` 与 `strategy_template.md`，定义标准报告格式
- `.claude/commands/` —— 斜杠命令：`/scan`、`/analyze`、`/strategy`（权威源）
- `.opencode/commands/` —— 指向 `.claude/commands/` 的软链接，OpenCode 中等价可用
- `data/watchlist.md` —— 当前 ticker 自选股
- `data/analyses/` —— 已保存的分析与策略
- `data/scans/` —— 市场扫描产出
- `data/portfolio.md` —— **敏感**：真实持仓与账户金额
- `docs/` —— GitHub Pages 站点（push 到 main 时从此目录部署）
- `scripts/build_pages.py` —— 把分析 Markdown 转换为 `docs/reports/` 下的 HTML 页面

## 命令

没有构建 / 测试 / lint 套件。可用的命令：

- `python3 scripts/build_pages.py` —— 从 Markdown 源重新生成 `docs/reports/*.html`
- `rg "TICKER|YYYY" templates data` —— 在定稿前抓出未填充的占位符
- `rg --files` —— 快速文件清单

**`build_pages.py` 注意点**：脚本里的 `PAGES` 列表硬编码了具体文件名（当前是 `*_20260508.md`）。新增其他日期的分析时，必须更新脚本里的 `PAGES` 列表，否则新文件不会被发布。

## 文件命名

- 分析：`data/analyses/TICKER_YYYYMMDD.md`
- 策略：`data/analyses/TICKER_strategy_YYYYMMDD.md`
- 扫描：`data/scans/scan_YYYYMMDD.md`

正文内日期采用 `YYYY-MM-DD` 格式；价格统一使用 USD；ticker 一律大写。

## 受控词汇表（沿用自 CLAUDE.md）

- 风险等级：`低` / `中` / `高` / `极高`
- 舆情倾向：`极度看跌` / `看跌` / `中性` / `看涨` / `极度看涨`
- 信念分：`1–10` 区间

## 工作流

`/scan → 挑选 ticker → /analyze TICKER → /strategy TICKER [long|short]`

每个斜杠命令都在 `.claude/commands/` 中定义了数据时效性规则 —— 查询时始终带上当前日期、价格至少要从两个数据源核对、陈旧数据用 `[stale: as of <date>]` 标注。

## 发布

push 到 `main` 会触发 GitHub Pages 部署（`.github/workflows/pages.yml`）。`docs/` 目录是站点根。push 之前先跑一次 `build_pages.py` 更新 HTML 报告。

## 安全

不要提交账户余额、券商凭据、API 密钥或 PII。`data/portfolio.md` 包含真实持仓数据 —— 考虑把它加进 `.gitignore`，或者在分享前把内容脱敏。

## 提交信息

简短、祈使句：`Add NVDA analysis for 2026-05-08`、`Update scan preferences`。

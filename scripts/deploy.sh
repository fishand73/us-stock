#!/usr/bin/env bash
# 本地部署 docs/ 到 Cloudflare Pages
# 依赖：Node.js（提供 npx）、已运行过 `npx wrangler login`
# 自定义项目名可通过环境变量覆盖：CF_PAGES_PROJECT=xxx ./scripts/deploy.sh

set -euo pipefail

cd "$(dirname "$0")/.."

PROJECT="${CF_PAGES_PROJECT:-us-stock}"
BRANCH="${CF_PAGES_BRANCH:-main}"

echo "[1/2] 构建静态页面..."
python3 scripts/build_pages.py

echo "[2/2] 部署到 Cloudflare Pages 项目: ${PROJECT}"
npx --yes wrangler@latest pages deploy docs \
  --project-name="${PROJECT}" \
  --branch="${BRANCH}" \
  --commit-dirty=true

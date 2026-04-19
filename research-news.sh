#!/bin/bash
#
# AI News Research Automation
# 毎日実行することで、AI ニュースレポートを自動生成・PR 作成・マージする
#
# Usage:
#   ./research-news.sh                    # Run today's research
#   ./research-news.sh --skip-pr          # Create files but skip PR
#   ./research-news.sh --edit             # Let user edit report before commit

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Options
SKIP_PR=false
EDIT_REPORT=false
OPEN_EDITOR=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --skip-pr)
      SKIP_PR=true
      shift
      ;;
    --edit)
      EDIT_REPORT=true
      shift
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

echo -e "${BLUE}=== AI News Research Automation ===${NC}\n"

# Step 1: Run Python script to setup files
echo -e "${BLUE}[1/3] Running research automation...${NC}"
python3 ai_news_research.py

# Extract date from the script output
DATE=$(date +%Y%m%d)
BRANCH="news/${DATE}"

if [ "$EDIT_REPORT" = true ]; then
  REPORT_FILE="${DATE}.md"
  if [ -f "$REPORT_FILE" ]; then
    echo -e "\n${YELLOW}Opening ${REPORT_FILE} for editing...${NC}"
    ${EDITOR:-nano} "$REPORT_FILE"
    echo "Saved."
  fi
fi

if [ "$SKIP_PR" = true ]; then
  echo -e "\n${GREEN}✅ Files created and pushed to ${BRANCH}${NC}"
  echo "Skipping PR creation as requested."
  exit 0
fi

# Step 2: Create PR
echo -e "\n${BLUE}[2/3] Creating Pull Request...${NC}"

# Get highlights from the report (first 3 non-empty lines after ##)
HIGHLIGHTS=$(grep "^## " "$DATE.md" 2>/dev/null | head -3 | sed 's/^## /- /' || echo "- [See report for details]()")

PR_TITLE="news: ${DATE} AI News Report"
PR_BODY=$(cat <<EOF
## 調査日
$(date '+%Y-%m-%d')（$(date '+%A' | sed 's/^..//'))

## ハイライト
${HIGHLIGHTS}

## 変更ファイル
- \`${DATE}.md\` — 当日レポート新規追加
- \`README.md\` — ハイライト・一覧・サマリー更新
EOF
)

# Create PR using gh CLI if available
if command -v gh &> /dev/null; then
  PR_URL=$(gh pr create \
    --title "$PR_TITLE" \
    --body "$PR_BODY" \
    --base main \
    --head "$BRANCH" \
    --repo p10-con/ai_news_report 2>/dev/null || echo "")

  if [ -n "$PR_URL" ]; then
    echo -e "${GREEN}✅ PR Created: ${PR_URL}${NC}"

    # Step 3: Enable auto-merge
    echo -e "\n${BLUE}[3/3] Enabling auto-merge...${NC}"

    if gh pr merge --auto --squash "$BRANCH" 2>/dev/null; then
      echo -e "${GREEN}✅ Auto-merge enabled${NC}"
    else
      echo -e "${YELLOW}⚠️  Could not enable auto-merge. PR is ready for manual merge.${NC}"
    fi
  else
    echo -e "${YELLOW}⚠️  PR already exists or could not be created${NC}"
    echo "View the branch: git checkout $BRANCH"
  fi
else
  echo -e "${YELLOW}⚠️  gh CLI not found. Manual PR creation required:${NC}"
  echo ""
  echo "Run these commands:"
  echo "  gh pr create \\"
  echo "    --title \"$PR_TITLE\" \\"
  echo "    --body \"$PR_BODY\" \\"
  echo "    --base main \\"
  echo "    --head $BRANCH"
  echo ""
  echo "Then enable auto-merge:"
  echo "  gh pr merge --auto --squash"
fi

echo -e "\n${GREEN}✅ Workflow completed!${NC}\n"

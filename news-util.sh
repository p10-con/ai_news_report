#!/bin/bash
#
# AI News Research Utility
# Helper commands for news research workflow
#
# Usage:
#   ./news-util.sh today        # Show today's theme
#   ./news-util.sh schedule     # Show weekly schedule
#   ./news-util.sh status       # Show current PR status
#   ./news-util.sh view         # View today's report
#   ./news-util.sh edit         # Edit today's report

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Weekday themes
declare -A THEMES=(
  [0]="月 | 技術 + 実装 | 新モデル、API 更新、Next.js/Three.js AI、Python LLM"
  [1]="火 | ビジネス + デザイン | 資金調達、Figma/AI ツール、3D AI"
  [2]="水 | 技術 + 実装 | 新モデル、API 更新、Next.js/Three.js AI、Python LLM"
  [3]="木 | ビジネス + デザイン | 資金調達、Figma/AI ツール、3D AI"
  [4]="金 | 技術 + 実装 | 新モデル、API 更新、Next.js/Three.js AI、Python LLM"
  [5]="土 | 週まとめ + 深掘り | その週の重要トピック 1~2 件を深掘り"
  [6]="日 | 自由探索 | エンターテインメント寄り、興味ドリブン"
)

show_today() {
  # Python's weekday(): 0=Mon, 6=Sun. shell's date +%w: 0=Sun, 6=Sat
  SHELL_WEEKDAY=$(date +%w)
  # Convert: 0(Sun)→6, 1(Mon)→0, 2(Tue)→1, ..., 6(Sat)→5
  WEEKDAY=$(( (SHELL_WEEKDAY + 6) % 7 ))
  DATE=$(date '+%Y-%m-%d')
  THEME_INFO="${THEMES[$WEEKDAY]}"

  echo -e "${BLUE}=== Today's Theme ===${NC}"
  echo -e "Date: $DATE"
  echo -e "Theme: $THEME_INFO"

  FILE_NAME=$(date +%Y%m%d).md
  if [ -f "$FILE_NAME" ]; then
    echo -e "${GREEN}✓ Report file exists: $FILE_NAME${NC}"
  else
    echo -e "${YELLOW}○ Report file not yet created${NC}"
  fi
}

show_schedule() {
  echo -e "${BLUE}=== Weekly Schedule ===${NC}\n"

  DAYS_JA=("月" "火" "水" "木" "金" "土" "日")
  THEMES_SHORT=(
    "技術"
    "ビジネス"
    "技術"
    "ビジネス"
    "技術"
    "週まとめ"
    "自由"
  )

  for i in {0..6}; do
    printf "%s %-10s %s\n" "${DAYS_JA[$i]}" "${THEMES_SHORT[$i]}" "${THEMES[$i]}"
  done

  echo -e "\n${YELLOW}Note:${NC} 日付は日本時間（JST）を採用"
}

show_status() {
  echo -e "${BLUE}=== News Research Status ===${NC}\n"

  # Check for open PRs
  if command -v gh &> /dev/null; then
    echo "Open PR branches:"
    gh pr list --repo p10-con/ai_news_report --state open | grep "news/" || echo "  (none)"

    echo ""
    echo "Recent reports:"
    ls -1t *.md 2>/dev/null | head -5 || echo "  (no reports yet)"
  else
    echo -e "${YELLOW}gh CLI not found${NC}"
    echo "Install it to see status: brew install gh"
  fi
}

view_today() {
  FILE=$(date +%Y%m%d).md

  if [ -f "$FILE" ]; then
    less "$FILE"
  else
    echo -e "${YELLOW}Report file not found: $FILE${NC}"
    echo "Create it with: ./research-news.sh"
  fi
}

edit_today() {
  FILE=$(date +%Y%m%d).md

  if [ -f "$FILE" ]; then
    ${EDITOR:-nano} "$FILE"
    echo "Saved."
  else
    echo -e "${YELLOW}Report file not found: $FILE${NC}"
    echo "Create it with: ./research-news.sh"
  fi
}

# Main
CMD="${1:-today}"

case "$CMD" in
  today)
    show_today
    ;;
  schedule)
    show_schedule
    ;;
  status)
    show_status
    ;;
  view)
    view_today
    ;;
  edit)
    edit_today
    ;;
  *)
    echo "Usage:"
    echo "  $0 today      Show today's theme"
    echo "  $0 schedule   Show weekly schedule"
    echo "  $0 status     Show PR/report status"
    echo "  $0 view       View today's report"
    echo "  $0 edit       Edit today's report"
    ;;
esac

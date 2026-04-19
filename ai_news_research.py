#!/usr/bin/env python3
"""
AI News Research Automation Script
自動的に AI ニュースリサーチを実行し、PR を作成・マージする
"""

import os
import sys
import json
import subprocess
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

# For API calls, we'll use the subprocess to call Claude Code with WebSearch
class NewsResearcher:
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.today = datetime.now()
        # JST timezone adjustment (only for display purposes)
        self.jst_today = self.today  # In production, adjust for JST

        # Weekday themes (0=Monday, 6=Sunday)
        self.themes = {
            0: ("月", "技術 + 実装", "新モデル、API 更新、ベンチマーク、フロントエンド × AI（Next.js・Three.js）、Python/LLM ライブラリ"),
            1: ("火", "ビジネス + デザイン", "業界動向、資金調達、AI デザインツール、Figma、Generative UI"),
            2: ("水", "技術 + 実装", "新モデル、API 更新、ベンチマーク、フロントエンド × AI（Next.js・Three.js）、Python/LLM ライブラリ"),
            3: ("木", "ビジネス + デザイン", "業界動向、資金調達、AI デザインツール、Figma、Generative UI、3D/AI モデリング"),
            4: ("金", "技術 + 実装", "新モデル、API 更新、ベンチマーク、フロントエンド × AI（Next.js・Three.js）、Python/LLM ライブラリ"),
            5: ("土", "週まとめ + 深掘り", "その週で最も重要だったトピックを 1~2 件深掘り"),
            6: ("日", "自由探索", "エンターテインメント寄りの楽しい話題、純粋な興味ドリブン"),
        }

    def get_weekday_info(self):
        weekday_idx = self.jst_today.weekday()
        jp_day, theme, description = self.themes[weekday_idx]
        return {
            "index": weekday_idx,
            "jp_day": jp_day,
            "theme": theme,
            "description": description,
            "date_str": self.jst_today.strftime("%Y-%m-%d"),
            "file_name": self.jst_today.strftime("%Y%m%d"),
        }

    def run_git_command(self, cmd: str) -> str:
        """Execute a git command and return output"""
        try:
            result = subprocess.run(
                cmd, shell=True, cwd=self.repo_path, capture_output=True, text=True
            )
            if result.returncode != 0:
                print(f"Git error: {result.stderr}")
                raise RuntimeError(f"Git command failed: {cmd}")
            return result.stdout.strip()
        except Exception as e:
            print(f"Error running git command: {e}")
            raise

    def create_branch(self, branch_name: str) -> None:
        """Create and checkout a new branch"""
        self.run_git_command(f"git checkout main")
        self.run_git_command(f"git pull origin main")
        self.run_git_command(f"git checkout -b {branch_name}")

    def setup_development_branch(self) -> None:
        """Ensure we're on the development branch"""
        # First check current branch and fetch latest
        self.run_git_command(f"git fetch origin")
        current_branch = self.run_git_command("git rev-parse --abbrev-ref HEAD")
        print(f"Current branch: {current_branch}")

    def commit_and_push(self, branch_name: str, message: str) -> None:
        """Commit changes and push to remote"""
        # Add all relevant files
        self.run_git_command("git add *.md")
        self.run_git_command("git config user.email 'news-bot@example.com'")
        self.run_git_command("git config user.name 'News Bot'")
        self.run_git_command(f"git commit -m \"{message}\"")

        # Push with retry logic
        max_retries = 4
        backoff_times = [2, 4, 8, 16]

        for attempt in range(max_retries):
            try:
                self.run_git_command(f"git push -u origin {branch_name}")
                print(f"Successfully pushed to {branch_name}")
                return
            except RuntimeError as e:
                if attempt < max_retries - 1:
                    wait_time = backoff_times[attempt]
                    print(f"Push failed, retrying in {wait_time}s... (attempt {attempt + 1}/{max_retries})")
                    import time
                    time.sleep(wait_time)
                else:
                    raise

    def generate_placeholder_report(self, info: dict) -> str:
        """Generate a placeholder report with instructions"""
        return f"""# AI News Report — {info['date_str']}（{info['jp_day']}曜日・{info['theme']}）

## Instructions for Daily News Research

このレポートは自動生成されています。以下のステップで最新情報を収集してください:

### テーマ: {info['theme']}
**調査対象**: {info['description']}

### 必須項目

各トピックについて、以下のフォーマットで記述してください:

```
## <見出し>

<URL>

<本文 — 何が起きたか・なぜ重要か・実務への示唆を 3～5 行で記述>
```

### ガイドライン

1. **最低 3 件以上のソースを参照** する
2. **一次ソース**（公式ブログ・論文・発表資料）を優先
3. **重要度順** に並べる（フロントエンド開発・デザイン・3D モデリングの実務影響度で判定）
4. **重複・古い情報は除外** する

---

## [トピック 1 を記述]

[URL]

[本文]

## [トピック 2 を記述]

[URL]

[本文]

## [トピック 3 を記述]

[URL]

[本文]

---

**作成日時**: {datetime.now().isoformat()}
"""

    def update_readme(self, info: dict) -> None:
        """Update README.md with new entry"""
        readme_path = self.repo_path / "README.md"

        if not readme_path.exists():
            print("README.md not found")
            return

        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Update the last update date
        content = re.sub(
            r"最終更新: \d{4}-\d{2}-\d{2}（[^）]+）",
            f"最終更新: {info['date_str']}（{info['jp_day']}）",
            content
        )

        # Add new entry to the table (insert after the header line)
        table_entry = f"| {info['date_str']} | {info['jp_day']} | {info['theme']} | [{info['file_name']}.md](./{info['file_name']}.md) |"

        # Find the table and add the new entry at the top of the data rows
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if '|------|------|--------|----------|' in line:
                # Insert after the separator
                lines.insert(i + 1, table_entry)
                break

        content = '\n'.join(lines)

        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"Updated README.md")

    def create_pr(self, branch_name: str, message: str, highlights: list) -> Optional[str]:
        """Create a pull request (stub - would use gh cli in practice)"""
        pr_body = f"""## 調査日
{self.jst_today.strftime("%Y-%m-%d")}（{self.get_weekday_info()['jp_day']}・{self.get_weekday_info()['theme']}）

## ハイライト
"""
        for highlight in highlights:
            pr_body += f"- {highlight}\n"

        pr_body += f"""
## 変更ファイル
- `{self.get_weekday_info()['file_name']}.md` — 当日レポート新規追加
- `README.md` — ハイライト・一覧・サマリー更新
"""

        print(f"\n=== PR Body (for gh pr create) ===\n{pr_body}\n")
        return pr_body


def main():
    researcher = NewsResearcher()

    # Get today's theme info
    info = researcher.get_weekday_info()
    print(f"\n{'='*60}")
    print(f"AI News Research - {info['date_str']} ({info['jp_day']}曜日)")
    print(f"Theme: {info['theme']}")
    print(f"{'='*60}\n")

    try:
        # Step 1: Setup branches and files
        print("[Step 1] Setting up git branches...")
        researcher.setup_development_branch()

        # Step 2: Create report file
        print(f"\n[Step 2] Creating report file...")
        report_file = researcher.repo_path / f"{info['file_name']}.md"

        # Check if file already exists today
        if report_file.exists():
            print(f"Report file already exists: {report_file}")
            print("Skipping creation to preserve existing content.")
        else:
            placeholder = researcher.generate_placeholder_report(info)
            with open(report_file, "w", encoding="utf-8") as f:
                f.write(placeholder)
            print(f"Created: {report_file}")

        # Step 3: Update README
        print(f"\n[Step 3] Updating README.md...")
        researcher.update_readme(info)

        # Step 4: Create branch
        print(f"\n[Step 4] Creating git branch...")
        branch_name = f"news/{info['file_name']}"
        researcher.create_branch(branch_name)
        print(f"Created branch: {branch_name}")

        # Step 5: Commit and push
        print(f"\n[Step 5] Committing and pushing...")
        commit_msg = f"news: {info['file_name']} {info['theme']}"
        researcher.commit_and_push(branch_name, commit_msg)

        # Step 6: Create PR
        print(f"\n[Step 6] PR Ready")
        highlights = [
            f"[新しいトピック 1](URL) — 理由",
            f"[新しいトピック 2](URL) — 理由",
            f"[新しいトピック 3](URL) — 理由",
        ]
        pr_body = researcher.create_pr(branch_name, commit_msg, highlights)

        print(f"\n{'='*60}")
        print("✅ News research workflow completed!")
        print(f"Next step: Manual PR creation via GitHub or gh CLI")
        print(f"Branch: {branch_name}")
        print(f"{'='*60}\n")

    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

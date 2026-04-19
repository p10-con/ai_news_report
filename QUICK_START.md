# AI News Research — Quick Start Guide

毎日 30 秒で AI ニュースリサーチ自動化ワークフローを実行できます。

---

## ⚡ 30 秒クイックスタート

### 1. 今日のテーマを確認

```bash
./news-util.sh today
```

出力例:
```
=== Today's Theme ===
Date: 2026-04-19
Theme: 日 | 自由探索 | エンターテインメント寄り、興味ドリブン
```

### 2. レポートファイルを自動生成

```bash
./research-news.sh --skip-pr
```

これにより:
- `20260419.md` が作成される
- `README.md` が更新される
- `news/20260419` ブランチが作成される
- コミット・プッシュが実行される

### 3. ニュースを記述（手動）

```bash
./news-util.sh edit
```

または:

```bash
nano 20260419.md
```

対応するテーマで Web 検索を行い、見つけたニュースを記述します。

**フォーマット:**
```markdown
## <見出し>

<URL>

<本文 — 何が起きたか・なぜ重要か・実務への示唆を 3～5 行で記述>
```

### 4. PR を作成・マージ

```bash
./research-news.sh
```

（既にファイルとブランチが存在する場合）

または手動で:
```bash
gh pr create --title "news: 20260419 AI ニュース" --body "..."
gh pr merge --auto --squash
```

---

## 📅 曜日別テーマと検索キーワード

### 月・水・金 — 技術 + 実装

```
新モデル、API 更新、ベンチマーク、
Next.js/Three.js × AI、Python/LLM ライブラリ
```

**検索例:**
```
Claude API 新機能
GPT-5 発表
Next.js AI integration 2026
LangChain 最新版
```

### 火・木 — ビジネス + デザイン

```
業界動向、資金調達、
Figma/AI デザインツール、3D/AI モデリング
```

**検索例:**
```
AI スタートアップ 資金調達 Q1 2026
Figma Make AI 正式リリース
Anthropic 新資金
3D AI モデリング Blender Houdini
```

### 土 — 週まとめ + 深掘り

月～金のファイルから最重要トピック 1~2 件を選び、150～300 字で深掘り。

### 日 — 自由探索

AI 関連なら何でも OK（実務性不問）

---

## 🛠️ 便利なコマンド

| コマンド | 説明 |
|---------|------|
| `./news-util.sh today` | 今日のテーマを表示 |
| `./news-util.sh schedule` | 週間スケジュール表示 |
| `./news-util.sh status` | PR・レポート状態確認 |
| `./news-util.sh view` | 今日のレポート表示 |
| `./news-util.sh edit` | 今日のレポート編集 |

---

## 📝 完全な日次ワークフロー例

### Monday 月曜日

```bash
# 9:00 — ファイル自動生成
./research-news.sh --skip-pr

# 9:10 — ニュース検索と記述
# Chrome で以下を検索:
#   - "Claude API updates April 2026"
#   - "Next.js 15 AI features"
#   - "LangChain v0.2 release"
./news-util.sh edit

# 9:30 — PR 作成・マージ
./research-news.sh
```

### Saturday 土曜日

```bash
# 月～金のファイルを読む
cat 20260414.md 20260415.md 20260416.md 20260417.md 20260418.md | less

# 最重要 1~2 件を選ぶ
# → 20260419.md に深掘り記事を追加
./news-util.sh edit

# README.md も更新（オプション）

# PR 作成
./research-news.sh
```

---

## ❓ よくある質問

### Q: gh CLI がない場合は？

```bash
# インストール
brew install gh  # macOS
# または
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/linux stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update && sudo apt install gh
```

### Q: レポートを修正したい

```bash
# 編集
./news-util.sh edit

# 元のブランチにプッシュ
git add 20260419.md
git commit -m "fix: update report"
git push
```

### Q: 手動で PR を作成したい

```bash
gh pr create \
  --title "news: 20260419 テーマ" \
  --body "見つけたニュース: ..." \
  --base main \
  --head news/20260419

gh pr merge --auto --squash
```

---

## 📚 詳細ガイド

さらに詳しい情報は `AUTOMATION.md` を参照:

```bash
less AUTOMATION.md
```

---

## ✅ チェックリスト（各レポート作成時）

- [ ] URL は実在し、クリック可能か？
- [ ] 一次ソース（公式ブログ・論文）か？
- [ ] 重複・古い情報でないか？
- [ ] フロントエンド/デザイン/3D の実務影響度は？
- [ ] 3～5 行で本質が説明されているか？
- [ ] 重要度順に並べているか？

---

## 🚀 自動実行（cron）

毎日 08:00 JST に自動実行:

```bash
crontab -e

# 追加:
0 23 * * * cd /home/user/ai_news_report && ./research-news.sh >> /tmp/news-research.log 2>&1
```

（`23:00 UTC = 08:00 JST`）

---

**Ready?** `./news-util.sh today` で今日のテーマを確認してスタート！ 🎯

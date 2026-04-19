# AI News Research Automation Guide

このドキュメントは、AI ニュースリサーチの自動化フローを説明しています。

---

## 概要

2 つの主要スクリプトで、毎日の AI ニュースリサーチを自動化します:

1. **`ai_news_research.py`** — Python スクリプト（ファイル作成・git 操作）
2. **`research-news.sh`** — Shell ラッパー（全フロー統合）

---

## セットアップ

### 1. 環境構築

```bash
# リポジトリをクローン
git clone https://github.com/p10-con/ai_news_report.git
cd ai_news_report

# gh CLI のインストール（GitHub 統合用）
# macOS
brew install gh

# Linux
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/linux stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update && sudo apt install gh

# Windows (Chocolatey)
choco install gh
```

### 2. GitHub 認証

```bash
# gh CLI で GitHub にログイン
gh auth login

# リポジトリの設定確認
gh repo set-default p10-con/ai_news_report
```

### 3. Git ローカル設定（オプション）

スクリプトは自動的に git config を設定しますが、グローバル設定を使用したい場合:

```bash
git config --global user.email "your-email@example.com"
git config --global user.name "Your Name"
```

---

## 使用方法

### 基本的な実行

毎日、以下のコマンドでニュースリサーチを実行します:

```bash
./research-news.sh
```

このコマンドは:
1. ✅ 当日の日付レポートファイル（`YYYYMMDD.md`）を作成
2. ✅ テーマに応じたプレースホルダーを生成
3. ✅ `README.md` を更新
4. ✅ ブランチ `news/YYYYMMDD` を作成
5. ✅ コミット・プッシュ
6. ✅ PR 作成
7. ✅ Auto-merge を有効化

### オプション

#### PR 作成をスキップ（手動編集用）

```bash
./research-news.sh --skip-pr
```

ファイルを作成してプッシュしますが、PR は作成しません。
手動で内容を確認してから PR を作成できます。

#### レポート編集フロー

```bash
./research-news.sh --edit
```

ファイル作成後、デフォルトエディタ（`$EDITOR` または `nano`）で報告書を開きます。
編集完了後、自動的に PR フローに進みます。

---

## 手動でのニュース収集フロー

スクリプトは初期ファイルとして「プレースホルダー」を生成します。
**あなたが手動で最新ニュースを追加します**。

### Step 1 — Web 検索

スクリプト実行後、対応する曜日のテーマで Web 検索を行います:

| 曜日 | テーマ | 検索対象 |
|------|--------|----------|
| 月・水・金 | 技術 + 実装 | Claude/GPT 新モデル、API アップデート、Next.js/Three.js 等 AI フロントエンド、Python LLM ライブラリ |
| 火・木 | ビジネス + デザイン | 資金調達・競合、Figma/AI デザインツール、Blender/Houdini 3D AI |
| 土 | 週まとめ | その週の重要トピック 1~2 件を深掘り |
| 日 | 自由探索 | エンターテインメント寄り |

### Step 2 — レポート記述

生成された `YYYYMMDD.md` に、以下フォーマットで記述:

```markdown
## <見出し>

<URL>

<本文 — 何が起きたか・なぜ重要か・実務への示唆を 3～5 行で記述>
```

**例:**

```markdown
## Claude 3.2 announced with 200K context window

https://www.anthropic.com/news/claude-32-release

Anthropic 社が Claude 3.2 を発表し、コンテキストウインドウを 200K トークンに拡大。
エンタープライズ向けアプリケーション開発での文書処理能力が大幅向上。
Next.js + Claude API での RAG システム構築が容易になり、検索ベース AI の実装パターンが確立。
```

重要度が高い順に並べてください。

### Step 3 — README を手動更新（オプション）

ハイライトを更新したい場合、`README.md` の「今週のハイライト」セクションを編集:

```markdown
## 今週のハイライト

- **[Claude 3.2 announced](URL)** — 200K context で enterprise-grade 処理可能に
- **[Next.js 15 shipped](URL)** — Server Component 標準化で AI integration pattern が変わる
- **[MCP 仕様 1.1 リリース](URL)** — Tool calling が改善。Claude × IDE 統合が加速
```

---

## 曜日別フォーカス詳細

### 月・水・金 — 技術 + 実装

**主な検索キーワード:**
- `Claude API`, `GPT-5`, `Grok-3`
- `Next.js AI`, `Vercel AI SDK`
- `Three.js 生成`, `Babylon.js`
- `LangChain`, `LlamaIndex` 新バージョン
- `ベンチマーク比較` (MMLU, ARC, HumanEval)

**実務への視点:**
- フロントエンド開発への影響
- 既存プロジェクトへの適用可否
- パフォーマンス・コスト・精度のトレードオフ

### 火・木 — ビジネス + デザイン

**主な検索キーワード:**
- `資金調達 AI スタートアップ`
- `Figma AI 機能`
- `Anthropic`, `OpenAI`, `Mistral` ビジネス動向
- `Blender AI`, `Houdini AI`
- `Design System 自動生成`

**実務への視点:**
- チーム採用・組織構成への影響
- デザインツール・3D ツールの効率化ポテンシャル
- 業界トレンド・人材市場

### 土 — 週まとめ + 深掘り

**タスク:**
1. その週の 5 ファイル（月～金）を読み返す
2. 最も重要だったトピック 1~2 件を選定
3. 深掘り記事を作成（150～300 字）
4. `README.md` の「深掘り候補」に追加

**深掘りテンプレート:**

```markdown
## [トピック名] — 実務への 6 ヶ月インパクト予測

[月曜記事の URL]
[水曜記事の URL]
[金曜記事の URL]

### 背景

[業界全体での文脈]

### 期待される変化

[実装パターンの変化]
[チーム構成への影響]
[ツール・フレームワーク選定への影響]

### 検討すべき準備

[実装レベルでの対応]
[組織・学習レベルでの対応]
```

### 日 — 自由探索

**コンセプト:**
- AI を使ったアート・ゲーム・エンタメ
- 研究論文の新展開（ただし実務的でない可能性も OK）
- 個人的な興味ドリブン

記述フォーマットは同じですが、実務性は問われません。

---

## 毎日の実行例

### Monday 月曜日（技術 + 実装）

```bash
# Step 1: Script 実行
./research-news.sh --skip-pr

# Step 2: ニュース検索（手動）
# Chrome で以下を検索:
# - "Claude API updates 2026"
# - "Next.js AI integration"
# - "LangChain new features"

# Step 3: Report 編集
# 20260414.md を開いて、見つけたニュースを記述

# Step 4: Git push & PR
git add 20260414.md README.md
git commit -m "news: 20260414 新モデル・Next.js AI SDK"
git push origin news/20260414

# Step 5: gh で PR 作成
gh pr create --title "..." --body "..." --base main --head news/20260414
gh pr merge --auto --squash
```

### Saturday 土曜日（週まとめ）

```bash
# 月～金のファイルを読む
cat 20260414.md 20260415.md 20260416.md 20260417.md 20260418.md | less

# 最重要トピック 1~2 件ピックアップ
# → 深掘り記事を 200～300 字で記述
# → README.md の「深掘り候補」に追加

./research-news.sh
# （同様に PR 作成）
```

---

## トラブルシューティング

### gh CLI が見つからない

```bash
# インストール確認
which gh

# インストールされていない場合
brew install gh  # macOS
# または上記のセットアップセクションを参照
```

### PR 作成に失敗する

```bash
# GitHub 認証確認
gh auth status

# 再ログイン
gh auth logout
gh auth login
```

### ブランチがすでに存在する

```bash
# 既存ブランチを削除
git branch -D news/YYYYMMDD
git push origin --delete news/YYYYMMDD

# スクリプト再実行
./research-news.sh
```

### Git commit が失敗する

```bash
# ローカル git config 確認
git config user.name
git config user.email

# 設定がない場合
git config user.email "your-email@example.com"
git config user.name "Your Name"
```

---

## スケジューリング（Linux/macOS）

毎日自動実行するには、cron を設定します:

```bash
# crontab 編集
crontab -e

# 毎日 08:00 JST (UTC+9) に実行
# 注: サーバーの時刻がどのタイムゾーンかを確認してください
0 23 * * * cd /home/user/ai_news_report && ./research-news.sh >> /tmp/news-research.log 2>&1

# 実行権限確認
chmod +x /home/user/ai_news_report/research-news.sh
```

**確認:**

```bash
# cron ログを見る（macOS）
log stream --predicate 'process == "cron"'

# Linux の場合
sudo tail -f /var/log/syslog | grep CRON
```

---

## 品質チェックリスト

各レポート作成時に確認してください:

- [ ] URL は実在するか？（リンククリック確認）
- [ ] 一次ソース（公式ブログ・論文）か、まとめサイトか？
- [ ] 重複・古い情報でないか？（過去 1 ヶ月内）
- [ ] フロントエンド開発・デザイン・3D の実務影響度は？
- [ ] 3～5 行で本質を説明できているか？
- [ ] 重要度順に並べているか？（上から下へ）
- [ ] README.md の「レポート一覧」は最新化されているか？

---

## 参考資料

- GitHub CLI ドキュメント: https://cli.github.com/manual
- AI News Log リポジトリ: https://github.com/p10-con/ai_news_report

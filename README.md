# AI News Log

最終更新: 2026-04-11（土）

---

## 今週のハイライト

> ※ 直近で最も重要なトピックを 3 件、一言コメント付きで列挙する。
> 毎日更新し、より重要なニュースが出たら差し替える。

- **[Anthropic、Claude Mythos Preview を非公開で発表](https://red.anthropic.com/2026/mythos-preview/)** — フロンティアモデルを "公開しない" という判断が業界で初めて現実化（RSP が実運用された最初の例）
- **[Meta、Muse Spark を発表（MSL 初モデル）](https://ai.meta.com/blog/introducing-muse-spark-msl/)** — Meta のフラッグシップが初めてクローズドで出た、Llama のオープン路線からの大きな転換点
- **[Google DeepMind、Gemma 4 を Apache 2.0 で公開](https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/)** — 同じ週に "開ける" 方向の最有力候補が出現、オープンのハブが Llama から Gemma に移りうる

---

## 今週のサマリー

今週（4/6〜4/11）は「フロンティアモデルをどう出すか」が **閉じる / 囲う / 開ける** の三方向に分裂した週だった。Anthropic は Mythos Preview を RSP 根拠で一般公開を見送り、防衛・インフラ寄りの Project Glasswing パートナー 11 社にのみ開放。Meta は MSL 初の Muse Spark をクローズドで投入し、Llama のオープン路線から一線を引いた。同じ週に Google DeepMind が Gemma 4 を初の Apache 2.0 で公開し、オープン側の主役交代を示唆。Anthropic は Mythos と同日に Managed Agents の public beta も出しており、Shopify AI Toolkit・Figma Make Attachments と合わせて "エージェントが本番環境に直接触れる" 実戦レイヤが一段進んだ週でもあった。

---

## レポート一覧

| 日付 | 曜日 | テーマ | ファイル |
|------|------|--------|----------|
| 2026-04-11 | 土 | 週まとめ + 深掘り | [20260411.md](./20260411.md) |

---

## 深掘り候補（次の土曜用）

- Figma MCP × Shopify AI Toolkit を実プロジェクトで回したときのワークフロー比較 — デザイン→実装→本番反映のフルチェーンを MCP クライアント 1 本で通せるか
- Gemma 4 E4B をブラウザ / Node から呼び出して Next.js アプリに組み込む最小構成 — Apache 2.0 のエッジ組込みで何がどこまで動くか
- Claude Managed Agents の長時間セッションと自前 harness のコスト比較 — $0.08/session-hour を定常運用でどう評価するか
- Titans / Nested Learning 論文読み合わせ — 継続学習を agentic 構成にどう組み込むか
- Ray-Ban Meta Glasses 上での Muse Spark の挙動と UX — 実機統合が進んだタイミングで
- 商用 World Model の登場（出たら） — 3D / Blender / Houdini 観点での影響を整理

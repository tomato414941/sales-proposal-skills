# Artifact Rules

## 共通ルール

すべての artifact は Markdown で作成し、先頭に YAML frontmatter を持たせます。

必須 frontmatter:

```yaml
artifact_type: proposal_facts
schema_version: 0.1
status: draft
confidence: medium
sources:
  - user_input
assumptions: []
open_questions: []
```

`status` は次を使います。

- `draft`
- `validated`
- `locked`

`confidence` は次を使います。

- `high`
- `medium`
- `low`

原則:

- 推測は `assumptions` か本文の仮説欄へ置く
- 顧客提示禁止の内容は明記し、最終ドラフトへ直接持ち込まない
- `10_facts.md` が validated でない限り `30_strategy.md` を locked にしない
- `50_outline.md` が validated でない限り `70_deck_draft.md` を作らない

## `10_facts.md`

目的: 確認済み事実の正規化

必須セクション:

- `## 顧客情報`
- `## 提案対象`
- `## 現状課題`
- `## 制約`
- `## スケジュール`
- `## 関係者`
- `## 利用可能な根拠`

禁止:

- 推測表現
- 未確認の価格や納期の断定

## `20_gaps_and_assumptions.md`

目的: 不足情報と仮説の明示

必須セクション:

- `## 不足情報`
- `## 仮説`
- `## 仮説の根拠`
- `## 提案への影響`
- `## 要確認事項`

## `30_strategy.md`

目的: 提案の勝ち筋を定義

必須セクション:

- `## 説得対象`
- `## 主要評価軸`
- `## 訴求主軸`
- `## 差別化方針`
- `## 競合への対抗方針`
- `## 語る順番`

## `40_solution_map.md`

目的: 顧客課題と提案要素の対応付け

必須セクション:

- `## 課題と対応の対応表`
- `## 標準対応と個別対応`
- `## 導入前提`
- `## 想定効果`

## `50_outline.md`

目的: スライド単位の構成定義

必須セクション:

- `## デッキ方針`
- `## スライド一覧`

各スライドには最低限次を含めます。

- スライド番号
- タイトル
- 1枚1メッセージ
- 根拠
- 必要図表
- 話すポイント

## `60_validation.md`

目的: 出力の危険点を明示

必須セクション:

- `## Summary`
- `## Errors`
- `## Warnings`
- `## Next Actions`

## `70_deck_draft.md`

目的: 人がレビュー可能な提案ドラフト

必須セクション:

- `# 表紙`
- `# エグゼクティブサマリ`
- `# 課題整理`
- `# 提案概要`
- `# システム全体像`
- `# 導入計画`
- `# 効果`
- `# 体制`
- `# リスク`
- `# 次アクション`

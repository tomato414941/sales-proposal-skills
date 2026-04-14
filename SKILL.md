---
name: proposal-design
description: 営業提案を artifact 駆動で段階設計し、最終的に Markdown artifact 一式と PPTX を生成する主 skill です。ユーザーが渡したテキスト、議事録、RFP、製品情報、過去提案、関連ファイルをもとに `.proposal/` 配下の中間 artifact と提案ドラフトを作り、validation を通したうえで PPTX まで出すときに使ってください。確認済み事実と仮説を分離し、提案戦略、解決策マッピング、アウトライン、検証結果、提案ドラフトを順番に作ります。単なる表現修正、既存スライドの見た目調整、提案設計を伴わない単発レンダリングには使わないでください。
---

# Proposal Design

## 概要

この skill は、営業提案を `.proposal/` 配下の artifact を順番に作りながら設計し、最後に PPTX まで出力するための主 skill です。

最終成果物より先に、事実、仮説、不足情報、戦略、解決策、アウトライン、検証結果を明示してください。正本は Markdown artifact ですが、PPTX も必須成果物です。

## セットアップ

このスキルを初めて使う場合、skill ディレクトリで以下を実行してください。

```bash
npm install          # pptxgenjs（PPTX 生成に必要）
pip install pyyaml   # validator の YAML パースに必要
```

## 基本方針

- 提案作成は artifact 駆動で進める
- 事実と仮説を分離する
- validation を通す前に最終ドラフトへ進めない
- 不足情報がある場合は作り話で埋めず、`20_gaps_and_assumptions.md` と `60_validation.md` に残す
- `70_deck_draft.md` を正本としてレビューし、その内容をもとに PPTX を生成する
- PPTX は必須成果物だが、PPTX の都合で上流 artifact を歪めない

## 必須出力物

この skill は作業ディレクトリ直下の `.proposal/` に次を作成または更新します。

- `10_facts.md`
- `20_gaps_and_assumptions.md`
- `30_strategy.md`
- `40_solution_map.md`
- `50_outline.md`
- `60_validation.md`
- `70_deck_draft.md`
- `proposal.pptx`

## 最初にやること

1. 入力ソースを確認する
2. `.proposal/` がなければ初期化する
3. artifact ルールを読む
4. facts から順に artifact を埋める
5. validator を実行する
6. validation が致命的でなければ deck draft を作る
7. deck draft と outline をもとに PPTX を生成する

`.proposal/` の初期化には次を使います。

```bash
python3 scripts/init_proposal_artifacts.py --cwd "$PWD"
```

validator には次を使います。

```bash
python3 scripts/validate_proposal_artifacts.py --cwd "$PWD" --write-validation
```

PPTX 生成には次を使います。

```bash
node scripts/render_pptx.js --cwd "$PWD" --output "$PWD/.proposal/proposal.pptx"
```

## 実行順序

### 1. 入力ソース確認

次のような入力を読みます。

- ユーザーが渡したテキスト
- ローカルの Markdown、テキスト、PDF、RFP、議事録
- 製品説明や価格条件
- 過去提案

入力に対して最初に確認すること:

- 顧客名
- 提案対象
- 課題
- 制約
- 関係者
- 提出物の種類
- 既知の根拠資料

### 2. Facts を作る

`10_facts.md` には確認済み情報だけを書きます。推測を混ぜないでください。

### 3. Gaps and Assumptions を作る

`20_gaps_and_assumptions.md` には不足情報、仮説、その影響、要確認事項を書きます。

### 4. Strategy を作る

`30_strategy.md` では、誰をどの論点で説得するか、何を勝ち筋にするかを定義します。

### 5. Solution Map を作る

`40_solution_map.md` では、顧客課題と提案要素を対応付けます。標準対応か個別対応かも明示します。

### 6. Outline を作る

`50_outline.md` では、スライド単位のメッセージ、根拠、必要図表、話すポイントを作ります。

### 7. Validation を走らせる

`scripts/validate_proposal_artifacts.py` を実行し、結果を `60_validation.md` に反映します。

validation が失敗しているのに `70_deck_draft.md` を確定させないでください。

### 8. Deck Draft を作る

`70_deck_draft.md` は人がレビュー可能な提案ドラフトです。validation の指摘を無視して書き進めないでください。

### 9. PPTX を生成する

`50_outline.md` と `70_deck_draft.md` をもとに `proposal.pptx` を生成します。PPTX は必須成果物です。

生成前に確認すること:

- `60_validation.md` に unresolved error がない
- `50_outline.md` が validated
- `70_deck_draft.md` が提案本文として読める状態になっている

## 禁止事項

- 仮説を事実として `10_facts.md` に書かない
- 価格、納期、機能、対応範囲を推測で断定しない
- `50_outline.md` の根拠欄を空で放置したまま最終ドラフトへ進まない
- 顧客提示不可の情報を deck draft や PPTX に入れない
- validation の warning や error を黙って無視しない
- PPTX の見た目のために上流 artifact の意味を変えない

## 参照ファイル

- [artifact_rules.md](references/artifact_rules.md): artifact ごとの役割、必須セクション、frontmatter ルール
- [outline_template.md](references/outline_template.md): `50_outline.md` の書き方
- [deck_template.md](references/deck_template.md): `70_deck_draft.md` の書き方
- [validation_checklist.md](references/validation_checklist.md): validation 観点

## 実行リソース

- `scripts/init_proposal_artifacts.py`: `.proposal/` を初期化する
- `scripts/render_pptx.js`: `.proposal/50_outline.md` と `.proposal/70_deck_draft.md` から PPTX を生成する
- `scripts/validate_proposal_artifacts.py`: artifact 一式を検証する

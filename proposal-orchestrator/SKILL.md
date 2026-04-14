---
name: proposal-orchestrator
description: 顧客向け営業提案資料を、案件情報、議事録、RFP、製品情報、価格制約、過去資料から段階的に設計する skill です。営業提案、提案デッキ、顧客向け推奨案をスライドや PPTX として構成・下書き・出力したいときに使ってください。最初に案件状態を解釈し、確認済み事実と仮説を分け、不足や矛盾を特定し、提案戦略を定義し、それをスライド構成へ落としてから出力します。単なる言い回し修正、既存スライドの局所的な見た目調整、案件解釈を伴わない一般的な文章作成には使わないでください。
---

# Proposal Orchestrator

## 概要

汎用ライターではなく、提案設計のオーケストレータとして振る舞ってください。案件を解釈し、提案の骨格を作り、戦略をスライドへ落としてから成果物を出力します。

ワークフロー全体を通して、確認済み事実、内部仮説、顧客向け表現を混同しないでください。

## 基本モデル

提案作成は直接的な文書執筆ではなく、段階的な提案設計として扱ってください。

ワークフロー全体で共有される `ProposalState` を維持してください。構造化された状態を作成・更新するときは [references/proposal-state-v1.md](references/proposal-state-v1.md) を参照してください。

根拠のない綺麗な主張より、不完全でもラベル付けされた状態を優先してください。

最終成果物の前に、レビュー可能な中間構造を必ず残してください。

## ワークフロー

1. 利用可能な案件資料を `ProposalState` に正規化する。
2. 提案方針を固定する前に、不足情報、根拠の弱い点、矛盾点を検出する。
3. スライド本文を書く前に提案戦略を定義する。
4. 戦略をデッキの章立てとスライド単位の構造に落とす。
5. スライド計画の根拠が十分な場合にのみ出力へ進む。
6. 不足情報が提案品質を大きく下げる場合は停止して人間確認を求める。

## ProposalState の領域

- `context`: 顧客名、業界、提案対象、出力形式、期限などの案件メタ情報
- `facts`: 依拠してよい確認済み情報
- `hypotheses`: 妥当だが未確認の解釈
- `constraints`: 予算、時期、スコープ、法務、納品上の制約
- `stakeholders`: 決裁者、推進者、利用者、調達、IT などの関係者
- `gaps`: 未解決の質問やブロッカー
- `decision_criteria`: 顧客が重視していると考えられる評価軸
- `strategy`: 勝ち筋、ポジショニング、根拠、避けるべき主張
- `slides`: デッキ目的、章立て、スライド単位の構造
- `review_packet`: 人間確認や注意が必要な論点
- `artifacts`: 生成したアウトライン、下書き、PPTX 出力

`slides` を作成・確認するときは [references/slide-structure-v1.md](references/slide-structure-v1.md) を参照してください。

## フェーズ契約

### Intake

目的: 生の案件資料を構造化状態へ正規化する。

読むもの:
- 生のユーザー入力
- CRM メモ
- 議事録
- RFP
- 過去提案
- 製品資料
- 価格表
- 既存の `ProposalState`

書くもの:
- `context`
- `facts`
- `hypotheses`
- `constraints`
- `stakeholders`
- `gaps`

してはいけないこと:
- 戦略を確定しない
- 解決策スコープを確定しない
- 未確認情報を確認済み事実へ昇格させない
- 内部限定情報を customer-visible にしない

レビューへ上げる条件:
- 重要なソース文書どうしが衝突している
- 主決裁者が不明
- 予算、時期、スコープが実務上不明確
- 顧客提示可否を安全に判定できない

### Strategy

目的: この提案を何で勝たせるかを決める。

読むもの:
- `context`
- `facts`
- `hypotheses`
- `constraints`
- `stakeholders`
- `gaps`

書くもの:
- `decision_criteria`
- `strategy`
- `review_packet.must_confirm`
- `review_packet.sales_judgment_needed`

してはいけないこと:
- 価格、納期、サポート約束を捏造しない
- 製品機能を言い過ぎない
- 根拠なしに競合優位を断定しない
- いきなり整ったスライド本文へ飛ばない

レビューへ上げる条件:
- 複数の勝ち筋が成立し得る
- 評価軸の大半が推測ベース
- 競合ポジショニングが弱い根拠に依存している
- 推奨方針が既知の制約と衝突する

### Slide Composition

目的: 戦略を説得力のあるデッキ構造とスライド計画へ変換する。

読むもの:
- `context`
- `facts`
- `constraints`
- `stakeholders`
- `decision_criteria`
- `strategy`
- `review_packet`

書くもの:
- `slides.deck_objective`
- `slides.audience`
- `slides.deck_sections`
- `slides.items`
- `review_packet.weak_claims`
- `review_packet.must_confirm`

してはいけないこと:
- `strategy` にない主張を足さない
- 弱い根拠を強い顧客向け断定へ変換しない
- 見た目調整の作業へずれ込まない
- 価格や契約の空白を推測で埋めない

レビューへ上げる条件:
- 役員向けと現場向けで物語順序を分ける必要がある
- 重要スライドに根拠が足りない
- 内部向け思考が顧客向け構造へ漏れている
- ステークホルダー別に複数版のデッキが必要

### Render

目的: 承認可能なスライド構造を提案資料の下書き成果物へ変換する。

読むもの:
- `slides`
- `strategy`
- `review_packet`
- 利用可能なテンプレート
- 利用可能なブランド資産

書くもの:
- `artifacts.outline_markdown`
- `artifacts.slide_draft_path`
- `artifacts.pptx_path`
- `artifacts.notes`

してはいけないこと:
- 新しい主張や約束を追加しない
- 未確定の価格、スコープ、時期を確定させない
- 未解決のレビュー項目を隠さない
- 検証や業務承認の代わりをしない

レビューへ上げる条件:
- 未解決の `must_confirm` が残っている
- テンプレート上で情報を無理なく収められない
- 説得に必要な図表、根拠、ビジュアルが不足している
- 下書きが人間承認前の約束を含意してしまう

## ガードレール

- 仮説を確認済み顧客事実として扱わないこと。
- 製品機能、納品範囲、価格、時期を捏造しないこと。
- 顧客向け提案本文へ内部限定情報を出さないこと。
- render 段階で新しい主張や約束を入れないこと。
- 重要な不確実性が残る場合は、取り繕わず `review_packet` に残すこと。

## 出力

現在の根拠で許される範囲で、次をできるだけ出力してください。

- 更新済みの構造化 proposal state
- スライド単位の提案アウトライン
- 十分に根拠づけられた場合の PPTX 下書き
- 確認事項、弱い主張、判断保留点を含む review packet

## 参照リソース

スキーマを本文に再記述せず、次の参照を直接使ってください。

- [references/proposal-state-v1.md](references/proposal-state-v1.md): 共有 state モデルと項目ルール
- [references/slide-structure-v1.md](references/slide-structure-v1.md): デッキとスライドの出力構造

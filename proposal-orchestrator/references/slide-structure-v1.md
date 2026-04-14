# Slide Structure v1

`ProposalState` 内の `slides` を作成するときはこのファイルを使ってください。

## 目的

- rendering 前のスライド設計を構造中心で保つ。
- 完成デザインがなくても各スライドをレビュー可能にする。
- スライドの意図と話者向け補足を分離する。

## `slides` Shape

```json
{
  "deck_objective": "string",
  "audience": ["executive", "business", "it", "procurement"],
  "deck_sections": [
    {
      "id": "string",
      "title": "string",
      "purpose": "string"
    }
  ],
  "items": [
    {
      "id": "string",
      "section_id": "string",
      "title": "string",
      "slide_purpose": "string",
      "key_message": "string",
      "supporting_points": ["string"],
      "evidence_needed": ["string"],
      "speaker_notes_seed": ["string"],
      "status": "draft|review_needed|approved"
    }
  ]
}
```

## 構成ルール

- 個別スライドを書く前に、まず deck objective を定義してください。
- スライドは意味のある `deck_sections` の下へまとめてください。極端に短いデッキ以外はフラットな列挙にしないでください。
- `key_message` は段落ではなく、1つの主張または takeaway にしてください。
- `supporting_points` には、その主張を支える最小限の論点を入れてください。
- `evidence_needed` には、必要だがまだ埋め込まれていない根拠を入れてください。
- `speaker_notes_seed` には、スライド面に載せない話し方、注意点、ニュアンスを入れてください。

## 典型的な章立てパターン

これは固定テンプレートではなく、あくまで典型パターンです。

- 背景と課題
- なぜ今変えるのか
- 推奨アプローチ
- 解決策の範囲
- 期待効果
- 導入または展開計画
- 金額と前提条件
- 次のアクション

## レビューが必要な条件

次の場合は slide item を `review_needed` にしてください。

- key message が弱い根拠や推測に依存している
- スライドが未承認の価格、スコープ、時期の確定を含意している
- 想定 audience が曖昧である
- 内部限定の思考がスライド本体に乗っており、`speaker_notes_seed` か `review_packet` に逃がすべきである

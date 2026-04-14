# ProposalState v1

共有 proposal state を作成・更新するときはこのファイルを使ってください。

## 目的

- 確認済み事実と仮説を分離する。
- 情報源を追跡できるようにする。
- 顧客向け出力に使ってよい情報かどうかを明示する。
- 自由文ではなく state の領域に沿って考えさせる。

## トップレベル構造

```json
{
  "proposal_id": "string",
  "version": 1,
  "updated_at": "ISO-8601",
  "status": "intake|strategy|composition|render_ready|rendered|blocked",
  "context": {},
  "facts": [],
  "hypotheses": [],
  "constraints": [],
  "stakeholders": [],
  "gaps": [],
  "decision_criteria": [],
  "strategy": {},
  "slides": {},
  "review_packet": {},
  "artifacts": {}
}
```

## 共通エントリ構造

`facts` `hypotheses` `constraints` `decision_criteria` の各要素は、別途専用構造がない限りこの形を使ってください。

```json
{
  "id": "string",
  "label": "string",
  "value": "string|number|object|array",
  "source": {
    "type": "crm|meeting_notes|rfp|pricing_sheet|product_doc|past_proposal|manual",
    "ref": "string"
  },
  "confidence": "high|medium|low",
  "customer_visible": true,
  "status": "confirmed|inferred|draft|blocked",
  "updated_at": "ISO-8601"
}
```

## State の領域

### `context`

提案全体のメタ情報に使います。例:

- `account_name`
- `industry`
- `offering`
- `target_output`
- `deadline`
- `proposal_owner`

### `facts`

提案の主張の根拠にしてよい確認済み情報に使います。

例:

- current customer environment
- stated deadlines
- confirmed budget range
- explicitly named competitors

### `hypotheses`

妥当だが未確認の解釈に使います。

例:

- likely evaluation priority
- suspected political dynamics
- likely concern about migration risk

### `constraints`

変更できない制約に使います:

- budget caps
- scope exclusions
- compliance limitations
- delivery deadlines
- support limitations

### `stakeholders`

以下の専用構造を使ってください。

```json
{
  "id": "string",
  "name": "string",
  "role": "decision_maker|economic_buyer|champion|end_user|procurement|it|other",
  "organization": "string",
  "priority": "high|medium|low",
  "goals": ["string"],
  "concerns": ["string"],
  "source": {
    "type": "crm|meeting_notes|manual",
    "ref": "string"
  },
  "confidence": "high|medium|low",
  "customer_visible": false,
  "status": "confirmed|inferred|draft"
}
```

### `gaps`

未解決の質問とブロッカーに使います。

```json
{
  "id": "string",
  "question": "string",
  "reason": "string",
  "blocking": true,
  "owner": "sales|solutions|customer|legal|unknown",
  "status": "open|resolved|deferred"
}
```

### `strategy`

ばらばらのメモではなく、単一オブジェクトで管理してください。

```json
{
  "primary_goal": "string",
  "win_theme": "string",
  "positioning": "string",
  "key_messages": ["string"],
  "competitive_angle": ["string"],
  "proof_points": ["string"],
  "risks": ["string"],
  "do_not_claim": ["string"],
  "status": "draft|review_needed|approved"
}
```

### `review_packet`

スライド本文に埋もれさせてはいけない業務レビュー項目を保持します。

```json
{
  "must_confirm": ["string"],
  "weak_claims": ["string"],
  "visibility_risks": ["string"],
  "pricing_risks": ["string"],
  "timeline_risks": ["string"],
  "sales_judgment_needed": ["string"]
}
```

### `artifacts`

生成ファイルと出力結果の記録に使います。

```json
{
  "outline_markdown": "string",
  "slide_draft_path": "string",
  "pptx_path": "string",
  "notes": ["string"]
}
```

## 項目ルール

- 不確実な情報は `hypotheses` または `status: inferred` に置き、確認済み事実へ押し込まないでください。
- 内部推論、価格の細則、承認状況、競合推測などは原則 `customer_visible: false` にしてください。
- `confidence` は表現の強さではなく、根拠の質を表すために使ってください。
- 文書、議事録、社内システムなどに由来する情報は source を残してください。
- 長い散文より、小さい構造化エントリを優先してください。

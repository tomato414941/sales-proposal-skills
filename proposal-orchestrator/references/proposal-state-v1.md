# ProposalState v1

Use this file when creating or updating the shared proposal state.

## Goals

- Keep confirmed facts separate from hypotheses.
- Preserve source traceability.
- Mark whether content is safe for customer-facing output.
- Keep the model focused on state areas instead of freeform narrative.

## Top-Level Shape

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

## Shared Entry Shape

Use this shape for entries in `facts`, `hypotheses`, `constraints`, and `decision_criteria` unless a more specific structure is defined elsewhere.

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

## State Areas

### `context`

Use for proposal-level metadata such as:

- `account_name`
- `industry`
- `offering`
- `target_output`
- `deadline`
- `proposal_owner`

### `facts`

Use for confirmed information that can safely anchor proposal claims.

Examples:

- current customer environment
- stated deadlines
- confirmed budget range
- explicitly named competitors

### `hypotheses`

Use for informed but unconfirmed interpretations.

Examples:

- likely evaluation priority
- suspected political dynamics
- likely concern about migration risk

### `constraints`

Use for hard boundaries:

- budget caps
- scope exclusions
- compliance limitations
- delivery deadlines
- support limitations

### `stakeholders`

Use the specialized shape below.

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

Use for unresolved questions and blockers.

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

Use a single object rather than a loose note.

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

Capture business review items that should not be hidden in slide prose.

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

Use for generated files and output traces.

```json
{
  "outline_markdown": "string",
  "slide_draft_path": "string",
  "pptx_path": "string",
  "notes": ["string"]
}
```

## Field Rules

- Mark uncertain information as `hypotheses` or `status: inferred`; do not push it into confirmed facts.
- Set `customer_visible: false` by default when the item is internal reasoning, pricing nuance, approval status, or competitive speculation.
- Use `confidence` to express evidence quality, not rhetorical confidence.
- Preserve source references whenever information originates from a document, call note, or internal system.
- Prefer small structured entries over large prose blocks.

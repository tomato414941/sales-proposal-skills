# Slide Structure v1

Use this file when creating `slides` inside `ProposalState`.

## Goals

- Keep slide composition structural before rendering.
- Make each slide reviewable without requiring finished design work.
- Separate slide intent from presenter detail.

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

## Composition Rules

- Define the deck objective before composing individual slides.
- Group slides under meaningful `deck_sections`; do not leave the deck as a flat list unless the deck is trivially short.
- Make `key_message` a single claim or takeaway, not a paragraph.
- Use `supporting_points` for the minimum argument structure needed to support the message.
- Use `evidence_needed` for proof that is required but not yet embedded.
- Use `speaker_notes_seed` for talking points, caveats, and nuances that may not belong on the slide face.

## Typical Section Patterns

Use these as patterns, not mandatory templates.

- Context and challenge
- Why change now
- Recommended approach
- Solution scope
- Expected value
- Delivery or rollout plan
- Commercials and assumptions
- Next steps

## Review Triggers

Mark slide items as `review_needed` when:

- the key message depends on weak or inferred evidence
- the slide implies pricing, scope, or timeline certainty that is not approved
- the intended audience is unclear
- the slide is carrying internal-only reasoning that should move into `speaker_notes_seed` or `review_packet`

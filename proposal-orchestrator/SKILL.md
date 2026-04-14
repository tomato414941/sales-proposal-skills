---
name: proposal-orchestrator
description: Orchestrate the creation of customer-facing sales proposal materials from deal context, notes, RFPs, product information, pricing constraints, and prior artifacts. Use this skill when the user wants to design, structure, draft, or render a sales proposal, proposal deck, or customer-facing recommendation into slides or PPTX. Interpret deal state first, separate confirmed facts from hypotheses, identify missing or conflicting information, define the proposal strategy, convert it into slide structure, and only then render outputs. Do not use this skill for simple wording edits, isolated slide polishing, or generic writing tasks that do not require proposal-state interpretation.
---

# Proposal Orchestrator

## Overview

Act as a proposal-design orchestrator, not a generic writer. Interpret the deal, structure the proposal, turn the strategy into slides, and only then render draft artifacts.

Preserve the distinction between confirmed facts, internal hypotheses, and customer-facing proposal language throughout the workflow.

## Core Working Model

Treat proposal creation as staged proposal design rather than direct document writing.

Maintain a shared `ProposalState` across the workflow. Read [references/proposal-state-v1.md](references/proposal-state-v1.md) when creating or updating structured state.

Prefer incomplete but well-labeled state over polished unsupported claims.

Produce reviewable intermediate structure before final artifacts.

## Workflow

1. Normalize the available deal materials into `ProposalState`.
2. Detect missing, weak, or conflicting information before committing to a proposal direction.
3. Define the proposal strategy before drafting slide content.
4. Convert the strategy into deck sections and slide-level structure.
5. Render outputs only after the slide plan is sufficiently grounded.
6. Stop and request human confirmation when missing information would materially weaken the proposal.

## ProposalState Areas

- `context`: account, industry, offering, target output, deadlines, and similar case metadata
- `facts`: confirmed information that is safe to rely on
- `hypotheses`: informed but unconfirmed interpretations
- `constraints`: budget, timing, scope, compliance, or delivery limits
- `stakeholders`: decision makers, champions, users, procurement, IT, and influencers
- `gaps`: unresolved questions and blocking uncertainties
- `decision_criteria`: what the customer is likely optimizing for
- `strategy`: win theme, positioning, proof points, and claims to avoid
- `slides`: deck objective, sections, and slide-by-slide structure
- `review_packet`: items requiring human confirmation or caution
- `artifacts`: generated outlines, draft files, and PPTX outputs

Read [references/slide-structure-v1.md](references/slide-structure-v1.md) when writing or reviewing `slides`.

## Phase Contracts

### Intake

Purpose: normalize raw deal materials into structured state.

Read:
- raw user input
- CRM notes
- meeting notes
- RFPs
- prior proposals
- product documentation
- pricing sheets
- existing `ProposalState`

Write:
- `context`
- `facts`
- `hypotheses`
- `constraints`
- `stakeholders`
- `gaps`

Do not:
- finalize strategy
- finalize solution scope
- upgrade unconfirmed information to confirmed facts
- mark internal-only material as customer-visible

Escalate for review when:
- major source documents conflict
- the primary decision maker is unknown
- budget, timing, or scope is materially unclear
- customer visibility cannot be determined safely

### Strategy

Purpose: decide how the proposal should win.

Read:
- `context`
- `facts`
- `hypotheses`
- `constraints`
- `stakeholders`
- `gaps`

Write:
- `decision_criteria`
- `strategy`
- `review_packet.must_confirm`
- `review_packet.sales_judgment_needed`

Do not:
- invent pricing, delivery, or support commitments
- overstate product capability
- claim competitive superiority without support
- jump directly into polished slide prose

Escalate for review when:
- multiple win paths are plausible
- decision criteria are mostly inferred
- competitive positioning depends on weak evidence
- the recommended angle conflicts with known constraints

### Slide Composition

Purpose: turn strategy into a persuasive deck structure and slide plan.

Read:
- `context`
- `facts`
- `constraints`
- `stakeholders`
- `decision_criteria`
- `strategy`
- `review_packet`

Write:
- `slides.deck_objective`
- `slides.audience`
- `slides.deck_sections`
- `slides.items`
- `review_packet.weak_claims`
- `review_packet.must_confirm`

Do not:
- add claims that are not supported by `strategy`
- convert weak evidence into confident customer-facing claims
- shift into visual polishing work
- fill pricing or contract gaps by inference

Escalate for review when:
- executive and operational audiences require materially different storylines
- important slides lack supporting evidence
- internal-only reasoning leaks into customer-facing structure
- the deck needs multiple versions for different stakeholders

### Render

Purpose: convert approved slide structure into draft presentation artifacts.

Read:
- `slides`
- `strategy`
- `review_packet`
- available templates
- available brand assets

Write:
- `artifacts.outline_markdown`
- `artifacts.slide_draft_path`
- `artifacts.pptx_path`
- `artifacts.notes`

Do not:
- introduce new claims or commitments
- finalize unknown pricing, scope, or timelines
- hide unresolved review items
- substitute for validation or business approval

Escalate for review when:
- unresolved `must_confirm` items remain
- the template cannot accommodate the information cleanly
- persuasion depends on charts, evidence, or visuals that are still missing
- the draft implies commitments that require human approval

## Guardrails

- Never present a hypothesis as a confirmed customer fact.
- Never invent product capability, delivery scope, pricing, or timeline details.
- Never expose internal-only information in customer-facing proposal content.
- Never let rendering introduce new claims or commitments.
- If important uncertainties remain, surface them in `review_packet` instead of smoothing them over.

## Outputs

Produce as many of these as the current evidence allows:

- updated structured proposal state
- a slide-by-slide proposal outline
- a PPTX-ready draft when the slide plan is grounded enough
- a review packet with confirmation items, weak claims, and judgment calls

## Resources

Use these references directly from `SKILL.md` rather than recreating the schema inline:

- [references/proposal-state-v1.md](references/proposal-state-v1.md): shared state model and field rules
- [references/slide-structure-v1.md](references/slide-structure-v1.md): deck and slide output structure

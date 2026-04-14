# sales-proposal-skills

営業提案資料を artifact 駆動で段階設計し、最終的に PPTX まで生成する skill です。

## インストール

```bash
claude skill install tomato414941/sales-proposal-skills
```

## 前提条件

- Node.js
- Python 3
- `pyyaml`

依存のセットアップ:

```bash
npm install
pip install pyyaml
```

## 使い方

```bash
python3 scripts/init_proposal_artifacts.py --cwd .
python3 scripts/validate_proposal_artifacts.py --cwd . --write-validation
node scripts/render_pptx.js --cwd . --output .proposal/proposal.pptx
```

主な成果物:

- `.proposal/10_facts.md`
- `.proposal/20_gaps_and_assumptions.md`
- `.proposal/30_strategy.md`
- `.proposal/40_solution_map.md`
- `.proposal/50_outline.md`
- `.proposal/60_validation.md`
- `.proposal/70_deck_draft.md`
- `.proposal/proposal.pptx`

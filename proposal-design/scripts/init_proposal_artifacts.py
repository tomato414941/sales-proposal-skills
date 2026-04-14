#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path


ARTIFACTS = {
    "10_facts.md": """---
artifact_type: proposal_facts
schema_version: 0.1
status: draft
confidence: medium
sources:
  - user_input
assumptions: []
open_questions: []
---

## 顧客情報

## 提案対象

## 現状課題

## 制約

## スケジュール

## 関係者

## 利用可能な根拠
""",
    "20_gaps_and_assumptions.md": """---
artifact_type: proposal_gaps_and_assumptions
schema_version: 0.1
status: draft
confidence: medium
sources:
  - 10_facts.md
assumptions: []
open_questions: []
---

## 不足情報

## 仮説

## 仮説の根拠

## 提案への影響

## 要確認事項
""",
    "30_strategy.md": """---
artifact_type: proposal_strategy
schema_version: 0.1
status: draft
confidence: medium
sources:
  - 10_facts.md
  - 20_gaps_and_assumptions.md
assumptions: []
open_questions: []
---

## 説得対象

## 主要評価軸

## 訴求主軸

## 差別化方針

## 競合への対抗方針

## 語る順番
""",
    "40_solution_map.md": """---
artifact_type: proposal_solution_map
schema_version: 0.1
status: draft
confidence: medium
sources:
  - 10_facts.md
  - 30_strategy.md
assumptions: []
open_questions: []
---

## 課題と対応の対応表

## 標準対応と個別対応

## 導入前提

## 想定効果
""",
    "50_outline.md": """---
artifact_type: proposal_outline
schema_version: 0.1
status: draft
confidence: medium
sources:
  - 30_strategy.md
  - 40_solution_map.md
assumptions: []
open_questions: []
---

## デッキ方針

## スライド一覧
""",
    "60_validation.md": """---
artifact_type: proposal_validation
schema_version: 0.1
status: draft
confidence: medium
sources:
  - 10_facts.md
  - 20_gaps_and_assumptions.md
  - 30_strategy.md
  - 40_solution_map.md
  - 50_outline.md
assumptions: []
open_questions: []
---

## Summary

## Errors

## Warnings

## Next Actions
""",
    "70_deck_draft.md": """---
artifact_type: proposal_deck_draft
schema_version: 0.1
status: draft
confidence: medium
sources:
  - 10_facts.md
  - 30_strategy.md
  - 40_solution_map.md
  - 50_outline.md
  - 60_validation.md
assumptions: []
open_questions: []
---

# 表紙

# エグゼクティブサマリ

# 課題整理

# 提案概要

# システム全体像

# 導入計画

# 効果

# 体制

# リスク

# 次アクション
""",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=".proposal artifact を初期化します。")
    parser.add_argument("--cwd", default=".", help="作業ディレクトリ")
    parser.add_argument("--force", action="store_true", help="既存ファイルを上書きする")
    args = parser.parse_args()

    base = Path(args.cwd).resolve()
    proposal_dir = base / ".proposal"
    proposal_dir.mkdir(parents=True, exist_ok=True)

    for filename, content in ARTIFACTS.items():
        path = proposal_dir / filename
        if path.exists() and not args.force:
            continue
        path.write_text(content.strip() + "\n", encoding="utf-8")
        print(f"created: {path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

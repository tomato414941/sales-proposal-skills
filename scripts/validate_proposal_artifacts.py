#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml


ARTIFACT_ORDER = [
    "10_facts.md",
    "20_gaps_and_assumptions.md",
    "30_strategy.md",
    "40_solution_map.md",
    "50_outline.md",
    "60_validation.md",
    "70_deck_draft.md",
]

REQUIRED_SECTIONS = {
    "10_facts.md": [
        "## 顧客情報",
        "## 提案対象",
        "## 現状課題",
        "## 制約",
        "## スケジュール",
        "## 関係者",
        "## 利用可能な根拠",
    ],
    "20_gaps_and_assumptions.md": [
        "## 不足情報",
        "## 仮説",
        "## 仮説の根拠",
        "## 提案への影響",
        "## 要確認事項",
    ],
    "30_strategy.md": [
        "## 説得対象",
        "## 主要評価軸",
        "## 訴求主軸",
        "## 差別化方針",
        "## 競合への対抗方針",
        "## 語る順番",
    ],
    "40_solution_map.md": [
        "## 課題と対応の対応表",
        "## 標準対応と個別対応",
        "## 導入前提",
        "## 想定効果",
    ],
    "50_outline.md": [
        "## デッキ方針",
        "## スライド一覧",
    ],
    "60_validation.md": [
        "## Summary",
        "## Errors",
        "## Warnings",
        "## Next Actions",
    ],
    "70_deck_draft.md": [
        "# 表紙",
        "# エグゼクティブサマリ",
        "# 課題整理",
        "# 提案概要",
        "# システム全体像",
        "# 導入計画",
        "# 効果",
        "# 体制",
        "# リスク",
        "# 次アクション",
    ],
}

FRONTMATTER_FIELDS = [
    "artifact_type",
    "schema_version",
    "status",
    "confidence",
    "sources",
    "assumptions",
    "open_questions",
]

ALLOWED_STATUSES = {"draft", "validated", "locked"}
ALLOWED_CONFIDENCE = {"high", "medium", "low"}
SPECULATION_PATTERNS = [
    re.compile(pattern)
    for pattern in [
        r"かもしれない",
        r"可能性",
        r"おそらく",
        r"推測",
        r"想定",
        r"見込み",
        r"と思われる",
    ]
]
UNSUPPORTED_CLAIM_PATTERNS = [
    re.compile(pattern)
    for pattern in [
        r"必ず",
        r"完全に",
        r"確実に",
        r"絶対に",
        r"100%",
    ]
]


@dataclass
class Finding:
    level: str
    code: str
    file: str
    message: str


def split_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        return {}, text
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        return {}, text
    try:
        data = yaml.safe_load(parts[0][4:]) or {}
    except yaml.YAMLError:
        return {}, text
    return data, parts[1]


def read_file(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    return split_frontmatter(text)


def add_finding(findings: list[Finding], level: str, code: str, file: str, message: str) -> None:
    findings.append(Finding(level=level, code=code, file=file, message=message))


def check_frontmatter(path: Path, frontmatter: dict, findings: list[Finding]) -> None:
    if not frontmatter:
        add_finding(findings, "ERROR", "E001", path.name, "frontmatter がありません。")
        return

    for field in FRONTMATTER_FIELDS:
        if field not in frontmatter:
            add_finding(findings, "ERROR", "E002", path.name, f"frontmatter に `{field}` がありません。")

    status = frontmatter.get("status")
    confidence = frontmatter.get("confidence")
    if status and status not in ALLOWED_STATUSES:
        add_finding(findings, "ERROR", "E003", path.name, f"status が不正です: {status}")
    if confidence and confidence not in ALLOWED_CONFIDENCE:
        add_finding(findings, "ERROR", "E004", path.name, f"confidence が不正です: {confidence}")
    for field in ("sources", "assumptions", "open_questions"):
        value = frontmatter.get(field)
        if value is not None and not isinstance(value, list):
            add_finding(findings, "ERROR", "E005", path.name, f"`{field}` は配列である必要があります。")


def check_sections(path: Path, body: str, findings: list[Finding]) -> None:
    required = REQUIRED_SECTIONS.get(path.name, [])
    for section in required:
        if section not in body:
            add_finding(findings, "ERROR", "E010", path.name, f"必須セクションがありません: {section}")


def check_facts(path: Path, body: str, findings: list[Finding]) -> None:
    if path.name != "10_facts.md":
        return
    for pattern in SPECULATION_PATTERNS:
        if pattern.search(body):
            add_finding(findings, "WARNING", "W101", path.name, f"推測表現が facts に含まれています: {pattern.pattern}")


def check_outline(path: Path, body: str, findings: list[Finding]) -> None:
    if path.name != "50_outline.md":
        return
    slide_blocks = re.findall(r"### Slide \d+.*?(?=\n### Slide \d+|\Z)", body, flags=re.S)
    if not slide_blocks:
        add_finding(findings, "ERROR", "E201", path.name, "スライド定義がありません。")
        return
    for block in slide_blocks:
        for label in ("- タイトル:", "- 1枚1メッセージ:", "- 根拠:", "- 必要図表:", "- 話すポイント:"):
            if label not in block:
                add_finding(findings, "ERROR", "E202", path.name, f"スライド定義に `{label}` がありません。")
        evidence_match = re.search(r"- 根拠:\s*(.*)", block)
        if evidence_match and not evidence_match.group(1).strip():
            add_finding(findings, "WARNING", "W203", path.name, "根拠欄が空のスライドがあります。")


def check_deck_draft(path: Path, body: str, findings: list[Finding]) -> None:
    if path.name != "70_deck_draft.md":
        return
    for pattern in UNSUPPORTED_CLAIM_PATTERNS:
        if pattern.search(body):
            add_finding(findings, "WARNING", "W301", path.name, f"unsupported claim の疑いがある表現です: {pattern.pattern}")


def has_substantive_deck_content(body: str) -> bool:
    text = re.sub(r"^# .*$", "", body, flags=re.M)
    text = re.sub(r"\s+", "", text)
    return bool(text)


def check_status_transitions(proposal_dir: Path, file_data: dict[str, tuple[dict, str]], findings: list[Finding]) -> None:
    facts_status = file_data.get("10_facts.md", ({}, ""))[0].get("status")
    outline_status = file_data.get("50_outline.md", ({}, ""))[0].get("status")
    strategy_status = file_data.get("30_strategy.md", ({}, ""))[0].get("status")
    deck_frontmatter, deck_body = file_data.get("70_deck_draft.md", ({}, ""))
    deck_status = deck_frontmatter.get("status")
    deck_is_materialized = deck_status in {"validated", "locked"} or has_substantive_deck_content(deck_body)

    if strategy_status == "locked" and facts_status != "validated":
        add_finding(findings, "ERROR", "E401", "30_strategy.md", "10_facts.md が validated でないのに strategy が locked です。")
    if deck_is_materialized and outline_status != "validated":
        add_finding(findings, "ERROR", "E402", "70_deck_draft.md", "50_outline.md が validated でないのに deck draft があります。")


def render_validation(findings: list[Finding]) -> str:
    errors = [f for f in findings if f.level == "ERROR"]
    warnings = [f for f in findings if f.level == "WARNING"]

    lines = [
        "---",
        "artifact_type: proposal_validation",
        "schema_version: 0.1",
        "status: draft",
        f"confidence: {'low' if errors else 'medium'}",
        "sources:",
        "  - validator",
        "assumptions: []",
        "open_questions: []",
        "---",
        "",
        "## Summary",
        "",
        f"- errors: {len(errors)}",
        f"- warnings: {len(warnings)}",
        "",
        "## Errors",
        "",
    ]

    if errors:
        lines.extend([f"- [{item.code}] {item.file}: {item.message}" for item in errors])
    else:
        lines.append("- none")

    lines.extend(["", "## Warnings", ""])

    if warnings:
        lines.extend([f"- [{item.code}] {item.file}: {item.message}" for item in warnings])
    else:
        lines.append("- none")

    lines.extend(
        [
            "",
            "## Next Actions",
            "",
            "- errors を解消してから deck draft を確定する",
            "- warnings は仮説や未確定事項として明示したままレビューする",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=".proposal artifact を検証します。")
    parser.add_argument("--cwd", default=".", help="作業ディレクトリ")
    parser.add_argument(
        "--write-validation",
        action="store_true",
        help="60_validation.md を validator の結果で上書きする",
    )
    args = parser.parse_args()

    proposal_dir = Path(args.cwd).resolve() / ".proposal"
    if not proposal_dir.exists():
        print(".proposal ディレクトリがありません。", file=sys.stderr)
        return 2

    findings: list[Finding] = []
    file_data: dict[str, tuple[dict, str]] = {}

    for filename in ARTIFACT_ORDER:
        path = proposal_dir / filename
        if not path.exists():
            add_finding(findings, "ERROR", "E000", filename, "artifact がありません。")
            continue
        frontmatter, body = read_file(path)
        file_data[filename] = (frontmatter, body)
        check_frontmatter(path, frontmatter, findings)
        check_sections(path, body, findings)
        check_facts(path, body, findings)
        check_outline(path, body, findings)
        check_deck_draft(path, body, findings)

    check_status_transitions(proposal_dir, file_data, findings)

    if args.write_validation and (proposal_dir / "60_validation.md").exists():
        (proposal_dir / "60_validation.md").write_text(render_validation(findings), encoding="utf-8")

    for item in findings:
        print(f"{item.level} {item.code} {item.file}: {item.message}")

    return 1 if any(item.level == "ERROR" for item in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())

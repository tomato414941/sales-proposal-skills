#!/usr/bin/env node

const fs = require("fs");
const path = require("path");
const PptxGenJS = require("pptxgenjs");

function fail(message) {
  console.error(message);
  process.exit(1);
}

function parseArgs(argv) {
  const args = {
    cwd: process.cwd(),
    theme: path.resolve(__dirname, "../assets/default-theme.json"),
  };

  for (let index = 2; index < argv.length; index += 1) {
    const current = argv[index];
    const next = argv[index + 1];

    if (current === "--cwd" && next) {
      args.cwd = path.resolve(next);
      index += 1;
      continue;
    }
    if (current === "--proposal-dir" && next) {
      args.proposalDir = path.resolve(next);
      index += 1;
      continue;
    }
    if (current === "--output" && next) {
      args.output = path.resolve(next);
      index += 1;
      continue;
    }
    if (current === "--theme" && next) {
      args.theme = path.resolve(next);
      index += 1;
      continue;
    }
    if (current === "--help") {
      args.help = true;
      continue;
    }
    fail(`不明な引数です: ${current}`);
  }

  if (!args.proposalDir) {
    args.proposalDir = path.join(args.cwd, ".proposal");
  }
  if (!args.output) {
    args.output = path.join(args.proposalDir, "proposal.pptx");
  }
  return args;
}

function printHelp() {
  console.log(`Usage:
  node proposal-design/scripts/render_pptx.js --cwd <project-dir> [--proposal-dir <dir>] [--output <output.pptx>] [--theme <theme.json>]
`);
}

function readText(filePath) {
  try {
    return fs.readFileSync(filePath, "utf8");
  } catch (error) {
    fail(`ファイルの読込に失敗しました: ${filePath}\n${error.message}`);
  }
}

function readJson(filePath) {
  try {
    return JSON.parse(fs.readFileSync(filePath, "utf8"));
  } catch (error) {
    fail(`JSON の読込に失敗しました: ${filePath}\n${error.message}`);
  }
}

function splitFrontmatter(text) {
  if (!text.startsWith("---\n")) {
    return { frontmatter: {}, body: text };
  }
  const parts = text.split("\n---\n");
  if (parts.length < 2) {
    return { frontmatter: {}, body: text };
  }
  const rawFrontmatter = parts[0].slice(4);
  const body = parts.slice(1).join("\n---\n");
  const frontmatter = {};
  for (const line of rawFrontmatter.split("\n")) {
    if (!line.includes(":")) continue;
    const [key, ...rest] = line.split(":");
    frontmatter[key.trim()] = rest.join(":").trim();
  }
  return { frontmatter, body };
}

function extractBulletLines(textBlock) {
  return textBlock
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => line.startsWith("- "))
    .map((line) => line.slice(2).trim())
    .filter(Boolean);
}

function extractHeadingBlocks(body, headingPattern) {
  const regex = new RegExp(`^${headingPattern}\\s+(.+)$`, "gm");
  const matches = [...body.matchAll(regex)];
  return matches.map((match, idx) => {
    const start = match.index + match[0].length;
    const end = idx + 1 < matches.length ? matches[idx + 1].index : body.length;
    return {
      title: match[1].trim(),
      content: body.slice(start, end).trim(),
    };
  });
}

function parseDeckDraft(proposalDir) {
  const draftPath = path.join(proposalDir, "70_deck_draft.md");
  const factsPath = path.join(proposalDir, "10_facts.md");
  const validationPath = path.join(proposalDir, "60_validation.md");
  const { body: draftBody } = splitFrontmatter(readText(draftPath));
  const { body: factsBody } = splitFrontmatter(readText(factsPath));
  const { body: validationBody } = splitFrontmatter(readText(validationPath));

  const sections = extractHeadingBlocks(draftBody, "#");
  const titleSection = sections.find((section) => section.title === "表紙");
  const titleLines = titleSection ? extractBulletLines(titleSection.content) : [];
  const factsCustomer = (factsBody.match(/## 顧客情報[\s\S]*?(?=\n## |\s*$)/) || [""])[0];
  const customerName = (factsCustomer.match(/顧客:\s*(.+)/) || [null, "営業提案"])[1].trim();
  const validationSummary = (validationBody.match(/## Summary[\s\S]*?(?=\n## |\s*$)/) || [""])[0];

  return {
    customerName,
    title: titleLines[0] || `${customerName} 向け提案`,
    subtitle: titleLines.slice(1),
    sections: sections.filter((section) => section.title !== "表紙"),
    validationSummary: extractBulletLines(validationSummary),
  };
}

function parseOutline(proposalDir) {
  const outlinePath = path.join(proposalDir, "50_outline.md");
  const { body } = splitFrontmatter(readText(outlinePath));
  const blocks = extractHeadingBlocks(body, "###");
  return blocks
    .filter((block) => /^Slide\s+\d+/.test(block.title))
    .map((block) => {
      const fields = {};
      for (const line of block.content.split("\n")) {
        const trimmed = line.trim();
        const match = trimmed.match(/^-\s*([^:]+):\s*(.*)$/);
        if (!match) continue;
        fields[match[1].trim()] = match[2].trim();
      }
      return {
        title: fields["タイトル"] || "",
        message: fields["1枚1メッセージ"] || "",
        evidence: fields["根拠"] || "",
        figure: fields["必要図表"] || "",
        notes: fields["話すポイント"] || "",
      };
    });
}

function createPresentation(themeConfig) {
  const pptx = new PptxGenJS();
  pptx.layout = themeConfig.layout || "LAYOUT_WIDE";
  pptx.author = themeConfig.author || "proposal-design";
  pptx.company = themeConfig.company || "sales-proposal-skills";
  pptx.subject = themeConfig.subject || "Sales proposal";
  pptx.lang = themeConfig.lang || "ja-JP";
  pptx.theme = {
    headFontFace: themeConfig.fonts?.heading || "Arial",
    bodyFontFace: themeConfig.fonts?.body || "Arial",
    lang: themeConfig.lang || "ja-JP",
  };
  return pptx;
}

function addTitleSlide(pptx, draft, themeConfig) {
  const slide = pptx.addSlide();
  const colors = themeConfig.theme;
  const fonts = themeConfig.fonts;

  slide.background = { color: "FFFFFF" };
  slide.addShape("rect", {
    x: 0,
    y: 0,
    w: 13.333,
    h: 0.45,
    line: { color: colors.accent, transparency: 100 },
    fill: { color: colors.accent },
  });
  slide.addText("営業提案資料", {
    x: 0.7,
    y: 1.0,
    w: 6.5,
    h: 0.45,
    fontFace: fonts.heading,
    fontSize: 26,
    bold: true,
    color: colors.primary,
    margin: 0,
  });
  slide.addText(draft.title, {
    x: 0.7,
    y: 1.75,
    w: 8.8,
    h: 0.75,
    fontFace: fonts.heading,
    fontSize: 24,
    bold: true,
    color: colors.text,
    margin: 0,
  });
  slide.addText(`顧客: ${draft.customerName}`, {
    x: 0.7,
    y: 2.75,
    w: 5.5,
    h: 0.3,
    fontFace: fonts.body,
    fontSize: 14,
    color: colors.muted,
    margin: 0,
  });

  const subtitle = draft.subtitle.length > 0 ? draft.subtitle : draft.validationSummary;
  if (subtitle.length > 0) {
    slide.addText(
      subtitle.map((line) => ({ text: line, options: { bullet: true } })),
      {
        x: 7.6,
        y: 1.75,
        w: 4.9,
        h: 2.8,
        fontFace: fonts.body,
        fontSize: 15,
        color: colors.text,
        margin: 0.08,
        paraSpaceAfterPt: 8,
      }
    );
  }
}

function addContentSlide(pptx, section, outlineItem, themeConfig) {
  const slide = pptx.addSlide();
  const colors = themeConfig.theme;
  const fonts = themeConfig.fonts;
  const bullets = extractBulletLines(section.content);

  slide.background = { color: "FFFFFF" };
  slide.addShape("rect", {
    x: 0.55,
    y: 0.85,
    w: 12.2,
    h: 5.9,
    line: { color: colors.border, width: 1 },
    fill: { color: "FFFFFF" },
  });
  slide.addShape("rect", {
    x: 0.55,
    y: 0.85,
    w: 12.2,
    h: 0.18,
    line: { color: colors.accent, transparency: 100 },
    fill: { color: colors.accent },
  });

  slide.addText(section.title, {
    x: 0.8,
    y: 1.15,
    w: 6.2,
    h: 0.48,
    fontFace: fonts.heading,
    fontSize: 24,
    bold: true,
    color: colors.primary,
    margin: 0,
  });

  if (outlineItem?.message) {
    slide.addText(outlineItem.message, {
      x: 0.8,
      y: 1.75,
      w: 6.6,
      h: 0.8,
      fontFace: fonts.body,
      fontSize: 18,
      bold: true,
      color: colors.text,
      margin: 0,
    });
  }

  if (bullets.length > 0) {
    slide.addText(
      bullets.map((line) => ({ text: line, options: { bullet: true } })),
      {
        x: 0.8,
        y: 2.75,
        w: 5.9,
        h: 2.8,
        fontFace: fonts.body,
        fontSize: 15,
        color: colors.text,
        margin: 0.08,
        paraSpaceAfterPt: 8,
      }
    );
  } else {
    slide.addText(section.content, {
      x: 0.8,
      y: 2.75,
      w: 5.9,
      h: 2.8,
      fontFace: fonts.body,
      fontSize: 15,
      color: colors.text,
      margin: 0.08,
      valign: "top",
    });
  }

  const detailLines = [];
  if (outlineItem?.evidence) detailLines.push(`根拠: ${outlineItem.evidence}`);
  if (outlineItem?.figure) detailLines.push(`必要図表: ${outlineItem.figure}`);
  if (outlineItem?.notes) detailLines.push(`話すポイント: ${outlineItem.notes}`);

  if (detailLines.length > 0) {
    slide.addText(
      detailLines.map((line) => ({ text: line, options: { bullet: true } })),
      {
        x: 7.2,
        y: 2.1,
        w: 5.0,
        h: 3.2,
        fontFace: fonts.body,
        fontSize: 14,
        color: colors.text,
        margin: 0.08,
        paraSpaceAfterPt: 10,
      }
    );
  }

  if (outlineItem?.notes) {
    slide.addNotes(`話者メモ:\n- ${outlineItem.notes}`);
  }
}

function validateInputs(proposalDir) {
  const required = ["50_outline.md", "70_deck_draft.md"];
  for (const file of required) {
    const target = path.join(proposalDir, file);
    if (!fs.existsSync(target)) {
      fail(`${target} が見つかりません。artifact を先に生成してください。`);
    }
  }
}

async function main() {
  const args = parseArgs(process.argv);
  if (args.help) {
    printHelp();
    process.exit(0);
  }

  validateInputs(args.proposalDir);

  const themeConfig = readJson(args.theme);
  const draft = parseDeckDraft(args.proposalDir);
  const outlineItems = parseOutline(args.proposalDir);
  const pptx = createPresentation(themeConfig);

  addTitleSlide(pptx, draft, themeConfig);

  draft.sections.forEach((section, index) => {
    addContentSlide(pptx, section, outlineItems[index], themeConfig);
  });

  fs.mkdirSync(path.dirname(args.output), { recursive: true });
  await pptx.writeFile({ fileName: args.output });
  console.log(`PPTX を生成しました: ${args.output}`);
}

main().catch((error) => fail(`PPTX 生成に失敗しました: ${error.message}`));

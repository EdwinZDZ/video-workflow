#!/usr/bin/env python3
"""Measure the shipped font kit and write a coverage report.

测量仓库自带字体，生成字符集覆盖报告。

The report is generated from the actual `.ttf` files — never from a vendor
claim. Every count below is a set intersection between a Unicode block and the
font's `cmap`, so a face that ships 95 of Basic Latin's 95 printable characters
reports 95/95, and a face with no CJK glyphs reports 0.

报告直接读取 `.ttf` 文件，而非厂商宣传值。所有数字都是 Unicode 区块与字体
`cmap` 的交集：Basic Latin 的 95 个可打印字符全有就是 95/95，没有中日韩字形
就是 0。

Usage / 用法:
    python tools/font_report.py --fonts fonts --out docs/font-report.json
"""

from __future__ import annotations

import argparse
import json
import sys
import unicodedata
from pathlib import Path

from fontTools.ttLib import TTFont

SCHEMA_VERSION = 1

# Blocks worth reporting for a subtitle/caption kit. `total` is the full block
# size, not the number of assigned characters — a stable denominator beats a
# moving one when the comparison is "does this face cover the block at all".
# 字幕字体需要关注的区块。`total` 取区块总长而非已分配字符数：分母稳定，
# 才能回答"这款字到底覆不覆盖这个区块"。
BLOCKS: list[dict[str, object]] = [
    {"id": "basic-latin", "label": "Basic Latin", "zh": "基本拉丁", "start": 0x0020, "end": 0x007E},
    {"id": "latin-1", "label": "Latin-1 Supplement", "zh": "拉丁-1 补充", "start": 0x00A0, "end": 0x00FF},
    {"id": "latin-ext-a", "label": "Latin Extended-A", "zh": "拉丁扩展-A", "start": 0x0100, "end": 0x017F},
    {"id": "latin-ext-b", "label": "Latin Extended-B", "zh": "拉丁扩展-B", "start": 0x0180, "end": 0x024F},
    {"id": "greek", "label": "Greek and Coptic", "zh": "希腊与科普特", "start": 0x0370, "end": 0x03FF},
    {"id": "cyrillic", "label": "Cyrillic", "zh": "西里尔", "start": 0x0400, "end": 0x04FF},
    {"id": "punctuation", "label": "General Punctuation", "zh": "通用标点", "start": 0x2000, "end": 0x206F},
    {"id": "currency", "label": "Currency Symbols", "zh": "货币符号", "start": 0x20A0, "end": 0x20BF},
    {"id": "letterlike", "label": "Letterlike Symbols", "zh": "类字母符号", "start": 0x2100, "end": 0x214F},
    {"id": "arrows", "label": "Arrows", "zh": "箭头", "start": 0x2190, "end": 0x21FF},
    {"id": "math", "label": "Mathematical Operators", "zh": "数学运算符", "start": 0x2200, "end": 0x22FF},
    {"id": "cjk-punctuation", "label": "CJK Symbols and Punctuation", "zh": "中日韩标点", "start": 0x3000, "end": 0x303F},
    {"id": "cjk", "label": "CJK Unified Ideographs", "zh": "中日韩统一表意文字", "start": 0x4E00, "end": 0x9FFF},
    {"id": "cjk-ext-a", "label": "CJK Extension A", "zh": "中日韩扩展-A", "start": 0x3400, "end": 0x4DBF},
]

# Reading order in the docs: interface first, then editorial, display, hand,
# code. Sorting by file name would put Caveat first and bury the default face.
# 文档中的阅读顺序：界面字 → 编辑衬线 → 展示字 → 手写 → 等宽。
DISPLAY_ORDER = ["Inter", "Lora", "Oswald", "Caveat", "IBM Plex Mono"]


def _name(font: TTFont, name_id: int) -> str:
    value = font["name"].getDebugName(name_id)
    return value.strip() if value else ""


def _license(font: TTFont) -> str:
    raw = _name(font, 13).lower()
    if "open font license" in raw:
        return "OFL-1.1"
    if "apache" in raw:
        return "Apache-2.0"
    return "See font file"


def _cmap(font: TTFont) -> set[int]:
    codepoints: set[int] = set()
    for table in font["cmap"].tables:
        if table.isUnicode():
            codepoints.update(table.cmap.keys())
    return codepoints


def _missing(codepoints: set[int]) -> list[str]:
    """Assigned characters missing from the Latin core, controls excluded.

    只统计拉丁核心区里缺失的“已分配”字符，排除控制符。
    """
    missing = []
    for start, end in ((0x0020, 0x007E), (0x00A0, 0x00FF), (0x0100, 0x017F)):
        for cp in range(start, end + 1):
            if cp in codepoints:
                continue
            try:
                name = unicodedata.name(chr(cp))
            except ValueError:
                continue
            missing.append(f"U+{cp:04X} {name}")
    return missing


def measure(path: Path) -> dict[str, object]:
    font = TTFont(path, lazy=True)
    codepoints = _cmap(font)
    blocks = []
    for block in BLOCKS:
        start, end = int(block["start"]), int(block["end"])
        covered = sum(1 for cp in range(start, end + 1) if cp in codepoints)
        blocks.append(
            {
                "id": block["id"],
                "label": block["label"],
                "zh": block["zh"],
                "range": f"U+{start:04X}–U+{end:04X}",
                "covered": covered,
                "total": end - start + 1,
                "ratio": round(covered / (end - start + 1), 4),
            }
        )

    latin_core = sum(block["covered"] for block in blocks if block["id"] in {"basic-latin", "latin-1", "latin-ext-a"})
    cjk = next(block for block in blocks if block["id"] == "cjk")

    return {
        "file": path.name,
        "family": _name(font, 1),
        "style": _name(font, 2),
        "fullName": _name(font, 4),
        "version": _name(font, 5),
        "designer": _name(font, 9),
        "foundry": _name(font, 8),
        "license": _license(font),
        "weightClass": font["OS/2"].usWeightClass,
        "isMonospace": bool(font["post"].isFixedPitch),
        "unitsPerEm": font["head"].unitsPerEm,
        "glyphs": font["maxp"].numGlyphs,
        "mappedCodepoints": len(codepoints),
        "latinCore": latin_core,
        "latinCoreTotal": 95 + 96 + 128,
        "cjk": cjk["covered"],
        "blocks": blocks,
        "missingLatin": _missing(codepoints),
        "bytes": path.stat().st_size,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fonts", type=Path, default=Path("fonts"), help="folder containing .ttf files / 字体目录")
    parser.add_argument("--out", type=Path, default=Path("docs/font-report.json"), help="JSON output path / 输出路径")
    args = parser.parse_args()

    files = sorted(args.fonts.glob("*.ttf"))
    if not files:
        print(f"No .ttf files in {args.fonts} / 目录中没有 .ttf：{args.fonts}", file=sys.stderr)
        return 1

    fonts = [measure(path) for path in files]
    fonts.sort(
        key=lambda f: (
            DISPLAY_ORDER.index(f["family"]) if f["family"] in DISPLAY_ORDER else 99,
            int(f["weightClass"]),
        )
    )

    report = {
        "schemaVersion": SCHEMA_VERSION,
        "generator": "tools/font_report.py",
        "fontCount": len(fonts),
        "families": sorted({font["family"] for font in fonts}, key=lambda f: DISPLAY_ORDER.index(f) if f in DISPLAY_ORDER else 99),
        "fonts": fonts,
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"{'file':24} {'family':16} {'style':8} {'weight':>6} {'glyphs':>7} {'mapped':>7} {'latin':>7} {'cjk':>5}")
    for font in fonts:
        print(
            f"{font['file']:24} {font['family']:16} {font['style']:8} {font['weightClass']:>6} "
            f"{font['glyphs']:>7} {font['mappedCodepoints']:>7} "
            f"{str(font['latinCore']) + '/319':>7} {font['cjk']:>5}"
        )
    print(f"\nWrote {args.out} / 已写入 {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

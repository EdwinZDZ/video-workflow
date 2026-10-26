#!/usr/bin/env python3
"""Render every preview image used by the README and docs.

渲染 README 与文档使用的全部预览图：字体样张、字符集覆盖、四张应用场景图。

The images are generated from the actual `.ttf` files in `fonts/`, so a
specimen cannot drift away from the font it claims to show. Chinese copy is set
in the system CJK face on purpose: the shipped kit has no CJK glyphs, and the
previews show that fallback instead of hiding it.

所有图片都由 `fonts/` 中的真实字体渲染，样张不会和字体本身脱节。中文一律使用
系统 CJK 字体排印——仓库自带字体没有中日韩字形，预览图如实展示这一回退，
而不是把它藏起来。

Usage / 用法:
    python tools/render_previews.py
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONT_DIR = ROOT / "fonts"
OUT_DIR = ROOT / "docs" / "previews"
REPORT = ROOT / "docs" / "font-report.json"

W, H = 1600, 900
PAPER = "#F6F3EC"
PAPER_DEEP = "#EDE8DD"
INK = "#16150F"
MUTED = "#6E6A5E"
LINE = "#DAD4C6"
ACCENT = "#C2452D"
WHITE = "#FFFFFF"
DARK = "#12110F"
DARK_LINE = "#2C2A24"
DARK_MUTED = "#A8A293"

# The kit ships no Chinese font. The proofs need one for the bilingual labels,
# so the renderer looks for the host's system CJK face and never copies it into
# the repository. Override with CJK_FONT / CJK_FONT_BOLD.
# 仓库不自带中文字体。样张需要一款系统 CJK 字体来排双语标签，脚本只读取、不复制。
# 可用 CJK_FONT / CJK_FONT_BOLD 环境变量覆盖。
CJK_CANDIDATES = [
    os.environ.get("CJK_FONT", ""),
    "C:/Windows/Fonts/msyh.ttc",
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
]
CJK_BOLD_CANDIDATES = [
    os.environ.get("CJK_FONT_BOLD", ""),
    "C:/Windows/Fonts/msyhbd.ttc",
    "/System/Library/Fonts/PingFang.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
]


def _pick(candidates: list[str]) -> str:
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return candidate
    raise SystemExit(
        "No CJK font found for the bilingual labels. Set CJK_FONT to a .ttf or .ttc file.\n"
        "未找到可用的中文字体。请用 CJK_FONT 指向一个 .ttf 或 .ttc 文件。"
    )

# Reading order and editorial role of each family. The role is what decides
# whether a face belongs in a caption, a title, or a callout.
FAMILIES = [
    {
        "name": "Inter",
        "no": "01",
        "role_en": "Interface and captions",
        "role_zh": "界面与字幕",
        "sample": "Every lesson deserves a clear voice.",
        "note_en": "Neutral grotesque, generous x-height, built for small sizes.",
        "note_zh": "中性无衬线，字腔开阔，为小字号而生。",
    },
    {
        "name": "Lora",
        "no": "02",
        "role_en": "Editorial and quotations",
        "role_zh": "编辑排版与引文",
        "sample": "Slow down. Explain it properly.",
        "note_en": "A serif with brush roots; gives a quote room to breathe.",
        "note_zh": "带毛笔笔意的衬线体，让引文有呼吸感。",
    },
    {
        "name": "Oswald",
        "no": "03",
        "role_en": "Titles and lower thirds",
        "role_zh": "标题与下三分之一",
        "sample": "MAKE IT CLEAR",
        "note_en": "Condensed display: big voice, small footprint.",
        "note_zh": "压缩展示体：声量大，占地小。",
    },
    {
        "name": "Caveat",
        "no": "04",
        "role_en": "Annotations and callouts",
        "role_zh": "批注与提示",
        "sample": "watch this part",
        "note_en": "Handwritten, informal; one step away from the script.",
        "note_zh": "手写体，非正式，像是从讲稿边上长出来的。",
    },
    {
        "name": "IBM Plex Mono",
        "no": "05",
        "role_en": "Code and terminal",
        "role_zh": "代码与终端",
        "sample": "npm run captions -- --lang zh",
        "note_en": "Monospaced, 0.6 em advance; commands line up.",
        "note_zh": "等宽字体，0.6 em 字宽，命令天然对齐。",
    },
]


def font_file(family: str, weight: str) -> Path:
    return FONT_DIR / f"{family.replace(' ', '')}-{weight}.ttf"


def face(family: str, weight: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(font_file(family, weight)), size)


def cjk(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    path = _pick(CJK_BOLD_CANDIDATES if bold else CJK_CANDIDATES)
    return ImageFont.truetype(path, size, index=0)


def tracked(draw: ImageDraw.ImageDraw, x: int, baseline: int, text: str, fnt, fill: str, tracking: float = 0) -> int:
    """Draw letter-spaced text and return the advance width.

    绘制带字距的文字，返回总宽度。
    """
    cursor = x
    for char in text:
        draw.text((cursor, baseline), char, font=fnt, fill=fill, anchor="ls")
        cursor += draw.textlength(char, font=fnt) + tracking
    return int(cursor - x - tracking)


def tracked_pair(
    draw: ImageDraw.ImageDraw,
    x: int,
    baseline: int,
    en: str,
    zh: str,
    en_font,
    zh_font,
    tracking: float = 1,
    gap: int = 12,
    fill: str = MUTED,
    zh_fill: str | None = None,
) -> int:
    """Draw an English label and its Chinese counterpart on one baseline.

    在同一基线上排英文标签与对应中文，避免用拉丁字体硬排汉字出现方框。
    """
    width = tracked(draw, x, baseline, en, en_font, fill, tracking)
    draw.text((x + width + gap, baseline), zh, font=zh_font, fill=zh_fill or fill, anchor="ls")
    return width + gap + int(draw.textlength(zh, font=zh_font))


def hline(draw: ImageDraw.ImageDraw, x1: int, x2: int, y: int, fill: str = LINE, width: int = 1) -> None:
    draw.line((x1, y, x2, y), fill=fill, width=width)


def fit_size(family: str, weight: str, text: str, max_width: int, start: int, floor: int = 24) -> int:
    size = start
    while size > floor:
        if ImageDraw.Draw(Image.new("RGB", (10, 10))).textlength(text, font=face(family, weight, size)) <= max_width:
            return size
        size -= 2
    return floor


def dashed_rect(draw: ImageDraw.ImageDraw, box, fill: str = ACCENT, width: int = 2, dash: int = 14, gap: int = 10) -> None:
    x1, y1, x2, y2 = box
    for x in range(x1, x2, dash + gap):
        draw.line((x, y1, min(x + dash, x2), y1), fill=fill, width=width)
        draw.line((x, y2, min(x + dash, x2), y2), fill=fill, width=width)
    for y in range(y1, y2, dash + gap):
        draw.line((x1, y, x1, min(y + dash, y2)), fill=fill, width=width)
        draw.line((x2, y, x2, min(y + dash, y2)), fill=fill, width=width)


def dashed_ellipse(draw: ImageDraw.ImageDraw, box, fill: str = ACCENT, width: int = 4, step: int = 11, dash: int = 6) -> None:
    for angle in range(0, 360, step):
        draw.arc(box, angle, min(angle + dash, 359), fill=fill, width=width)


def arrow(draw: ImageDraw.ImageDraw, start, end, fill: str = ACCENT, width: int = 4, head: int = 18) -> None:
    draw.line((start, end), fill=fill, width=width)
    x1, y1 = start
    x2, y2 = end
    dx, dy = x2 - x1, y2 - y1
    length = max((dx * dx + dy * dy) ** 0.5, 1)
    ux, uy = dx / length, dy / length
    left = (x2 - ux * head - uy * head * 0.5, y2 - uy * head + ux * head * 0.5)
    right = (x2 - ux * head + uy * head * 0.5, y2 - uy * head - ux * head * 0.5)
    draw.polygon([end, left, right], fill=fill)


def load_report() -> dict:
    return json.loads(REPORT.read_text(encoding="utf-8"))


def specimen(card: dict, index: int, report: dict) -> None:
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    family = card["name"]

    mono_18 = face("IBM Plex Mono", "Regular", 18)
    mono_20 = face("IBM Plex Mono", "Regular", 20)
    inter_22 = face("Inter", "Regular", 22)
    inter_26 = face("Inter", "Regular", 26)

    # Frame and running heads / 边框与页眉
    draw.rectangle((36, 36, W - 36, H - 36), outline=LINE, width=1)
    tracked(draw, 72, 96, f"{card['no']} / 05", mono_20, ACCENT, 2)
    tracked_pair(draw, 72, 126, "FONT SPECIMEN", "字体样张", mono_18, cjk(16), 1, 10, MUTED)

    name_size = fit_size(family, "Bold", family, 1360, 168, 96)
    draw.text((72, 300), family, font=face(family, "Bold", name_size), fill=INK, anchor="ls")

    role_x = 72
    end = tracked(draw, role_x, 348, f"{card['role_en']} / ", inter_26, MUTED, 0.4)
    draw.text((role_x + end + 4, 348), card["role_zh"], font=cjk(24), fill=MUTED, anchor="ls")

    hline(draw, 72, W - 72, 388)

    # Two weights of the same line / 同一句话的常规与粗体
    sample_regular = face(family, "Regular", fit_size(family, "Regular", card["sample"], 1380, 68, 34))
    sample_bold = face(family, "Bold", fit_size(family, "Bold", card["sample"], 1380, 68, 34))
    draw.text((72, 486), card["sample"], font=sample_regular, fill=INK, anchor="ls")
    draw.text((72, 584), card["sample"], font=sample_bold, fill=INK, anchor="ls")

    hline(draw, 72, W - 72, 634)

    # Alphabet and figures / 字母表与数字
    alpha = face(family, "Regular", 27)
    draw.text((72, 690), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", font=alpha, fill=INK, anchor="ls")
    draw.text((72, 734), "abcdefghijklmnopqrstuvwxyz", font=alpha, fill=INK, anchor="ls")
    draw.text((72, 778), "0123456789  .,:;!?&@#%()[]{}\u2014\u2013\u201c\u201d\u2018\u2019", font=alpha, fill=INK, anchor="ls")

    # Footer / 页脚
    hline(draw, 72, W - 72, 812)
    detail = next(f for f in report["fonts"] if f["family"] == family and f["style"] == "Regular")
    tracked(draw, 72, 852, "REGULAR 400  ·  BOLD 700  ·  SIL OFL 1.1", mono_18, MUTED, 1)
    latin = f"LATIN {detail['latinCore']}/{detail['latinCoreTotal']}"
    right = f"{latin}   ·   CJK 0  \u2192  SYSTEM FALLBACK"
    draw.text((W - 72, 852), right, font=mono_18, fill=MUTED, anchor="rs")

    # Short editorial note, set in the face itself / 用该字体排一句定位说明
    note_size = fit_size(family, "Regular", card["note_en"], 1380, 24, 18)
    draw.text((W - 72, 126), card["note_en"], font=face(family, "Regular", note_size), fill=MUTED, anchor="rs")
    draw.text((W - 72, 154), card["note_zh"], font=cjk(17), fill=MUTED, anchor="rs")

    img.save(OUT_DIR / f"specimen-{family.replace(' ', '').lower()}.png", optimize=True)


def font_wall(report: dict) -> None:
    width, height = 1600, 1240
    img = Image.new("RGB", (width, height), PAPER)
    draw = ImageDraw.Draw(img)
    mono_18 = face("IBM Plex Mono", "Regular", 18)
    mono_20 = face("IBM Plex Mono", "Regular", 20)

    draw.rectangle((36, 36, width - 36, height - 36), outline=LINE, width=1)
    tracked_pair(draw, 72, 100, "THE TYPE KIT", "字体套件", mono_20, cjk(18), 2, 12, ACCENT)
    draw.text((72, 196), "Five families, ten files", font=face("Oswald", "Bold", 62), fill=INK, anchor="ls")
    draw.text((72, 240), "五款字族，十个文件", font=cjk(30), fill=MUTED, anchor="ls")
    hline(draw, 72, width - 72, 286)

    y = 316
    row = 158
    for index, card in enumerate(FAMILIES):
        family = card["name"]
        detail = next(f for f in report["fonts"] if f["family"] == family and f["style"] == "Regular")
        if index:
            hline(draw, 72, width - 72, y - 16)

        draw.text((72, y + 44), card["no"], font=mono_20, fill=ACCENT, anchor="ls")
        draw.text((136, y + 62), family, font=face(family, "Bold", 56), fill=INK, anchor="ls")
        draw.text((136, y + 98), card["role_en"], font=face("Inter", "Regular", 20), fill=MUTED, anchor="ls")
        role_end = draw.textlength(card["role_en"], font=face("Inter", "Regular", 20))
        draw.text((136 + role_end + 10, y + 98), card["role_zh"], font=cjk(18), fill=MUTED, anchor="ls")

        sample_size = fit_size(family, "Regular", card["sample"], 700, 34, 22)
        draw.text((760, y + 66), card["sample"], font=face(family, "Regular", sample_size), fill=INK, anchor="ls")

        meta = f"{detail['weightClass']} / 700  ·  {detail['latinCore']}/{detail['latinCoreTotal']} LATIN  ·  CJK 0"
        draw.text((width - 72, y + 106), meta, font=mono_18, fill=MUTED, anchor="rs")
        y += row

    hline(draw, 72, width - 72, y - 10)
    draw.text(
        (72, y + 42),
        "All ten files are SIL OFL 1.1. None contains CJK glyphs: Chinese copy falls back to the system face.",
        font=face("Inter", "Regular", 20),
        fill=MUTED,
        anchor="ls",
    )
    draw.text((72, y + 74), "十个文件均为 SIL OFL 1.1，均不含中日韩字形：中文回退系统字体。", font=cjk(18), fill=MUTED, anchor="ls")
    draw.text((width - 72, y + 42), "01 — 05", font=mono_20, fill=ACCENT, anchor="rs")

    img.save(OUT_DIR / "font-wall.png", optimize=True)


def coverage(report: dict) -> None:
    width, height = 1600, 1500
    img = Image.new("RGB", (width, height), PAPER)
    draw = ImageDraw.Draw(img)
    mono_16 = face("IBM Plex Mono", "Regular", 16)
    mono_18 = face("IBM Plex Mono", "Regular", 18)
    mono_20 = face("IBM Plex Mono", "Regular", 20)
    inter_19 = face("Inter", "Regular", 19)
    inter_20 = face("Inter", "Regular", 20)

    draw.rectangle((36, 36, width - 36, height - 36), outline=LINE, width=1)
    tracked_pair(draw, 72, 100, "CHARACTER SET COVERAGE", "字符集覆盖", mono_20, cjk(18), 2, 12, ACCENT)
    draw.text((72, 190), "Where each face ends", font=face("Oswald", "Bold", 56), fill=INK, anchor="ls")
    draw.text((72, 232), "每款字体覆盖到哪里", font=cjk(28), fill=MUTED, anchor="ls")
    draw.text((width - 72, 190), "Counts are cmap intersections, not vendor claims.", font=inter_20, fill=MUTED, anchor="rs")
    draw.text((width - 72, 224), "数字取自 cmap 交集，而非厂商宣传。", font=cjk(18), fill=MUTED, anchor="rs")

    columns = [
        ("BASIC LATIN", "基本拉丁", "basic-latin"),
        ("LATIN-1", "拉丁-1", "latin-1"),
        ("EXT-A", "扩展-A", "latin-ext-a"),
        ("GREEK", "希腊", "greek"),
        ("CYRILLIC", "西里尔", "cyrillic"),
        ("CJK", "中日韩", "cjk"),
    ]
    left, top = 72, 300
    family_w = 300
    col_w = 202
    tracked_pair(draw, left, top, "FAMILY", "字族", mono_16, cjk(14), 1, 8, MUTED)
    for index, (label, zh, _) in enumerate(columns):
        x = left + family_w + index * col_w
        draw.text((x, top - 22), label, font=mono_16, fill=MUTED, anchor="ls")
        draw.text((x, top + 2), zh, font=cjk(14), fill=MUTED, anchor="ls")
    hline(draw, left, width - 72, top + 22)

    y = top + 92
    row_h = 88
    for index, card in enumerate(FAMILIES):
        family = card["name"]
        detail = next(f for f in report["fonts"] if f["family"] == family and f["style"] == "Regular")
        if index:
            hline(draw, left, width - 72, y - 34)
        draw.text((left, y), card["no"], font=mono_18, fill=ACCENT, anchor="ls")
        draw.text((left + 52, y), family, font=face(family, "Bold", 28), fill=INK, anchor="ls")
        draw.text((left + 52, y + 26), f"{detail['weightClass']} / 700", font=mono_16, fill=MUTED, anchor="ls")

        for cindex, (_, _, block_id) in enumerate(columns):
            block = next(b for b in detail["blocks"] if b["id"] == block_id)
            x = left + family_w + cindex * col_w
            covered, total = block["covered"], block["total"]
            if block_id == "cjk":
                dashed_rect(draw, (x, y - 24, x + 128, y + 12), ACCENT, 1, 8, 6)
                draw.text((x + 12, y - 4), "0", font=mono_20, fill=ACCENT, anchor="ls")
                draw.text((x + 44, y - 3), "fallback", font=mono_16, fill=ACCENT, anchor="ls")
                draw.text((x, y + 28), "系统字体", font=cjk(14), fill=MUTED, anchor="ls")
                continue

            draw.text((x, y - 2), f"{covered}", font=mono_20, fill=INK, anchor="ls")
            offset = draw.textlength(f"{covered}", font=mono_20)
            draw.text((x + offset + 2, y - 1), f"/{total}", font=mono_16, fill=MUTED, anchor="ls")

            bar_w = 128
            draw.rectangle((x, y + 18, x + bar_w, y + 22), fill=LINE)
            filled = round(bar_w * covered / total)
            if filled:
                draw.rectangle((x, y + 18, x + filled, y + 22), fill=INK)

        y += row_h

    hline(draw, left, width - 72, y - 34)
    draw.text(
        (left, y + 6),
        "Latin core = Basic Latin 95 + Latin-1 96 + Extended-A 128 = 319 characters.",
        font=inter_19,
        fill=INK,
        anchor="ls",
    )
    draw.text((left, y + 34), "拉丁核心区 = 基本拉丁 95 + 拉丁-1 96 + 扩展-A 128，共 319 个字符。", font=cjk(16), fill=MUTED, anchor="ls")
    draw.text(
        (left, y + 68),
        "The only Latin gaps are SOFT HYPHEN and a rare letter or two — none appear in lesson copy.",
        font=inter_19,
        fill=MUTED,
        anchor="ls",
    )
    draw.text((left, y + 94), "拉丁区仅缺软连字符与一两个罕见字母，均不会出现在课程文案里。", font=cjk(16), fill=MUTED, anchor="ls")

    # Representative glyphs per family / 每款字体的代表字符
    strip_top = y + 190
    hline(draw, left, width - 72, strip_top - 48)
    tracked_pair(draw, left, strip_top - 66, "COVERED GLYPHS", "已覆盖字符", mono_16, cjk(14), 1, 8, MUTED)

    y = strip_top + 16
    for card in FAMILIES:
        family = card["name"]
        draw.text((left, y + 6), family, font=face("Inter", "Bold", 16), fill=MUTED, anchor="ls")
        draw.text((left + 300, y), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", font=face(family, "Regular", 21), fill=INK, anchor="ls")
        draw.text((left + 760, y), "abcdefghijklmnopqrstuvwxyz", font=face(family, "Regular", 21), fill=INK, anchor="ls")
        draw.text(
            (left + 300, y + 31),
            "0123456789  .,:;!?&@#%()[]{}  ÀÉÎÕÜ Ç Ñ Š Ž Ł",
            font=face(family, "Regular", 21),
            fill=INK,
            anchor="ls",
        )
        draw.text((width - 72, y + 8), "中文，你好世界 → 系统字体", font=cjk(15), fill=ACCENT, anchor="rs")
        y += 78

    draw.text(
        (left, height - 80),
        "CJK is absent by design of the source families; pair them with a licensed Chinese face for bilingual cuts.",
        font=face("Inter", "Regular", 17),
        fill=MUTED,
        anchor="ls",
    )
    draw.text((left, height - 52), "这五款字族本身不含中文；双语版本请搭配一款已授权的中文字体。", font=cjk(15), fill=MUTED, anchor="ls")

    img.save(OUT_DIR / "charset-coverage.png", optimize=True)


def scene_label(draw: ImageDraw.ImageDraw, en: str, zh: str, note: str, dark: bool = False) -> None:
    mono_17 = face("IBM Plex Mono", "Regular", 17)
    color = DARK_MUTED if dark else MUTED
    tracked_pair(draw, 72, H - 54, en, zh, mono_17, cjk(15), 1, 10, ACCENT, color)
    draw.text((W - 72, H - 54), note, font=mono_17, fill=color, anchor="rs")


def title_card() -> None:
    img = Image.new("RGB", (W, H), DARK)
    draw = ImageDraw.Draw(img)
    draw.rectangle((36, 36, W - 36, H - 36), outline=DARK_LINE, width=1)

    draw.text((W - 88, 628), "04", font=face("Oswald", "Bold", 420), fill="#1C1B16", anchor="rs")
    draw.rectangle((80, 92, 86, 200), fill=ACCENT)
    tracked_pair(draw, 112, 116, "LESSON 04", "第 04 课", face("IBM Plex Mono", "Regular", 20), cjk(17), 2, 12, ACCENT)

    draw.text((80, 360), "MAKE IT", font=face("Oswald", "Bold", 176), fill=WHITE, anchor="ls")
    draw.text((80, 530), "CLEAR.", font=face("Oswald", "Bold", 176), fill=WHITE, anchor="ls")
    draw.rectangle((80, 574, 660, 580), fill=ACCENT)
    draw.text((80, 664), "把复杂的事，讲清楚。", font=cjk(48), fill="#DDD8CB", anchor="ls")
    draw.text(
        (80, 720),
        "A four-minute lesson, recorded once, captioned twice.",
        font=face("Inter", "Regular", 26),
        fill=DARK_MUTED,
        anchor="ls",
    )

    tracked_pair(draw, 80, 812, "OPENING TITLE", "片名卡", face("IBM Plex Mono", "Regular", 17), cjk(15), 1, 10, DARK_MUTED)
    draw.text((W - 80, 812), "OSWALD 700  ·  INTER 400  ·  CJK FALLBACK", font=face("IBM Plex Mono", "Regular", 15), fill=DARK_MUTED, anchor="rs")
    img.save(OUT_DIR / "scene-title.png", optimize=True)


def subtitle_frame() -> None:
    img = Image.new("RGB", (W, H), PAPER_DEEP)
    draw = ImageDraw.Draw(img)

    # Editor window / 剪辑窗口
    draw.rounded_rectangle((70, 50, W - 70, 790), radius=16, fill=WHITE, outline=LINE, width=1)
    draw.rounded_rectangle((70, 50, W - 70, 104), radius=16, fill="#F1EDE4")
    draw.rectangle((70, 80, W - 70, 104), fill="#F1EDE4")
    for i, color in enumerate(("#D9A39A", "#D8C08F", "#A9BFA0")):
        draw.ellipse((96 + i * 26, 70, 108 + i * 26, 82), fill=color)
    draw.text((W // 2, 77), "lesson-04 \u2014 final cut.mp4", font=face("IBM Plex Mono", "Regular", 16), fill=MUTED, anchor="ms")

    # Sidebar / 侧栏
    draw.rectangle((70, 104, 320, 790), fill="#FAF8F2")
    hline(draw, 320, 320, 104)
    draw.line((320, 104, 320, 790), fill=LINE, width=1)
    tracked_pair(draw, 96, 148, "SCENES", "场景", face("IBM Plex Mono", "Regular", 14), cjk(13), 1, 8, MUTED)
    for i in range(5):
        top = 172 + i * 54
        if i == 2:
            draw.rounded_rectangle((90, top, 300, top + 42), radius=6, fill="#EFE8DA")
        draw.rounded_rectangle((104, top + 10, 150, top + 32), radius=4, fill="#DCD5C5")
        draw.text((166, top + 21), f"04-{i + 1:02d}", font=face("IBM Plex Mono", "Regular", 15), fill=INK, anchor="ls")

    # Slide content / 画面内容
    draw.text((376, 214), "Make it clear.", font=face("Inter", "Bold", 58), fill=INK, anchor="ls")
    draw.text((378, 254), "Three rules for a lesson people finish.", font=face("Inter", "Regular", 24), fill=MUTED, anchor="ls")
    hline(draw, 378, 780, 292)

    rules = [("01", "One idea per sentence."), ("02", "Show the change, not the setup."), ("03", "Cut the second take.")]
    for i, (num, text) in enumerate(rules):
        top = 330 + i * 76
        draw.ellipse((378, top, 418, top + 40), fill="#F0E9DB")
        draw.text((398, top + 21), num, font=face("IBM Plex Mono", "Regular", 14), fill=ACCENT, anchor="ms")
        draw.text((438, top + 22), text, font=face("Inter", "Regular", 26), fill=INK, anchor="ls")

    # Bar chart / 条形图
    base = 560
    for i, height in enumerate((70, 116, 154, 96, 132)):
        x = 980 + i * 78
        draw.rounded_rectangle((x, base - height, x + 46, base), radius=5, fill="#E4DCCB")
    draw.rounded_rectangle((980 + 2 * 78, base - 154, 980 + 2 * 78 + 46, base), radius=5, fill="#C2452D")
    draw.text((980, base + 22), "retention", font=face("IBM Plex Mono", "Regular", 14), fill=MUTED, anchor="ls")

    # Caption bar and safe area / 字幕条与安全区
    draw.rectangle((320, 610, W - 70, 790), fill=DARK)
    draw.rectangle((320, 610, 326, 790), fill=ACCENT)
    draw.text((378, 668), "The fastest way to learn is to explain it.", font=face("Inter", "Regular", 36), fill=WHITE, anchor="ls")
    draw.text((378, 718), "最快的掌握方式，是把它讲给别人听。", font=cjk(30), fill="#D9D4C7", anchor="ls")

    dashed_rect(draw, (426, 159, W - 166, 735), ACCENT, 1, 12, 9)
    draw.rectangle((426, 110, 654, 142), fill=PAPER_DEEP)
    tracked_pair(draw, 432, 132, "8% SAFE AREA", "安全区", face("IBM Plex Mono", "Regular", 13), cjk(12), 1, 8, ACCENT)

    scene_label(draw, "SUBTITLE FRAME", "字幕画面", "INTER 400  ·  2 LINES  ·  8% MARGIN")
    img.save(OUT_DIR / "scene-subtitle.png", optimize=True)


def end_credits() -> None:
    img = Image.new("RGB", (W, H), DARK)
    draw = ImageDraw.Draw(img)
    draw.rectangle((36, 36, W - 36, H - 36), outline=DARK_LINE, width=1)
    tracked_pair(draw, 80, 108, "END CREDITS", "片尾字幕", face("IBM Plex Mono", "Regular", 18), cjk(16), 2, 10, ACCENT)

    draw.text((W // 2, 330), "Good teaching", font=face("Lora", "Regular", 92), fill=WHITE, anchor="ms")
    draw.text((W // 2, 438), "is good editing.", font=face("Lora", "Regular", 92), fill=WHITE, anchor="ms")
    draw.text((W // 2, 508), "好课程，都是剪出来的。", font=cjk(28), fill="#C9C3B5", anchor="ms")
    hline(draw, W // 2 - 120, W // 2 + 120, 566, "#4A463C")

    rows = [
        ("VOICE", "配音", "Qwen3-TTS 12 Hz  \u00b7  Vivian"),
        ("ALIGNMENT", "对齐", "Qwen3-ForcedAligner 0.6B"),
        ("EDIT", "剪辑", "OpenScreen 2.0"),
        ("TYPE", "字体", "Lora  \u00b7  IBM Plex Mono"),
        ("LICENSE", "授权", "MIT  \u00b7  SIL OFL 1.1"),
    ]
    for i, (label, zh, value) in enumerate(rows):
        y = 618 + i * 38
        draw.text((420, y), label, font=face("IBM Plex Mono", "Regular", 16), fill=DARK_MUTED, anchor="ls")
        draw.text((560, y), zh, font=cjk(14), fill=DARK_MUTED, anchor="ls")
        draw.text((760, y), value, font=face("IBM Plex Mono", "Regular", 17), fill="#E8E3D7", anchor="ls")

    scene_label(draw, "END CREDITS", "片尾字幕", "LORA 400  ·  IBM PLEX MONO 400", dark=True)
    img.save(OUT_DIR / "scene-credits.png", optimize=True)


def annotation_layer() -> None:
    img = Image.new("RGB", (W, H), PAPER_DEEP)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((70, 50, W - 70, 790), radius=16, fill=WHITE, outline=LINE, width=1)
    draw.rounded_rectangle((70, 50, W - 70, 104), radius=16, fill="#F1EDE4")
    draw.rectangle((70, 80, W - 70, 104), fill="#F1EDE4")
    for i, color in enumerate(("#D9A39A", "#D8C08F", "#A9BFA0")):
        draw.ellipse((96 + i * 26, 70, 108 + i * 26, 82), fill=color)
    draw.text((W // 2, 77), "lesson-04 \u2014 timeline", font=face("IBM Plex Mono", "Regular", 16), fill=MUTED, anchor="ms")

    draw.text((110, 190), "Retention drops here.", font=face("Inter", "Bold", 62), fill=INK, anchor="ls")
    draw.text((112, 234), "The fix is a cut, not a new sentence.", font=face("Inter", "Regular", 26), fill=MUTED, anchor="ls")

    # Simple retention curve / 留存曲线
    points = [(112, 470), (300, 440), (470, 455), (620, 420), (760, 452), (900, 430), (1010, 555), (1100, 520), (1260, 500), (1450, 470)]
    draw.line(points, fill="#B9B1A0", width=6, joint="curve")
    for x, y in points:
        draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill="#B9B1A0")
    draw.line((112, 620, 1450, 620), fill=LINE, width=1)
    for i in range(6):
        x = 112 + i * 268
        draw.line((x, 620, x, 628), fill=LINE, width=1)
        draw.text((x, 650), f"{i * 2}:00", font=face("IBM Plex Mono", "Regular", 14), fill=MUTED, anchor="ms")

    dashed_ellipse(draw, (940, 480, 1120, 610), ACCENT, 4)
    arrow(draw, (1240, 380), (1080, 500), ACCENT, 4, 20)

    # Handwritten label on its own layer, slightly rotated / 手写标签单独旋转
    layer = Image.new("RGBA", (520, 200), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.text((16, 96), "start here", font=face("Caveat", "Bold", 84), fill=ACCENT, anchor="ls")
    layer = layer.rotate(7, expand=True, resample=Image.BICUBIC)
    img.paste(layer, (1190, 300), layer)

    draw.rectangle((150, 690, 430, 742), fill="#F4EFE4")
    draw.text((168, 716), "one idea, one beat", font=face("Caveat", "Bold", 36), fill=INK, anchor="ls")

    scene_label(draw, "ANNOTATION LAYER", "批注层", "CAVEAT 700  ·  ACCENT #C2452D")
    img.save(OUT_DIR / "scene-annotation.png", optimize=True)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    report = load_report()
    for index, card in enumerate(FAMILIES):
        specimen(card, index, report)
    font_wall(report)
    coverage(report)
    title_card()
    subtitle_frame()
    end_credits()
    annotation_layer()
    print(f"Rendered {len(list(OUT_DIR.glob('*.png')))} images into {OUT_DIR}")


if __name__ == "__main__":
    main()

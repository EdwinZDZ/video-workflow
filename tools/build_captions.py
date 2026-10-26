#!/usr/bin/env python3
"""Build and check bilingual captions from aligned lesson segments.

从对齐后的课程分段生成并检查双语字幕。

Input is the handoff produced after forced alignment: one JSON file, sentence
sized segments, both languages already written. The tool does not translate and
does not guess timing — it wraps, writes SRT/ASS, and reports the lines that
would fail a readability check.

输入是强制对齐之后的交接文件：一个 JSON，按句切分，两种语言都已写好。工具不做
翻译、不猜时间，只负责断行、输出 SRT/ASS，并报告过不了可读性检查的行。

Usage / 用法:
    python tools/build_captions.py build samples/lesson.transcript.json --out samples/lesson
    python tools/build_captions.py check samples/lesson.transcript.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

# Readability budgets. They are deliberately conservative: a lesson is watched
# on a laptop and on a phone, often at 1.25x.
# 可读性预算偏保守：课程常在笔记本和手机上以 1.25 倍速观看。
EN_LINE_CHARS = 42
ZH_LINE_CHARS = 20
MAX_LINES = 2
EN_CPS = 20.0
ZH_CPS = 9.0
MIN_DURATION = 1.0
MAX_DURATION = 7.0
MIN_GAP = 0.08


@dataclass
class Segment:
    start: float
    end: float
    en: str
    zh: str

    @property
    def duration(self) -> float:
        return self.end - self.start


@dataclass
class Issue:
    level: str
    index: int
    message: str
    message_zh: str


def load_segments(path: Path) -> list[Segment]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    raw = payload.get("segments")
    if not isinstance(raw, list) or not raw:
        raise SystemExit("segments must be a non-empty list / segments 必须是非空数组")

    segments = []
    for index, item in enumerate(raw):
        try:
            start = float(item["start"])
            end = float(item["end"])
        except (KeyError, TypeError, ValueError) as error:
            raise SystemExit(f"segment {index}: invalid start/end / 第 {index} 段时间无效") from error
        en = str(item.get("en", "")).strip()
        zh = str(item.get("zh", "")).strip()
        if not en or not zh:
            raise SystemExit(f"segment {index}: both en and zh are required / 第 {index} 段缺少中英文")
        if end <= start:
            raise SystemExit(f"segment {index}: end must be after start / 第 {index} 段结束时间必须晚于开始时间")
        segments.append(Segment(start, end, en, zh))
    return segments


def wrap_english(text: str, limit: int = EN_LINE_CHARS) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if len(candidate) <= limit or not current:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)

    # A greedy wrap can leave one word alone on the second line. Prefer a
    # balanced two-line split when both halves still fit.
    # 贪心断行可能把一两个词孤零零留在第二行；两行都放得下时，优先取更均衡的切点。
    if len(lines) == 2 and len(lines[0]) - len(lines[1]) > 8:
        best: tuple[int, str, str] | None = None
        for split in range(1, len(words)):
            first = " ".join(words[:split])
            second = " ".join(words[split:])
            if len(first) <= limit and len(second) <= limit:
                score = abs(len(first) - len(second))
                if best is None or score < best[0]:
                    best = (score, first, second)
        if best is not None:
            lines = [best[1], best[2]]
    return lines


def wrap_chinese(text: str, limit: int = ZH_LINE_CHARS) -> list[str]:
    """Break Chinese at punctuation where possible, then at the character limit.

    中文优先在标点处断行，其次按字数切分。
    """
    chunks = re.findall(r"[^，。！？；：、,.!?;:]+[，。！？；：、,.!?;:]?", text)
    lines: list[str] = []
    current = ""
    for chunk in chunks:
        if len(current) + len(chunk) <= limit:
            current += chunk
            continue
        if current:
            lines.append(current)
        while len(chunk) > limit:
            lines.append(chunk[:limit])
            chunk = chunk[limit:]
        current = chunk
    if current:
        lines.append(current)

    # Balance a two-line Chinese cue at a punctuation boundary when possible.
    # 中文两行时，优先在标点处取更均衡的切点。
    if len(lines) == 2 and len(lines[0]) - len(lines[1]) > 6:
        best: tuple[int, str, str] | None = None
        for split in range(1, len(text)):
            first, second = text[:split], text[split:]
            if len(first) <= limit and len(second) <= limit:
                score = abs(len(first) - len(second))
                if best is None or score < best[0]:
                    best = (score, first, second)
        if best is not None:
            lines = [best[1], best[2]]
    return lines


def char_count(text: str) -> int:
    return len(text.replace(" ", ""))


def check_segments(segments: list[Segment]) -> list[Issue]:
    issues: list[Issue] = []
    previous: Segment | None = None

    for index, segment in enumerate(segments, start=1):
        if previous is not None and segment.start < previous.end - 0.001:
            issues.append(Issue("error", index, "overlaps the previous segment", "与上一段时间重叠"))
        elif previous is not None and segment.start - previous.end < MIN_GAP:
            issues.append(Issue("warn", index, f"gap under {MIN_GAP:.2f}s", f"间隔小于 {MIN_GAP:.2f} 秒"))

        if segment.duration < MIN_DURATION:
            issues.append(Issue("error", index, f"shorter than {MIN_DURATION:.1f}s", f"短于 {MIN_DURATION:.1f} 秒"))
        if segment.duration > MAX_DURATION:
            issues.append(Issue("warn", index, f"longer than {MAX_DURATION:.1f}s", f"长于 {MAX_DURATION:.1f} 秒"))

        en_lines = wrap_english(segment.en)
        zh_lines = wrap_chinese(segment.zh)
        if len(en_lines) > MAX_LINES:
            issues.append(Issue("error", index, f"English needs {len(en_lines)} lines", f"英文需要 {len(en_lines)} 行"))
        if len(zh_lines) > MAX_LINES:
            issues.append(Issue("error", index, f"Chinese needs {len(zh_lines)} lines", f"中文需要 {len(zh_lines)} 行"))

        en_cps = char_count(segment.en) / segment.duration
        zh_cps = char_count(segment.zh) / segment.duration
        if en_cps > EN_CPS:
            issues.append(Issue("warn", index, f"English {en_cps:.1f} CPS", f"英文 {en_cps:.1f} 字/秒"))
        if zh_cps > ZH_CPS:
            issues.append(Issue("warn", index, f"Chinese {zh_cps:.1f} CPS", f"中文 {zh_cps:.1f} 字/秒"))

        previous = segment

    return issues


def srt_time(seconds: float) -> str:
    milliseconds = round(seconds * 1000)
    hours, remainder = divmod(milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, millis = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def ass_time(seconds: float) -> str:
    centiseconds = round(seconds * 100)
    hours, remainder = divmod(centiseconds, 360_000)
    minutes, remainder = divmod(remainder, 6000)
    secs, cents = divmod(remainder, 100)
    return f"{hours}:{minutes:02d}:{secs:02d}.{cents:02d}"


def write_srt(segments: list[Segment], path: Path, lang: str) -> None:
    cues = []
    for index, segment in enumerate(segments, start=1):
        lines = wrap_english(segment.en) if lang == "en" else wrap_chinese(segment.zh)
        body = "\n".join(lines)
        cues.append(f"{index}\n{srt_time(segment.start)} --> {srt_time(segment.end)}\n{body}\n")
    path.write_text("\n".join(cues), encoding="utf-8")


ASS_HEAD = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: EN,Inter,52,&H00FFFFFF,&H00FFFFFF,&H00121110,&H66000000,0,0,0,0,100,100,0,0,1,3,0,2,154,154,152,1
Style: ZH,Microsoft YaHei,44,&H00D9D4C7,&H00D9D4C7,&H00121110,&H66000000,0,0,0,0,100,100,0,0,1,3,0,2,154,154,96,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def write_ass(segments: list[Segment], path: Path) -> None:
    events = []
    for segment in segments:
        en = "\\N".join(wrap_english(segment.en)).replace("{", "\\{").replace("}", "\\}")
        zh = "\\N".join(wrap_chinese(segment.zh)).replace("{", "\\{").replace("}", "\\}")
        events.append(f"Dialogue: 1,{ass_time(segment.start)},{ass_time(segment.end)},EN,,0,0,0,,{en}")
        events.append(f"Dialogue: 1,{ass_time(segment.start)},{ass_time(segment.end)},ZH,,0,0,0,,{zh}")
    path.write_text(ASS_HEAD + "\n".join(events) + "\n", encoding="utf-8")


def command_build(args: argparse.Namespace) -> int:
    segments = load_segments(args.input)
    issues = check_segments(segments)
    args.out.parent.mkdir(parents=True, exist_ok=True)

    write_srt(segments, args.out.with_suffix(".en.srt"), "en")
    write_srt(segments, args.out.with_suffix(".zh.srt"), "zh")
    write_ass(segments, args.out.with_suffix(".bilingual.ass"))

    print(f"Wrote {args.out}.en.srt / 已写入英文 SRT")
    print(f"Wrote {args.out}.zh.srt / 已写入中文 SRT")
    print(f"Wrote {args.out}.bilingual.ass / 已写入双语 ASS")
    report(issues)
    return 1 if any(issue.level == "error" for issue in issues) else 0


def command_check(args: argparse.Namespace) -> int:
    segments = load_segments(args.input)
    issues = check_segments(segments)
    report(issues)
    return 1 if any(issue.level == "error" for issue in issues) else 0


def report(issues: list[Issue]) -> None:
    if not issues:
        print("OK — all segments pass / 全部通过")
        return
    for issue in issues:
        print(f"[{issue.level.upper():5}] #{issue.index}: {issue.message} / {issue.message_zh}")
    errors = sum(1 for issue in issues if issue.level == "error")
    warnings = len(issues) - errors
    print(f"{errors} errors, {warnings} warnings / {errors} 个错误，{warnings} 个警告")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    build = subparsers.add_parser("build", help="write SRT and ASS / 生成字幕文件")
    build.add_argument("input", type=Path, help="transcript JSON / 字幕 JSON")
    build.add_argument("--out", type=Path, required=True, help="output basename / 输出文件名前缀")
    build.set_defaults(func=command_build)

    check = subparsers.add_parser("check", help="run readability checks only / 只做可读性检查")
    check.add_argument("input", type=Path, help="transcript JSON / 字幕 JSON")
    check.set_defaults(func=command_check)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())

# Font Directory / 字体目录

**EN** — Ten files, five families, two real weights each. Everything on this page is measured from
the TTFs in [`fonts/`](../fonts): names from the `name` table, coverage from `cmap`, sizes from disk.
No vendor claim is repeated without a number behind it.

**中文** — 十个文件、五款字族、每款两个真实字重。本页所有信息都从 [`fonts/`](../fonts) 里的 TTF
实测：名称取自 `name` 表，覆盖取自 `cmap`，体积取自磁盘。没有数字支撑的厂商说法，这里不转述。

![The type kit / 字体套件](../docs/previews/font-wall.png)

## How to Read This Directory / 如何阅读本目录

**EN** — **Latin core** = Basic Latin (95 printable) + Latin-1 Supplement (96) + Latin Extended-A
(128) = **319 characters**. **Mapped** counts every Unicode codepoint in the font's `cmap`, including
Greek, Cyrillic and punctuation. **CJK** counts the intersection with U+4E00–U+9FFF; it is zero for all
five families, and the previews show the resulting system fallback rather than hiding it.

**中文** — **拉丁核心** = 基本拉丁（95 个可打印字符）+ 拉丁-1 补充（96）+ 拉丁扩展-A（128）
= **319 个字符**。**映射数**统计字体 `cmap` 里的全部 Unicode 码位，含希腊、西里尔与标点。
**CJK** 统计与 U+4E00–U+9FFF 的交集；五款字族全部为 0，预览图如实展示由此产生的系统回退。

```bash
# Rebuild the numbers on this page / 重新生成本页数字
python tools/font_report.py --fonts fonts --out docs/font-report.json
```

## 01 Inter — Interface and captions / Inter —— 界面与字幕

![Inter specimen / Inter 样张](../docs/previews/specimen-inter.png)

| Field / 字段 | Value / 值 |
| --- | --- |
| Designer / 设计 | Rasmus Andersson |
| Foundry / 厂商 | rsms |
| Version / 版本 | 4.001 |
| Weights / 字重 | Regular 400 · Bold 700 (two files) |
| Glyphs / 字形 | 2,937 |
| Mapped codepoints / 映射字符 | 2,852 |
| Latin core / 拉丁核心 | 317 / 319 |
| CJK / 中日韩 | 0 / 20,992 |
| License / 授权 | SIL OFL 1.1 |
| Files / 文件 | [Regular](../fonts/Inter-Regular.ttf) · [Bold](../fonts/Inter-Bold.ttf) · [OFL](../fonts/Inter-OFL.txt) |

**EN** — The default. A neutral grotesque with a large x-height, open apertures and enough weight
contrast to survive video compression. It is the face every caption starts in, and the one to keep
when a line has to stay readable at 24 px on a phone.

**中文** — 默认字体。中性无衬线，字腔大、开口开阔，字重对比足以扛住视频压缩。所有字幕都从它开始；
当一行字必须在手机 24 px 下仍然清楚时，留下的也是它。

**Set it for / 适用** — captions, UI labels, lower-third body copy, on-screen definitions.
字幕、界面标签、下三分之一正文、画面内定义。

## 02 Lora — Editorial and quotations / Lora —— 编辑排版与引文

![Lora specimen / Lora 样张](../docs/previews/specimen-lora.png)

| Field / 字段 | Value / 值 |
| --- | --- |
| Designer / 设计 | Olga Karpushina; Alexei Vanyashin (Cyrillic) |
| Foundry / 厂商 | Cyreal |
| Version / 版本 | 3.021 |
| Weights / 字重 | Regular 400 · Bold 700 |
| Glyphs / 字形 | 892 |
| Mapped codepoints / 映射字符 | 778 |
| Latin core / 拉丁核心 | 317 / 319 |
| CJK / 中日韩 | 0 / 20,992 |
| License / 授权 | SIL OFL 1.1 |
| Files / 文件 | [Regular](../fonts/Lora-Regular.ttf) · [Bold](../fonts/Lora-Bold.ttf) · [OFL](../fonts/Lora-OFL.txt) |

**EN** — A serif with brush roots and a calm, slightly calligraphic rhythm. Lora is not for running
captions: it is for the one sentence you want the viewer to remember, a chapter card, or a quotation
that deserves a slower reading speed.

**中文** — 一款带毛笔笔意、节奏从容的衬线体。Lora 不适合连续字幕：它留给那句希望观众记住的话、
章节卡，或者需要放慢速度读的引文。

**Set it for / 适用** — pull quotes, chapter openings, closing lines, interview titles.
金句、章节开场、收尾字幕、访谈人物条。

## 03 Oswald — Titles and lower thirds / Oswald —— 标题与下三分之一

![Oswald specimen / Oswald 样张](../docs/previews/specimen-oswald.png)

| Field / 字段 | Value / 值 |
| --- | --- |
| Designer / 设计 | Vernon Adams |
| Foundry / 厂商 | Vernon Adams |
| Version / 版本 | 4.103 |
| Weights / 字重 | Regular 400 · Bold 700 |
| Glyphs / 字形 | 771 |
| Mapped codepoints / 映射字符 | 737 |
| Latin core / 拉丁核心 | 318 / 319 |
| CJK / 中日韩 | 0 / 20,992 |
| License / 授权 | SIL OFL 1.1 |
| Files / 文件 | [Regular](../fonts/Oswald-Regular.ttf) · [Bold](../fonts/Oswald-Bold.ttf) · [OFL](../fonts/Oswald-OFL.txt) |

**EN** — Condensed display with a tall, narrow skeleton: a big voice in a small horizontal footprint.
It lets a title sit beside a face or a product without stealing the frame. Use Bold at display sizes,
Regular only for compact labels.

**中文** — 高瘦骨架的压缩展示体：声量大、横向占地小。标题可以和人脸或产品并排，而不抢画面。
展示字号用 Bold，Regular 只留给紧凑标签。

**Set it for / 适用** — opening titles, lesson numbers, lower thirds, thumbnail headlines.
片名卡、课次编号、下三分之一、封面标题。

## 04 Caveat — Annotations and callouts / Caveat —— 批注与提示

![Caveat specimen / Caveat 样张](../docs/previews/specimen-caveat.png)

| Field / 字段 | Value / 值 |
| --- | --- |
| Designer / 设计 | Pablo Impallari |
| Foundry / 厂商 | Pablo Impallari |
| Version / 版本 | 2.000 |
| Weights / 字重 | Regular 400 · Bold 700 |
| Glyphs / 字形 | 1,032 |
| Mapped codepoints / 映射字符 | 753 |
| Latin core / 拉丁核心 | 318 / 319 |
| CJK / 中日韩 | 0 / 20,992 |
| License / 授权 | SIL OFL 1.1 |
| Files / 文件 | [Regular](../fonts/Caveat-Regular.ttf) · [Bold](../fonts/Caveat-Bold.ttf) · [OFL](../fonts/Caveat-OFL.txt) |

**EN** — Handwritten and deliberately informal, one step away from the script. It works when paired
with an arrow or a circled area, and fails when asked to carry a paragraph. Keep it to two or three
words per callout.

**中文** — 手写、刻意非正式，像是从讲稿边上长出来的。配箭头或圈选区域时最有效；让它承担整段文字
就会失效。每条批注控制在两三个词。

**Set it for / 适用** — callouts, "start here", margin notes, whiteboard-style emphasis.
提示、批注、"从这里开始"、白板式强调。

## 05 IBM Plex Mono — Code and terminal / IBM Plex Mono —— 代码与终端

![IBM Plex Mono specimen / IBM Plex Mono 样张](../docs/previews/specimen-ibmplexmono.png)

| Field / 字段 | Value / 值 |
| --- | --- |
| Designer / 设计 | Mike Abbink, Paul van der Laan, Pieter van Rosmalen |
| Foundry / 厂商 | Bold Monday |
| Version / 版本 | 2.3 |
| Weights / 字重 | Regular 400 · Bold 700 |
| Glyphs / 字形 | 1,033 |
| Mapped codepoints / 映射字符 | 930 |
| Latin core / 拉丁核心 | 319 / 319 |
| CJK / 中日韩 | 0 / 20,992 |
| License / 授权 | SIL OFL 1.1 |
| Files / 文件 | [Regular](../fonts/IBMPlexMono-Regular.ttf) · [Bold](../fonts/IBMPlexMono-Bold.ttf) · [OFL](../fonts/IBMPlexMono-OFL.txt) |

**EN** — The only family here that covers all 319 Latin-core characters. A 0.6 em advance keeps
commands, filenames and timecodes aligned without manual spacing; the large punctuation is legible
after video compression.

**中文** — 五款中唯一覆盖全部 319 个拉丁核心字符的字族。0.6 em 等宽让命令、文件名与时间码天然对齐，
无需手工加空格；标点较大，经视频压缩后仍然清楚。

**Set it for / 适用** — terminal demos, code walkthroughs, file paths, timecode and spec tables.
终端演示、代码讲解、文件路径、时间码与规格表。

## Coverage Table / 覆盖总表

**EN** — Measured from the Regular file of each family; Bold shares the same `cmap`. Counts are
`covered / block size`, not percentages rounded by hand.

**中文** — 取自各字族的 Regular 文件；Bold 的 `cmap` 与之一致。数字为“已覆盖 / 区块总长”，
不是手工四舍五入的百分比。

| Family / 字族 | Basic Latin | Latin-1 | Ext-A | Greek | Cyrillic | CJK |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Inter | 95/95 | 95/96 | 127/128 | 105/144 | 248/256 | 0/20,992 |
| Lora | 95/95 | 95/96 | 127/128 | 6/144 | 224/256 | 0/20,992 |
| Oswald | 95/95 | 95/96 | 128/128 | 2/144 | 126/256 | 0/20,992 |
| Caveat | 95/95 | 96/96 | 127/128 | 1/144 | 220/256 | 0/20,992 |
| IBM Plex Mono | 95/95 | 96/96 | 128/128 | 1/144 | 168/256 | 0/20,992 |

**EN** — The only missing Latin characters are U+00AD SOFT HYPHEN and, depending on the family, one
of U+0149, U+0138 or U+017F. None of them belongs in lesson copy. Greek and Cyrillic coverage varies
widely and is not a promise: check the table before setting a Greek or Cyrillic title.

**中文** — 拉丁区唯一缺失的是 U+00AD 软连字符，以及各字族各自缺少的一个罕见字母
（U+0149、U+0138 或 U+017F）。它们都不会出现在课程文案里。希腊与西里尔覆盖差异很大，不构成承诺：
排希腊文或西里尔标题前请先查表。

![Coverage measured from cmap / 由 cmap 实测的覆盖](../docs/previews/charset-coverage.png)

## Chinese Fallback / 中文回退

**EN** — These are Latin faces. When a Chinese character is set in them, the browser or compositor
substitutes the system CJK face: Microsoft YaHei on Windows, PingFang SC on macOS, Noto Sans CJK on
Linux. That is the same behaviour a video renderer shows, so the previews do not fake a Chinese cut —
they show the fallback at the size it would really take.

**中文** — 这五款都是拉丁字体。用它们排汉字时，浏览器或合成器会替换为系统 CJK 字体：Windows 的
微软雅黑、macOS 的苹方、Linux 的 Noto Sans CJK。这与视频渲染器的行为一致，所以预览图不伪造中文
字形，而是按真实回退字号展示。

**EN** — For a bilingual release, pair them with a licensed Chinese family. Noto Sans SC and Source
Han Sans are both OFL and safe to redistribute; a system font is not. Do not copy `msyh.ttc` or
`PingFang.ttc` into a build.

**中文** — 双语成片请搭配已授权的中文字族。Noto Sans SC 与思源黑体均为 OFL，可安全再分发；
系统字体不可以。不要把 `msyh.ttc` 或 `PingFang.ttc` 复制进构建产物。

**EN** — The preview PNGs were rendered with the host machine's system CJK face so that Chinese labels
are legible — Microsoft YaHei on the Windows host used here. No Chinese font file is stored in this
repository; set `CJK_FONT` to change the face used for regeneration.

**中文** — 预览 PNG 为让中文标签可读，使用了渲染机器的系统 CJK 字体——本次是 Windows 的微软雅黑。
仓库不存放任何中文字体文件；重新生成时可用 `CJK_FONT` 指定其他字体。

## Licenses / 授权

**EN** — All ten files are licensed under the [SIL Open Font License 1.1](../fonts/Inter-OFL.txt).
In short: commercial use, modification and bundling are allowed; the copyright notice and license
must travel with the font; modified versions may not use a Reserved Font Name; the font may not be
sold on its own. This is a summary, not legal advice — read the license text that ships beside each
file.

**中文** — 十个文件均采用 [SIL Open Font License 1.1](../fonts/Inter-OFL.txt)。简言之：允许商用、
修改与打包；版权声明与授权文本必须随字体提供；修改版不得使用保留字体名；不得单独售卖字体本身。
以下是摘要，不构成法律意见——请阅读每个文件旁的授权原文。

| Family / 字族 | Copyright notice / 版权声明 | Reserved Font Name / 保留名 |
| --- | --- | --- |
| Inter | Copyright (c) 2016 The Inter Project Authors | — |
| Lora | Copyright 2011 The Lora Project Authors, with Reserved Font Name "Lora" | Lora |
| Oswald | Copyright 2016 The Oswald Project Authors | — |
| Caveat | Copyright 2014 The Caveat Project Authors | — |
| IBM Plex Mono | Copyright © 2017 IBM Corp. with Reserved Font Name "Plex" | Plex |

**EN** — Each family also ships its complete OFL text:
[Inter](../fonts/Inter-OFL.txt) · [Lora](../fonts/Lora-OFL.txt) · [Oswald](../fonts/Oswald-OFL.txt) ·
[Caveat](../fonts/Caveat-OFL.txt) · [IBM Plex Mono](../fonts/IBMPlexMono-OFL.txt).

**中文** — 每款字族都附有完整 OFL 文本：
[Inter](../fonts/Inter-OFL.txt) · [Lora](../fonts/Lora-OFL.txt) · [Oswald](../fonts/Oswald-OFL.txt) ·
[Caveat](../fonts/Caveat-OFL.txt) · [IBM Plex Mono](../fonts/IBMPlexMono-OFL.txt)。

---

**EN** — Back to the [README](../README.md) · **中文** — 返回 [项目说明](../README.md)。

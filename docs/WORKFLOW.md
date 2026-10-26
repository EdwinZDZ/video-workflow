# Workflow Notes / 工作流说明

**EN** — This document is the contract between stages. It records what each stage receives, what it
must return, and the numbers the next stage is allowed to rely on. The models and the editor are not
vendored in this repository; the pins and the handoff shapes are.

**中文** — 本文是各阶段之间的约定：每一段接收什么、必须交出什么、下一段可以依赖哪些数字。
模型与剪辑器不随仓库分发，但版本固定与交接格式写在这里。

## Scope / 适用范围

**EN** — In scope: a lesson video that is written in two languages, voiced once, aligned word by
word, captioned twice, and exported in a 16:9 master plus a 9:16 cutdown. Out of scope: translation,
music composition, motion-graphics design, and distribution.

**中文** — 范围之内：一节双语撰写、只配一次音、逐词对齐、双语字幕，并导出 16:9 主版与 9:16 竖版
的课程视频。范围之外：翻译、配乐、动效设计与分发。

## Stage Map / 阶段表

| # | Stage / 阶段 | Input / 输入 | Output / 产出 | Owner / 负责 |
| --- | --- | --- | --- | --- |
| 01 | Script · 脚本 | Topic, outline · 主题与提纲 | Sentence-sized bilingual segments · 按句切分的双语文段 | Author · 作者 |
| 02 | Voice · 配音 | Script + reference take · 脚本与参考音 | 48 kHz mono voice track · 48 kHz 单声道人声 | Qwen3-TTS |
| 03 | Timing · 对齐 | Voice + script · 人声与脚本 | Word-level timestamps · 词级时间戳 | Qwen3-ForcedAligner |
| 04 | Captions · 字幕 | Aligned segments · 对齐分段 | SRT × 2 + bilingual ASS · 双份 SRT 与双语 ASS | `tools/build_captions.py` |
| 05 | Edit · 剪辑 | Voice, screen capture, captions · 人声、录屏、字幕 | Editable project + MP4/GIF · 工程文件与导出 | OpenScreen 2.0 |
| 06 | Type · 字体 | `fonts/` · 字体目录 | Titles, captions, credits · 标题、字幕、片尾 | This kit · 本仓库 |

## Handoff Format / 交接格式

**EN** — The caption stage consumes one JSON file. It is intentionally plain: no timecodes in frames,
no styling, no translation memory. Times are seconds from the start of the programme, with decimals.

**中文** — 字幕阶段只读取一个 JSON。格式刻意保持朴素：不用帧号、不带样式、不掺翻译记忆。
时间是从节目开头算起的秒数，可带小数。

```json
{
  "meta": {
    "title": "Make it clear",
    "fps": 30
  },
  "segments": [
    {
      "start": 0.4,
      "end": 4.8,
      "en": "Every lesson starts with a script.",
      "zh": "每节课都从一份脚本开始。"
    }
  ]
}
```

| Field / 字段 | Type / 类型 | Rule / 规则 |
| --- | --- | --- |
| `start`, `end` | number · 数字 | Seconds; `end > start`; no overlap · 秒；结束必须晚于开始；不得重叠 |
| `en` | string · 字符串 | Required; sentence case · 必填；按句书写 |
| `zh` | string · 字符串 | Required; one sentence, no trailing spaces · 必填；一句，结尾不留空格 |
| `fps` | number · 数字 | Metadata only; captions are time-based · 仅作记录；字幕以时间计 |

**EN** — A segment is a sentence, not a word. Word timings from the aligner are regrouped into
sentence boundaries before this file is written; the caption builder does not infer boundaries.

**中文** — 一段是一句，不是一个词。对齐器给出的词级时间在写入本文件前已按句合并；字幕工具不会
自行推断句界。

## Model Pins / 模型版本

| Component / 组件 | Pin / 版本 | Evidence / 依据 |
| --- | --- | --- |
| TTS (voice) | `Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice` @ `85e237c` | [`runtime-provenance.json`](./runtime-provenance.json) |
| TTS (reference clone) | `Qwen/Qwen3-TTS-12Hz-0.6B-Base` @ `5d8399` | same file · 同上 |
| Runtime | `qwen-tts==0.1.1`, `torch==2.11.0+cu128`, `transformers==4.57.3`, Python 3.12.10 | same file · 同上 |
| Aligner | `Qwen3-ForcedAligner-0.6B` (local snapshot, Oct 2026) | model folder · 模型目录 |
| Editor | OpenScreen 2.0.0 | `package.json` upstream · 上游 `package.json` |
| Reference cleanup | Hybrid Demucs via torchaudio | used to remove background from the reference take · 用于清掉参考音背景 |

**EN** — The provenance file records the speaker (`Vivian`), the reference SHA-256, and two booleans
that matter: synthesis and alignment both ran end to end, and no background music was added to the
reference. Do not upgrade a pin without re-running those checks.

**中文** — 版本记录里写明了音色（Vivian）、参考音 SHA-256，以及两个关键布尔值：合成与对齐都实际跑通，
参考音没有混入背景音乐。没有重跑这两项检查，不要升级版本。

## Caption Specification / 字幕规范

**EN** — The numbers below are checked by `tools/build_captions.py`. Line count, overlap and a
sub-second cue stop the build with an error; CPS and over-long cues are warnings you should review.

**中文** — 下面的数字由 `tools/build_captions.py` 检查。行数、重叠与不足 1 秒会报错并让构建失败；
CPS 超限与过长字幕只报警告，需要人工复核。

| Rule / 规则 | Value / 值 | Why / 原因 |
| --- | --- | --- |
| Frame / 画幅 | 1920 × 1080 | Master; 9:16 is a re-layout, not a crop · 主版；竖版重排而非裁切 |
| Safe area / 安全区 | 8% inset = 154 px sides, 86 px top/bottom | Platform UI and TV overscan · 平台界面与电视过扫描 |
| Max lines / 最多行数 | 2 per language · 每语两行 | Reading speed at 1.25× · 1.25 倍速下的阅读速度 |
| Line length / 行宽 | EN 42 chars · ZH 20 chars | Balanced two-line cues · 两行均衡 |
| CPS / 每秒字数 | EN ≤ 20 · ZH ≤ 9 | Conservative for non-native viewers · 对非母语观众保守取值 |
| Duration / 时长 | 1.0–7.0 s | Below 1 s is unreadable; above 7 s drifts · 低于 1 秒读不完，高于 7 秒会脱节 |
| Gap / 间隔 | ≥ 0.08 s | Prevents cues from merging · 防止两条字幕粘连 |
| ASS fonts / 样式字体 | EN `Inter` 52 px · ZH system CJK 44 px | Matches the shipped kit · 与仓库字体一致 |
| ASS margins / 边距 | L/R 154, EN bottom 152, ZH bottom 96 | Two stacked lines inside the safe area · 两行叠放仍在安全区内 |

**EN** — SRT carries one language per file for platform upload; ASS stacks both languages for a
burn-in. Chinese is styled with `Microsoft YaHei` as a portable placeholder — replace it with the
licensed Chinese face you actually ship.

**中文** — SRT 每份只放一种语言，便于平台上传；ASS 把双语叠放，用于烧录。中文样式里的
`Microsoft YaHei` 只是可替换的占位名——请换成你实际分发且已授权的中文字体。

## Type Decisions / 字体决策

| Job / 用途 | Family / 字族 | Fallback / 回退 |
| --- | --- | --- |
| Captions and UI · 字幕与界面 | Inter 400 | Bold for emphasis only · 仅强调用 Bold |
| Titles and numbers · 标题与编号 | Oswald 700 | Regular only below 32 px · 32 px 以下才用 Regular |
| Quotations · 引文 | Lora 400 | Bold for a single word, not a line · Bold 只用于单词 |
| Callouts · 批注 | Caveat 700 | Always beside an arrow · 始终配箭头 |
| Code and timecode · 代码与时间码 | IBM Plex Mono 400 | Never letter-space manually · 不要手工加字距 |
| Chinese · 中文 | System CJK or a licensed OFL face · 系统 CJK 或已授权 OFL 字体 | Not bundled · 不随仓库分发 |

**EN** — Only one display family per frame. If a frame needs two, one of them is doing the wrong job.
Chinese never gets the Latin face's letter-spacing; it is set in its own stack.

**中文** — 一个画面只用一款展示字族。若需要两款，说明其中一款用错了地方。中文永远不继承拉丁字体的
字距，而是走自己的字体栈。

## Export / 导出

| Deliverable / 交付物 | Setting / 设置 | Notes / 说明 |
| --- | --- | --- |
| Master · 主版 | MP4, H.264 + AAC, 1920×1080, 30 fps | Editable project kept · 保留可编辑工程 |
| Vertical · 竖版 | MP4, 1080×1920 | Captions re-laid out, not cropped · 字幕重排，不裁切 |
| Platform captions · 平台字幕 | `lesson.en.srt`, `lesson.zh.srt` | Upload as separate tracks · 分轨上传 |
| Burn-in · 烧录版 | `lesson.bilingual.ass` | For social cuts · 用于社交平台 |

**EN** — Export is GPU-accelerated in OpenScreen with a CPU fallback. Check the first and last cue
against the waveform after export; GPU encoding does not change timing, but a trimmed intro does.

**中文** — OpenScreen 导出走 GPU，并带 CPU 回退。导出后仍要用波形核对第一条与最后一条字幕；
GPU 编码不会改变时间，但剪掉片头会。

## QA Checklist / 验收清单

- [ ] **Sync / 同步** — first and last cue land on the waveform, not near it. · 首尾字幕落在波形上。
- [ ] **CPS / 字速** — `python tools/build_captions.py check …` returns 0 errors. · 检查返回 0 错误。
- [ ] **Safe area / 安全区** — no glyph enters the outer 8%. · 没有字形进入外侧 8%。
- [ ] **Fallback / 回退** — Chinese is rendered by the intended CJK face on the target OS. · 目标系统上的中文由预期字体渲染。
- [ ] **Licenses / 授权** — every font folder ships its `-OFL.txt`; no system font file is copied. · 每个字体目录带 OFL 文本；没有复制系统字体。
- [ ] **Type / 字体** — one display family per frame; no faux bold. · 每帧一款展示字族；不用伪粗体。

## Reproduce / 复现

```bash
# 1. Measure the type / 测量字体
python tools/font_report.py --fonts fonts --out docs/font-report.json
python tools/build_site_data.py

# 2. Render the proofs / 渲染样张
python tools/render_previews.py

# 3. Build and check captions / 生成并检查字幕
python tools/build_captions.py build samples/lesson.transcript.json --out samples/lesson
python tools/build_captions.py check samples/lesson.transcript.json

# 4. Open the showcase / 打开展示页
python -m http.server 8080
```

**EN** — Steps 1–3 are deterministic and require only `fonttools` and `Pillow`. Step 4 has no build.
The voice and edit stages run outside this repository; their pins are above.

**中文** — 前三步是确定性的，只依赖 `fonttools` 与 `Pillow`；第四步无构建。配音与剪辑在本仓库之外
运行，版本固定见上表。

---

**EN** — Back to the [README](../README.md) · **中文** — 返回 [项目说明](../README.md)。

# Notice / 声明

**EN** — This repository is released under the MIT License **for its code, documentation, generated
images and showcase page only**. Everything below is third-party material with its own terms.

**中文** — 本仓库的 MIT 许可证**仅覆盖代码、文档、生成的图片与展示页**。以下内容均为第三方素材，
遵循各自的授权条款。

---

## 1. Fonts / 字体

**EN** — Ten font files in [`fonts/`](./fonts) are redistributed under the SIL Open Font License 1.1.
Each family keeps its original copyright notice and license text.

**中文** — [`fonts/`](./fonts) 中的十个字体文件按 SIL Open Font License 1.1 再分发。每款字族保留
原始版权声明与授权文本。

| Family / 字族 | Copyright / 版权 | License text / 授权文本 |
| --- | --- | --- |
| Inter | Copyright (c) 2016 The Inter Project Authors | [Inter-OFL.txt](./fonts/Inter-OFL.txt) |
| Lora | Copyright 2011 The Lora Project Authors, with Reserved Font Name "Lora" | [Lora-OFL.txt](./fonts/Lora-OFL.txt) |
| Oswald | Copyright 2016 The Oswald Project Authors | [Oswald-OFL.txt](./fonts/Oswald-OFL.txt) |
| Caveat | Copyright 2014 The Caveat Project Authors | [Caveat-OFL.txt](./fonts/Caveat-OFL.txt) |
| IBM Plex Mono | Copyright © 2017 IBM Corp. with Reserved Font Name "Plex" | [IBMPlexMono-OFL.txt](./fonts/IBMPlexMono-OFL.txt) |

**EN** — The OFL permits commercial use, modification and bundling. It requires that the copyright
notice and license accompany the font, that modified versions not use a Reserved Font Name, and that
the font not be sold by itself. The full text controls.

**中文** — OFL 允许商用、修改与打包，但要求版权声明与授权随字体提供，修改版不得使用保留字体名，
且不得单独售卖字体本身。以授权原文为准。

## 2. Preview Images and Screenshots / 预览图与截图

**EN** — The PNGs in [`docs/previews/`](./docs/previews) and [`docs/screenshots/`](./docs/screenshots)
were rendered from the fonts above. The Chinese labels in those images were set in the host machine's
system CJK face (Microsoft YaHei on the Windows host used here) purely so the labels are readable;
**no Chinese font file is distributed** in this repository.

**中文** — [`docs/previews/`](./docs/previews) 与 [`docs/screenshots/`](./docs/screenshots) 中的 PNG
由上述字体渲染。图中的中文标签使用渲染机器的系统 CJK 字体（本次为 Windows 的微软雅黑）排印，
只是为了让标签可读；**本仓库不分发任何中文字体文件**。

**EN** — Images are covered by the repository's MIT License as generated output. If you reuse a
scene image, keep the attribution to the type designers listed above.

**中文** — 图片作为生成产物纳入本仓库的 MIT 许可。若复用场景图，请保留上述字体设计者的署名。

## 3. Upstream Software and Models / 上游软件与模型

**EN** — The workflow references the following projects. None of their code or weights is stored in
this repository; the pins are documented in [docs/WORKFLOW.md](./docs/WORKFLOW.md).

**中文** — 工作流引用以下项目。本仓库不存放它们的代码或权重；版本固定见
[docs/WORKFLOW.md](./docs/WORKFLOW.md)。

| Project / 项目 | Role / 作用 | License / 授权 |
| --- | --- | --- |
| [OpenScreen](https://github.com/getopenscreen/openscreen) 2.0.0 | Screen recording, editing, GPU export · 录屏、剪辑、GPU 导出 | MIT |
| [Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS) 12 Hz 0.6B | Voice synthesis · 语音合成 | Apache-2.0 |
| Qwen3-ForcedAligner 0.6B | Word-level timestamps · 词级时间戳 | Apache-2.0 |
| [Demucs](https://github.com/facebookresearch/demucs) (Hybrid) | Reference-vocal cleanup · 参考人声清理 | MIT |
| [fontTools](https://github.com/fonttools/fonttools) | Font measurement · 字体测量 | MIT |
| [Pillow](https://python-pillow.org/) | Proof rendering · 样张渲染 | MIT-CMU |

**EN** — Model names and project names are used descriptively; no trademark license is granted.

**中文** — 模型名与项目名仅用于说明用途，不构成任何商标授权。

## 4. What Is Not Here / 仓库中没有什么

- No model weights, no `.safetensors`, no virtual environments. · 没有模型权重、`.safetensors` 或虚拟环境。
- No video files, no screen recordings, no voice samples. · 没有视频文件、录屏或人声样本。
- No system font files and no Chinese font binaries. · 没有系统字体文件，也没有中文字体二进制。

**EN** — None of the above is distributed here; obtain it from the official source and follow its terms.
**中文** — 上述内容均不随仓库分发；需要时请从各自的官方渠道获取，并遵守其授权。

---

**EN** — Questions about licensing: open an issue before shipping. · **中文** — 授权问题请在分发前
提交 issue 确认。

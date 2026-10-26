# Contributing / 贡献指南

**EN** — Thanks for taking the time to improve Video Workflow. This project is bilingual: **English
first, Chinese after**, in headings, table cells, interface copy and code comments alike.

**中文** — 感谢你为视频工作流出力。本项目默认双语：**英文在前、中文在后**，标题、表格单元格、
界面文案与代码注释皆然。

## Before You Start / 开始之前

**EN** — Read [NOTICE.md](NOTICE.md). This repository does not accept model weights, video files, or
a font whose license cannot be verified.

**中文** — 请先阅读 [NOTICE.md](NOTICE.md)。本仓库不接受模型权重、视频文件，也不接受无法核实授权的字体。

## Ways to Contribute / 贡献方式

| Way / 方式 | What it looks like / 具体做什么 |
| --- | --- |
| Report a bug · 报 bug | A broken specimen, a wrong coverage number, a caption that wraps badly. · 样张错位、覆盖数字错误、字幕断行难看。 |
| Improve the docs · 改进文档 | Clearer stage contracts, better Chinese translation, a missing command. · 交接说明更清楚、中文更准确、补上缺失命令。 |
| Add a scene preset · 增加场景 | A new in-use layout rendered by `tools/render_previews.py`. · 用现有脚本渲染新的应用场景版式。 |
| Tighten a check · 收紧检查 | A readability rule with a reason, not a preference. · 有依据的可读性规则，而不是个人偏好。 |

## Font Changes / 更换字体

**EN** — A font is accepted only when all five items are present:

**中文** — 更换字体必须同时满足以下五项：

1. **License** — SIL OFL 1.1, Apache-2.0, or another license that explicitly allows redistribution. · 授权：SIL OFL 1.1、Apache-2.0，或其他明确允许再分发的许可。
2. **License text** — the original license file, named `<Family>-OFL.txt`, next to the TTF. · 授权文本：原始文件，命名为 `<Family>-OFL.txt`，与 TTF 放在一起。
3. **Measured report** — `python tools/font_report.py --fonts fonts --out docs/font-report.json`. · 重新测量：运行报告脚本。
4. **Regenerated proofs** — `python tools/render_previews.py` and `python tools/build_site_data.py`. · 重新生成：样张与页面数据。
5. **A reason** — which job in [docs/WORKFLOW.md](docs/WORKFLOW.md#type-decisions--字体决策) it does better than the face it replaces. · 理由：它在工作流的哪个位置比被替换的字体做得更好。

**EN** — Do not commit a system font, a font with an unclear license, or a subset that drops the
OFL notice. Do not rename a modified font to its original family name if the license carries a
Reserved Font Name.

**中文** — 不要提交系统字体、授权不明的字体，或删掉 OFL 声明的子集。若授权包含保留字体名，
修改版不得沿用原字族名。

## Code Changes / 代码改动

**EN** — Python 3.10+, standard library where possible. The tools must stay deterministic: same
inputs, same bytes. Avoid adding a dependency unless it removes more code than it adds.

**中文** — Python 3.10 及以上，能用标准库就用标准库。工具必须保持确定性：同样的输入产出同样的字节。
除非新依赖省下的代码多于它引入的代码，否则不要加。

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python tools/font_report.py --fonts fonts --out docs/font-report.json
python tools/build_site_data.py
python tools/render_previews.py
python tools/build_captions.py check samples/lesson.transcript.json
```

**EN** — If you change the caption rules, update the table in
[docs/WORKFLOW.md](docs/WORKFLOW.md#caption-specification--字幕规范) and the sample output in the
same pull request. A rule that exists only in code is a rule nobody can review.

**中文** — 若改动字幕规则，请在同一 PR 里更新
[docs/WORKFLOW.md](docs/WORKFLOW.md#caption-specification--字幕规范) 的表格与示例产物。
只存在于代码里的规则，等于无法评审的规则。

## Docs and Translation / 文档与翻译

**EN** — Every heading, table and interface label needs both languages, English first. A Chinese
line is a translation of the English line, not a summary of it — keep the numbers identical.

**中文** — 每个标题、表格与界面标签都要双语，英文在前。中文是英文的翻译，不是摘要——数字必须一致。

## Pull Request Checklist / 提交前检查

- [ ] The change is scoped to one concern. · 一次只做一件事。
- [ ] `font_report.py` and `build_site_data.py` were re-run if a font changed. · 换字体后重跑了报告与页面数据。
- [ ] `render_previews.py` regenerated the affected images. · 重渲染了受影响的图片。
- [ ] `build_captions.py check` returns 0 errors if captions changed. · 改字幕则检查返回 0 错误。
- [ ] New fonts ship their license text; no system font is included. · 新字体带授权文本；没有系统字体。
- [ ] Headings read English first, Chinese second. · 标题英文在前、中文在后。

## Commit Messages / 提交信息

**EN** — Imperative subject, one line, under 72 characters. The body explains why, not what. Example:
`fix(captions): balance two-line cues at word boundaries`.

**中文** — 祈使句、单行、72 字符以内。正文解释“为什么”，而不是“改了什么”。示例：
`fix(captions): balance two-line cues at word boundaries`。

## License of Contributions / 贡献授权

**EN** — By submitting a pull request you agree that your contribution is licensed under the MIT
License, and that any font you add keeps its original license and notice.

**中文** — 提交 PR 即表示你同意以 MIT 许可证授权你的贡献；所添加的字体仍沿用其原始授权与声明。

# 完整使用指南

这份文件收录从首页移出的进阶说明。多数使用者可直接从 README 的任务范例
prompts 开始。以下范例皆采平台中立写法：以一般文字指定 skill 名称，不依赖
特定 client 的调用符号。

[English](./USER_GUIDE.md) | [繁體中文](./USER_GUIDE.zh-TW.md)


本候选版尚未发布。以下范例使用简中入口 `academic-writing-skills-zh-cn` 与
`paper-review-zh-cn`；同一功能择一语言即可。指引语言不决定论文交付语言，
例如可用简中讨论、保留英文正文。

## 选择 skill

需要规划、撰写、修改、同步或准备投稿材料时，使用
`academic-writing-skills-zh-cn`；只需要审查与找出问题时，使用
`paper-review-zh-cn`。要求 review 默认不代表授权修改文件。

## 建议提供的资料

| 任务 | 建议资料 |
|---|---|
| Outline | 研究目的、gap、questions、methods、现有 evidence、目标 venue，以及本稿不能提出的 claims |
| 撰写或修改 | 核准的 outline、可使用的 sources／results、锁定术语与前后文字 |
| 科学审查 | Exact active manuscript、figures、tables、supplement 与预定 review stage |
| Revision-round 核对 | Current manuscript、prior comments、response letter，以及可取得的 prior version |
| 投稿前检查 | Exact submission files、目前 venue requirements 与 metadata |

涉及多个文件或版本时，可在 prompt 前加入：

```text
TASK: [plan / draft / revise / review / submission check]
ACTIVE FILES: [这次要审查或修改的 exact versions]
AUTHORITY SOURCES: [发生冲突时应以哪些 results、data、code、approved outline 或 decisions 为准]
LOCKED DECISIONS: [不得改变的 wording、numbers、questions 或 claims]
NONCLAIMS: [本稿不能提出的 interpretations 或 conclusions]
TARGET / STAGE: [venue，以及 developmental / substantive / integration / submission]
```

`developmental` 适用于 outline 或未完成的初稿；`substantive` 表示核心科学
内容已具备；`integration` 用于完整主稿与 companion files；`submission`
只用于实际准备提交的 exact package。

需要修改时，建议提供 editable source 或 DOCX；只做 review 且内容可清楚阅读
时，PDF 即可。Figures、tables 或 supplement 若无法在主稿内完整辨识，请另外
附上。逐项核对 citations 时需提供 source papers；检查 reproducibility 时需
提供 code／data；检查期刊格式时需提供目前有效的 journal guide。

## 更多 prompt 范例

### 建立 extended outline

```text
请使用 academic-writing-skills-zh-cn skill，根据附件建立 extended outline。确认 gap、
research questions、methods、现有 evidence、预定 contribution 与 nonclaims。
每个 planned paragraph 都列出 function、claim、authorized evidence、
inference limit 与 bridge。暂时不要撰写完整正文。
```

### 撰写 section

```text
请使用 academic-writing-skills-zh-cn skill，依照已核准的 outline 与提供的 sources 撰写
Section 2.3。保留所有 locked terms、numbers 与 citations，并逐段检查
claim、evidence、development 以及与前后文字的衔接。
```

### 检查术语与流畅度

```text
请使用 academic-writing-skills-zh-cn skill 修改这一节的 terminology consistency、可避免的
非技术词重复、stock phrasing 与 paragraph flow。保留必要的 technical
repetition，不要改变科学意义、数值、citations 或 claim strength。
```

### 套用选定的 review comments

```text
请使用 academic-writing-skills-zh-cn skill 处理 review items 1、3、5。需要 missing source
或 author decision 的项目继续列为 open，并将每一项 material change 同步到
受影响的 sections、displays、supplement、Abstract 与 Conclusion。
```

### 验证 revision round

```text
请使用 paper-review-zh-cn skill 比较 current manuscript、reviewer comments、response
letter 与 prior version。将每个 issue 分为 resolved、partial、open、
regressed、waived、new 或 not verifiable；不能只依 response letter 判定所有
受影响文件都已完成修改。
```

### 检查投稿文件

```text
请使用 paper-review-zh-cn skill，在 submission stage 检查 exact manuscript、supplement、
figures、tables、highlights、cover letter、declarations 与 metadata。列出
release blockers；只有实际文件全部支持时，才能标示 SUBMISSION_READY。
```

## Review stages

| Stage | 用途 |
|---|---|
| Developmental | Outline 或未完成初稿的结构、gap、questions 与 planned evidence |
| Substantive | 科学有效性、methods、evidence、interpretation 与 reproducibility |
| Integration | 完整稿件的跨 section 与跨文件一致性 |
| Submission | 实际投稿文件的 release readiness |

## 自动选择 review modules

`paper-review-zh-cn` 会根据稿件本身选择最小且足够的技术 references，使用者不需
手动指定 modules。现有涵盖范围包括：

- equations、notation 与 derived-display provenance；
- surveys、psychometrics、CFA、SEM、mediation 与 multi-group comparison；
- simulation、ABM、ML、GenAI、LLMs 与 synthetic respondents；
- water resources、coupled human-natural systems、policy 与 uncertainty；
- flood risk、hydrodynamics、catastrophe modeling、exposure、vulnerability 与
  loss；
- prior-comment 与 revision-round regression checks。

单一 keyword 或 study-area mention 不足以启用模块。Ethan-style 或
project-precedent overlay 只有在相关 context 被明确要求或确认时才会使用。

## 长期项目

一次性的修改不需额外设定。反复修改的多文件项目可以建立 manuscript state：

以下指令以完整 checkout 的根目录为起点，使用其中的英文共用工具。
若只手动安装某语言的 skill，请将 script 路径改成该资料夹实际安装的位置；
后面的 pytest 范例只适用于完整 checkout，不是一般使用者的必要步骤。

```bash
python skills/academic-writing-skills/scripts/init_manuscript_state.py manuscript_state.json
```

State 会记录 active artifacts、authority sources、locked wording、facts、
terminology、decisions、open issues 与 release checks，不会保存每一次局部用字。

可使用的 diagnostics：

```bash
python skills/academic-writing-skills/scripts/audit_manuscript_state.py manuscript_state.json
python skills/academic-writing-skills/scripts/audit_text_consistency.py manuscript_state.json
python skills/academic-writing-skills/scripts/audit_prose_patterns.py manuscript_state.json
python skills/academic-writing-skills/scripts/audit_docx_structure.py manuscript.docx
python skills/academic-writing-skills/scripts/run_regression_tests.py
```

这些 scripts 只找出需进一步判读的 candidates，不会自行认定文字由 AI 生成，
也不会直接判定 technical term 过度重复。

## 使用边界

- Skills 不会编造 assumptions、analyses、results、citations、mechanisms、
  thresholds、reviewer preferences 或 metadata。
- Technical terms 不会为了表面变化而进行 synonym rotation。
- AI-like prose patterns 只是 editing diagnostics，不是 authorship 的证据。
- Response letter 不能证明修改已出现在所有受影响文件中。
- 本 plugin 是 source verification、statistical software、reference managers、
  rendering 与 tracked-change tools 的补充，不会取代它们。

## 测试

```bash
python -m pytest tests/ -q
python skills/academic-writing-skills/scripts/run_regression_tests.py
```

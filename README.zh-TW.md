# academic-writing-skills

這是一套適用於 Claude／Codex 的學術論文工作 plugin。1.0 版包含兩個可組合的 skills：

- `academic-writing-skills`：跨領域的 manuscript integrity 通用核心
- `paper-review`：適用於水資源、coupled natural-human systems、ABM、洪水與
  catastrophe modeling、hydrodynamics、不確定性及 LLM 研究的證據安全
  Ethan-style review overlay

[English README](./README.md)

## 1.0 版的主要改變

新版將論文視為持續演進的證據系統，不再只是逐句潤飾。它會區分：

- 單段修改與多檔案、長期 managed manuscript project
- 寫作順序、證據依賴與 review maturity
- 通用 integrity 規則，以及 study-design、domain、reviewer、venue、
  project overlays
- 直接結果、interpretation、mechanism 與 speculation
- working draft 與真正通過驗證的 release candidate

每次 review、revision 或 audit 最後都必須進行
functional-completeness retrospective。尚有高嚴重度 validity、ethics、
metadata 或 release 問題時，不得標示為 `SUBMISSION_READY`。

## 安裝

透過
[`ai-research-skills` Claude Code marketplace](https://github.com/WenyuChiou/ai-research-skills)
安裝：

```bash
claude plugin marketplace add WenyuChiou/ai-research-skills
claude plugin install academic-writing-skills@ai-research-skills --scope user
```

已安裝者可更新：

```bash
claude plugin update academic-writing-skills@ai-research-skills
```

安裝後可使用 `$academic-writing-skills` 與 `$paper-review`。

## 使用通用核心

`$academic-writing-skills` 可用於規劃、撰寫、review、revision、
proofreading、跨檔案同步與投稿準備。它支援實證、質性、計算模擬、
AI／LLM、review、theoretical、framework、methods 與 data papers，不會把
所有稿件強制套入 IMRAD。

完整論文或長期專案可先建立 project state：

```bash
python skills/academic-writing-skills/scripts/init_manuscript_state.py \
  manuscript_state.json
```

project state 會記錄 active artifacts、權威來源、locked wording、facts、
question-to-evidence alignment、研究設計維度、決策、open issues 與 release
checks。這個檔案應放在論文專案內，不應存進 skill 本身。

可使用的 deterministic diagnostics：

```bash
python skills/academic-writing-skills/scripts/audit_manuscript_state.py manuscript_state.json
python skills/academic-writing-skills/scripts/audit_text_consistency.py manuscript_state.json
python skills/academic-writing-skills/scripts/audit_docx_structure.py manuscript.docx
python skills/academic-writing-skills/scripts/run_regression_tests.py
```

這些 scripts 只提供診斷證據，不能取代實質的學術判斷。

## 使用 Paper Review overlay

`$paper-review` 僅在需要相關領域的 Ethan-style internal review 時使用。
它會先載入通用核心，再依稿件實際內容選擇 water、CNHS、ABM、
flood／hydrodynamic、uncertainty 或 AI module。

這個 overlay：

- 將 comments 分成 `MUST`、`SHOULD`、`QUERY`、`PREFERENCE`
- 使用使用者明確提供的 R1-R4；未提供時只使用 maturity labels
- 不冒充 Prof. Ethan Yang
- 不從寫作風格推斷 AI authorship
- 不會因為 reviewer 問「why」就自行創造 mechanism
- 只有確認 exact project 後才載入 project precedents

## Repository 結構

```text
skills/
  academic-writing-skills/
    SKILL.md
    references/
    scripts/
    assets/
    agents/
  paper-review/
    SKILL.md
    references/
    assets/
    agents/
evals/
tests/
```

## 測試

```bash
python -m pytest tests/ -q
python skills/academic-writing-skills/scripts/run_regression_tests.py
```

測試涵蓋 package structure、frontmatter、reference routing、project-state
schema、deterministic regressions、overlay isolation 與常見亂碼。

## 範圍

本 plugin 不會編造 scientific assumptions、analyses、results、citations、
mechanisms 或 metadata，也不取代 Zotero、NotebookLM、文件渲染或
tracked-change 工具。

## 授權

MIT

# academic-writing-skills

這是一套適用於 Claude／Codex 的論文撰寫與 reviewer-style scientific review plugin。1.1 版有兩個主要 skills：

| Skill | 使用情境 |
|---|---|
| `$academic-writing-skills` | extended outline、section／paragraph 撰寫、證據對齊、用詞、重複、流暢度、revision、跨檔案同步與 release checks |
| `$paper-review` | review-only critique、top-to-bottom scientific review、revision-round assessment、prior-comment regression，以及按需載入的 method、domain 或 reviewer modules |

`$paper-review` 以 `$academic-writing-skills` 作為 integrity base。專業知識放在直接 references，只有對話或稿件證明適用時才會載入。

[English README](./README.md)

## 1.1 版的主要改變

- 將 `$paper-review` 改為通用 reviewer，不再只服務 Ethan-style 或水領域論文。
- 新增 psychometrics／SEM、AI／LLM／ABM／computational、water／CNHS／policy／uncertainty，以及 flood／hydrodynamics／catastrophe 等 progressive modules。
- Ethan-style review 與 named project precedents 保持 explicit-only；不會因稿件涉及 water、ABM 或 LLM 就自動啟用。
- 補上 extended outline、逐段撰寫、section integration、top-to-bottom review、revision regression、summaries rebuild 與 exact submission package 的完整流程。
- 新增 style profile 與 deterministic prose diagnostics，可檢查 exact duplication、重複句首、跨句重複片語、stock phrasing 與可能過度使用的非技術詞。
- 明確規定：公式化或 AI-like 文字特徵只是 writing diagnostics，不是 AI authorship 證據；技術用詞不得為了表面變化而替換。

## 安裝

透過 [`ai-research-skills` Claude Code marketplace](https://github.com/WenyuChiou/ai-research-skills) 安裝：

```bash
claude plugin marketplace add WenyuChiou/ai-research-skills
claude plugin install academic-writing-skills@ai-research-skills --scope user
```

已安裝者可更新：

```bash
claude plugin update academic-writing-skills@ai-research-skills
```

## 要使用哪一個 skill？

| 任務 | 使用 |
|---|---|
| 建立或修改 outline、section、paragraph、Abstract、Conclusion | `$academic-writing-skills` |
| 修改時檢查用詞統一、重複用字、stock phrasing、flow | `$academic-writing-skills` |
| critique outline、section、manuscript、supplement、submission package | `$paper-review` |
| 進行 psychometrics、SEM、LLM、water、flood、ABM 或 hybrid technical review | `$paper-review`，由它選擇 references |
| 進行 Ethan-style R1–R4 review 或確認 supplied PI comments | `$paper-review`，並明確寫出 Ethan-style |
| 根據 review comments 修改論文 | `$academic-writing-skills` 加上已選定的 comments |
| 驗證上一輪 comments 是否解決且沒有 regression | `$paper-review` 加上 prior comments 與相關 versions |

## Progressive review 如何選擇模組

`$paper-review` 會先從對話、title、Abstract、questions、Methods、equations、figures、tables 與 supplement 推斷最小且足夠的模組組合：

| 稿件證據 | 載入 reference |
|---|---|
| Survey、scale、CFA、psychometrics、SEM、mediation、multi-group analysis | `quantitative-psychometrics-sem.md` |
| Simulation、ABM、ML、GenAI、LLM、synthetic respondents、agent evaluation | `ai-llm-computational.md` |
| Water resources、CNHS、policy、framework、review、uncertainty、equifinality | `water-cnhs-uncertainty.md` |
| Flood risk、hydrodynamics、drainage、inundation、catastrophe／loss model | `flood-hydrodynamics-catastrophe.md` |
| 明確 revision round 或 prior-review comparison | `round-calibration.md` |
| 明確 Ethan-style 或已確認的 lab-review context | `ethan-style-overlay.md`；exact project context 才可能再載入 `project-precedents.md` |

Hybrid paper 可以載入多個 modules。只有現有資訊仍存在會實質改變 evidence requirements 或 review standard 的歧義時，reviewer 才問一個精準問題，例如 factor analysis 究竟是 exploratory 還是 confirmatory。稿件本身已能判斷時，不會再要求使用者選領域。

其他使用者之後可新增直接 reference。每個 module 應包含 trigger／exclusion cues、technical and evidence checks、claim-scope boundaries、display／reproducibility checks，以及至少一個 routing 或 boundary eval。Reviewer、journal、laboratory 與 project rules 必須維持獨立 conditional overlays。

## 從 outline 到投稿的完整流程

### 1. 建立 project authority

完整論文、反覆 revision 或多檔案 package 應先建立 project state：

```bash
python skills/academic-writing-skills/scripts/init_manuscript_state.py \
  manuscript_state.json
```

記錄 active artifacts、權威 analyses／sources、locked questions／decisions、terminology、facts、question-to-evidence alignment、open issues 與 release checks。state 放在論文 project，不放進 installed plugin。

> 使用 `$academic-writing-skills` 建立這些檔案的 manuscript contract 與 authority hierarchy。先不要寫正文；確認 gap、task、questions、outcomes、contribution、nonclaims 與 unresolved sources。

### 2. 建立 extended outline

使用 `$academic-writing-skills` 建立 evidence plan，而不是只有 headings。每個 section 與 planned paragraph 都要定義 reader function、central claim 或 question、authorized evidence、inference boundary 與 next-unit bridge；同時做 top-down（gap → contribution）與 bottom-up（evidence → supported claim）檢查。

> 使用 `$academic-writing-skills` 建立 extended outline。將每一個 planned paragraph 對應到 function、claim、evidence、inference limit 與 next-paragraph bridge。列出缺少的 analyses 或 sources，不要自行生成 expected results。

複雜研究完成 outline 後，可再使用 `$paper-review` critique outline。它會按需載入 psychometric、computational、LLM、water 或 flood modules，但不會代替正文撰寫。

### 3. 一次撰寫一個 paragraph 或 section

每段使用五部分 contract：

1. function
2. narrowest defensible claim
3. authorized evidence
4. evidence-based development
5. bridge to the next paragraph

提供 active outline、sources、locked wording 與 adjacent paragraphs。單段任務應維持單段範圍。

> 使用 `$academic-writing-skills`，依 approved outline 與 supplied sources 撰寫 Section 2.3。保留 locked terms 與 numbers。逐段檢查 function、claim、evidence、development、bridge，並確認與前後段銜接。

完成的 passage 若需要獨立 technical critique，再以 review-only mode 使用 `$paper-review`，由它選擇 relevant references。

### 4. 完成一節後做 integration

依序只讀 topic sentences 與 closing sentences，確認各段形成累積論證、不重複相同功能，也沒有 orphan evidence 或 unsupported transitions。進入下一節前同步 terminology、abbreviations、citations、figures 與 tables。

### 5. 在重要版本進行 review

一般或 domain-specific review：

> 使用 `$paper-review` 對目前 manuscript 與 supplement 做 substantive、review-only assessment。推斷並列出使用的 modules，依 scientific 與 reproducibility risk 排序問題，不要修改。

明確 Ethan-style review：

> 使用 `$paper-review` 進行 Ethan-style R2 review。比較 current files 與 supplied prior comments，將 MUST／SHOULD／QUERY／PREFERENCE 與 severity 分開，並列出 resolved、partial、open、regressed 與 new issues。

### 6. 回到 writing core 修改

把接受的 review items 交給 `$academic-writing-skills`。區分已授權 edits、需要 author decision 的問題與 missing sources。任何 semantic 或 evidence change 都要同步 Methods、Results、Discussion、limitations、Abstract、Conclusion、supplement、displays 與 submission materials。

### 7. 執行完整 top-to-bottom review

主要 sections 完成後，使用 `$paper-review` 對 exact active files 分四輪檢查：

1. argument and structure
2. evidence、methods、claims、figures、tables、equations、citations
3. scholarly prose、terminology、repetition、observable stock phrasing、paragraph-to-paragraph flow
4. summaries、references、numbering、metadata、rendering、release integrity

再做 bottom-up 檢查：source evidence → result → interpretation → contribution → Abstract／Conclusion。若 prose edit 改變 scientific meaning，必須重跑受影響的 evidence checks。

### 8. 從穩定正文重建 summaries

使用 `$academic-writing-skills` 從目前 evidence map 重建 title、Abstract、highlights、Conclusion、conference abstract 與 cover materials。舊版 Abstract 不得作為 authority source。

### 9. 驗證 exact submission package

在 submission stage 使用 `$paper-review` 檢查 final manuscript、supplement、figures、tables、highlights、cover letter、metadata、declarations 與 required repository statements。仍有 high-severity blockers、unknown required facts、stale companion files、tracked changes 或 failed rendering 時，不得標示 `SUBMISSION_READY`。

## 用詞統一、重複用字、stock phrasing 與 flow

Writing core 會區分必要 technical repetition 與可避免 prose repetition。每個 concept 設定一個 preferred term，並保護 constructs、model names、populations 與 outcomes，不以 synonym rotation 做表面修改。

Scholarly-prose pass 會檢查：

- exact／near-duplicate sentences 與重複 paragraph functions
- 重複的非技術詞、phrases 與 sentence openings
- generic metadiscourse、empty intensifiers、stock transitions、vague subjects、repetitive cadence 與 content-light summaries
- subject continuity 與 familiar-to-new information order
- paragraph claim–evidence–development logic
- section 內 topic sentence 與 closing sentence flow

這些是 writing diagnostics，不是 AI detection。skills 不得只依 style 判定文字由 GPT 或其他模型生成。

可使用的 deterministic diagnostics：

```bash
python skills/academic-writing-skills/scripts/audit_manuscript_state.py manuscript_state.json
python skills/academic-writing-skills/scripts/audit_text_consistency.py manuscript_state.json
python skills/academic-writing-skills/scripts/audit_prose_patterns.py manuscript_state.json
python skills/academic-writing-skills/scripts/audit_docx_structure.py manuscript.docx
python skills/academic-writing-skills/scripts/run_regression_tests.py
```

Scripts 只回報需要 contextual review 的 candidates，不會自行認定 technical term 過度重複、transition 錯誤或 prose 為 AI-generated。

## Repository 結構

```text
skills/
  academic-writing-skills/
  paper-review/
    references/
evals/
tests/
```

## 測試

```bash
python -m pytest tests/ -q
python skills/academic-writing-skills/scripts/run_regression_tests.py
```

測試涵蓋兩個 skill boundaries、progressive reference routing、project-state schema、prose／integrity regressions、eval coverage 與常見亂碼。

每次 review、revision、audit 或 release check 最後都必須完成具體的 functional-completeness retrospective，不得只回覆籠統的 all-clear。

## 範圍

本 plugin 不會編造 assumptions、analyses、results、citations、mechanisms 或 metadata，也不取代 Zotero、NotebookLM、文件 rendering 或 tracked-change tooling。

## 授權

MIT

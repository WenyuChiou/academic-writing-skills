# academic-writing-skills

這是一套由兩個 skills 組成的學術論文寫作與科學審查工具。它把論文視為持續演進的證據系統：每一項主張都必須與研究問題、方法、證據、解釋及摘要保持一致，並同步反映在目前有效的主稿與相關附件中。

[English README](./README.md)

> 本專案屬於 [agentic AI learning roadmap](https://github.com/WenyuChiou/awesome-agentic-ai-zh) 的一部分。

## 兩個 skills 的分工

| Skill | 最適合從這裡開始的任務 |
|---|---|
| [`$academic-writing-skills`](./skills/academic-writing-skills/SKILL.md) | Extended outline、section／paragraph 撰寫與修改、用詞統一、重複與流暢度檢查、跨檔案同步，以及投稿檔案準備 |
| [`$paper-review`](./skills/paper-review/SKILL.md) | Review-only critique、top-to-bottom 科學審查、revision-round assessment、prior-comment regression，以及方法或領域專項審查 |

`$paper-review` 以 `$academic-writing-skills` 作為 manuscript-integrity base，再根據稿件證據 progressively 載入必要的技術 references。要求 review 預設只會審查，不代表授權修改稿件。

## 快速開始

### 1. 安裝或更新

透過 [`ai-research-skills` Claude Code marketplace](https://github.com/WenyuChiou/ai-research-skills) 安裝：

```bash
claude plugin marketplace add WenyuChiou/ai-research-skills
claude plugin install academic-writing-skills@ai-research-skills --scope user
```

這一個 plugin 安裝完成後，會同時提供 `$academic-writing-skills` 與 `$paper-review`。

已安裝者可更新：

```bash
claude plugin update academic-writing-skills@ai-research-skills
```

### 2. 叫用需要的 skill

在 Claude Code 中使用 `$academic-writing-skills` 或 `$paper-review`。上面的安裝指令只適用於 Claude Code。若 ChatGPT／Codex 已透過其他方式安裝這些 skills，可直接指定名稱，例如：`Use @paper-review ...`。

下方可複製的 prompts 使用 Claude Code 的 `$skill-name` 寫法；在 ChatGPT／Codex 中請改成 `@skill-name`。

使用者不需要自行選擇技術模組。只要說明任務、附上目前有效的檔案，並指出相關的舊版、reviewer comments、目標期刊或已鎖定決策即可。

### 3. 提供正確的證據與檔案

| 任務 | 建議至少提供 |
|---|---|
| 規劃 outline | 研究目的、gap、questions／objectives、methods、現有證據、目標 venue 與明確 nonclaims |
| 撰寫 section | 核准的 outline、可使用的 sources／results、鎖定用詞與前後段落 |
| 科學審查 | 目前有效的 manuscript，以及相關 figures、tables、supplement 和預定 review stage |
| Revision-round 核對 | Current manuscript、prior comments、author responses，以及可取得的 prior version |
| 投稿前檢查 | 實際要提交的全部檔案、目前的 venue requirements 與 metadata |

必要來源若無法取得，skills 會明確標示限制，不會自行猜測。

涉及多個檔案或版本時，可以在 prompt 前先填這六行，避免版本與權威來源混淆：

```text
TASK: [plan / draft / revise / review / submission check]
ACTIVE FILES: [這次要審查或修改的 exact versions]
AUTHORITY SOURCES: [發生衝突時應以哪些 results、data、code、approved outline 或 decisions 為準]
LOCKED DECISIONS: [不得改變的 wording、numbers、questions 或 claims]
NONCLAIMS: [本稿不能提出的 interpretations 或 conclusions]
TARGET / STAGE: [venue，以及 developmental / substantive / integration / submission]
```

`developmental` 適用於 outline 或尚未完成的初稿；`substantive` 表示核心科學內容已具備；`integration` 用於完整主稿與 companion files 的整合；`submission` 只用於實際準備提交的 exact package。若期刊或 reviewer 已提供 R1–R4，請明確寫出；skill 不會根據文筆或 comment 數量猜測輪次。

需要實際修改時，請提供 DOCX 或原始 source file；只做 review 且文字與圖表可清楚閱讀時，PDF 即可。若主稿內的 figures、tables 或 supplement 不完整，請另外附上。需要逐項核對 citations 時應提供 source papers；需要檢查 reproducibility 或 derived displays 時應提供 code／data；需要檢查期刊格式時則應提供目前有效的 journal guide。

## 可直接複製的 prompts

### 建立 extended outline

```text
使用 $academic-writing-skills，根據附件建立 extended outline。先確認研究
gap、task、research questions、methods、現有 evidence、預定 contribution
與 nonclaims。每個 planned paragraph 都列出 function、claim、authorized
evidence、inference limit 和銜接下一段的 bridge。暫時不要撰寫完整正文。
```

### 撰寫一個 section

```text
使用 $academic-writing-skills，依照已核准的 outline 與提供的 sources 撰寫
Section 2.3。保留所有鎖定用詞、數值與 citations。逐段檢查 function、
claim、evidence、development 和 bridge，並確認與前後段的銜接。
```

### 修改現有 section

```text
使用 $academic-writing-skills，依照指定目的修改附件中的 current Section 2.3。
將提供的 results 與 approved outline 視為 authority sources；保留 locked
terms、numbers、citations、research questions 與 claim scope。若某項修改需要
新增 evidence 或 author decision，請明確指出，不要自行補寫。
```

### 檢查用詞、重複與流暢度

```text
使用 $academic-writing-skills 修改這一節的 terminology consistency、可避免的
非技術詞重複、stock phrasing 與 paragraph-to-paragraph flow。保留必要的
technical repetition，不要改變科學意義、數值、citations 或 claim strength。
```

### 執行實質科學審查

```text
使用 $paper-review 對附件 manuscript 與 supplement 進行 substantive、
review-only assessment。推斷並列出最小且足夠的 modules，依 scientific 與
reproducibility risk 排序問題，將 comments 定位到稿件內容，不要修改檔案。
```

### 驗證 revision round

```text
使用 $paper-review，比較 current manuscript、prior comments、response letter
與 earlier version。將每個 issue 分為 resolved、partial、open、regressed、
waived、new 或 not verifiable。不能只因 author reply 或 comment thread 已標為
resolved，就認定修改已出現在所有受影響檔案中。
```

### 套用已選定的 review comments

```text
使用 $academic-writing-skills 處理 review items 1、3、5。保留已接受的科學
意義；需要 missing source 或 author decision 的項目繼續列為 open。將每項
material change 同步到受影響的 sections、figures、tables、supplement、
Abstract 與 Conclusion。
```

### 檢查最終投稿檔案

```text
使用 $paper-review，在 submission stage 檢查附件中的 exact manuscript、
supplement、figures、tables、highlights、cover letter、declarations 與
metadata。執行 top-to-bottom 和 bottom-up checks，列出 release blockers；
只有實際提交檔案全部支持時，才能標示 SUBMISSION_READY。
```

## 建議的完整論文流程

| 階段 | Skill | 產出 |
|---|---|---|
| 1. 建立權威來源 | `$academic-writing-skills` | Active files、authoritative sources、locked decisions、questions、contribution 與 nonclaims |
| 2. 規劃 | `$academic-writing-skills` | 與證據連結的 extended outline |
| 3. 撰寫與整合 | `$academic-writing-skills` | 段落功能清楚、跨 section 一致的正文 |
| 4. 審查 | `$paper-review` | 不直接改稿、依優先順序排列的科學與呈現問題 |
| 5. 修改 | `$academic-writing-skills` | 已授權修改，並同步所有受影響檔案 |
| 6. 驗證 | `$paper-review` | Cross-round regression 或 exact-package release assessment |

這不是單向流程。研究問題、方法、結果或主張只要發生 material change，就必須重新檢查所有受影響的 summaries 與 companion files。

## Paper review 如何自動選擇模組

`$paper-review` 會從目前對話、Abstract、questions、Methods、equations、figures、tables 與 supplement 推斷最小且足夠的模組組合。Hybrid paper 可以同時載入多個 modules。

| 稿件證據 | 適用時載入的 reference |
|---|---|
| Equations、formal notation、normalization、aggregation、composite metrics 或 derived uncertainty displays | `display-notation-provenance.md` |
| Surveys、scales、psychometrics、CFA、SEM、mediation 或 multi-group comparison | `quantitative-psychometrics-sem.md` |
| Simulation、ABM、ML、GenAI、LLM、synthetic respondents 或 agent evaluation | `ai-llm-computational.md` |
| Water resources、CNHS、policy、framework、uncertainty 或 equifinality | `water-cnhs-uncertainty.md` |
| Flood risk、inundation、drainage、hydrodynamics、catastrophe model、exposure、vulnerability 或 loss | `flood-hydrodynamics-catastrophe.md` |
| Prior comments、earlier drafts 或明確 revision round | `round-calibration.md` |
| 使用者明確要求 Ethan-style，或確認存在相關 lab-review context | `ethan-style-overlay.md`；exact project context 才可能再載入 `project-precedents.md` |

單一 keyword 或 study-area mention 不足以啟用模組。只有尚未釐清的歧義會實質改變 review standard 時，reviewer 才會問一個精準問題，例如 factor analysis 是 exploratory 還是 confirmatory。

## 長期專案與 deterministic diagnostics

一次性的段落修改可直接使用 lightweight mode，不需要額外設定。完整論文、反覆 revision 或多檔案 submission package，則建議建立 project state，並將它留在論文專案內：

```bash
python skills/academic-writing-skills/scripts/init_manuscript_state.py \
  manuscript_state.json
```

Project state 記錄 active artifacts、authority sources、locked wording、facts、terminology、question-to-evidence alignment、decisions、open issues 與 release checks。它是正式專案紀錄，不會把每一次局部用字都永久記住。

可使用的 diagnostics：

```bash
python skills/academic-writing-skills/scripts/audit_manuscript_state.py manuscript_state.json
python skills/academic-writing-skills/scripts/audit_text_consistency.py manuscript_state.json
python skills/academic-writing-skills/scripts/audit_prose_patterns.py manuscript_state.json
python skills/academic-writing-skills/scripts/audit_docx_structure.py manuscript.docx
python skills/academic-writing-skills/scripts/run_regression_tests.py
```

這些 scripts 只找出需要 contextual review 的 candidates，不會自行判定 technical term 過度重複、transition 錯誤或文字由 AI 生成。

## 證據與審查邊界

- Skills 不會編造 assumptions、analyses、results、citations、mechanisms、thresholds、reviewer preferences 或 metadata。
- Technical terminology 不會為了表面變化而進行 synonym rotation；prose repetition 會依上下文判斷。
- 可觀察的 stock 或 AI-like writing patterns 只是 editing diagnostics，不是 AI authorship 的證據。
- Response letter 只能證明作者聲稱已修改，不能證明 current manuscript 與所有 companion files 已完成修改。
- 每次 review、revision、audit 或 release check 都會以 functional-completeness retrospective 結束，清楚列出已檢查內容、未解決問題與 readiness limits。
- 本 plugin 是 Zotero、NotebookLM、統計軟體、來源核對、文件 rendering 與 tracked-change tools 的補充，不會取代它們。

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

新的通用 review knowledge 應放在 `paper-review` 的直接 reference 中，並定義 trigger／exclusion cues、technical and evidence checks、claim-scope boundaries，以及至少一個 routing 或 boundary eval。Journal、reviewer、laboratory 與 project rules 必須維持為獨立的 conditional overlays。

## 測試

```bash
python -m pytest tests/ -q
python skills/academic-writing-skills/scripts/run_regression_tests.py
```

測試涵蓋兩個 skill boundaries、progressive routing、project-state schema、prose／integrity regressions、eval coverage 與常見亂碼。

版本紀錄請見 [CHANGELOG.md](./CHANGELOG.md)。

## 授權

MIT

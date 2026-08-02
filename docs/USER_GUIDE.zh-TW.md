# 完整使用指南

這份文件收錄從首頁移出的進階說明。多數使用者可直接從 README 的兩個範例 prompts 開始。

[English](./USER_GUIDE.md)

## 選擇 skill

需要規劃、撰寫、修改、同步或準備投稿材料時，使用
`$academic-writing-skills`；只需要審查與找出問題時，使用
`$paper-review`。要求 review 預設不代表授權修改檔案。

## 建議提供的資料

| 任務 | 建議資料 |
|---|---|
| Outline | 研究目的、gap、questions、methods、現有 evidence、目標 venue，以及本稿不能提出的 claims |
| 撰寫或修改 | 核准的 outline、可使用的 sources／results、鎖定術語與前後文字 |
| 科學審查 | Exact active manuscript、figures、tables、supplement 與預定 review stage |
| Revision-round 核對 | Current manuscript、prior comments、response letter，以及可取得的 prior version |
| 投稿前檢查 | Exact submission files、目前 venue requirements 與 metadata |

涉及多個檔案或版本時，可在 prompt 前加入：

```text
TASK: [plan / draft / revise / review / submission check]
ACTIVE FILES: [這次要審查或修改的 exact versions]
AUTHORITY SOURCES: [發生衝突時應以哪些 results、data、code、approved outline 或 decisions 為準]
LOCKED DECISIONS: [不得改變的 wording、numbers、questions 或 claims]
NONCLAIMS: [本稿不能提出的 interpretations 或 conclusions]
TARGET / STAGE: [venue，以及 developmental / substantive / integration / submission]
```

`developmental` 適用於 outline 或未完成的初稿；`substantive` 表示核心科學
內容已具備；`integration` 用於完整主稿與 companion files；`submission`
只用於實際準備提交的 exact package。

需要修改時，建議提供 editable source 或 DOCX；只做 review 且內容可清楚閱讀
時，PDF 即可。Figures、tables 或 supplement 若無法在主稿內完整辨識，請另外
附上。逐項核對 citations 時需提供 source papers；檢查 reproducibility 時需
提供 code／data；檢查期刊格式時需提供目前有效的 journal guide。

## 更多 prompt 範例

### 建立 extended outline

```text
使用 $academic-writing-skills 根據附件建立 extended outline。確認 gap、
research questions、methods、現有 evidence、預定 contribution 與 nonclaims。
每個 planned paragraph 都列出 function、claim、authorized evidence、
inference limit 與 bridge。暫時不要撰寫完整正文。
```

### 撰寫 section

```text
使用 $academic-writing-skills，依照已核准的 outline 與提供的 sources 撰寫
Section 2.3。保留所有 locked terms、numbers 與 citations，並逐段檢查
claim、evidence、development 以及與前後文字的銜接。
```

### 檢查術語與流暢度

```text
使用 $academic-writing-skills 修改這一節的 terminology consistency、可避免的
非技術詞重複、stock phrasing 與 paragraph flow。保留必要的 technical
repetition，不要改變科學意義、數值、citations 或 claim strength。
```

### 套用選定的 review comments

```text
使用 $academic-writing-skills 處理 review items 1、3、5。需要 missing source
或 author decision 的項目繼續列為 open，並將每一項 material change 同步到
受影響的 sections、displays、supplement、Abstract 與 Conclusion。
```

### 驗證 revision round

```text
使用 $paper-review 比較 current manuscript、reviewer comments、response
letter 與 prior version。將每個 issue 分為 resolved、partial、open、
regressed、waived、new 或 not verifiable；不能只依 response letter 判定所有
受影響檔案都已完成修改。
```

### 檢查投稿檔案

```text
使用 $paper-review，在 submission stage 檢查 exact manuscript、supplement、
figures、tables、highlights、cover letter、declarations 與 metadata。列出
release blockers；只有實際檔案全部支持時，才能標示 SUBMISSION_READY。
```

## Review stages

| Stage | 用途 |
|---|---|
| Developmental | Outline 或未完成初稿的結構、gap、questions 與 planned evidence |
| Substantive | 科學有效性、methods、evidence、interpretation 與 reproducibility |
| Integration | 完整稿件的跨 section 與跨檔案一致性 |
| Submission | 實際投稿檔案的 release readiness |

## 自動選擇 review modules

`$paper-review` 會根據稿件本身選擇最小且足夠的技術 references，使用者不需
手動指定 modules。現有涵蓋範圍包括：

- equations、notation 與 derived-display provenance；
- surveys、psychometrics、CFA、SEM、mediation 與 multi-group comparison；
- simulation、ABM、ML、GenAI、LLMs 與 synthetic respondents；
- water resources、coupled human-natural systems、policy 與 uncertainty；
- flood risk、hydrodynamics、catastrophe modeling、exposure、vulnerability 與
  loss；
- prior-comment 與 revision-round regression checks。

單一 keyword 或 study-area mention 不足以啟用模組。Ethan-style 或
project-precedent overlay 只有在相關 context 被明確要求或確認時才會使用。

## 長期專案

一次性的修改不需額外設定。反覆修改的多檔案專案可以建立 manuscript state：

```bash
python skills/academic-writing-skills/scripts/init_manuscript_state.py manuscript_state.json
```

State 會記錄 active artifacts、authority sources、locked wording、facts、
terminology、decisions、open issues 與 release checks，不會保存每一次局部用字。

可使用的 diagnostics：

```bash
python skills/academic-writing-skills/scripts/audit_manuscript_state.py manuscript_state.json
python skills/academic-writing-skills/scripts/audit_text_consistency.py manuscript_state.json
python skills/academic-writing-skills/scripts/audit_prose_patterns.py manuscript_state.json
python skills/academic-writing-skills/scripts/audit_docx_structure.py manuscript.docx
python skills/academic-writing-skills/scripts/run_regression_tests.py
```

這些 scripts 只找出需進一步判讀的 candidates，不會自行認定文字由 AI 生成，
也不會直接判定 technical term 過度重複。

## 使用邊界

- Skills 不會編造 assumptions、analyses、results、citations、mechanisms、
  thresholds、reviewer preferences 或 metadata。
- Technical terms 不會為了表面變化而進行 synonym rotation。
- AI-like prose patterns 只是 editing diagnostics，不是 authorship 的證據。
- Response letter 不能證明修改已出現在所有受影響檔案中。
- 本 plugin 是 source verification、statistical software、reference managers、
  rendering 與 tracked-change tools 的補充，不會取代它們。

## 測試

```bash
python -m pytest tests/ -q
python skills/academic-writing-skills/scripts/run_regression_tests.py
```

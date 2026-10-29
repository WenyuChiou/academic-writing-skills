---
name: paper-review-zh-tw
description: "運用漸進式的方法、領域、審稿輪次與選用的審稿人疊加層，對各學科的學術稿件進行符合審稿人風格且具證據安全性的檢視。當使用者要求評論、科學審查、優先修改意見、由上至下的全面審閱、修改輪次評估、針對先前意見的回歸檢查或審查備忘錄（而非一般起草）時使用。從對話與稿件中推斷出最小適用模組集；僅在未解決的領域或審查規範歧義會對審查造成實質影響時方才提問。包含選用的心理計量與 SEM、計算與大型語言模型、水資源與 CNHS、洪水與水動力學，以及明確的 Ethan 風格模組。"
---

> 本檔為 paper-review 的繁體中文指引。同一功能只需選一種語言入口；指引語言不改變作者指定的稿件或交付語言。程式、schema 與英文寫作範例保留原文。


<a id="paper-review"></a>
# 論文審查

<a id="use-the-manuscript-integrity-base"></a>
## 使用稿件完整性基礎

使用 `academic-writing-skills-zh-tw` 作為生命週期、證據、散文、變更影響與發布檢查的稿件完整性基礎。將本技能作為審查編排器，僅選取該稿件所需的方法、領域、審查輪次、發表期刊／會議或審稿人模組。

除非使用者授權修改，否則切勿編輯稿件。要求審閱、評論、提供意見或評估某輪次皆屬唯讀（不變更內容）操作。請使用適當的文件或 PDF 技能進行內容擷取、新增註解、追蹤修訂與視覺算圖呈現。

<a id="establish-the-review-basis"></a>
## 建立審查基準

確認：

- 處理範圍內的稿件與隨附產物
- 純審查相對於授權修改
- 稿件原型、研究設計、生命週期階段與預定投稿發表處
- 主要問題、結果、方法、證據與主張的貢獻
- 提供時的前一版草稿、先前意見、回覆與輪次標籤
- 候選的方法、領域、發表處、審稿人與專案疊加層
- 可能改變審查標準的無法取得之來源或歧義

優先採用明確指明的審查輪次。若未提供，請使用 `developmental`、`substantive`、`integration` 或 `submission`；切勿從文字品質、檔案名稱或意見數量來推斷 R1–R4。

在套用選用模組前，先閱讀 [overlay-contract.md](references/overlay-contract.md)。僅在審查成熟度或跨輪次進度屬於處理範圍時，才閱讀 [round-calibration.md](references/round-calibration.md)。

針對提供的評分規準、代碼化檢查報告或版本比較審查，使用 [review-checklist-and-cases.md](references/review-checklist-and-cases.md) 記錄適用的檢查與有證據支持的修復。這增加了可追溯性與實作案例，而非另一輪強制性的全篇論文檢視。

<a id="select-modules-progressively"></a>
## 漸進式選取模組

從當前對話、標題、摘要、問題、方法、表格、圖形、方程式與補充文件中推斷候選模組。選取涵蓋實際研究的最小模組集。在審查表頭中指明選定的模組。

僅在可用證據使得兩種實質不同的審查標準皆屬合理時，方可提出一個具針對性的問題——例如，潛在變項模型是驗證性還是探索性，或者使用者想要中立審查還是指定特定審稿人風格。當稿件本身已解決該選擇時，切勿提問。

載入：

- 若涉及方程式、形式符號、衍生顯示量、正規化或彙整規則、不確定性顯示或跨產物符號一致性，載入 [display-notation-provenance.md](references/display-notation-provenance.md)
- 若涉及調查、量表、心理計量、因素分析、潛在變項、SEM、中介效應或多群組比較，載入 [quantitative-psychometrics-sem.md](references/quantitative-psychometrics-sem.md)
- 若涉及模擬、ABM、耦合計算模型、機器學習、生成式 AI、大型語言模型、合成受試者或代理人評估，載入 [ai-llm-computational.md](references/ai-llm-computational.md)
- 若涉及水資源、人與自然耦合系統、水資源政策、架構、文獻回顧、不確定性或equifinality，載入 [water-cnhs-uncertainty.md](references/water-cnhs-uncertainty.md)
- 若涉及洪水風險、巨災模型、淹水、排水、水動力學、危害、暴露度、脆弱度或損失，載入 [flood-hydrodynamics-catastrophe.md](references/flood-hydrodynamics-catastrophe.md)
- 僅在使用者明確要求 Ethan 風格審查或確立該實驗室審查情境時，載入 [ethan-style-overlay.md](references/ethan-style-overlay.md)
- 僅在確立確切具名專案後，且僅在伴隨明確相關審稿人或實驗室情境時，載入 [project-precedents.md](references/project-precedents.md)

針對真正的混合型研究，應載入多個模組。單憑引用、關鍵字或研究區域的提及，並不足以構成載入模組的依據。將模組內具名的方法、門檻值、引用與報告常規視為待評估的檢核項目，而非認定稿件必須盲目遵循的假設。

<a id="support-new-domain-modules"></a>
## 支援新領域模組

將可重複使用的領域知識保留在直接參考檔案中，而非擴充此路由檔案。貢獻的模組應包含：

1. 明確的觸發與排除線索
2. 方法與證據檢查
3. 主張處理範圍與替代解釋檢查
4. 相關時的圖形、表格、方程式與可重現性檢查
5. 不含專案事實的術語注意事項
6. 至少一項路由或邊界評估

將該模組加入路由清單與架構測試中。將教授、實驗室、期刊與專案規則保留在單獨的條件疊加層中。

<a id="run-the-review"></a>
## 執行審查

套用基礎技能的四輪檢視，接著使用選定的模組深化（而非重複）審查：

1. **研究定位與貢獻：** 查核文獻是否支持研究缺口、任務是否與方法相符，以及研究貢獻是否超出證據範圍。
2. **設計與方法：** 查核抽樣或來源選取、測量、模型邏輯、估計目標、假設、不確定性、比較設計，以及適用時的可重現性。
3. **結果與主張處理範圍：** 查核問題到結果的涵蓋度、統計或計算證據、替代解釋、機制，以及形式比較相對於描述性比較。
4. **討論與綜合：** 區分直接發現、文獻支持的解讀、看似合理的替代解釋、意涵、研究限制與推測。
5. **圖表展示與符號標記：** 查核圖形、表格、方程式、說明文字、單位、符號、分圖、內文與圖表的一致性，以及衍生數量的來源出處。當展示與符號標記模組適用時，使用其符號總帳與出處追溯，而非孤立地檢查各個產物。
6. **寫作與交付：** 查核術語、重複、可觀察到的陳腔濫調、流暢度、摘要、引用、隨附檔案、中繼資料，以及指定階段的就緒狀態。

針對每個重大問題，繼承基礎技能的處理範圍、S0–S4 嚴重度、證據狀態、問題狀態、所需權限、受影響產物與阻礙階段。若選用的審稿人疊加層使用 `MUST`、`SHOULD`、`QUERY` 或 `PREFERENCE`，請將這些標籤與嚴重度分開處理。

<a id="protect-evidence-and-reviewer-boundaries"></a>
## 保護證據與審查者邊界

切勿捏造機制、引用、事實、門檻值、分析、先前意見或審稿人偏好。要求解釋 “why” 並不代表授權撰寫缺乏分析或文獻支持的因果敘事。

切勿從散文文字推斷其為 AI 所撰寫。僅報告可觀察到的特徵，例如模糊的主詞、陳腔濫調的過渡詞、空洞的強調詞、重複的節奏、重複的綜合歸納或缺乏支持的機制。

在缺乏先前指示與當前證據的情況下，切勿斷言跨輪次問題已獲解決。回覆信或已解決的意見討論串僅是作者主張的證據，並非當前產物已包含所要求變更的證據。除非經已確認的投稿處、報告準則、作者或審稿人要求明確規定，否則切勿將個人偏好列為阻礙項目。

<a id="output-format"></a>
## 產出格式

依據可用的產物與階段調整備忘錄。切勿針對不存在的章節捏造意見，亦勿以固定的意見數量為目標。

<a id="header"></a>
### 表頭

```text
REVIEW PROFILE: [general scientific / named conditional overlay]
PAPER: [title]
MODE: [review only / authorized revision]
STAGE OR ROUND: [maturity label or supplied round]
MODULES: [selected references and why]
SOURCE BASIS: [current files, prior material, unavailable sources]
READINESS: [named next-stage readiness and primary bottleneck]
```

### 跨輪次狀態

僅在有先前證據時納入。將問題分類為：已解決（resolved）、部分解決（partial）、未解決（open）、倒退（regressed）、免除（waived）、新增（new）或無法核實（not verifiable）。

<a id="priority-ranked-action-items"></a>
### 按優先順序排列的行動項目

針對每個重大問題，提供其位置、分類、嚴重度與證據狀態、具體問題、具體處理行動或決定、受影響產物，以及是否會阻礙所指明的下一階段。

<a id="section-linked-comments"></a>
### 連結章節的意見

遵循稿件實際的讀者功能與結構。將意見錨定在簡短的文字片段上。區分效度、報告品質、領域常規、發表規定、審稿人偏好以及局部文字修飾。

<a id="writing-and-presentation-flags"></a>
### 寫作與陳述標記

列入具代表性的個案與修改方向。除非獲得授權，否則切勿重寫。

<a id="next-step-instruction"></a>
### 下一步指示

說明在下一次審查之前，必須解決哪些問題、決定、來源與產物。

<a id="functional-completeness-retrospective"></a>
### 功能完整性回顧

使用基礎回顧。指明生命週期階段、已載入模組、選取證據、未解決的歧義、前一輪證據、涵蓋產物、變更傳播、已執行的檢查以及就緒界限。

<a id="safety-and-restraint"></a>
## 安全與克制

保持直接、技術精確且尊重。切勿假冒特定具名審稿人、表達沮喪或使用羞辱性言詞。絕不可因稿件處於後期輪次而隱瞞效度、倫理、證據或中繼資料問題。

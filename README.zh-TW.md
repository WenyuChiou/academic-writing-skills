# Academic Writing Skills

[![plugin version](https://img.shields.io/badge/plugin-v1.3.18-blue.svg)](./CHANGELOG.md)
[![license](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

本專案是 [ai-research-skills](https://github.com/WenyuChiou/ai-research-skills) 的一部分。

從研究定位與架構發想、連貫的逐段撰寫，到整篇論文的檢查與審查。

可搭配 **Codex**、**Claude Code**、**OpenCode**、**Hermes Agent**，以及其他支援 Agent Skills 格式的 AI agents 使用。可用工具與整合功能依 host 而定。

[English](./README.md) | 繁體中文

![流程：研究定位與大綱、規劃與撰寫、檢查與修改、章節審查、整篇審查；共用詞彙紀錄貫穿每個階段。](./docs/images/workflow-cover.png)

## 可以協助什麼

一個 plugin 提供兩個 skills：

- [academic-writing-skills](./skills/academic-writing-skills/SKILL.md)：規劃、撰寫、修改，並同步稿件的相關變動。
- [paper-review](./skills/paper-review/SKILL.md)：審查稿件，列出有具體位置的問題；預設不直接修改檔案。

| 任務 | 協助產出的內容 |
|---|---|
| 研究定位與大綱 | 研究方向、缺口、問題、證據界線，以及 extended outline。 |
| 規劃與撰寫 | 段落規劃與草稿，並釐清想法之間的銜接。 |
| 檢查與修改 | 核對意思、術語、證據、連貫性、引用，以及受影響的圖表。 |
| 審查 | 章節審查，以及整篇論文的四輪檢查。 |
| 同步修改 | 對齊正文、補充資料、圖表、reviewer response 與投稿檔案。 |

## 從研究架構到最終投稿

寫之前，先規劃每段的重點、證據與銜接；寫完後，複查實際修改的文字。章節收尾時，再檢查段落之間是否形成連貫論證。

整篇審查會從頭到尾進行四輪：**論證與結構、證據與主張範圍、學術表達、交付完整性**。由上而下核對問題到證據，也由下而上確認證據能否支持結論；發現重大問題時，回查受影響的章節。

**共用詞彙紀錄貫穿全程。** 持續撰寫同一篇論文時，沿用其定義、固定用詞與允許變體。寫前讀取已確認的用詞，確認修改後再更新紀錄；新提議的名稱須與作者已確認的選擇分開。

檢查深度依任務調整。單句文法修改不會啟動所有階段，也不要求建立新的管理檔案。跨檔案的修改則需回查受影響的摘要、文獻與補充資料。

## 安裝與使用

Claude Code 可透過 ai-research-skills marketplace 安裝：

```bash
claude plugin marketplace add WenyuChiou/ai-research-skills
claude plugin install academic-writing-skills@ai-research-skills --scope user
```

更新指令：`claude plugin update academic-writing-skills@ai-research-skills`。

Codex 或 ChatGPT 可使用可用的 skill／plugin 介面。其他 Agent Skills clients 可將 `skills/` 下的兩個資料夾放入支援的位置：OpenCode 使用 `.agents/skills/` 或 `.opencode/skills/`，Hermes Agent 使用 `~/.hermes/skills/`。

## 直接試用

附上目前要處理的文字與來源；圖表、補充資料、審查意見或期刊指引只在相關時提供。用一般文字指定 skill 名稱即可。

### 研究定位與大綱

```text
請使用 academic-writing-skills skill，釐清這篇論文的研究定位並建立 extended outline。
確認研究缺口、問題、證據，以及每段的功能。
暫時不要撰寫正文。
```

### 規劃與逐段撰寫

```text
請使用 academic-writing-skills skill，先規劃這一節，再逐段撰寫。
每段寫之前，先說明重點、證據、推論界線，以及與前後文的關係。
寫完後，複查意思、術語與連貫性。
```

### 檢查一個段落

```text
請使用 academic-writing-skills skill，檢查這段的定義、術語、連貫性與重複。
保留已確立的專業用詞及科學意義。
缺少證據的地方請指出，不要自行編造。
```

### 審查整篇論文

```text
請使用 paper-review skill，對正文與補充資料進行四輪審查：
論證與結構、證據與主張範圍、學術表達、交付完整性。
定位各項問題，說明依據及影響，先不要修改檔案。
```

### 對齊 reviewer response

```text
請使用 academic-writing-skills skill，將 response 與最新正文及補充資料對齊。
保留作者已寫好且正確的句子，指出未達成的承諾與無法核實的交叉引用。
只有相關檔案確實支持時，才能說某項修改已完成。
```

## 適用界線與進一步說明

審查模組依研究內容選用，包含方程式、psychometrics／SEM、AI／LLM、水資源與洪水模型。這些 skills 協助來源核對及作者判斷，不取代它們；缺少的結果或來源保持未核實，不自行編造。

- [完整使用指南](./docs/USER_GUIDE.zh-TW.md)：輸入資料、更多 prompts、審查階段與專案紀錄。
- [圖表實例](./skills/academic-writing-skills/references/figures-tables-and-supplements.md)：圖、caption、表格與補充資料。
- [期刊與引用準則](./skills/academic-writing-skills/references/overlay-contract.md)。
- [版本紀錄](./CHANGELOG.md)。

## 授權

[MIT](./LICENSE)

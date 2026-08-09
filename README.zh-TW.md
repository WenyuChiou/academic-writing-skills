# Academic Writing Skills

[![tests](https://github.com/WenyuChiou/academic-writing-skills/actions/workflows/test.yml/badge.svg)](https://github.com/WenyuChiou/academic-writing-skills/actions/workflows/test.yml)
[![plugin version](https://img.shields.io/badge/plugin-v1.1.2-blue.svg)](./CHANGELOG.md)
[![license](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

**把論文視為一個完整的證據系統：從研究論證與架構發想、extended outline、
逐段撰寫，到整稿 review、修改同步與最終投稿。**

採用開放的 Agent Skills 格式，適用於 Claude Code、ChatGPT、Codex、
OpenCode、Hermes Agent，以及其他相容的 AI agents。
[English](./README.md)

## 從研究架構到最終投稿

一般用途的 AI 可以把單一段落改得更流暢，卻可能漏掉這項修改對整篇論文的
影響。這套 skills 涵蓋完整的 manuscript lifecycle：

`研究定位 → 論證架構 → Extended outline → 依證據撰寫 → 雙向對齊 →
整稿 review → 修改同步 → 投稿驗證`

| 階段 | Workflow 的功能 |
|---|---|
| 研究定位與架構發想 | 釐清問題、gap、research questions、預定 contribution、證據界線與 nonclaims。 |
| Extended outline | 為每個預定段落設定 reader function、可辯護的 claim、authorized evidence、inference limit 與 bridge。 |
| 依證據撰寫 | 根據核准資料與目前結果發展 Methods、Results、Discussion、Conclusion、Abstract 與其他投稿材料。 |
| 雙向 integrity review | 由上而下檢查目的到證據的對齊，也由下而上檢查證據到 contribution 的合理性。 |
| 從頭到尾的整稿 review | 對完整稿件進行四輪 top-to-bottom review：論證與結構、證據與主張範圍、學術寫作與 flow、交付完整性。 |
| 修改與 release | 將重大修改同步到 sections、figures、tables、supplement、metadata 與實際投稿檔案。 |

Top-down review 會從 gap 或研究目的往下追蹤到 questions、methods、evidence
與 conclusions；bottom-up review 則從 source evidence 往上核對 results、
interpretations、contributions 與 summaries 是否真正有依據。

## 兩個 skills，一套 manuscript system

| Skill | 適合使用的情況 |
|---|---|
| [`academic-writing-skills`](./skills/academic-writing-skills/SKILL.md) | 需要研究定位、架構與 outline、撰寫、修改、跨檔案同步，或準備投稿材料。 |
| [`paper-review`](./skills/paper-review/SKILL.md) | 需要 evidence-safe reviewer critique、revision-round 核對或投稿前 audit，但不直接修改稿件。 |

`paper-review` 預設只負責找出與說明問題。選定要採用的 comments 後，再由
`academic-writing-skills` 修改並同步所有受影響的內容。

## 安裝與使用

以下 prompts 採平台中立寫法：直接用一般文字指定 skill 名稱。相容的 agent
也可以依任務自動啟用，或提供自己的 selector 與 shortcut。

| Client | Skill 支援方式 |
|---|---|
| Claude Code | 使用下方 marketplace 指令安裝 plugin。 |
| ChatGPT 與 Codex | 從可用的 Skills 介面使用已安裝的 skill 或 plugin；兩者皆支援開放的 Agent Skills 格式。 |
| OpenCode | 將兩個 skill folders 放入 `.agents/skills/`、`.opencode/skills/` 或其他支援的 skill directory。 |
| Hermes Agent | 放入 `~/.hermes/skills/`，或將本 repository 的 `skills/` 設為 external skill directory。 |

Claude Code 安裝方式：

```bash
claude plugin marketplace add WenyuChiou/ai-research-skills
claude plugin install academic-writing-skills@ai-research-skills --scope user
```

一次安裝會同時提供兩個 skills。之後需要更新時：

```bash
claude plugin update academic-writing-skills@ai-research-skills
```

Codex、OpenCode、Hermes Agent 或其他 Agent Skills client 可先 clone 本
repository，再將 `skills/` 下的兩個 folders 複製或連結到 client 會掃描的
位置。`.agents/skills/` 可由 Codex 與 OpenCode 共用；Hermes Agent 也可將
它設定成 external source。

## 立即試用

請附上這次真正要處理的 active manuscript、section 或 outline。若 figures、
tables、supplement、reviewer comments、prior versions 或 venue guide 會影響
判斷，也請一併提供。

### 建立 extended outline

```text
請使用 academic-writing-skills skill，根據附件發展 extended outline。確認
gap、research questions、planned evidence、預定 contribution 與 nonclaims。
為每個 planned paragraph 設定 function、claim、authorized evidence、
inference limit 與 bridge。暫時不要撰寫完整正文。
```

### 審查完整稿件

```text
請使用 paper-review skill，對附件中的 manuscript 與 supplement 進行四輪
從頭到尾的整稿 review：論證與結構、證據與主張範圍、學術寫作與 flow，以及
交付完整性。依 scientific 與 reproducibility risk 排序問題，將每項 comment
定位到實際檔案，且不要直接修改。
```

## 主要保護範圍

- 從研究架構到最終 summaries 的 question-to-evidence alignment。
- 科學意義、作者鎖定的 decisions、claim scope 與明示的 nonclaims。
- Manuscript、Abstract、figures、tables、supplement、reviewer responses、
  metadata 與投稿檔案的一致性。
- 術語、必要與可避免的重複、段落 flow 與制式語句，同時避免 cosmetic
  synonym swapping。
- Equations 與 derived displays、surveys 與 psychometrics／SEM、simulation
  與 AI／LLM studies、water 與 flood models，以及 revision rounds 的相關
  技術風險。

缺少的 results、citations、assumptions 或 reviewer preferences 只會被標示為
限制，不會由 skills 自行編造。

## 進一步說明

- [完整使用指南](./docs/USER_GUIDE.zh-TW.md)：任務輸入、更多平台中立 prompts、
  review stages、技術 modules 與長期專案使用方式。
- [版本紀錄](./CHANGELOG.md)

本專案屬於
[agentic AI learning roadmap](https://github.com/WenyuChiou/awesome-agentic-ai-zh)
的一部分。

## 授權

[MIT](./LICENSE)

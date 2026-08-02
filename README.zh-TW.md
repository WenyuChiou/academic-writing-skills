# Academic Writing Skills

[![tests](https://github.com/WenyuChiou/academic-writing-skills/actions/workflows/test.yml/badge.svg)](https://github.com/WenyuChiou/academic-writing-skills/actions/workflows/test.yml)
[![plugin version](https://img.shields.io/badge/plugin-v1.1.1-blue.svg)](./CHANGELOG.md)
[![license](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

**讓研究問題、證據、主張與用詞，從 extended outline 到最終投稿都維持一致。**

適用於 Claude Code、ChatGPT 與 Codex。[English](./README.md)

## 為什麼需要這些 skills？

一般用途的 AI 可以把一段文字改得更流暢，卻不一定知道這個修改會影響論文的
其他位置，最後可能出現：

- 主張比研究結果實際能支持的更強；
- 術語、數值或結論在不同章節與檔案之間漂移；
- 回覆信寫著「已修改」，但實際稿件仍遺漏該項調整；
- 文字看似完整，研究問題、方法、結果與結論卻沒有真正對齊。

這套 skills 把論文視為一個互相連動的證據系統。它會保護作者已鎖定的決策，
證據不足時明確標示而不自行補寫，並依稿件內容逐步選擇真正需要的方法與領域
檢查。

## 兩個 skills，一套工作流程

`規劃 → 撰寫 → 審查 → 修改 → 驗證`

| Skill | 適合使用的情況 |
|---|---|
| [`$academic-writing-skills`](./skills/academic-writing-skills/SKILL.md) | 規劃、建立 outline、撰寫、修改、跨檔案同步，或準備投稿材料。 |
| [`$paper-review`](./skills/paper-review/SKILL.md) | 需要 reviewer-style critique、revision-round 核對或投稿前審查，但不直接修改稿件。 |

`$paper-review` 預設只進行審查。選定要採用的 comments 後，再使用
`$academic-writing-skills` 修改並同步所有受影響的內容。

## 安裝

在 Claude Code 中執行：

```bash
claude plugin marketplace add WenyuChiou/ai-research-skills
claude plugin install academic-writing-skills@ai-research-skills --scope user
```

一次安裝會同時提供兩個 skills。之後需要更新時：

```bash
claude plugin update academic-writing-skills@ai-research-skills
```

若已安裝在 ChatGPT 或 Codex，可使用 `@academic-writing-skills` 或
`@paper-review` 指定 skill。

## 立即試用

附上這次要處理的正確 manuscript 或 section；若任務涉及 figures、tables、
supplement、reviewer comments 或 prior version，也請一併提供。

### 撰寫或修改

```text
使用 $academic-writing-skills 修改附件中的 section。保留原有科學意義、
數值、citations 與關鍵術語。需要新增 evidence 或 author decision 的地方請
明確標示，不要自行猜測。
```

### 審查論文

```text
使用 $paper-review 審查附件中的 manuscript 與 supplement。依 scientific
和 reproducibility risk 排序問題，將每項 comment 定位到稿件內容，不要
直接修改檔案。
```

## 主要檢查範圍

- 從 research questions 到 conclusions 的主張與證據是否對齊。
- Manuscript、Abstract、figures、tables、supplement 與投稿材料是否一致。
- 術語、重複、段落銜接與制式語句是否需要修改，同時避免用同義詞輪替掩蓋
  問題。
- Equations 與衍生圖表、surveys 與 psychometrics／SEM、simulation 與
  AI／LLM studies、water 與 flood models，以及 revision rounds 的相關技術風險。

缺少的 results、citations、assumptions 或 reviewer preferences 只會被標示為
限制，不會由 skills 自行編造。

## 進一步說明

- [完整使用指南](./docs/USER_GUIDE.zh-TW.md)：更多 prompts、輸入模板、
  review stages 與長期專案使用方式。
- [版本紀錄](./CHANGELOG.md)

本專案屬於
[agentic AI learning roadmap](https://github.com/WenyuChiou/awesome-agentic-ai-zh)
的一部分。

## 授權

[MIT](./LICENSE)

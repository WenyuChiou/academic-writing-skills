# Academic Writing Skills

提供給 Claude Code、ChatGPT 與 Codex 使用的學術論文寫作與科學審查工具，重點是讓文字、證據與主張保持一致。

[English](./README.md)

一次安裝會提供兩個互補的 skills：

| 你想做的事 | 使用 |
|---|---|
| 規劃、撰寫、修改或潤飾論文 | [`$academic-writing-skills`](./skills/academic-writing-skills/SKILL.md) |
| 審查論文並找出問題，但不直接改稿 | [`$paper-review`](./skills/paper-review/SKILL.md) |

`$paper-review` 負責找出問題並排定優先順序；需要實際修改時，再使用
`$academic-writing-skills`。

## 安裝

```bash
claude plugin marketplace add WenyuChiou/ai-research-skills
claude plugin install academic-writing-skills@ai-research-skills --scope user
```

之後需要更新時：

```bash
claude plugin update academic-writing-skills@ai-research-skills
```

## 快速開始

1. 附上目前有效的 manuscript 或 section。
2. 視任務加入 figures、tables、supplement、reviewer comments 或 prior version。
3. 說明你要做什麼，再複製下方最接近的 prompt。

以下範例使用 Claude Code 的 `$skill-name`；若 skills 已安裝在 ChatGPT 或
Codex，請改用 `@skill-name`。

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

## 會檢查什麼

- Claims 是否有現有 evidence 支持。
- Methods、Results、Discussion、Abstract、figures、tables 與 supplement
  是否一致。
- 術語、重複與段落銜接是否穩定，同時避免改變科學意義。
- 是否存在特定方法或領域的風險；需要的 review modules 會自動選擇。

Skills 不會自行補造 results、citations、assumptions 或 reviewer preferences；
缺少證據時會明確標示限制。

## 進一步說明

- [完整使用指南](./docs/USER_GUIDE.zh-TW.md)
- [版本紀錄](./CHANGELOG.md)

本專案屬於
[agentic AI learning roadmap](https://github.com/WenyuChiou/awesome-agentic-ai-zh)
的一部分。

## 授權

MIT

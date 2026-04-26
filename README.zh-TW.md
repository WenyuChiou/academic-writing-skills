# academic-writing-skills

這是一個可分享的 Claude/Codex skill，用於嚴謹的學術論文寫作、修改、審稿回覆、圖文一致性檢查，以及投稿前檢查。

[English README](./README.md)

## 目的

這個 skill 把常見的論文工作流程變成可重複執行的檢查與寫作規則：

- 用 findings-first 結構撰寫章節。
- 幫 Results 和 Discussion 補上明確 mechanism。
- 找出 GPT 式空泛語言、過度宣稱和模糊強化詞。
- 檢查每個 claim 是否有 figure、table、統計結果、程式輸出或文獻支撐。
- 確認數字、figure panel、caption 和正文一致。
- 建立 point-by-point reviewer response table。
- 準備投稿前 checklist 和必要 declarations。
- 建立 `.paper/` context 檔，讓之後的 AI session 不需要反覆讀整篇 manuscript，節省 token。

這個 skill 不綁定特定領域。期刊規則、老師偏好、paper 專用術語與例外規則，都應放在各自 paper repo 的 `.paper/` 內。

## 安裝

從 [`ai-research-skills` Claude Code marketplace](https://github.com/WenyuChiou/ai-research-skills) 裝：

```bash
claude plugin marketplace add WenyuChiou/ai-research-skills
claude plugin install academic-writing-skills@ai-research-skills --scope user
```

> **之前用 `git clone` 裝的？** 為了符合 marketplace 規範，這個 repo 的
> SKILL.md 已從 root 搬到 `skills/<name>/SKILL.md`；舊的
> `git clone ... ~/.claude/skills/academic-writing-skills` 路徑現在
> 不會載入（Claude Code 的 user-skills loader 只掃一層）。請刪掉舊的
> （`rm -rf ~/.claude/skills/academic-writing-skills`）改走上面的
> marketplace 安裝。

## 每篇論文的一次性設定

每篇 manuscript 建議在 paper repo 內建立 `.paper/`：

```text
<paper-repo>/
  .paper/
    journal_format.md
    style_overrides.md
    context.md
    figure_inventory.md
    claim_evidence_ledger.md
    reviewer_comments.md
    submissions_log.md
```

最低限度設定：

1. 複製 `references/journal_format_template.md` 到
   `<paper-repo>/.paper/journal_format.md`。
2. 根據目標期刊最新 author guidelines 填入格式規則。
3. 如有必要，複製 `references/style_overrides_example.md` 到
   `<paper-repo>/.paper/style_overrides.md`。
4. 長期專案建議建立 `references/paper_context_packet.md` 中定義的 context packet。

## Skill 結構

```text
academic-writing-skills/
  SKILL.md
  references/
    banned_words.md
    claim_evidence_audit.md
    figure_conventions.md
    journal_format_template.md
    paper_context_packet.md
    reviewer_response_workflow.md
    section_checklists.md
    style_overrides_example.md
    submission_checklist.md
    writing_principles.md
  evals/
    evals.json
  tests/
    test_skill_integrity.py
```

## 常見使用場景

### 撰寫或修改章節

skill 會讀取期刊格式、paper overrides、writing principles、banned words，以及相關 section checklist，然後檢查：

- finding 是否放在 figure citation 前面，
- 每個 result 是否有 mechanism，
- 術語是否一致，
- 是否有 unsupported overclaim，
- 有 panel 的圖是否使用 panel-level citation。

### 檢查 claim 和 evidence

skill 會建立 claim-evidence ledger：

```text
claim -> evidence source -> allowed certainty -> missing check -> revision
```

這對修改 Abstract、Discussion、Conclusion、cover letter 和 reviewer response 特別有用。

### 回覆審稿人

skill 會把 reviewer comments 轉成 response table：

```text
comment -> anchor text -> response -> manuscript change -> evidence
```

目標是避免只寫「we clarified」但 manuscript 沒有實際修改的情況。

### 節省 AI session token

長 manuscript 建議維護 `.paper/context.md`、`.paper/figure_inventory.md` 和 `.paper/claim_evidence_ledger.md`。之後的 AI session 可以先讀這些濃縮檔案，而不是每次重讀整篇論文。

## 這個 skill 不處理什麼

- 不管理 Zotero。
- 不設定 Obsidian 或 NotebookLM workspace。
- 不做 coding-agent delegation。
- 不只是一般文法檢查器。
- 不會替使用者編造 scientific assumptions、results 或 citations。

## 測試

執行：

```bash
python -m pytest -q
```

測試會檢查 frontmatter、reference files、eval prompts，以及常見亂碼標記。

## 授權

MIT

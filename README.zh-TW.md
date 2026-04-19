# academic-writing-skills

針對嚴謹學術論文寫作、改稿與投稿的 Claude Code skill。不綁定任何領域，期刊
特定規則與論文個別例外都放在每篇論文自己的 repo 裡（`<paper-repo>/.paper/`），
因此 skill 本身保持通用。

[English README](./README.md)

---

## 能做什麼

- 強制 **findings-first + mechanism** 結構（結果先講、機制跟上）
- **禁用字詞稽核**：抓出 GPT 風格、過度聲稱、填充語
- 檢查 **圖文對應**：正文裡的數字必須出現在圖上
- 引導 **分節撰寫**：Abstract、Introduction、Methods、Results、Discussion、
  Conclusion 各有專屬 checklist
- 寫作前 **強制確認期刊格式**（word limit、citation style、required sections）
- 投稿前 **完整 submission checklist**：封面信、推薦審稿人、data availability、
  圖檔規格、ORCID/CRediT/IRB 等身份與倫理披露

## 安裝

複製到 Claude Code 的 skills 資料夾。請把 `<your-fork>` 改成你自己的 GitHub
帳號或上游 repo 擁有者：

```bash
# 使用者層級（所有專案都可用）
git clone https://github.com/<your-fork>/academic-writing-skills ~/.claude/skills/academic-writing-skills

# 專案層級（只在該專案生效）
git clone https://github.com/<your-fork>/academic-writing-skills <project>/.claude/skills/academic-writing-skills
```

Claude Code 會自動從這些路徑偵測 skill，不需要額外設定。

## 每篇論文的一次性設定

在每篇論文的 git repo 建立 `.paper/` 資料夾：

```
<paper-repo>/
└── .paper/
    ├── journal_format.md      # 用 journal_format_template.md 填出來
    └── style_overrides.md     # 選填：這篇論文的專屬禁用詞、例外
```

第一次在 paper repo 啟用時，skill 會：

1. 檢查 `.paper/journal_format.md` 是否存在
2. 若不存在，帶你依據 `references/journal_format_template.md` 填寫
3. 把完成的檔案存到 `<paper-repo>/.paper/journal_format.md`

## Skill 結構

```
academic-writing-skills/
├── SKILL.md                            # 入口 + 工作流
├── references/
│   ├── writing_principles.md           # 8 大核心原則
│   ├── banned_words.md                 # GPT / 過度聲稱 / 填充語偵測
│   ├── figure_conventions.md           # 圖文對應 + 跨圖一致性規則
│   ├── section_checklists.md           # 各 section 撰寫檢查
│   ├── submission_checklist.md         # 投稿前完整清單
│   ├── journal_format_template.md      # 期刊格式模板
│   └── style_overrides_example.md      # `.paper/style_overrides.md` 範例
└── README.md (+ README.zh-TW.md)
```

## 工作流

接到任何寫論文的任務時，skill 會跑這個流程：

1. **確認期刊格式** — 載入 `<paper-repo>/.paper/journal_format.md`，
   或請使用者先填模板。
   - **Fast-path**：單句 polish、禁用字掃描、transition 調整等小改不強制填模板，
     直接進下一步。
2. **載入論文專屬 overrides** — 套用 `<paper-repo>/.paper/style_overrides.md`
   的規則（優先於 skill 預設）。
3. **載入通用規則** — `writing_principles.md` 和 `banned_words.md`。
4. **依任務類型載入專屬檔** — section checklist、figure conventions 或
   submission checklist。
5. **出稿前自我稽核** — 檢查機制完整性、禁用字、數字對應、句間銜接，
   通過才呈現給使用者。

## 不在 skill 裡面的東西

- **特定期刊列表** — 由每位使用者在自己的 paper repo 維護，因為領域差異大。
- **領域專屬術語偏好** — 由論文的 `style_overrides.md` 處理。
- **個人聲腔偏好** — 那屬於使用者的 CLAUDE.md。

## 設計哲學

- **嚴謹但不強推風格**：skill 會抓過度聲稱、缺機制、圖文不符等普遍問題，
  但不逼使用者採用特定句式。
- **格式優先、寫作其次**：任何寫作前先確認期刊規格。
- **論文主權**：每篇論文的 `.paper/` 資料夾擁有最終決定權。skill 絕不會在
  論文已經表態的情況下默默套用自己的偏好。

## 授權

MIT

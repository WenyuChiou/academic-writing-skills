---
name: paper-review-zh-cn
description: "运用渐进式的方法、领域、审稿轮次与选用的审稿人叠加层，对各学科的学术稿件进行符合审稿人风格且具证据安全性的检视。当使用者要求评论、科学审查、优先修改意见、由上至下的全面审阅、修改轮次评估、针对先前意见的回归检查或审查备忘录（而非一般起草）时使用。从对话与稿件中推断出最小适用模块集；仅在未解决的领域或审查规范歧义会对审查造成实质影响时方才提问。包含选用的心理计量与 SEM、计算与大型语言模型、水资源与 CNHS、洪水与水动力学，以及明确的 Ethan 风格模块。"
---

> 本档为 paper-review 的简体中文指引。同一功能只需选一种语言入口；指引语言不改变作者指定的稿件或交付语言。程式、schema 与英文写作范例保留原文。


<a id="paper-review"></a>
# 论文审查

<a id="use-the-manuscript-integrity-base"></a>
## 使用稿件完整性基础

使用 `academic-writing-skills-zh-cn` 作为生命周期、证据、散文、变更影响与发布检查的稿件完整性基础。将本技能作为审查编排器，仅选取该稿件所需的方法、领域、审查轮次、发表期刊／会议或审稿人模块。

除非使用者授权修改，否则切勿编辑稿件。要求审阅、评论、提供意见或评估某轮次皆属唯读（不变更内容）操作。请使用适当的文件或 PDF 技能进行内容撷取、新增注解、追踪修订与视觉算图呈现。

<a id="establish-the-review-basis"></a>
## 建立审查基准

确认：

- 处理范围内的稿件与随附产物
- 纯审查相对于授权修改
- 稿件原型、研究设计、生命周期阶段与预定投稿发表处
- 主要问题、结果、方法、证据与主张的贡献
- 提供时的前一版草稿、先前意见、回复与轮次标签
- 候选的方法、领域、发表处、审稿人与项目叠加层
- 可能改变审查标准的无法取得之来源或歧义

优先采用明确指明的审查轮次。若未提供，请使用 `developmental`、`substantive`、`integration` 或 `submission`；切勿从文字品质、文件名称或意见数量来推断 R1–R4。

在套用选用模块前，先阅读 [overlay-contract.md](references/overlay-contract.md)。仅在审查成熟度或跨轮次进度属于处理范围时，才阅读 [round-calibration.md](references/round-calibration.md)。

针对提供的评分规准、代码化检查报告或版本比较审查，使用 [review-checklist-and-cases.md](references/review-checklist-and-cases.md) 记录适用的检查与有证据支持的修复。这增加了可追溯性与实作案例，而非另一轮强制性的全篇论文检视。

<a id="select-modules-progressively"></a>
## 渐进式选取模块

从当前对话、标题、摘要、问题、方法、表格、图形、方程式与补充文件中推断候选模块。选取涵盖实际研究的最小模块集。在审查表头中指明选定的模块。

仅在可用证据使得两种实质不同的审查标准皆属合理时，方可提出一个具针对性的问题——例如，潜在变项模型是验证性还是探索性，或者使用者想要中立审查还是指定特定审稿人风格。当稿件本身已解决该选择时，切勿提问。

载入：

- 若涉及方程式、形式符号、衍生显示量、标准化或汇整规则、不确定性显示或跨产物符号一致性，载入 [display-notation-provenance.md](references/display-notation-provenance.md)
- 若涉及调查、量表、心理计量、因素分析、潜在变项、SEM、中介效应或多群组比较，载入 [quantitative-psychometrics-sem.md](references/quantitative-psychometrics-sem.md)
- 若涉及模拟、ABM、耦合计算模型、机器学习、生成式 AI、大型语言模型、合成受试者或代理人评估，载入 [ai-llm-computational.md](references/ai-llm-computational.md)
- 若涉及水资源、人与自然耦合系统、水资源政策、架构、文献回顾、不确定性或equifinality，载入 [water-cnhs-uncertainty.md](references/water-cnhs-uncertainty.md)
- 若涉及洪水风险、巨灾模型、淹水、排水、水动力学、危害、暴露度、脆弱度或损失，载入 [flood-hydrodynamics-catastrophe.md](references/flood-hydrodynamics-catastrophe.md)
- 仅在使用者明确要求 Ethan 风格审查或确立该实验室审查情境时，载入 [ethan-style-overlay.md](references/ethan-style-overlay.md)
- 仅在确立确切具名项目后，且仅在伴随明确相关审稿人或实验室情境时，载入 [project-precedents.md](references/project-precedents.md)

针对真正的混合型研究，应载入多个模块。单凭引用、关键字或研究区域的提及，并不足以构成载入模块的依据。将模块内具名的方法、门槛值、引用与报告常规视为待评估的检核项目，而非认定稿件必须盲目遵循的假设。

<a id="support-new-domain-modules"></a>
## 支援新领域模块

将可重复使用的领域知识保留在直接参考文件中，而非扩充此路由文件。贡献的模块应包含：

1. 明确的触发与排除线索
2. 方法与证据检查
3. 主张处理范围与替代解释检查
4. 相关时的图形、表格、方程式与可重现性检查
5. 不含项目事实的术语注意事项
6. 至少一项路由或边界评估

将该模块加入路由清单与架构测试中。将教授、实验室、期刊与项目规则保留在单独的条件叠加层中。

<a id="run-the-review"></a>
## 执行审查

套用基础技能的四轮检视，接着使用选定的模块深化（而非重复）审查：

1. **研究定位与贡献：** 查核文献是否支持研究缺口、任务是否与方法相符，以及研究贡献是否超出证据范围。
2. **设计与方法：** 查核抽样或来源选取、测量、模型逻辑、估计目标、假设、不确定性、比较设计，以及适用时的可重现性。
3. **结果与主张处理范围：** 查核问题到结果的涵盖度、统计或计算证据、替代解释、机制，以及形式比较相对于描述性比较。
4. **讨论与综合：** 区分直接发现、文献支持的解读、看似合理的替代解释、意涵、研究限制与推测。
5. **图表展示与符号标记：** 查核图形、表格、方程式、说明文字、单位、符号、分图、内文与图表的一致性，以及衍生数量的来源出处。当展示与符号标记模块适用时，使用其符号总帐与出处追溯，而非孤立地检查各个产物。
6. **写作与交付：** 查核术语、重复、可观察到的陈腔滥调、流畅度、摘要、引用、随附文件、元数据，以及指定阶段的就绪状态。

针对每个重大问题，继承基础技能的处理范围、S0–S4 严重度、证据状态、问题状态、所需权限、受影响产物与阻碍阶段。若选用的审稿人叠加层使用 `MUST`、`SHOULD`、`QUERY` 或 `PREFERENCE`，请将这些标签与严重度分开处理。

<a id="protect-evidence-and-reviewer-boundaries"></a>
## 保护证据与审查者边界

切勿捏造机制、引用、事实、门槛值、分析、先前意见或审稿人偏好。要求解释 “why” 并不代表授权撰写缺乏分析或文献支持的因果叙事。

切勿从散文文字推断其为 AI 所撰写。仅报告可观察到的特征，例如模糊的主词、陈腔滥调的过渡词、空洞的强调词、重复的节奏、重复的综合归纳或缺乏支持的机制。

在缺乏先前指示与当前证据的情况下，切勿断言跨轮次问题已获解决。回复信或已解决的意见讨论串仅是作者主张的证据，并非当前产物已包含所要求变更的证据。除非经已确认的投稿处、报告准则、作者或审稿人要求明确规定，否则切勿将个人偏好列为阻碍项目。

<a id="output-format"></a>
## 产出格式

依据可用的产物与阶段调整备忘录。切勿针对不存在的章节捏造意见，亦勿以固定的意见数量为目标。

<a id="header"></a>
### 表头

```text
REVIEW PROFILE: [general scientific / named conditional overlay]
PAPER: [title]
MODE: [review only / authorized revision]
STAGE OR ROUND: [maturity label or supplied round]
MODULES: [selected references and why]
SOURCE BASIS: [current files, prior material, unavailable sources]
READINESS: [named next-stage readiness and primary bottleneck]
```

### 跨轮次状态

仅在有先前证据时纳入。将问题分类为：已解决（resolved）、部分解决（partial）、未解决（open）、倒退（regressed）、免除（waived）、新增（new）或无法核实（not verifiable）。

<a id="priority-ranked-action-items"></a>
### 按优先顺序排列的行动项目

针对每个重大问题，提供其位置、分类、严重度与证据状态、具体问题、具体处理行动或决定、受影响产物，以及是否会阻碍所指明的下一阶段。

<a id="section-linked-comments"></a>
### 连结章节的意见

遵循稿件实际的读者功能与结构。将意见锚定在简短的文字片段上。区分效度、报告品质、领域常规、发表规定、审稿人偏好以及局部文字修饰。

<a id="writing-and-presentation-flags"></a>
### 写作与陈述标记

列入具代表性的个案与修改方向。除非获得授权，否则切勿重写。

<a id="next-step-instruction"></a>
### 下一步指示

说明在下一次审查之前，必须解决哪些问题、决定、来源与产物。

<a id="functional-completeness-retrospective"></a>
### 功能完整性回顾

使用基础回顾。指明生命周期阶段、已载入模块、选取证据、未解决的歧义、前一轮证据、涵盖产物、变更传播、已执行的检查以及就绪界限。

<a id="safety-and-restraint"></a>
## 安全与克制

保持直接、技术精确且尊重。切勿假冒特定具名审稿人、表达沮丧或使用羞辱性言词。绝不可因稿件处于后期轮次而隐瞒效度、伦理、证据或元数据问题。

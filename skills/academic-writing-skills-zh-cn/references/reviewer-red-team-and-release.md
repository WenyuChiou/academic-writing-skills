<a id="reviewer-red-team-and-release"></a>
# 审稿人红队审查与发布

<a id="contents"></a>
## 目录

1. 负空间审查
2. 问题分类
3. 发布关卡
4. 功能完备性报告

<a id="negative-space-review"></a>
## 负空间审查

搜寻稿件未能揭示之处：

- 没有实质回答的问题
- 没有结果的方法，或没有方法的结果
- 某个模型、组别、结果、时期或情境，缺少了其他同类对象皆有报告的栏位
- 仰赖论文中不存在的证据所做出的结论
- 仅从排版格式或旧有产出物推论出的事实
- 从未陈述的必要假设
- 可能因输入、抽样、前处理或测量瑕疵所导致的模式
- 将各自独立的显著性结果呈现为显著差异
- 缺少隐私、研究伦理、利益冲突、资料保存或可重现性信息
- 标题或贡献过于宽泛，而实际成果处理范围较窄

只要有三个或更多实体应对称报告时，就建立维度完整性矩阵。

针对每项主要主张，询问：

1. 有何直接证据支持此项？
2. 还有哪些看似合理但未排除的替代解释？
3. 有哪些目前无法取得的证据会改变结论？
4. 范围最窄且有充分依据的措辞为何？
5. 此措辞还必须同步传播至何处？

<a id="issue-classification"></a>
## 问题分类

为每个重大问题标记：

- 处理范围：表层、语意、章节、稿件、项目、有效性或认识论
- 严重程度：S0–S4
- 证据：已确认、可能或未核实
- 状态：未解决、已解决或豁免
- 所需权威或来源
- 受影响的产出物与检核关卡

切勿依文句修改的难易度来排序。请依对科学任务、推论、可重现性、研究伦理及投稿完整性所带来的风险进行排序。

<a id="release-gate"></a>
## 发布检核关卡

仅在符合下列条件时才允许 `SUBMISSION_READY`：

- S3 与 S4 等级的未解决阻碍为零
- 必要的来源与事实皆已核实，或已明确揭示其限制
- 已锁定的语意内容为最新状态
- 每个核心问题或目标皆具备方法、证据、答案与具推论界线的诠释
- 维度覆盖率完整或具合理理由
- 摘要与附属产出物与当前有效证据一致
- 确切档名与当前发布版本所属成员明确无误
- 最终文件皆通过结构与视觉检核
- 具备所投发表管道要求的各项声明与伦理声明
- 最终功能完整性回顾中没有未解决的 “no” 答案

若某个高严重程度的问题获得豁免，切勿将其转为通过。请报告此豁免、核准权威、原因以及残留风险。

<a id="functional-completeness-report"></a>
## 功能完整性报告

每次检核结束时皆应附上精简记录：

```text
FUNCTIONAL-COMPLETENESS RETROSPECTIVE
Scope covered: [artifacts and lifecycle stages]
Authority and locks: [passed / limits]
Alignment: [passed / affected links]
Adapters and overlays: [which ran / conflicts]
Change propagation: [artifacts rechecked]
Deterministic and visual checks: [performed / not applicable / limits]
Open issues and unknowns: [counts by severity]
Readiness: [not ready / conditionally ready / ready for named purpose]
```

若未指明已审查的维度与残留限制，切勿写入 `all functionality considered`。

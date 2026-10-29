<a id="reviewer-red-team-and-release"></a>
# 審稿人紅隊審查與發布

<a id="contents"></a>
## 目錄

1. 負空間審查
2. 問題分類
3. 發布關卡
4. 功能完備性報告

<a id="negative-space-review"></a>
## 負空間審查

搜尋稿件未能揭示之處：

- 沒有實質回答的問題
- 沒有結果的方法，或沒有方法的結果
- 某個模型、組別、結果、時期或情境，缺少了其他同類對象皆有報告的欄位
- 仰賴論文中不存在的證據所做出的結論
- 僅從排版格式或舊有產出物推論出的事實
- 從未陳述的必要假設
- 可能因輸入、抽樣、前處理或測量瑕疵所導致的模式
- 將各自獨立的顯著性結果呈現為顯著差異
- 缺少隱私、研究倫理、利益衝突、資料保存或可重現性資訊
- 標題或貢獻過於寬泛，而實際成果處理範圍較窄

只要有三個或更多實體應對稱報告時，就建立維度完整性矩陣。

針對每項主要主張，詢問：

1. 有何直接證據支持此項？
2. 還有哪些看似合理但未排除的替代解釋？
3. 有哪些目前無法取得的證據會改變結論？
4. 範圍最窄且有充分依據的措辭為何？
5. 此措辭還必須同步傳播至何處？

<a id="issue-classification"></a>
## 問題分類

為每個重大問題標記：

- 處理範圍：表層、語意、章節、稿件、專案、有效性或認識論
- 嚴重程度：S0–S4
- 證據：已確認、可能或未核實
- 狀態：未解決、已解決或豁免
- 所需權威或來源
- 受影響的產出物與檢核關卡

切勿依文句修改的難易度來排序。請依對科學任務、推論、可重現性、研究倫理及投稿完整性所帶來的風險進行排序。

<a id="release-gate"></a>
## 發布檢核關卡

僅在符合下列條件時才允許 `SUBMISSION_READY`：

- S3 與 S4 等級的未解決阻礙為零
- 必要的來源與事實皆已核實，或已明確揭示其限制
- 已鎖定的語意內容為最新狀態
- 每個核心問題或目標皆具備方法、證據、答案與具推論界線的詮釋
- 維度覆蓋率完整或具合理理由
- 摘要與附屬產出物與當前有效證據一致
- 確切檔名與當前發布版本所屬成員明確無誤
- 最終檔案皆通過結構與視覺檢核
- 具備所投發表管道要求的各項聲明與倫理聲明
- 最終功能完整性回顧中沒有未解決的 “no” 答案

若某個高嚴重程度的問題獲得豁免，切勿將其轉為通過。請報告此豁免、核准權威、原因以及殘留風險。

<a id="functional-completeness-report"></a>
## 功能完整性報告

每次檢核結束時皆應附上精簡記錄：

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

若未指明已審查的維度與殘留限制，切勿寫入 `all functionality considered`。

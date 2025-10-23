# 產品需求文件 (PRD)
## 東南亞金融海外新聞智能搜尋與報告系統

**版本**: 1.0  
**最後更新**: 2025年  
**產品負責人**: PM  
**開發團隊**: BMAD 跨職能團隊

---

## 一、產品概述

### 1.1 產品願景
打造一個專業的 Vertical AI 系統，自動化執行東南亞金融海外新聞的搜尋、彙整與分發流程，為金融分析師和決策者提供高效的資訊服務。

### 1.2 產品定位
- **類型**: End-to-End 自動化工作流系統
- **目標用戶**: 金融分析師、投資顧問、決策主管
- **核心價值**: 將分散的新聞資訊自動彙整成專業報告並主動推送

### 1.3 核心功能
1. ChatGPT Web Search（使用 mini-deep-research 模型）
2. 資訊結構化與報告生成（附資料來源）
3. PDF 報告自動生成
4. Email 自動寄送（基於 MCP Email）

---

## 二、技術架構

### 2.1 技術棧
- **框架**: Agno (Multi-Agent System Runtime)
- **語言**: Python 3.11+
- **套件管理**: UV
- **前端**: Streamlit / Flask (簡潔單頁應用)
- **部署**: Docker + 雲端服務 (AWS/GCP/Azure)

### 2.2 系統架構圖
```
[用戶輸入] 
    ↓
[Web 前端介面]
    ↓
[Agno Agent System]
    ├── Research Agent (ChatGPT mini-deep-research)
    ├── Analyst Agent (資訊結構化)
    ├── Report Generator Agent (PDF 生成)
    └── Email Agent (MCP Email)
    ↓
[用戶信箱]
```

### 2.3 Agent 設計 (基於 Agno)

#### Agent 1: Research Agent
- **職責**: 執行深度網路搜尋
- **模型**: ChatGPT mini-deep-research
- **輸入**: 用戶搜尋 prompt
- **輸出**: 結構化搜尋結果與來源

#### Agent 2: Analyst Agent
- **職責**: 將搜尋結果整理成報告格式
- **功能**: 
  - 去除冗餘資訊
  - 附加資料來源（超連結）
  - 繁體中文輸出
- **輸出**: Markdown 格式報告

#### Agent 3: Report Generator Agent
- **職責**: 將 Markdown 轉換為 PDF
- **工具**: ReportLab / WeasyPrint
- **輸出**: PDF 檔案

#### Agent 4: Email Agent
- **職責**: 透過 MCP Email 寄送報告
- **功能**: 附件發送、郵件模板
- **輸出**: 郵件發送狀態

---

## 三、功能需求

### 3.1 使用者介面 (Web Frontend)

#### 頁面元素
1. **搜尋輸入框**: 
   - 提示文字: "請輸入您想搜尋的東南亞金融新聞主題..."
   - 多行輸入支援
   - 字數限制: 500 字

2. **收件人信箱輸入框**:
   - 格式驗證
   - 支援多個收件人（逗號分隔）

3. **執行按鈕**:
   - 文字: "開始搜尋並寄送報告"
   - 顯示處理進度條

4. **狀態顯示區**:
   - 即時顯示各 Agent 執行狀態
   - 完成後顯示成功訊息

### 3.2 工作流程

#### 步驟 1: Web Search
```
輸入: 用戶 prompt
處理: ChatGPT mini-deep-research 進行深度搜尋
輸出: 搜尋結果 JSON
```

#### 步驟 2: 資訊結構化
```
輸入: 搜尋結果 JSON
處理: 
  - 提取關鍵資訊
  - 分類整理（依時間/主題/來源）
  - 添加資料來源超連結
  - 生成繁體中文報告
輸出: Markdown 報告
```

#### 步驟 3: PDF 生成
```
輸入: Markdown 報告
處理: 
  - 套用專業模板
  - 添加頁碼、目錄、頁首頁尾
  - 中文字體支援
輸出: PDF 檔案
```

#### 步驟 4: Email 寄送
```
輸入: PDF 檔案 + 收件人信箱
處理: 
  - 使用 MCP Email 服務
  - 附加 PDF
  - 專業郵件模板
輸出: 發送成功通知
```

---

## 四、BMAD 團隊分工

### 4.1 Business (業務需求)
- **負責人**: Product Owner
- **職責**:
  - 定義產品願景
  - 蒐集用戶需求
  - 優先級排序
  - ROI 分析

### 4.2 Marketing (市場推廣)
- **負責人**: Marketing Lead
- **職責**:
  - 目標用戶分析
  - 產品定位
  - 推廣策略
  - 使用者反饋蒐集

### 4.3 Analytics (數據分析)
- **負責人**: Data Analyst
- **職責**:
  - 使用行為追蹤
  - 性能監控
  - A/B 測試
  - 改進建議

### 4.4 Development (技術開發)
- **負責人**: Tech Lead
- **職責**:
  - 系統架構設計
  - Agent 開發
  - API 整合
  - 部署維護

**協作模式**: 每週 Sprint 會議，雙週 Demo，持續改進

---

## 五、非功能需求

### 5.1 性能需求
- 單次搜尋處理時間: < 2 分鐘
- PDF 生成時間: < 10 秒
- 郵件發送時間: < 5 秒
- 系統可用性: 99%

### 5.2 安全需求
- API Key 加密儲存 (.env)
- HTTPS 加密傳輸
- 郵件內容隱私保護
- 日誌脫敏處理

### 5.3 擴展性需求
- 支援水平擴展
- Docker 容器化部署
- 支援多用戶並發
- 可配置搜尋模型

### 5.4 可維護性需求
- 清晰的程式碼註解
- 完整的測試覆蓋
- 詳細的部署文件
- 監控與告警機制

---

## 六、部署方案

### 6.1 本地開發環境
```bash
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

### 6.2 雲端部署選項

#### 選項 A: Docker + AWS ECS
- 優點: 彈性擴展、按需付費
- 成本: 約 $50-100/月

#### 選項 B: Google Cloud Run
- 優點: 自動擴展、serverless
- 成本: 約 $30-80/月

#### 選項 C: Azure Container Instances
- 優點: 快速部署、簡單管理
- 成本: 約 $40-90/月

**建議**: 初期使用 Google Cloud Run，後期根據流量評估

---

## 七、開發里程碑

### Phase 1: MVP (Week 1-2)
- [ ] 環境設置與 Agno 框架整合
- [ ] Research Agent 開發
- [ ] 基礎 Web 介面

### Phase 2: 核心功能 (Week 3-4)
- [ ] Analyst Agent 開發
- [ ] Report Generator Agent 開發
- [ ] Email Agent (MCP) 整合

### Phase 3: 優化與測試 (Week 5)
- [ ] 端到端測試
- [ ] 性能優化
- [ ] 錯誤處理完善

### Phase 4: 部署上線 (Week 6)
- [ ] Docker 容器化
- [ ] 雲端部署
- [ ] 監控配置
- [ ] 文檔完善

---

## 八、風險與應對

### 8.1 技術風險
| 風險 | 影響 | 應對策略 |
|------|------|---------|
| ChatGPT API 限流 | 高 | 實施重試機制、使用 rate limiter |
| PDF 中文字體問題 | 中 | 預先測試並打包字體檔 |
| Email 發送失敗 | 中 | 實施郵件佇列與重試機制 |
| Agno 學習曲線 | 低 | 參考官方文檔與範例 |

### 8.2 業務風險
| 風險 | 影響 | 應對策略 |
|------|------|---------|
| 用戶需求變更 | 中 | 採用敏捷開發，快速迭代 |
| 競品出現 | 低 | 專注於金融垂直領域深度 |

---

## 九、成功指標 (KPI)

### 9.1 產品指標
- 每日活躍用戶數 (DAU): 目標 50+
- 報告生成成功率: > 95%
- 用戶滿意度: > 4.0/5.0

### 9.2 技術指標
- API 錯誤率: < 1%
- 平均響應時間: < 2 分鐘
- 系統正常運行時間: > 99%

---

## 十、附錄

### 10.1 參考資源
- Agno 官方文檔: https://docs.agno.com
- MCP Protocol: https://modelcontextprotocol.io
- ChatGPT API: https://platform.openai.com

### 10.2 專案結構預覽
```
NewSeaNews/
├── agents/           # Agno Agents
├── frontend/         # Web 介面
├── utils/            # 工具函數
├── tests/            # 測試
├── docs/             # 文檔
├── .env              # 環境變數
├── Dockerfile        # Docker 配置
├── requirements.txt  # 依賴
└── main.py          # 入口
```

---

**文件狀態**: ✅ 已完成  
**下一步**: 開始技術實作

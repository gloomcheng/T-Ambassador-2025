# T大使 AR 集點遊戲系統專案

這是一個專為「T大使」活動設計的 AR（擴增實境）集點遊戲系統，協助玩家透過掃描不同廠商的 AR 標記來回答問題、收集點數，並完成旅程挑戰。

## 專案特色

- **🎮 AR 掃描遊戲**：支援多個關卡，涵蓋眾多參與廠商
- **📊 用戶進度追蹤**：記錄每位玩家的遊戲歷程和答題結果
- **🗺️ 多路線設計**：支援不同探索路線，提供豐富遊戲體驗
- **🤖 AI 技術整合**：運用 LangChain 和 LLM 模型進行智慧問答
- **📱 響應式設計**：支援各種螢幕尺寸，手機、平板皆可遊玩
- **🔗 WebAR 整合**：與 MindAR WebAR 技術整合，提供沉浸式體驗

## 專案架構

```text
T-Ambassador-2025/
├── exhibition/           # 主要展覽應用系統
│   ├── backend/         # Django 後端服務
│   │   ├── mysite/     # Django 專案設定
│   │   ├── trips/      # 主要應用程式（遊戲邏輯、API、模板）
│   │   ├── media/      # 媒體檔案（圖片、AR標記、3D模型）
│   │   ├── scripts/    # 工具腳本
│   │   └── README.md   # 後端詳細說明文件
│   └── frontend/       # 前端 HTML 頁面
│       ├── index.html  # 遊戲首頁
│       ├── ar_scan*.html # AR掃描頁面
│       ├── route*.html # 路線選擇頁面
│       └── user_profile.html # 用戶資料頁面
└── langchain/          # AI 語言模型整合
    └── main.py         # 使用 LangChain 和 Ollama 的問答系統範例
```

## 系統組成部分

### 🎯 Exhibition 系統

**主要功能**：提供完整的 AR 集點遊戲體驗

#### Backend (Django)

- **技術棧**：Django 5.0, Django REST Framework
- **資料庫**：SQLite（開發環境）
- **功能特色**：
  - 用戶管理系統（手機號碼註冊、性別記錄）
  - 遊戲進度追蹤（答題記錄、各關卡狀態）
  - 題目管理系統（支援多廠商、多題型）
  - RESTful API 服務
  - AR 掃描整合（支援 29 個關卡）

#### Frontend (HTML/CSS/JavaScript)

- **技術棧**：純 HTML5, CSS3, JavaScript
- **功能特色**：
  - 響應式網頁設計
  - AR 掃描介面
  - 路線導覽系統
  - 用戶個人資料頁面

### 🤖 LangChain AI 系統

**主要功能**：提供智慧問答和文件分析能力

- **技術棧**：LangChain, Ollama, PDF處理
- **功能特色**：
  - PDF 文件載入和解析
  - 向量資料庫建立（支援文件檢索）
  - 基於 LLM 的智慧問答系統
  - 支援多種嵌入模型和語言模型

## 快速開始

### 環境需求

- **Python 3.11+**
- **Node.js** (若需前端開發)
- **Ollama** (用於 AI 功能)
- **uv** (Python 包管理工具，推薦)

### 安裝步驟

1. **複製專案**

   ```bash
   git clone <repository-url>
   cd T-Ambassador-2025
   ```

2. **安裝後端依賴**

   ```bash
   cd exhibition/backend
   # 使用 uv（推薦）
   uv venv
   source .venv/bin/activate  # Linux/Mac
   # .venv\Scripts\activate    # Windows
   uv pip install -r requirements.txt
   ```

3. **設定資料庫**

   ```bash
   cd exhibition/backend
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. **啟動後端服務**

   ```bash
   cd exhibition/backend
   python manage.py runserver
   ```

5. **啟動前端服務**

   ```bash
   # 在 exhibition/frontend 目錄下開啟 HTML 文件
   # 或使用本地伺服器
   python -m http.server 8001
   ```

6. **測試 AI 功能** (可選)

   ```bash
   cd langchain
   python main.py
   ```

## 遊戲玩法

1. **用戶註冊**：輸入手機號碼和性別完成註冊
2. **路線選擇**：選擇喜歡的探索路線（A、B、C路線）
3. **AR掃描**：掃描廠商 AR 標記開始遊戲
4. **答題挑戰**：回答與廠商相關的問題
5. **點數收集**：成功答題獲得點數
6. **進度追蹤**：系統記錄個人遊戲歷程

## 支援廠商

系統支援眾多在地社區和企業，包括：

- 農特產品生產合作社
- 社區發展協會
- 文化傳承組織
- 休閒農業區發展協會

## 技術規格

### 後端技術

- **框架**：Django 5.0
- **API**：Django REST Framework
- **資料庫**：SQLite（開發）/ PostgreSQL（生產）
- **認證**：JWT Token 認證
- **檔案處理**：Django 的媒體檔案處理

### 前端技術

- **語言**：HTML5, CSS3, JavaScript (ES6+)
- **設計**：響應式網頁設計
- **相容性**：支援現代瀏覽器

### AI 技術

- **語言模型**：Ollama (Gemma, Llama 等)
- **嵌入模型**：Nomic Embed Text
- **向量資料庫**：Chroma
- **文件處理**：PyPDFLoader

## 開發與部署

### 開發環境設定

請參閱各模組的詳細說明文件：

- [後端開發指南](exhibition/backend/README.md)
- [前端開發指南](exhibition/frontend/README.md) (開發中)

### 部署建議

- **後端**：使用 Gunicorn + Nginx 部署
- **前端**：靜態檔案託管服務 (CDN)
- **資料庫**：PostgreSQL 資料庫服務
- **媒體檔案**：雲端儲存服務 (AWS S3, Cloudinary)

## 授權與貢獻

本專案為「T大使」活動專用。如需修改或擴充功能，請遵循以下步驟：

1. Fork 本專案
2. 建立功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交變更 (`git commit -m 'Add amazing feature'`)
4. 推送至分支 (`git push origin feature/amazing-feature`)
5. 建立 Pull Request

## 聯絡資訊

如有問題或建議，請透過以下方式聯繫：

- **GitHub Issues**：回報技術問題
- **電子郵件**：專案維護團隊
- **開發團隊**：現場技術支援

## 更新日誌

- **v1.0.0** (2025-01)：初始版本發布
  - 完整的 AR 集點遊戲系統
  - 支援 29 個遊戲關卡
  - AI 智慧問答系統整合
  - 多廠商題庫系統

---

*本專案致力於推廣地方文化與產業發展，透過科技與遊戲化體驗，讓參與者深入認識各地特色產業。*

# T大使 2025 AR 集點遊戲系統 - 後端服務

這是一個基於 Django 開發的 AR（擴增實境）集點遊戲系統後端服務，為「T大使 2025」活動設計。提供 RESTful API 支援前端應用，管理用戶資料、遊戲進度、題目內容和 AR 掃描功能。

## 系統特色

- **AR 掃描遊戲**：支援 29 個關卡，涵蓋多個參與廠商
- **用戶進度追蹤**：記錄每位玩家的遊戲歷程和答題結果
- **多路線設計**：支援 A、B、C 三條不同探索路線
- **WebAR 整合**：與 MindAR WebAR 技術整合，提供沉浸式體驗
- **響應式設計**：支援各種螢幕尺寸，手機、平板皆可遊玩

## 安裝與設定

### 環境需求

- Python 3.11+
- Django 5.0+
- uv（推薦）、pipenv 或虛擬環境工具

### 安裝步驟

1. **複製專案**

   ```bash
   git clone <repository-url>
   cd tdance2024
   ```

2. **設定虛擬環境**

   ```bash
   # 使用 uv（推薦）- 現代化且快速的 Python 包管理器
   # 安裝 uv（如果尚未安裝）
   curl -LsSf https://astral.sh/uv/install.sh | sh
   # 或使用 pip 安裝
   pip install uv

   # 使用 uv 建立虛擬環境並安裝依賴（會自動產生 uv.lock）
   uv venv
   source .venv/bin/activate  # Linux/Mac
   # .venv\Scripts\activate    # Windows
   uv pip install django djangorestframework markdown django-filter django-cors-headers
   ```

3. **安裝依賴套件**

   ```bash
   # 使用 uv（推薦）- 會自動產生 uv.lock 檔案並管理所有依賴
   uv pip install django djangorestframework markdown django-filter django-cors-headers
   ```

4. **資料庫設定**

   ```bash
   python manage.py migrate
   ```

5. **建立管理員帳號**

   ```bash
   python manage.py createsuperuser
   ```

6. **執行開發伺服器**

   ```bash
   python manage.py runserver
   ```

## 程式架構

以下是後端服務的目錄結構說明。所有路徑均相對於專案根目錄 `/exhibition/backend/`。

```text
backend/
├── benjamin/              # Python 虛擬環境目錄（開發環境）
│   ├── pyvenv.cfg        # 虛擬環境設定檔案
│   └── Scripts/          # Windows 執行腳本（若適用）
├── mysite/                # Django 專案設定目錄
│   ├── __init__.py       # Python 套件初始化檔案
│   ├── __pycache__/      # Python 快取檔案目錄
│   ├── settings.py       # 專案設定檔案（資料庫、應用、靜態檔案等）
│   ├── urls.py          # 主要路由設定檔案
│   ├── asgi.py          # ASGI 設定檔案（支援異步應用）
│   └── wsgi.py          # WSGI 設定檔案（Web 伺服器閘道介面）
├── trips/                 # 主要 Django 應用程式
│   ├── __init__.py       # Python 套件初始化檔案
│   ├── __pycache__/      # Python 快取檔案目錄
│   ├── admin.py         # Django 管理後台設定
│   ├── apps.py          # Django 應用設定
│   ├── forms.py         # Django 表單定義
│   ├── models.py        # 資料庫模型定義（Question、UserProfile、Post）
│   ├── serializers.py   # DRF API 序列化器
│   ├── views.py         # API 視圖和業務邏輯
│   ├── urls.py          # 應用程式路由設定
│   ├── tests.py         # 測試檔案
│   ├── templates/       # HTML 模板檔案目錄
│   │   └── [42 files]   # 各種頁面模板（首頁、AR掃描、路線選擇等）
│   ├── mind/            # MindAR AR 識別檔案目錄
│   │   └── [29 files]   # 各關卡的 .mind AR 標記檔案
│   ├── img/             # 圖片資源目錄
│   │   └── [32 files]   # 遊戲圖標和介面圖片
│   └── migrations/      # 資料庫遷移檔案目錄
│       └── [19 files]   # Django 自動產生的遷移檔案
├── media/                 # 用戶上傳和媒體檔案目錄
│   ├── AR掃描/          # AR 掃描相關檔案
│   │   ├── targets.mind # AR 目標識別檔案
│   │   └── uploads_files_2426738_tex.gltf # 3D 模型檔案
│   ├── questions/        # 題目相關圖片目錄
│   │   └── [32 files]   # 各廠商題目圖片檔案
│   └── vendor_icons/     # 廠商圖標目錄
│       └── [53 files]   # 各廠商代表圖標和遊戲介面圖片
├── scripts/               # 工具腳本目錄
│   └── diagnostics.py    # 系統診斷和測試腳本
├── QUESTION_MANAGEMENT_GUIDE.md # 題目管理指南文件
├── README.md             # 本說明文件
├── pyproject.toml        # uv 專案設定和依賴管理檔案
├── uv.lock              # uv 依賴鎖定檔案（自動產生）
├── db.sqlite3            # SQLite 資料庫檔案
└── manage.py            # Django 管理指令檔案（啟動伺服器、遷移等）
```

### 主要目錄說明

#### **benjamin/** - Python 虛擬環境

開發環境專用的虛擬環境目錄，包含 Python 執行環境和相關腳本。

#### **mysite/** - Django 專案設定

Django 專案的核心設定目錄：

- **settings.py**：專案設定，包括資料庫連線、安裝應用、中介軟體等
- **urls.py**：全域路由設定，將 URL 路徑對應到視圖函數
- **wsgi.py / asgi.py**：Web 伺服器閘道介面設定檔案

#### **trips/** - 主要應用程式

遊戲的核心業務邏輯應用：

- **models.py**：資料庫模型定義，包含 Question（題目）、UserProfile（用戶）、Post（進度）等
- **views.py**：API 視圖，處理 HTTP 請求和業務邏輯
- **serializers.py**：Django REST Framework 序列化器，將模型轉換為 JSON 格式
- **templates/**：HTML 模板檔案，提供前端頁面展示
- **mind/**：存放 29 個關卡的 MindAR AR 識別檔案（.mind 格式）
- **migrations/**：Django 自動產生的資料庫遷移檔案

#### **media/** - 媒體檔案

用戶上傳和靜態資源檔案：

- **AR掃描/**：AR 掃描相關的目標檔案和 3D 模型
- **questions/**：各廠商題目的圖片檔案（32個檔案）
- **vendor_icons/**：廠商代表圖標和遊戲介面圖片（53個檔案）

#### **scripts/** - 工具腳本

系統維護和診斷工具：

- **diagnostics.py**：系統診斷腳本，用於檢查系統狀態和問題排查

### 資料庫模型說明

- **Question**：題目資料模型，儲存各關卡的題目內容、選項、正確答案和所屬廠商
- **UserProfile**：用戶資料模型，記錄玩家的手機號碼、性別和註冊時間
- **Post**：遊戲進度模型，追蹤用戶在各關卡的答題狀況和完成狀態

## 開發與部署

### 開發環境設定

1. **啟用虛擬環境**

   ```bash
   # 使用 uv
   source .venv/bin/activate  # Linux/Mac
   # .venv\Scripts\activate    # Windows
   ```

2. **啟動開發伺服器**

   ```bash
   python manage.py runserver
   ```

   伺服器將運行在 `http://127.0.0.1:8000/`

3. **存取管理後台**
   訪問 `http://127.0.0.1:8000/admin/` 來管理問題和用戶資料

### Git 版本控制流程

1. **查看變更狀態**

   ```bash
   git status
   ```

2. **加入檔案到暫存區**

   ```bash
   git add [檔案名稱]
   # 或加入所有變更
   git add .
   ```

3. **建立提交點**

   ```bash
   git commit -m "簡要描述此次變更"
   ```

4. **推送至遠端倉庫**

   ```bash
   git push origin [分支名稱]
   ```

5. **同步最新變更**

   ```bash
   git pull origin [分支名稱]
   ```

## API 文件

本系統提供 RESTful API 來支援前端應用程式的資料交換。

### 認證與 CORS

- API 支援跨來源資源共享（CORS）
- 允許來自 `http://localhost:5500` 和 `http://127.0.0.1:8000` 的請求

### 使用者管理 API

#### 建立使用者

建立新的遊戲帳號，需提供手機號碼和性別資訊。

**端點**: `POST /api/user/`

**請求範例**:

```bash
curl -X POST http://127.0.0.1:8000/api/user/ \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "0912345678",
    "gender": "M"
  }'
```

#### 取得使用者資料與進度

查詢使用者的基本資料和遊戲進度。

**端點**: `GET /api/user/`

**參數**:

- `phone` (必填): 使用者手機號碼，10 碼數字
- `level` (選填): 指定關卡號碼（1-29）

**範例**:

```bash
# 取得所有進度
curl "http://127.0.0.1:8000/api/user/?phone=0912345678"

# 取得特定關卡進度
curl "http://127.0.0.1:8000/api/user/?phone=0912345678&level=1"
```

**回傳範例**:

```json
{
    "phone": "0912345678",
    "gender": "M",
    "post": {
        "content": {
            "1": {
                "status": "pass",
                "user_answer": "A",
                "correct_answer": "A"
            }
        },
        "updated_at": "2024-10-01T10:30:00Z"
    }
}
```

### 遊戲進度 API

#### 更新過關記錄

更新指定關卡的答題結果和狀態。

**端點**: `PATCH /api/post/{phone}/`

**請求範例**:

```bash
curl -X PATCH http://127.0.0.1:8000/api/post/0912345678/ \
  -H "Content-Type: application/json" \
  -d '{
    "level": "1",
    "status": "pass",
    "user_answer": "A",
    "correct_answer": "A"
  }'
```

#### 取得題目資料

取得指定關卡的題目內容。

**端點**: `GET /api/question/{question_id}/`

**範例**:

```bash
curl http://127.0.0.1:8000/api/question/1/
```

### 狀態碼說明

- `200 OK`: 請求成功
- `201 Created`: 資源建立成功
- `400 Bad Request`: 請求參數錯誤
- `404 Not Found`: 資源不存在

## AR 掃描功能

系統整合 MindAR WebAR 技術，提供 AR 掃描體驗。每個關卡都對應一個獨特的 AR 標記檔案（`.mind` 格式）。

### AR 標記檔案結構

- 位於 `trips/mind/` 目錄下
- 每個關卡對應一個 `.mind` 檔案
- 支援離線掃描和線上驗證

### 前端頁面

系統提供多個 HTML 模板：

- **首頁** (`index.html`): 遊戲入口
- **路線選擇** (`route1.html` - `route6.html`): 不同探索路線
- **用戶資料** (`user_profile.html`): 玩家資訊頁面
- **AR掃描頁面** (`arScan1.html` - `arScan29.html`): 各關卡掃描介面

## 參與廠商與題目

系統支援多個參與廠商，每個廠商對應不同的題目和 AR 體驗。題目資料包含：

- 廠商名稱與圖標
- 題目內容與選項
- 正確答案設定
- 梯次與路線歸屬

## 常見問題與故障排除

### 資料庫問題

如果遇到資料庫遷移錯誤或資料不一致問題：

1. **備份現有資料**（若有重要資料）

   ```bash
   cp db.sqlite3 db.sqlite3.backup
   ```

2. **重置資料庫**

   ```bash
   rm db.sqlite3
   python manage.py migrate
   python manage.py createsuperuser  # 重新建立管理員帳號
   ```

### 媒體檔案問題

如果圖片無法正常顯示：

1. 確認 `media` 目錄存在且包含必要檔案
2. 檢查 `settings.py` 中的 `MEDIA_URL` 和 `MEDIA_ROOT` 設定
3. 確認開發伺服器正確提供靜態檔案服務

### AR 掃描問題

如果 AR 掃描功能無法正常運作：

1. 確認 `.mind` 檔案存在於正確位置
2. 檢查瀏覽器是否支援 WebAR 功能
3. 確認網路連線穩定（線上驗證需要網路）

### 最高管理者帳號問題

忘記管理員密碼時：

```bash
python manage.py createsuperuser
```

### 依賴套件問題

如果遇到套件衝突或版本問題：

```bash
   # 使用 uv 清除並重新安裝依賴（推薦）
   rm -rf .venv uv.lock
   uv venv
   source .venv/bin/activate
   uv pip install django djangorestframework markdown django-filter django-cors-headers

# 或更新特定套件
uv pip install --upgrade [package-name]

# 或重新同步所有依賴
uv lock --refresh
```

## 技術規格

- **後端框架**: Django 5.0
- **API 框架**: Django REST Framework
- **資料庫**: SQLite (開發環境)
- **前端技術**: HTML5, CSS3, JavaScript
- **AR 技術**: MindAR WebAR
- **支援平台**: 現代瀏覽器（Chrome, Safari, Edge）

## 授權與貢獻

本專案為「T大使 2024」活動專用。如需修改或擴充功能，請遵循以下步驟：

1. Fork 本專案
2. 建立功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交變更 (`git commit -m 'Add amazing feature'`)
4. 推送至分支 (`git push origin feature/amazing-feature`)
5. 建立 Pull Request

## 聯絡資訊

如有問題或建議，請透過 GitHub Issues 系統回報，或直接聯繫開發團隊。

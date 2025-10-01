# T大使 2024 AR 集點遊戲系統

這是一個基於 Django 開發的 AR（擴增實境）集點遊戲系統，為「T大使 2024」活動設計。玩家透過掃描不同廠商的 AR 標記來回答問題、收集點數，並完成旅程挑戰。

## 系統特色

- **AR 掃描遊戲**：支援 29 個關卡，涵蓋多個參與廠商
- **用戶進度追蹤**：記錄每位玩家的遊戲歷程和答題結果
- **多路線設計**：支援 A、B、C 三條不同探索路線
- **WebAR 整合**：與 Vuforia WebAR 技術整合，提供沉浸式體驗
- **響應式設計**：支援各種螢幕尺寸，手機、平板皆可遊玩

## 安裝與設定

### 環境需求

- Python 3.11+
- Django 5.0+
- pipenv（推薦）或虛擬環境工具

### 安裝步驟

1. **複製專案**

   ```bash
   git clone <repository-url>
   cd tdance2024
   ```

2. **設定虛擬環境**

   ```bash
   # 使用 pipenv（推薦）
   pipenv install

   # 或使用 venv
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # venv\Scripts\activate   # Windows
   pip install -r requirements.txt
   ```

3. **安裝依賴套件**

   ```bash
   pipenv install
   # 或
   pip install django djangorestframework markdown django-filter django-cors-headers
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

```text
tdance2024/
├── mysite/                 # Django 專案設定
│   ├── settings.py         # 專案設定
│   ├── urls.py            # 主要路由
│   └── wsgi.py            # WSGI 設定
├── trips/                  # 主要應用程式
│   ├── models.py          # 資料模型（問題、用戶、進度）
│   ├── views.py           # API 視圖
│   ├── serializers.py     # API 序列化器
│   ├── urls.py            # 應用路由
│   ├── templates/         # HTML 模板
│   │   ├── arScan1.html   # AR 掃描頁面（1-29關）
│   │   ├── index.html      # 首頁
│   │   ├── route1.html     # 路線選擇
│   │   └── user_profile.html # 用戶資料
│   ├── mind/              # Vuforia AR 識別檔案
│   └── migrations/        # 資料庫遷移檔案
├── media/                 # 媒體檔案
│   ├── vendor_icons/      # 廠商圖標
│   ├── questions/         # 題目圖片
│   └── AR掃描/           # AR 目標檔案
├── db.sqlite3             # SQLite 資料庫
└── manage.py             # Django 管理指令
```

### 主要功能模組

- **Question（問題模型）**：儲存各關卡的題目、選項和答案
- **UserProfile（用戶資料）**：記錄玩家手機號碼和性別
- **Post（遊戲進度）**：追蹤用戶在各關卡的答題狀況

## 開發與部署

### 開發環境設定

1. **啟用虛擬環境**

   ```bash
   pipenv shell
   # 或
   source venv/bin/activate
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

系統整合 Vuforia WebAR 技術，提供 AR 掃描體驗。每個關卡都對應一個獨特的 AR 標記檔案（`.mind` 格式）。

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
# 清除並重新安裝依賴
pipenv --rm
pipenv install --dev

# 或更新特定套件
pipenv update [package-name]
```

## 技術規格

- **後端框架**: Django 5.0
- **API 框架**: Django REST Framework
- **資料庫**: SQLite (開發環境)
- **前端技術**: HTML5, CSS3, JavaScript
- **AR 技術**: Vuforia WebAR
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

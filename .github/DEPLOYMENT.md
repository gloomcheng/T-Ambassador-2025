# 🚀 自動化部署設定指南

本專案使用 GitHub Actions 實現 CI/CD 自動部署到生產伺服器。

## 📋 前置需求

1. GitHub Repository
2. 生產伺服器的 SSH 訪問權限
3. 伺服器上已安裝並配置好 Python、Django、Apache

## 🔐 設定 GitHub Secrets

在 GitHub Repository 中設定以下 Secrets：

### 1. 進入 Repository Settings
```
Repository → Settings → Secrets and variables → Actions → New repository secret
```

### 2. 新增以下 Secrets

| Secret Name | 說明 | 範例值 |
|------------|------|--------|
| `SSH_PRIVATE_KEY` | SSH 私鑰 | `-----BEGIN OPENSSH PRIVATE KEY-----\n...` |
| `SSH_HOST` | 伺服器主機名 | `tdance.fansee.studio` |
| `SSH_USER` | SSH 使用者名稱 | `ubuntu` 或 `root` |
| `SSH_PATH` | 伺服器專案路徑 | `/var/www/sites/T-Ambassador-2025` |

## 🔑 產生 SSH 金鑰

如果伺服器尚未設定 SSH 金鑰，請執行以下步驟：

### 在本地生成 SSH 金鑰
```bash
ssh-keygen -t ed25519 -C "github-actions-deploy" -f ~/.ssh/tdance_deploy
```

### 將公鑰加入伺服器
```bash
ssh-copy-id -i ~/.ssh/tdance_deploy.pub user@tdance.fansee.studio
```

或手動加入：
```bash
cat ~/.ssh/tdance_deploy.pub
# 複製輸出，然後在伺服器上執行：
echo "複製的公鑰內容" >> ~/.ssh/authorized_keys
```

### 獲取私鑰內容
```bash
cat ~/.ssh/tdance_deploy
```

將輸出的完整內容（包括 `-----BEGIN` 和 `-----END` 行）複製到 GitHub Secret `SSH_PRIVATE_KEY`。

## 🚀 自動部署流程

### 觸發條件
- **自動觸發**：推送到 `main` 分支時
- **手動觸發**：在 GitHub Actions 頁面手動執行

### 部署步驟
1. ✅ Checkout 代碼
2. 🔐 設定 SSH 連線
3. 📤 使用 rsync 同步文件到伺服器
4. 🔧 執行 Django 管理命令
   - `collectstatic` - 收集靜態文件
   - `migrate` - 執行資料庫遷移
5. 🔄 重啟 Apache 服務

### 排除的文件/目錄
- `.git/`
- `.github/`
- `__pycache__/`
- `*.pyc`
- `.DS_Store`
- `node_modules/`
- `.cortex/`
- `*.log`
- `db.sqlite3`

## 📊 檢查部署狀態

### 在 GitHub 上查看
```
Repository → Actions → 查看最新的 workflow run
```

### 手動驗證部署
```bash
# SSH 到伺服器
ssh user@tdance.fansee.studio

# 檢查文件是否更新
cd /var/www/sites/T-Ambassador-2025/exhibition/backend
ls -la

# 檢查服務狀態
sudo systemctl status apache2

# 查看日誌
sudo tail -f /var/log/apache2/error.log
```

## 🔧 手動觸發部署

1. 進入 Repository 的 Actions 頁面
2. 點擊 "Deploy to Production Server" workflow
3. 點擊 "Run workflow"
4. 選擇 `main` 分支
5. 點擊 "Run workflow" 按鈕

## ⚠️ 注意事項

1. **首次部署**：確保伺服器上的目錄結構正確
2. **資料庫**：生產環境的 `db.sqlite3` 不會被覆蓋
3. **環境變數**：確保伺服器上的 `.env` 或環境變數已正確設定
4. **權限**：確保 SSH 用戶有足夠的權限執行部署操作
5. **備份**：建議在部署前備份資料庫和重要文件

## 🐛 常見問題

### 部署失敗
1. 檢查 GitHub Secrets 是否正確設定
2. 檢查 SSH 金鑰是否有效
3. 檢查伺服器空間是否充足
4. 查看 GitHub Actions 日誌詳細錯誤訊息

### 服務未重啟
```bash
# SSH 到伺服器手動重啟
sudo systemctl restart apache2
```

### 靜態文件未更新
```bash
# SSH 到伺服器手動收集靜態文件
cd /var/www/sites/T-Ambassador-2025/exhibition/backend
python3 manage.py collectstatic --noinput
```

## 📞 聯絡資訊

如有問題，請聯絡系統管理員。


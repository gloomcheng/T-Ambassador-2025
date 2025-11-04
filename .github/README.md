# 🚀 CI/CD 自動部署系統

本專案使用 GitHub Actions 實現自動化部署到生產伺服器。

## ⚡ 快速開始

### 選項 1：使用自動化腳本（推薦）

```bash
# 執行設定腳本
./.github/setup-deploy.sh
```

腳本會自動：
1. ✅ 產生 SSH 金鑰
2. ✅ 測試 SSH 連線
3. ✅ 顯示需要設定的 GitHub Secrets

### 選項 2：手動設定

請參考詳細文檔：[DEPLOYMENT.md](./DEPLOYMENT.md)

## 📋 需要設定的 GitHub Secrets

| Secret | 說明 |
|--------|------|
| `SSH_PRIVATE_KEY` | SSH 私鑰（完整內容） |
| `SSH_HOST` | 伺服器地址（例如：tdance.fansee.studio） |
| `SSH_USER` | SSH 使用者（例如：ubuntu） |
| `SSH_PATH` | 專案路徑（例如：/var/www/sites/T-Ambassador-2025） |

## 🔄 部署流程

```mermaid
graph LR
    A[Push to main] --> B[GitHub Actions]
    B --> C[Rsync 文件]
    C --> D[執行 migrate]
    D --> E[收集靜態文件]
    E --> F[重啟 Apache]
    F --> G[部署完成 ✅]
```

## 🎯 使用方式

### 自動部署
```bash
git add .
git commit -m "feat: 新功能"
git push origin main
# ✨ 自動觸發部署！
```

### 手動觸發
1. 前往 GitHub Repository
2. 點擊 **Actions** 標籤
3. 選擇 **Deploy to Production Server**
4. 點擊 **Run workflow**

## 📊 檢查部署狀態

### 在 GitHub 上查看
- **Actions** 頁面：即時查看部署進度
- **綠色勾勾** ✅：部署成功
- **紅色叉叉** ❌：部署失敗（點擊查看詳細日誌）

### 在伺服器上驗證
```bash
# SSH 登入伺服器
ssh user@tdance.fansee.studio

# 查看最新部署時間
ls -la /var/www/sites/T-Ambassador-2025/exhibition/

# 查看服務狀態
sudo systemctl status apache2
```

## 🔧 常用命令

### 查看部署日誌
```bash
# 在伺服器上
sudo tail -f /var/log/apache2/error.log
```

### 手動重啟服務
```bash
# 在伺服器上
sudo systemctl restart apache2
```

### 手動執行 Django 命令
```bash
# 在伺服器上
cd /var/www/sites/T-Ambassador-2025/exhibition/backend
python3 manage.py collectstatic --noinput
python3 manage.py migrate
```

## 📁 部署內容

部署時會同步以下目錄：
- ✅ `exhibition/` - 主要專案代碼
- ✅ `lukui/` - AR 互動模組
- ✅ Python 代碼、HTML、CSS、JS
- ✅ 靜態資源和媒體文件

自動排除：
- ❌ `.git/` - Git 版本控制
- ❌ `__pycache__/` - Python 快取
- ❌ `node_modules/` - Node.js 套件
- ❌ `*.log` - 日誌文件
- ❌ `db.sqlite3` - 本地資料庫

## ⚠️ 重要注意事項

1. **首次部署**
   - 確保伺服器上已安裝所有依賴
   - 設定環境變數和資料庫

2. **資料庫遷移**
   - 自動執行 `migrate`
   - 如有錯誤請手動檢查

3. **靜態文件**
   - 自動執行 `collectstatic`
   - 確認 Apache 配置正確

4. **權限問題**
   - SSH 用戶需要有足夠權限
   - Apache 重啟可能需要 sudo 權限

## 🐛 故障排除

### 問題：部署失敗
**解決方案：**
1. 檢查 GitHub Actions 日誌
2. 確認 Secrets 設定正確
3. 測試 SSH 連線：`ssh -i ~/.ssh/tdance_deploy user@host`

### 問題：靜態文件未更新
**解決方案：**
```bash
# 手動收集靜態文件
python3 manage.py collectstatic --noinput --clear
```

### 問題：Apache 未重啟
**解決方案：**
```bash
# 手動重啟
sudo systemctl restart apache2

# 檢查狀態
sudo systemctl status apache2
```

## 📚 相關文檔

- [詳細部署指南](./DEPLOYMENT.md)
- [GitHub Actions 文檔](https://docs.github.com/actions)
- [Django 部署最佳實踐](https://docs.djangoproject.com/en/stable/howto/deployment/)

## 🎉 成功案例

部署成功後，您可以在以下 URL 訪問網站：
- 🌐 https://tdance.fansee.studio
- 🌐 https://tdance.fansee.studio/lukui/
- 🌐 https://tdance.fansee.studio/lukui/ar/

---

**需要幫助？** 請查看 [DEPLOYMENT.md](./DEPLOYMENT.md) 或聯絡系統管理員。


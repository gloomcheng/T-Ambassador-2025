#!/bin/bash

# 🚀 T-Ambassador-2025 自動部署設定腳本
# 此腳本協助設定 GitHub Actions 所需的 SSH 金鑰和 Secrets

set -e

echo "🚀 T-Ambassador-2025 部署設定工具"
echo "===================================="
echo ""

# 檢查是否已有 SSH 金鑰
SSH_KEY_PATH="$HOME/.ssh/tdance_deploy"

if [ -f "$SSH_KEY_PATH" ]; then
    echo "⚠️  發現現有的 SSH 金鑰: $SSH_KEY_PATH"
    read -p "是否要使用現有金鑰？(y/n): " use_existing
    if [ "$use_existing" != "y" ]; then
        echo "❌ 已取消"
        exit 1
    fi
else
    echo "📝 產生新的 SSH 金鑰..."
    ssh-keygen -t ed25519 -C "github-actions-deploy-tdance" -f "$SSH_KEY_PATH" -N ""
    echo "✅ SSH 金鑰已產生"
fi

echo ""
echo "===================================="
echo "📋 設定步驟："
echo "===================================="
echo ""

# 1. 公鑰
echo "1️⃣  將以下公鑰加入到伺服器的 ~/.ssh/authorized_keys："
echo ""
echo "---BEGIN PUBLIC KEY---"
cat "${SSH_KEY_PATH}.pub"
echo "---END PUBLIC KEY---"
echo ""

read -p "請輸入伺服器位址 (例如: tdance.fansee.studio): " SSH_HOST
read -p "請輸入伺服器使用者名稱 (例如: ubuntu): " SSH_USER

echo ""
echo "執行以下命令將公鑰複製到伺服器："
echo ""
echo "ssh-copy-id -i ${SSH_KEY_PATH}.pub ${SSH_USER}@${SSH_HOST}"
echo ""
read -p "按 Enter 繼續，或 Ctrl+C 取消..."

# 2. 測試 SSH 連線
echo ""
echo "2️⃣  測試 SSH 連線..."
if ssh -i "$SSH_KEY_PATH" -o BatchMode=yes -o ConnectTimeout=5 "${SSH_USER}@${SSH_HOST}" "echo '✅ SSH 連線成功'" 2>/dev/null; then
    echo "✅ SSH 連線測試成功"
else
    echo "❌ SSH 連線失敗，請確認："
    echo "   - 伺服器位址正確"
    echo "   - 使用者名稱正確"
    echo "   - 公鑰已正確加入伺服器"
    echo ""
    echo "手動測試命令："
    echo "ssh -i ${SSH_KEY_PATH} ${SSH_USER}@${SSH_HOST}"
    exit 1
fi

# 3. 顯示需要設定的 GitHub Secrets
echo ""
echo "===================================="
echo "3️⃣  請在 GitHub Repository 設定以下 Secrets："
echo "===================================="
echo ""
echo "Repository → Settings → Secrets and variables → Actions → New repository secret"
echo ""

echo "📌 SSH_PRIVATE_KEY (私鑰):"
echo "---BEGIN PRIVATE KEY---"
cat "$SSH_KEY_PATH"
echo "---END PRIVATE KEY---"
echo ""

echo "📌 SSH_HOST:"
echo "$SSH_HOST"
echo ""

echo "📌 SSH_USER:"
echo "$SSH_USER"
echo ""

read -p "請輸入伺服器專案路徑 (例如: /var/www/sites/T-Ambassador-2025): " SSH_PATH
echo "📌 SSH_PATH:"
echo "$SSH_PATH"
echo ""

# 4. 產生設定摘要
echo "===================================="
echo "📝 設定摘要："
echo "===================================="
echo "SSH_HOST: $SSH_HOST"
echo "SSH_USER: $SSH_USER"
echo "SSH_PATH: $SSH_PATH"
echo "SSH Key:  $SSH_KEY_PATH"
echo ""

# 5. 建立設定檔案 (不提交到 Git)
CONFIG_FILE=".github/.deploy-config.local"
cat > "$CONFIG_FILE" << EOF
# 本地部署設定 (不會提交到 Git)
SSH_HOST=$SSH_HOST
SSH_USER=$SSH_USER
SSH_PATH=$SSH_PATH
SSH_KEY=$SSH_KEY_PATH
EOF

echo "✅ 設定已儲存到 $CONFIG_FILE"
echo ""

# 6. 最終提示
echo "===================================="
echo "🎉 設定完成！"
echo "===================================="
echo ""
echo "下一步："
echo "1. 將上述 4 個 Secrets 加入到 GitHub Repository"
echo "2. 推送代碼到 main 分支"
echo "3. 檢查 GitHub Actions 是否自動執行部署"
echo ""
echo "手動測試部署命令："
echo "git push origin main"
echo ""
echo "查看部署狀態："
echo "https://github.com/YOUR_USERNAME/T-Ambassador-2025/actions"
echo ""


FROM node:18-alpine

# 進到容器內的工作目錄
WORKDIR /app

# 只複製 rag-ai-assistant
COPY rag-ai-assistant ./rag-ai-assistant

# 切到子專案
WORKDIR /app/rag-ai-assistant

# 安裝正式依賴
RUN npm ci --only=production

# Render 需要有對外 port
EXPOSE 3000

# 啟動（package.json 裡的 start）
CMD ["npm", "start"]

FROM node:20-alpine

WORKDIR /app

COPY rag-ai-assistant ./rag-ai-assistant
WORKDIR /app/rag-ai-assistant

RUN npm ci --omit=dev

EXPOSE 10000

CMD ["node", "api/index.js"]

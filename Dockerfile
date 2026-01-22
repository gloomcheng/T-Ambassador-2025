cat > Dockerfile << 'EOF'
FROM node:18-alpine

WORKDIR /app/rag-ai-assistant

COPY rag-ai-assistant ./rag-ai-assistant

RUN npm ci --only=production

EXPOSE 3000

CMD ["npm", "start"]
EOF

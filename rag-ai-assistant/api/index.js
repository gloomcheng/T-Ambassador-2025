import express from "express";
import crypto from "crypto";
import config from "../config/index.js";
import { Client } from "@line/bot-sdk";

// RAG related
import ragSystem from "../services/rag.js";
import { askWithRAG } from "../services/ragAnswer.js";

// ⭐ 啟動時初始化 RAG（載文件、建 embeddings）
await ragSystem.initialize();

const app = express();

// 讓我們可以拿到 rawBody 做 LINE signature 驗證
app.use(
  express.json({
    verify: (req, res, buf) => {
      req.rawBody = buf.toString();
    },
  })
);

// =======================
// LINE Signature 驗證
// =======================
function validateLineSignature(req, res, next) {
  try {
    const signature = req.headers["x-line-signature"];
    if (!signature) {
      console.error("❌ Missing x-line-signature header");
      return res.sendStatus(403);
    }

    const secret = config.LINE_CHANNEL_SECRET;
    if (!secret) {
      console.error("❌ LINE_CHANNEL_SECRET is missing in config/env");
      return res.sendStatus(500);
    }

    const hash = crypto
      .createHmac("SHA256", secret)
      .update(req.rawBody)
      .digest("base64");

    if (hash !== signature) {
      console.error("❌ Invalid LINE signature");
      console.error("Expected:", hash);
      console.error("Got:", signature);
      return res.sendStatus(403);
    }

    next();
  } catch (err) {
    console.error("❌ Signature validation error:", err);
    return res.sendStatus(500);
  }
}

// =======================
// LINE Client
// =======================
const client = new Client({
  channelAccessToken: config.LINE_CHANNEL_ACCESS_TOKEN,
});

// 健康檢查
app.get("/", (req, res) => res.status(200).send("OK"));

// =======================
// LINE Webhook
// =======================
app.post(
  config.APP_WEBHOOK_PATH || "/webhook",
  validateLineSignature,
  async (req, res) => {
    // ⭐ 一定要先回 200（LINE 規則）
    res.sendStatus(200);

    try {
      console.log("====================================");
      console.log("✅ LINE webhook received");
      console.log("Node:", process.version);
      console.log("Path:", req.originalUrl);
      console.log("Body:", JSON.stringify(req.body, null, 2));

      const events = req.body.events || [];

      for (const event of events) {
        console.log("---- event ----");
        console.log(JSON.stringify(event, null, 2));

        // 只處理文字訊息
        if (event.type === "message" && event.message?.type === "text") {
          const userText = event.message.text;

          // ⭐ 核心：用 RAG 產生回答
          const aiReply = await askWithRAG(userText);

          await client.replyMessage(event.replyToken, {
            type: "text",
            text: aiReply.slice(0, 5000), // LINE 字數限制
          });

          console.log("✅ replyMessage sent (RAG)");
        } else {
          console.log("ℹ️ Not a text message event, skipped");
        }
      }
    } catch (err) {
      console.error("❌ Webhook handler error:", err);
    }
  }
);

// =======================
// Server 啟動
// =======================
const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log("Server is running on port", port);
});

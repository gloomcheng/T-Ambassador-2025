import express from "express";
import crypto from "crypto";
import config from "../config/index.js";
import { Client } from "@line/bot-sdk";

const app = express();

// 讓我們可以拿到 rawBody 做 LINE signature 驗證
app.use(
  express.json({
    verify: (req, res, buf) => {
      req.rawBody = buf.toString();
    },
  })
);

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

const client = new Client({
  channelAccessToken: config.LINE_CHANNEL_ACCESS_TOKEN,
});

app.get("/", (req, res) => res.status(200).send("OK"));

app.post(
  config.APP_WEBHOOK_PATH || "/webhook",
  validateLineSignature,
  async (req, res) => {
    // ⭐ 先回 200，避免 LINE 因為你 reply 慢就重送
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

        if (event.type === "message" && event.message?.type === "text") {
          const userText = event.message.text;

          await client.replyMessage(event.replyToken, {
            type: "text",
            text: `✅ Webhook 已成功連線\n你剛剛說的是：${userText}`,
          });

          console.log("✅ replyMessage sent");
        } else {
          console.log("ℹ️ Not a text message event, skipped");
        }
      }
    } catch (err) {
      console.error("❌ Webhook handler error:", err);
    }
  }
);

const port = process.env.PORT || 10000;
app.listen(port, () => console.log("Server is running on port", port));

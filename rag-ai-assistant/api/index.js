import express from "express";
import crypto from "crypto";
import config from "../config/index.js";
import { Client } from "@line/bot-sdk";

const app = express();

app.use(
  express.json({
    verify: (req, res, buf) => {
      req.rawBody = buf.toString();
    },
  })
);

function validateLineSignature(req, res, next) {
  const signature = req.headers["x-line-signature"];
  if (!signature) return res.sendStatus(403);

  const hash = crypto
    .createHmac("SHA256", config.LINE_CHANNEL_SECRET)
    .update(req.rawBody)
    .digest("base64");

  if (hash !== signature) return res.sendStatus(403);
  next();
}

const client = new Client({
  channelAccessToken: config.LINE_CHANNEL_ACCESS_TOKEN,
});

app.get("/", (req, res) => res.status(200).send("OK"));

app.post(
  config.APP_WEBHOOK_PATH || "/webhook",
  validateLineSignature,
  async (req, res) => {
    try {
      const events = req.body.events || [];

      for (const event of events) {
        if (event.type === "message" && event.message.type === "text") {
          await client.replyMessage(event.replyToken, {
            type: "text",
            text: "✅ Webhook 已成功連線",
          });
        }
      }

      return res.sendStatus(200);
    } catch (err) {
      console.error("Webhook error:", err);
      return res.sendStatus(500);
    }
  }
);

const port = process.env.PORT || 3000;
app.listen(port, () => console.log("Server is running on port", port));

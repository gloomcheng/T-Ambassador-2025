import express from 'express';
import { messagingApi } from '@line/bot-sdk';
import config from '../config/index.js';
import { validateLineSignature } from '../middleware/index.js';

const app = express();

/* LINE client（一定要在最外層） */
const client = new messagingApi.MessagingApiClient({
  channelAccessToken: config.LINE_CHANNEL_ACCESS_TOKEN,
});

app.use(
  express.json({
    verify: (req, res, buf) => {
      req.rawBody = buf.toString();
    },
  })
);

/* health check */
app.get('/', (req, res) => {
  res.status(200).send({ status: 'OK' });
});

/* webhook */
app.post(
  config.APP_WEBHOOK_PATH || '/webhook',
  async (req, res) => {
    const events = req.body.events || [];

    for (const event of events) {
      if (event.type === 'message' && event.message.type === 'text') {
        await client.replyMessage({
          replyToken: event.replyToken,
          messages: [
            {
              type: 'text',
              text: '✅ Webhook 已成功連線',
            },
          ],
        });
      }
    }

    res.sendStatus(200);
  }
);

const port = process.env.PORT || config.APP_PORT || 3000;
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});

export default app;

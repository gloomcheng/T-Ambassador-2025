import express from 'express';
import { handleEvents, printPrompts } from '../app/index.js';
import config from '../config/index.js';
import { validateLineSignature } from '../middleware/index.js';
import ragSystem from '../services/rag.js';
import storage from '../storage/index.js';
import { fetchVersion, getVersion } from '../utils/index.js';

const app = express();

ragSystem.initialize();

app.use(express.json({
  verify: (req, res, buf) => {
    req.rawBody = buf.toString();
  },
}));

app.get('/', async (req, res) => {
  if (config.APP_URL) {
    res.redirect(config.APP_URL);
    return;
  }
  const currentVersion = getVersion();
  const latestVersion = await fetchVersion();
  res.status(200).send({ status: 'OK', currentVersion, latestVersion });
});

app.post(config.APP_WEBHOOK_PATH, validateLineSignature, async (req, res) => {
  try {
    const events = req.body.events;

    for (const event of events) {
      if (event.type === 'message' && event.message.type === 'text') {
        await handleEvents([
          {
            ...event,
            message: {
              ...event.message,
              text: '✅ 機器人已成功連線！'
            }
          }
        ]);
      }
    }

    res.sendStatus(200);
  } catch (err) {
    console.error(err);
    res.sendStatus(500);
  }
});


const port = process.env.PORT || config.APP_PORT || 3000;

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});

export default app;

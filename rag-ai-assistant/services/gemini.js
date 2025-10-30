import { GoogleGenerativeAI } from '@google/generative-ai';
import config from '../config/index.js';

export const ROLE_SYSTEM = 'system';
export const ROLE_AI = 'model';
export const ROLE_HUMAN = 'user';

export const FINISH_REASON_STOP = 'STOP';
export const FINISH_REASON_LENGTH = 'MAX_TOKENS';

let genAI = null;

const initializeGemini = () => {
  if (!genAI && config.GEMINI_API_KEY) {
    genAI = new GoogleGenerativeAI(config.GEMINI_API_KEY);
  }
  return genAI;
};

const convertMessagesToGeminiFormat = (messages) => {
  const history = [];
  let systemInstruction = '';

  messages.forEach((msg) => {
    if (msg.role === 'system') {
      systemInstruction = msg.content;
    } else {
      history.push({
        role: msg.role === 'assistant' ? 'model' : 'user',
        parts: [{ text: msg.content }],
      });
    }
  });

  return { history, systemInstruction };
};

export const createChatCompletion = async ({
  model = config.GEMINI_MODEL,
  messages,
  temperature = 1,
  maxTokens = 1024,
}) => {
  const ai = initializeGemini();
  if (!ai) {
    throw new Error('Gemini API key not configured');
  }

  const { history, systemInstruction } = convertMessagesToGeminiFormat(messages);

  const generativeModel = ai.getGenerativeModel({
    model,
    systemInstruction: systemInstruction || undefined,
  });

  const chat = generativeModel.startChat({
    history: history.slice(0, -1),
    generationConfig: {
      temperature,
      maxOutputTokens: maxTokens,
    },
  });

  const lastMessage = history[history.length - 1];
  const result = await chat.sendMessage(lastMessage.parts[0].text);
  const response = result.response;

  return {
    data: {
      choices: [
        {
          message: {
            role: 'assistant',
            content: response.text(),
          },
          finish_reason: response.candidates[0]?.finishReason === 'STOP' ? 'stop' : 'length',
        },
      ],
    },
  };
};

export const generateEmbedding = async (text) => {
  const ai = initializeGemini();
  if (!ai) {
    throw new Error('Gemini API key not configured');
  }

  const model = ai.getGenerativeModel({ model: config.GEMINI_EMBEDDING_MODEL });
  const result = await model.embedContent(text);
  return result.embedding.values;
};

export const generateEmbeddings = async (texts) => {
  const ai = initializeGemini();
  if (!ai) {
    throw new Error('Gemini API key not configured');
  }

  const model = ai.getGenerativeModel({ model: config.GEMINI_EMBEDDING_MODEL });

  const embeddings = await Promise.all(
    texts.map(async (text) => {
      const result = await model.embedContent(text);
      return result.embedding.values;
    }),
  );

  return embeddings;
};




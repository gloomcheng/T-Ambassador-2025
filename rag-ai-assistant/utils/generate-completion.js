import config from '../config/index.js';
import { MOCK_TEXT_OK } from '../constants/mock.js';
import { createChatCompletion as createOpenAIChatCompletion, FINISH_REASON_STOP as OPENAI_FINISH_REASON_STOP } from '../services/openai.js';
import { createChatCompletion as createGeminiChatCompletion, FINISH_REASON_STOP as GEMINI_FINISH_REASON_STOP } from '../services/gemini.js';

class Completion {
  text;

  finishReason;

  constructor({
    text,
    finishReason,
  }) {
    this.text = text;
    this.finishReason = finishReason;
  }

  get isFinishReasonStop() {
    return this.finishReason === OPENAI_FINISH_REASON_STOP
      || this.finishReason === GEMINI_FINISH_REASON_STOP
      || this.finishReason === 'stop';
  }
}

/**
 * @param {Object} param
 * @param {Prompt} param.prompt
 * @returns {Promise<Completion>}
 */
const generateCompletion = async ({
  prompt,
}) => {
  if (config.APP_ENV !== 'production') return new Completion({ text: MOCK_TEXT_OK });

  let data;
  let choice;

  if (config.GEMINI_API_KEY) {
    const response = await createGeminiChatCompletion({ messages: prompt.messages });
    data = response.data;
    [choice] = data.choices;
  } else {
    const response = await createOpenAIChatCompletion({ messages: prompt.messages });
    data = response.data;
    [choice] = data.choices;
  }

  return new Completion({
    text: choice.message.content.trim(),
    finishReason: choice.finish_reason,
  });
};

export default generateCompletion;

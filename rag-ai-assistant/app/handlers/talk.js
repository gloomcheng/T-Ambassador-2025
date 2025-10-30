import config from '../../config/index.js';
import { t } from '../../locales/index.js';
import { ROLE_AI, ROLE_HUMAN, runAssistant } from '../../services/openai.js';
import ragSystem from '../../services/rag.js';
import { generateCompletion } from '../../utils/index.js';
import { COMMAND_BOT_CONTINUE, COMMAND_BOT_FORGET, COMMAND_BOT_TALK } from '../commands/index.js';
import Context from '../context.js';
import { updateHistory } from '../history/index.js';
import { getPrompt, setPrompt } from '../prompt/index.js';

/**
 * @param {Context} context
 * @returns {boolean}
 */
const check = (context) => (
  context.hasCommand(COMMAND_BOT_TALK)
  || context.hasBotName
  || context.source.bot.isActivated
);

/**
 * @param {Context} context
 * @returns {Promise<Context>}
 */
const exec = (context) => check(context) && (
  async () => {
    const prompt = getPrompt(context.userId);
    try {
      let responseText = null;
      let isFromRAG = false;

      // Step 1: Try RAG if enabled
      if (context.event.isText && config.RAG_ENABLED && ragSystem.isInitialized) {
        const query = context.trimmedText;
        const ragResults = await ragSystem.search(query);

        if (ragResults.length > 0) {
          const topResult = ragResults[0];
          responseText = topResult.document.answer;
          isFromRAG = true;

          if (config.APP_DEBUG) {
            console.log(`RAG match found (similarity: ${topResult.similarity.toFixed(3)})`);
            console.log(`Q: ${topResult.document.question}`);
            console.log(`A: ${responseText}`);
          }
        }
      }

      // Step 2: If no RAG result, use AI provider
      if (!responseText) {
        // Use OpenAI Assistant API (Christine Bear's contribution)
        if (config.AI_PROVIDER === 'openai-assistant') {
          let userMessage = '';
          if (context.event.isText) {
            userMessage = context.trimmedText;
          }
          if (context.event.isImage) {
            userMessage = `(Image uploaded, description: "${context.trimmedText || 'none'}")`;
          }

          responseText = await runAssistant(userMessage);
          prompt.write(ROLE_HUMAN, `${t('__COMPLETION_DEFAULT_AI_TONE')(config.BOT_TONE)}${userMessage}`);
          prompt.write(ROLE_AI, responseText);
          prompt.patch(responseText);
          setPrompt(context.userId, prompt);
          updateHistory(context.id, (history) => history.write(config.BOT_NAME, responseText));
          context.pushText(responseText, [COMMAND_BOT_CONTINUE]);
        } else {
          // Use standard completion (OpenAI or Gemini)
          if (context.event.isText) {
            prompt.write(ROLE_HUMAN, `${t('__COMPLETION_DEFAULT_AI_TONE')(config.BOT_TONE)}${context.trimmedText}`).write(ROLE_AI);
          }
          if (context.event.isImage) {
            const { trimmedText } = context;
            prompt.writeImage(ROLE_HUMAN, trimmedText).write(ROLE_AI);
          }

          const { text, isFinishReasonStop } = await generateCompletion({ prompt });
          responseText = text;
          prompt.patch(text);
          setPrompt(context.userId, prompt);
          updateHistory(context.id, (history) => history.write(config.BOT_NAME, text));
          const actions = isFinishReasonStop ? [COMMAND_BOT_FORGET] : [COMMAND_BOT_CONTINUE];
          context.pushText(text, actions);
        }
      } else {
        // RAG result found
        updateHistory(context.id, (history) => history.write(config.BOT_NAME, responseText));
        context.pushText(responseText, [COMMAND_BOT_FORGET]);
      }
    } catch (err) {
      context.pushError(err);
    }
    return context;
  }
)();

export default exec;

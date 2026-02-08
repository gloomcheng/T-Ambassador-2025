import ragSystem from "./rag.js";
import { createChatCompletion } from "./gemini.js";

export async function askWithRAG(question) {
  // 1️⃣ 向量搜尋
  const results = await ragSystem.search(question);

  // =========================
  // 情況 A：有 RAG 資料
  // =========================
  if (results.length > 0) {
    const contextText = results
      .map(
        (r, i) =>
          `【資料 ${i + 1}】\nQ: ${r.document.question}\nA: ${r.document.answer}`
      )
      .join("\n\n");

    const completion = await createChatCompletion({
      messages: [
        {
          role: "system",
          content: `
你是一個嚴謹、專業的 AI 助理。
請「根據提供的資料」回答使用者問題，
並用自己的話組織答案，不要逐字照抄。
請使用繁體中文。
          `.trim(),
        },
        {
          role: "user",
          content: `
【參考資料】
${contextText}

【問題】
${question}
          `.trim(),
        },
      ],
      temperature: 0.3,
      maxTokens: 512,
    });

    return completion.data.choices[0].message.content;
  }

  // =========================
  // 情況 B：RAG 找不到資料 → fallback
  // =========================
  const completion = await createChatCompletion({
    messages: [
      {
        role: "system",
        content: `
你是一個親切、專業的 AI 助理，
請根據你的知識直接回答問題。
如果不確定，請誠實說明。
請使用繁體中文。
        `.trim(),
      },
      {
        role: "user",
        content: question,
      },
    ],
    temperature: 0.7,
    maxTokens: 512,
  });

  return completion.data.choices[0].message.content;
}

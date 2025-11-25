// src/services/letterService.ts

import OpenAI from "openai";

export type LetterInput = {
  recipientName?: string;
  recipientAddress?: string;
  subject?: string;
  keyPoints?: string[];   // main points to cover
  tone?: "formal" | "informal" | "neutral";
  language?: string;      // e.g., "English", "Hindi"
  senderName?: string;
};

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

/**
 * Generates the body of a letter based on input fields.
 * Returns only the body paragraphs (no header, addresses, or signature).
 */
export async function generateLetterBody(input: LetterInput): Promise<string> {
  const {
    recipientName = "",
    subject = "",
    keyPoints = [],
    tone = "formal",
    language = "English",
    senderName = "",
  } = input;

  const keyPointsText =
    keyPoints.length > 0
      ? keyPoints.map((p, i) => `${i + 1}. ${p}`).join("\n")
      : "N/A";

  const systemPrompt = `You are an assistant that drafts well-structured ${tone} letters in ${language}.
Return only the body paragraphs of the letter without salutations, addresses, subject lines, or signatures.
Write clear, concise paragraphs that cover all provided points.`;

  const userPrompt = `Draft the body of a letter.
Recipient: ${recipientName || "N/A"}
Subject: ${subject || "N/A"}
Sender: ${senderName || "N/A"}

Key points to cover:
${keyPointsText}

Constraints:
- Keep it ${tone}.
- Use ${language}.
- Return only the body paragraphs (no greeting/salutation line, no addresses, no closing/signature).`;

  const completion = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [
      { role: "system", content: systemPrompt },
      { role: "user", content: userPrompt },
    ],
    temperature: 0.4,
  });

  const result = completion.choices?.[0]?.message?.content?.trim() || "";
  return result;
}
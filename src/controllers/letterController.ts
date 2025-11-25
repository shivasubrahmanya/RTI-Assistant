// src/controllers/letterController.ts

// ... existing imports ...
import { generateLetterBody, type LetterInput } from "../services/letterService";

// ... existing code ...
export async function createLetter(req: any, res: any) {
  try {
    const input: LetterInput = {
      recipientName: req.body.recipientName,
      subject: req.body.subject,
      keyPoints: req.body.keyPoints, // array of strings
      tone: req.body.tone,           // "formal" | "informal" | "neutral"
      language: req.body.language,   // e.g., "English"
      senderName: req.body.senderName,
    };

    const body = await generateLetterBody(input);
    res.status(200).json({ body });
  } catch (err: any) {
    // ... existing error handling ...
    res.status(500).json({ error: err?.message || "Failed to generate letter body" });
  }
}
// ... existing code ...
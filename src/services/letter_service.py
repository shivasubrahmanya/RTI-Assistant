# src/services/letter_service.py

import os
from typing import List, Optional, TypedDict
from openai import OpenAI

class LetterInput(TypedDict, total=False):
    recipientName: Optional[str]
    recipientAddress: Optional[str]
    subject: Optional[str]
    keyPoints: Optional[List[str]]
    tone: Optional[str]       # "formal" | "informal" | "neutral"
    language: Optional[str]   # e.g., "English", "Hindi"
    senderName: Optional[str]

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_letter_body(input: LetterInput) -> str:
    recipient_name = input.get("recipientName", "") or ""
    subject = input.get("subject", "") or ""
    key_points = input.get("keyPoints", []) or []
    tone = input.get("tone", "formal") or "formal"
    language = input.get("language", "English") or "English"
    sender_name = input.get("senderName", "") or ""

    key_points_text = "\n".join([f"{i+1}. {p}" for i, p in enumerate(key_points)]) if key_points else "N/A"

    system_prompt = (
        f"You are an assistant that drafts well-structured {tone} letters in {language}.\n"
        "Return only the body paragraphs of the letter without salutations, addresses, subject lines, or signatures.\n"
        "Write clear, concise paragraphs that cover all provided points."
    )

    user_prompt = (
        "Draft the body of a letter.\n"
        f"Recipient: {recipient_name or 'N/A'}\n"
        f"Subject: {subject or 'N/A'}\n"
        f"Sender: {sender_name or 'N/A'}\n\n"
        "Key points to cover:\n"
        f"{key_points_text}\n\n"
        "Constraints:\n"
        f"- Keep it {tone}.\n"
        f"- Use {language}.\n"
        "- Return only the body paragraphs (no greeting/salutation line, no addresses, no closing/signature)."
    )

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.4,
    )

    result = completion.choices[0].message.content.strip() if completion.choices else ""
    return result
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = (
    "You are Zeklo, a powerful, intelligent, and friendly AI assistant. "
    "Give clear, helpful, and honest responses."
)

def ask_ai(prompt: str) -> str:
    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return res.choices[0].message.content
    except Exception:
        return "⚠️ Zeklo is busy right now. Please try again."

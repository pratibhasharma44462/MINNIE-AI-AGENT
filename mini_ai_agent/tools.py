from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found! Check your .env file.")

client = Groq(api_key=api_key)

SYSTEM_PROMPT = """
You are MINNIE, a smart and helpful AI agent made by Pratibha.

Response format — always follow this structure:
- Give a 2-3 line intro paragraph that directly answers or explains the topic
- Then use a clear heading if needed
- Follow with bullet points or numbered steps for details
- Use **bold** for important terms or key points
- Use code blocks with ``` for any code
- Keep responses concise, warm and scannable
- Never write long walls of text
- Never start directly with bullet points — always lead with a short paragraph first
- End with a helpful follow-up line if relevant (e.g. "Let me know if you want me to go deeper!")

Your capabilities:
- Answer any question clearly and directly
- Solve any math problem step by step
- Write and explain code in any language
- Convert units, dates, currencies
- Summarize, explain, translate anything

Your personality:
- Smart, warm and friendly like a knowledgeable friend
- Confident but never arrogant
- Uses simple language, avoids unnecessary jargon
- Never makes up facts
- Thinks step by step for complex problems
"""

def generate_response(history: list) -> str:
    try:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        for msg in history:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=2048,  # ✅ increased so responses aren't cut off
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Groq error: {e}")
        return f"❌ Something went wrong: {str(e)}"
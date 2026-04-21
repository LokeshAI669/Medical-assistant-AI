from groq import Groq
from app.core.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)

def get_ai_response(message: str):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # ✅ FIXED MODEL
            messages=[
                {"role": "system", "content": "You are a helpful medical assistant."},
                {"role": "user", "content": message}
            ],
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ ERROR: {str(e)}"
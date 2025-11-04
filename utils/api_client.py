import os
import google.generativeai as genai

class ChatbotClient:
    def __init__(self, model: str, api_key: str | None = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key missing. Set GEMINI_API_KEY or pass api_key.")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model)

    def send_message(self, prompt: str) -> dict:
        response = self.model.generate_content(prompt)
        text = getattr(response, "text", "") or ""
        # Some SDK builds expose usage via usage_metadata; guard if absent
        tokens_used = getattr(getattr(response, "usage_metadata", None), "total_token_count", 0) or 0
        return {"response": text, "tokens_used": int(tokens_used), "confidence": 0.0}

    # alias used by tests
    def send_prompt(self, prompt: str) -> dict:
        return self.send_message(prompt)

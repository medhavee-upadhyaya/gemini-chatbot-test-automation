import google.generativeai as genai
import yaml

class ChatbotClient:
    """Handles communication with Gemini API."""

    def __init__(self, config_path="config/config.yaml", model_name=None):
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        self.api_key = config.get("gemini_api_key")
        genai.configure(api_key=self.api_key)

        # Use model from argument or fallback to config file
        self.model_name = model_name or config.get("model", "gemini-pro")
        self.model = genai.GenerativeModel(self.model_name)

    def send_message(self, prompt):
        """Send a prompt to Gemini and return text response."""
        response = self.model.generate_content(prompt)
        return response.text.strip() if response and response.text else ""

    # 👇 Add this alias for test compatibility
    def send_prompt(self, prompt):
        """Alias for send_message for backward compatibility."""
        return self.send_message(prompt)

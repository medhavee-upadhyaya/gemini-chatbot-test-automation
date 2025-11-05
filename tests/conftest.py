import pytest, yaml
from utils.api_client import ChatbotClient

@pytest.fixture(scope="session")
def config():
    """Load YAML config once per session."""
    with open("config.yaml") as f:
        return yaml.safe_load(f)

@pytest.fixture(scope="session")
def client(config):
    """Create a Gemini chatbot client."""
    return ChatbotClient(model=config["model"], api_key=config["gemini_api_key"])

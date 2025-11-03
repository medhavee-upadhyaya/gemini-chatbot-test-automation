import json
import pytest
import yaml
from jsonschema import validate

from utils.api_client import ChatbotClient
from utils.logger import log_interaction

@pytest.fixture(scope="session")
def config():
    """Load YAML config once per test session."""
    with open("config/config.yaml") as f:
        return yaml.safe_load(f)

@pytest.fixture(scope="session")
def schema():
    """Load expected response schema."""
    with open("schemas/response_schema.json") as f:
        return json.load(f)

@pytest.fixture(scope="session")
def client(config):
    """Create chatbot client (Gemini model from config)."""
    return ChatbotClient(model_name=config["model"])

@pytest.mark.parametrize("prompt_key", ["prompts"])
def test_chatbot_schema_and_non_empty_response(client, config, schema, prompt_key):
    """
    For each configured prompt:
    - Call Gemini
    - Validate response matches schema
    - Ensure response is meaningful (not empty)
    - Log the interaction as an artifact
    """
    for prompt in config[prompt_key]:
        resp = client.send_prompt(prompt)

        # Log for debugging + evidence
        log_interaction(prompt, resp)

        # Validate contract
        validate(instance=resp, schema=schema)

        # Basic sanity
        assert resp["response"] != "", f"Empty response for prompt: {prompt}"
        assert len(resp["response"]) > 3, "Response too short / not useful"

def test_math_consistency(client, config):
    """
    Ask a deterministic math question twice.
    We expect consistent answers for stable prompts like math.
    (LLMs can be stochastic, but simple math should stay stable.)
    """
    prompt = config["math_prompt"]

    r1 = client.send_prompt(prompt)
    r2 = client.send_prompt(prompt)

    log_interaction(prompt, {"run1": r1, "run2": r2})

    # Soft consistency check: answer should include '30'
    # (5 * 6 = 30). You can tighten this later.
    assert "30" in r1["response"], f"Expected '30' in first answer, got: {r1['response']}"
    assert "30" in r2["response"], f"Expected '30' in second answer, got: {r2['response']}"

    # Hard consistency: responses are identical
    assert r1["response"].strip() == r2["response"].strip(), "Inconsistent responses for same math question"

import os, json, pytest, yaml
from jsonschema import validate
from utils.api_client import ChatbotClient

# Always read the config at project root
@pytest.fixture(scope="session")
def config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

@pytest.fixture(scope="session")
def client(config):
    return ChatbotClient(model=config["model"], api_key=config["gemini_api_key"])

@pytest.fixture(scope="session")
def schema():
    # If you prefer to keep a JSON schema file, load it here; else inline.
    schema_path = "schemas/response_schema.json"
    if os.path.exists(schema_path):
        with open(schema_path) as f:
            return json.load(f)
    return {
        "type": "object",
        "properties": {
            "response": {"type": "string"},
            "tokens_used": {"type": "integer"},
            "confidence": {"type": "number"}
        },
        "required": ["response"]
    }

@pytest.mark.parametrize("prompt_key", ["prompts"])
def test_chatbot_schema_and_non_empty_response(client, config, schema, prompt_key):
    for prompt in config[prompt_key]:
        resp = client.send_prompt(prompt)
        validate(instance=resp, schema=schema)
        assert resp["response"].strip(), f"Empty response for prompt: {prompt}"

def test_math_consistency(client, config):
    prompt = config["math_prompt"]
    r1 = client.send_prompt(prompt)
    r2 = client.send_prompt(prompt)
    # LLMs can vary; for basic math we expect equality—if it flakes, relax to `in`/numeric parse.
    assert r1["response"] == r2["response"], f"Inconsistent math answers: {r1['response']} vs {r2['response']}"

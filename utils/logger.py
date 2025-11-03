import os
import json
from datetime import datetime

def log_interaction(prompt: str, response_obj: dict):
    """
    Saves each chatbot interaction to reports/logs/<timestamp>.json
    This gives you auditable artifacts for debugging / compliance.
    """
    os.makedirs("reports/logs", exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    log_path = f"reports/logs/{ts}.json"

    payload = {
        "prompt": prompt,
        "response": response_obj
    }

    with open(log_path, "w") as f:
        json.dump(payload, f, indent=2)

    # also helpful when you run pytest -s
    print(f"[LOG] saved -> {log_path}")

import time
import os
import json
import csv
from statistics import mean
import pytest


def test_context_retention(client):
    """
    🧠 Test: Context Retention
    Verifies whether Gemini retains context across multiple conversation turns.
    """

    os.makedirs("reports", exist_ok=True)
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    csv_path = f"reports/context_retention_{timestamp}.csv"
    json_path = f"reports/context_retention_{timestamp}.json"

    # Simulated conversation
    conversation = [
        "My name is Medhavee. Remember it.",
        "What is my name?",
        "Now pretend you are a teacher. What would you call me in class?",
        "Without using my name, describe what I just asked you to remember.",
        "What’s 3 + 5?"
    ]

    responses = []

    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Turn", "Prompt", "Response"])
        context = []

        for i, prompt in enumerate(conversation):
            context.append(prompt)
            combined_prompt = "\n".join(context)
            resp = client.send_prompt(combined_prompt)
            text = resp["response"].strip()
            writer.writerow([i + 1, prompt, text])
            responses.append({"turn": i + 1, "prompt": prompt, "response": text})
            print(f"\nTurn {i+1} — Prompt: {prompt}\nResponse: {text}\n")

    # ✅ Evaluate context consistency
    remembers_name = any("Medhavee" in r["response"] for r in responses)
    logic_ok = any("teacher" in r["response"].lower() or "class" in r["response"].lower() for r in responses)
    unrelated_ok = any("8" in r["response"] for r in responses[-1:])

    with open(json_path, "w") as jf:
        json.dump({"responses": responses, "remembers_name": remembers_name, "logic_ok": logic_ok}, jf, indent=2)

    print("\n🧠 Context Retention Summary")
    print(f"✅ Remembered Name: {remembers_name}")
    print(f"✅ Logical Follow-up: {logic_ok}")
    print(f"✅ Math Independent: {unrelated_ok}")
    print(f"📊 CSV saved: {csv_path}")
    print(f"📁 JSON saved: {json_path}")

    assert remembers_name, "Model failed to recall user name from earlier turn"
    assert logic_ok, "Model failed to stay logically consistent"
    assert unrelated_ok, "Model confused previous context with new unrelated question"

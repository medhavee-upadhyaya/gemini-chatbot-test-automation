# tests/test_edge_case_responses.py
import os
import time
import csv
import json
import pytest

# Uses the existing fixtures: client, config (from your conftest.py)
#   - client: ChatbotClient already configured with model & API key
#   - config: dict with model, prompts, etc.

EDGE_PROMPTS = [
    "",  # Empty → should raise in SDK; we handle and record as error
    "asdfghjklqwertyuiopzxcvbnm" * 50,  # Gibberish, very long
    "💀🔥✨💡🤖❤️" * 10,                  # Emojis only
    "Explain testing but in Japanese and English mixed ありがとう test please.",
    "What happens if I ask something impossible like divide by zero repeatedly?" * 5,
    "Give me a summary of testing but use only the letter 't'."  # Odd constraint
]

FORBIDDEN_HINTS = ["forbidden", "policy", "unsafe", "not allowed", "i can't", "i cannot"]


def safe_ask(client, prompt: str):
    """Call model safely. Never throws; returns dict with text + ok flag."""
    start = time.time()
    try:
        resp = client.send_prompt(prompt)
        text = (resp or {}).get("response", "")
        ok = bool(text.strip())
        error = None
    except Exception as e:
        text = f"[Error: {e.__class__.__name__}: {str(e)}]"
        ok = False
        error = f"{e.__class__.__name__}"
    latency = round(time.time() - start, 2)
    return {"prompt": prompt, "text": text.strip(), "ok": ok, "latency": latency, "error": error}


@pytest.mark.timeout(120)
def test_edge_case_responses(client, config):
    """
    Stress-test the model with malformed, long, and odd prompts.
    - Never crash on SDK errors (e.g., empty prompt).
    - Record outputs to CSV & JSON for auditing.
    - Make light assertions: empty prompt handled; at least one non-empty edge case returns text.
    """
    os.makedirs("reports", exist_ok=True)
    ts = time.strftime("%Y-%m-%d_%H-%M-%S")
    csv_path = f"reports/edge_case_responses_{ts}.csv"
    json_path = f"reports/edge_case_responses_{ts}.json"

    results = []
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Prompt", "Latency(s)", "OK", "Response_Prefix(100)", "Length", "Error"])

        for p in EDGE_PROMPTS:
            r = safe_ask(client, p)
            # Additional validity check: not obviously a refusal/error text
            valid_text = r["ok"] and not any(h in r["text"].lower() for h in FORBIDDEN_HINTS)
            r["valid"] = bool(valid_text)
            results.append(r)

            writer.writerow([
                (p[:80] + "…") if len(p) > 80 else p,
                r["latency"],
                r["ok"],
                (r["text"][:100] + "…") if len(r["text"]) > 100 else r["text"],
                len(r["text"]),
                r["error"] or ""
            ])
            print(f"\nPrompt: {(p[:80] + '…') if len(p) > 80 else p}")
            print(f"→ OK: {r['ok']}, Valid: {r['valid']}, Time: {r['latency']}s")
            print(f"Response: {r['text'][:120]}{'…' if len(r['text'])>120 else ''}")

    with open(json_path, "w") as jf:
        json.dump({"results": results, "timestamp": ts}, jf, indent=2)

    # ----- Assertions (lightweight, robust) -----
    # 1) We created one result per prompt
    assert len(results) == len(EDGE_PROMPTS)

    # 2) Empty prompt should be handled gracefully (no crash)
    assert results[0]["ok"] is False, "Empty prompt should not be accepted as OK."

    # 3) At least one of the *non-empty* prompts produced a non-empty response
    non_empty_results = results[1:]
    assert any(r["ok"] for r in non_empty_results), \
        "Model returned empty/error for all non-empty edge prompts."

    # 4) Report files were created
    assert os.path.exists(csv_path), "CSV not written"
    assert os.path.exists(json_path), "JSON not written"

    print(f"\n📊 CSV saved: {csv_path}")
    print(f"📁 JSON saved: {json_path}")

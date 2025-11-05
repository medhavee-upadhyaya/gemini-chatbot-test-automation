import pytest, os, csv, json, time
from statistics import mean
from difflib import SequenceMatcher

def similarity(a, b):
    """Return a quick textual similarity ratio."""
    return round(SequenceMatcher(None, a, b).ratio(), 3)

def test_prompt_robustness(client, config):
    """
    Checks Gemini's response consistency when prompts are rephrased.
    Measures semantic stability and saves results to CSV and JSON.
    """
    prompts = [
        "What is software testing?",
        "Explain software testing in simple words.",
        "Could you describe testing of software?",
        "Tell me briefly about software testing.",
        "In short, what does software testing mean?"
    ]

    os.makedirs("reports", exist_ok=True)
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    csv_path = f"reports/prompt_robustness_{timestamp}.csv"
    json_path = f"reports/prompt_robustness_{timestamp}.json"

    responses = []

    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Prompt", "Response", "Response_Length"])

        for p in prompts:
            resp = client.send_prompt(p)
            text = resp["response"].strip()
            writer.writerow([p, text, len(text)])
            responses.append({"prompt": p, "response": text})

    similarities = []
    for i in range(len(responses) - 1):
        sim = similarity(responses[i]["response"], responses[i + 1]["response"])
        similarities.append(sim)

    avg_similarity = mean(similarities)

    with open(json_path, "w") as jf:
        json.dump({"similarities": similarities, "avg_similarity": avg_similarity, "responses": responses}, jf, indent=2)

    print("\n🧩 Prompt Robustness Results")
    for i, sim in enumerate(similarities, 1):
        print(f"Pair {i}: Similarity = {sim}")
    print(f"✅ Average Semantic Similarity: {avg_similarity:.3f}")
    print(f"📊 CSV saved: {csv_path}")
    print(f"📁 JSON saved: {json_path}")

    assert avg_similarity > 0.6, f"Responses too inconsistent: {avg_similarity}"

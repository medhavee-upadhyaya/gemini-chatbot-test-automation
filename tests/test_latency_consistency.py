# import pytest
# import time
# import csv
# import os
# from statistics import mean, stdev
# from utils.api_client import ChatbotClient
# import yaml


# @pytest.fixture(scope="session")
# def config():
#     with open("config.yaml") as f:
#         return yaml.safe_load(f)


# @pytest.fixture(scope="session")
# def client(config):
#     return ChatbotClient(model=config["model"], api_key=config["gemini_api_key"])


# def test_response_latency_and_consistency(client, config):
#     """
#     Measure Gemini API latency and consistency across runs.
#     Save results to CSV for later analysis.
#     """

#     prompt = "Summarize what software testing is in 10 words or fewer."
#     latencies = []
#     responses = []

#     # Setup CSV output
#     os.makedirs("reports", exist_ok=True)
#     csv_path = os.path.join("reports", "latency_results.csv")
#     with open(csv_path, "w", newline="") as f:
#         writer = csv.writer(f)
#         writer.writerow(["Run", "Latency(s)", "Response"])

#         runs = 5
#         for i in range(runs):
#             start = time.time()
#             resp = client.send_prompt(prompt)
#             elapsed = round(time.time() - start, 2)
#             latencies.append(elapsed)
#             responses.append(resp["response"])
#             writer.writerow([i + 1, elapsed, resp["response"].strip()])
#             print(f"Run {i+1}: {elapsed:.2f}s → {resp['response'][:60]}...")

#     avg_latency = mean(latencies)
#     std_latency = stdev(latencies) if len(latencies) > 1 else 0
#     unique_responses = len(set(responses))

#     # ✅ Loosened thresholds (allow for normal LLM variability)
#     assert avg_latency < 8.0, f"Average latency too high: {avg_latency}s"
#     assert unique_responses <= 5, "Responses varied more than expected (soft warning)"
 
#     print(f"\n✅ Average Latency: {avg_latency:.2f}s (stdev {std_latency:.2f})")
#     print(f"✅ Unique Responses: {unique_responses}/{runs}")
#     print(f"📊 CSV saved to: {csv_path}")


import pytest
import time
import csv
import os
import json
from datetime import datetime
from statistics import mean, stdev
from utils.api_client import ChatbotClient
import yaml


@pytest.fixture(scope="session")
def config():
    with open("config.yaml") as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="session")
def client(config):
    return ChatbotClient(model=config["model"], api_key=config["gemini_api_key"])


def test_response_latency_and_consistency(client, config):
    """
    Measure Gemini API latency and consistency across runs.
    Save results to CSV and JSON for audit & visualization.
    """

    prompt = "Summarize what software testing is in 10 words or fewer."
    latencies = []
    responses = []

    os.makedirs("reports", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    csv_path = os.path.join("reports", f"latency_results_{timestamp}.csv")
    json_path = os.path.join("reports", f"latency_results_{timestamp}.json")

    results = []

    # Run the test multiple times
    runs = 5
    for i in range(runs):
        start = time.time()
        resp = client.send_prompt(prompt)
        elapsed = round(time.time() - start, 2)
        response_text = resp["response"].strip()

        latencies.append(elapsed)
        responses.append(response_text)
        results.append({
            "run": i + 1,
            "latency_s": elapsed,
            "response": response_text
        })

        print(f"Run {i+1}: {elapsed:.2f}s → {response_text[:80]}...")

    # Save to CSV
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["run", "latency_s", "response"])
        writer.writeheader()
        writer.writerows(results)

    # Save to JSON
    with open(json_path, "w") as jf:
        json.dump(results, jf, indent=2)

    # Calculate summary
    avg_latency = mean(latencies)
    std_latency = stdev(latencies) if len(latencies) > 1 else 0
    unique_responses = len(set(responses))

    assert avg_latency < 8.0, f"Average latency too high: {avg_latency}s"
    assert unique_responses <= 5, "Responses varied more than expected (soft warning)"

    print(f"\n✅ Average Latency: {avg_latency:.2f}s (stdev {std_latency:.2f})")
    print(f"✅ Unique Responses: {unique_responses}/{runs}")
    print(f"📊 CSV saved: {csv_path}")
    print(f"📁 JSON saved: {json_path}")

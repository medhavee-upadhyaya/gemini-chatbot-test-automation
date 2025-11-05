# Gemini Chatbot Test Automation Framework  

A modular **PyTest-based LLM testing framework** designed to evaluate **Google Gemini’s** performance, reliability, and robustness across multiple testing dimensions — built by **Medhavee Upadhyaya**.

---

## Overview  
This project automates the testing of a Gemini-based chatbot using **Python, PyTest, and the Google Generative AI SDK**.  
It validates **how consistently, accurately, and efficiently** the model responds to a variety of prompts — from simple math to extreme edge cases.  

---

## Key Features  

| Test Suite                | Purpose                  | What It Checks                                              |
|---------------------------|--------------------------|-------------------------------------------------------------|
| **Schema Validation**     | Functional correctness   | Response structure, completeness, and type validation       |
| **Latency & Consistency** | Performance testing      | Response time averages, stability across runs               |
| **Prompt Robustness**     | Semantic testing         | Similarity across paraphrased prompts                       |
| **Context Retention**     | Conversational coherence | Model’s ability to remember past context                    |
| **Edge-Case Responses**   | Resilience & safety      | Handling of gibberish, emojis, multilingual or empty inputs |

---

## Tech Stack  
- **Language:** Python 3.14  
- **Frameworks:** PyTest, PyTest-HTML  
- **Libraries:** `google-generativeai`, `yaml`, `jsonschema`, `csv`, `time`, `os`  
- **Reports:** HTML, CSV, JSON (auto-generated)  

---

## Setup Instructions  

1. **Clone the repository**
   ```bash
   git clone https://github.com/medhavee-upadhyaya/gemini-chatbot-test-automation.git
   cd gemini-chatbot-test-automation


2. **Create a virtual environment**
   ```bash
    python3 -m venv venv
    source venv/bin/activate

3. **Install dependencies**
   ```bash
    pip install -r requirements.txt

4. **Set your Gemini API key**
   ```bash
    export GEMINI_API_KEY="your_api_key_here"

5. **Run all tests**
   ```bash
    pytest -v --html=reports/test_summary.html --self-contained-html


## Example Output

1. **Latency Test (sample run):**
   ```bash
    Run 1: 4.1s → “Finding defects, ensuring software quality...”
    Run 2: 3.8s → “Testing verifies system reliability...”
    ✅ Average Latency: 4.55s (stdev 1.30)
    📊 CSV saved: reports/latency_results_2025-11-04_13-27-07.csv

2. **Context Retention Test:**
   ```bash
    Turn 1 — My name is Medhavee.
    Turn 2 — What is my name? → “Your name is Medhavee.”
    ✅ Remembered Name: True
    ✅ Logical Follow-up: True


## Project Structure

gemini-chatbot-test-automation/
│
├── tests/
│   ├── test_chatbot_basic.py
│   ├── test_latency_consistency.py
│   ├── test_prompt_robustness.py
│   ├── test_context_retention.py
│   └── test_edge_case_responses.py
│
├── utils/
│   ├── api_client.py
│   └── __init__.py
│
├── reports/
│   ├── *.html
│   ├── *.csv
│   └── *.json
│
├── config.yaml
├── requirements.txt
└── README.md


## Result Summary

| Test Suite            | Result      | Key Finding                                      |
| --------------------- | ----------- | ------------------------------------------------ |
| Schema Validation     | ✅ Passed   | Gemini returns structured, non-empty responses   |
| Latency & Consistency | ✅ Passed   | Avg. latency ~4.5s, within stable range          |
| Prompt Robustness     | ⚠️ Partial  | Semantic variation found (0.09 similarity)       |
| Context Retention     | ✅ Passed   | Maintains multi-turn context                     |
| Edge Cases            | ✅ Passed   | Handled invalid & multilingual prompts gracefully|




## Highlights

Demonstrates end-to-end LLM quality automation

Combines QA, ML, and DevOps-style reporting

Fully reproducible test suite — plug in any LLM model easily

## Author  
**Medhavee Upadhyaya**  

🔗 **Connect with me:**  
- [LinkedIn](https://www.linkedin.com/in/medhavee-upadhyaya)  
- [GitHub](https://github.com/medhavee-upadhyaya)

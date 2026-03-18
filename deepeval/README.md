# Phase 1 — LLM Evaluation with DeepEval

## What This Is

A pytest-based test suite that evaluates LLM outputs using DeepEval's metrics framework. Unlike RAGAS (Phase 2) which tests RAG pipelines specifically, DeepEval tests **any LLM output** — summarization, Q&A, content generation, bias detection.

Everything runs locally using Ollama (Llama 3.1) — no API keys, no cost.

## How It Differs from RAGAS (Phase 2)

| | RAGAS (Phase 2) | DeepEval (Phase 1) |
|---|---|---|
| **Tests what** | RAG pipeline (retriever + generator together) | Any LLM output (no retrieval needed) |
| **Test format** | Evaluation script with dataset | Pytest test cases (CI/CD native) |
| **Use case** | "Is my knowledge base chatbot working?" | "Is this LLM response good?" |
| **Analogy** | API integration test | Unit test |

## Metrics Covered

### Answer Relevancy (`test_answer_relevancy.py`)
Does the LLM's response actually address the question asked?
- Scenario: AI assistant answering employee questions
- Higher score = more relevant

### Faithfulness (`test_faithfulness.py`)
Is the answer grounded in the provided context, or is it making things up?
- Scenario: Customer support chatbot using product documentation
- Higher score = more faithful to source

### Hallucination (`test_hallucination.py`)
Does the LLM contradict the provided source material?
- Scenario: AI summarizing meeting notes, incident reports, product info
- **Lower score = better** (0.0 = no hallucination)
- Key distinction: Faithfulness checks "is it supported?", Hallucination checks "does it contradict?"

### Bias (`test_bias.py`)
Does the LLM exhibit gender, racial, or other biases?
- Scenario: AI writing job descriptions or customer-facing content
- **Lower score = better** (0.0 = no bias detected)
- This is a responsible AI metric that RAGAS doesn't cover

## Evaluation Results (Llama 3.1 8B, local via Ollama)

| Test | Score | Status | Notes |
|---|---|---|---|
| Answer Relevancy — automated vs manual testing | 0.90 | PASSED | |
| Answer Relevancy — load vs stress testing | 0.62 | FAILED | Judge model was overly strict |
| Answer Relevancy — flaky tests | 0.86 | PASSED | |
| Faithfulness — return policy | 0.75 | PASSED | |
| Faithfulness — password reset | 0.60 | FAILED | Omitted details from context |
| Faithfulness — shipping options | 0.75 | PASSED | |
| Hallucination — product summary | 0.17 | PASSED | Omitted water resistance detail |
| Hallucination — company policy | 0.25 | PASSED | Minor omission on sick leave |
| Hallucination — incident report | 0.00 | PASSED | Perfect — zero hallucination |
| Bias — software engineer job desc | 0.00 | PASSED | No bias detected |
| Bias — nursing job desc | 0.00 | PASSED | No bias detected |
| Bias — toy review | 0.50 | PASSED | Borderline — flagged "great option" as bias |

## Prerequisites

- **Ollama** installed and running (`ollama serve`)
- **Llama 3.1** pulled: `ollama pull llama3.1`
- **Python 3.10+**

No API keys needed — everything runs locally.

## Setup

```bash
cd deepeval

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Run all tests
```bash
deepeval test run test_answer_relevancy.py test_faithfulness.py test_hallucination.py test_bias.py -v
```

### Run a single test file
```bash
deepeval test run test_hallucination.py -v
```

### Run with standard pytest (also works)
```bash
pytest test_answer_relevancy.py -v
```

## Project Structure

```
deepeval/
├── conftest.py                  # Shared fixtures: Ollama model, response generator
├── test_answer_relevancy.py     # 4 tests — is the answer on-topic?
├── test_faithfulness.py         # 3 tests — is the answer grounded in context?
├── test_hallucination.py        # 3 tests — does the answer contradict the source?
├── test_bias.py                 # 3 tests — is the output biased?
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## How It Works

1. **conftest.py** sets up a shared Ollama model and a `generate_response()` helper
2. Each test file defines realistic scenarios with test data
3. For each test case, the LLM generates a real response at runtime
4. DeepEval's metric (acting as a "judge") evaluates the response
5. The test passes or fails based on the threshold

The LLM is both the **system under test** (generating responses) and the **judge** (evaluating quality via DeepEval). In production, you'd use a stronger model as the judge.

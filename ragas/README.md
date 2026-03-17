# Phase 2 — RAG Pipeline Testing with RAGAS

## What This Is

A minimal Retrieval-Augmented Generation (RAG) pipeline built with LangChain + ChromaDB, evaluated using the RAGAS framework. The knowledge base currently contains placeholder QA engineering docs — these can be swapped for any real company documents later.

Everything runs locally using Ollama (Llama 3.1) — no API keys, no cost.

## How RAG Works

```
User Question
      │
      ▼
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│  Embedding  │───▶│  ChromaDB    │───▶│  Top-K      │
│  Model      │    │  Vector      │    │  Relevant   │
│             │    │  Search      │    │  Chunks     │
└─────────────┘    └──────────────┘    └──────┬──────┘
                                              │
                                              ▼
                                     ┌────────────────┐
                   User Question ───▶│  Llama 3.1     │───▶ Answer
                                     │  (via Ollama)  │
                                     └────────────────┘
```

1. Documents are split into ~500 character chunks and stored as vector embeddings in ChromaDB
2. When a question comes in, the 3 most relevant chunks are retrieved via similarity search
3. The retrieved chunks + question are sent to Llama 3.1 (via Ollama), which generates an answer grounded in the context

## RAGAS Metrics Explained

| Metric | What It Measures | Why It Matters |
|---|---|---|
| **Context Precision** | Are the retrieved chunks actually relevant to the question? | Low precision means the retriever is pulling in noise — irrelevant chunks that dilute the context |
| **Faithfulness** | Is the answer grounded in the retrieved context (not hallucinated)? | Low faithfulness means the LLM is making things up instead of using the provided context |
| **Answer Relevancy** | Does the answer actually address the question asked? | Low relevancy means the answer may be factual but doesn't help the user |

**Key distinction:** Context Precision evaluates the *retriever* — is it finding the right chunks? Faithfulness evaluates the *generator* — is the LLM sticking to those chunks? These are independent failure modes. A pipeline can retrieve perfect context but still hallucinate, or retrieve garbage but produce a plausible-sounding answer.

## Evaluation Results (Llama 3.1 8B, local via Ollama)

| Metric | Score |
|---|---|
| **Context Precision** | 0.88 |
| **Faithfulness** | 0.70 |
| **Answer Relevancy** | 0.69 |

### Per-question breakdown

| Question | Context Precision | Faithfulness | Answer Relevancy |
|---|---|---|---|
| What is the Page Object Model? | 1.00 | 1.00 | 1.00 |
| P95 response time thresholds for APIs? | 1.00 | 1.00 | 0.66 |
| How should flaky tests be managed? | 1.00 | 0.33 | 0.68 |
| What test levels should a web app have? | 0.58 | 0.50 | 0.71 |
| What status code for POST success? | 0.83 | 0.67 | 0.40 |

### What the scores tell us

- **Retriever is strong** — context precision is high (0.88), meaning ChromaDB finds the right chunks
- **Faithfulness varies** — some answers stay grounded (1.0), others drift beyond context (0.33)
- **Answer relevancy drops on short answers** — "201 Created" is correct but too terse for the metric

These are expected baseline scores for a local 8B model. Swapping in a larger model or tuning the prompt would improve faithfulness and relevancy.

## Prerequisites

- **Ollama** installed and running (`ollama serve`)
- **Llama 3.1** pulled: `ollama pull llama3.1`
- **Python 3.10+**

No API keys needed — everything runs locally.

## Setup

```bash
cd ragas

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### 1. Interactive chat (manual verification)

```bash
python chat.py
```

Ask questions and see both the retrieved context chunks and the LLM's answer. Use this to manually verify that the pipeline retrieves the right content and generates correct answers.

### 2. Test the RAG pipeline

```bash
python rag_pipeline.py
```

Builds the vector store from docs/ and runs sample questions.

### 3. Run RAGAS evaluation

```bash
python evaluate_ragas.py
```

Runs 5 test questions through the pipeline and evaluates with RAGAS metrics. Takes ~6 minutes on local Ollama.

## Swapping in Your Own Documents

The placeholder docs in `docs/` can be replaced with any content:

1. Delete or replace the `.md` files in `docs/`
2. Add your own documents (`.md` format)
3. Delete the `chroma_db/` folder to force a rebuild
4. Update the test questions in `evaluate_ragas.py` to match your new content
5. Run `python rag_pipeline.py` to rebuild, then `python evaluate_ragas.py` to evaluate

The framework stays the same — only the content and test questions change.

## Project Structure

```
ragas/
├── docs/                          # Knowledge base documents (swappable)
│   ├── test_strategy.md
│   ├── qa_automation_best_practices.md
│   └── api_testing_guide.md
├── rag_pipeline.py                # RAG pipeline: load, chunk, embed, query
├── evaluate_ragas.py              # RAGAS evaluation script (3 metrics, 5 questions)
├── chat.py                        # Interactive chat for manual verification
├── requirements.txt               # Python dependencies
├── .env.example                   # Placeholder (no keys needed for Ollama)
└── README.md                      # This file
```

"""
RAGAS evaluation script for the RAG pipeline.

Runs a set of test questions through the pipeline and evaluates
the results using RAGAS metrics:
  - context_precision: Are the retrieved chunks relevant to the question?
  - faithfulness: Is the answer grounded in the retrieved context?
  - answer_relevancy: Does the answer actually address the question?

Usage:
    python evaluate_ragas.py
"""

from datasets import Dataset
from langchain_ollama import ChatOllama
from langchain_huggingface import HuggingFaceEmbeddings
from ragas import evaluate
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.metrics._context_precision import LLMContextPrecisionWithoutReference
from ragas.metrics._faithfulness import Faithfulness
from ragas.metrics._answer_relevance import ResponseRelevancy

from rag_pipeline import build_rag_chain, build_vector_store, query

# --- Test Dataset ---
# Each entry has a question and a ground truth answer for evaluation.
# The RAG pipeline will generate the actual answer and retrieved contexts.

TEST_QUESTIONS = [
    {
        "question": "What is the Page Object Model?",
        "ground_truth": (
            "The Page Object Model is a design pattern that creates an abstraction "
            "layer between test code and the UI. Each page or component gets its own "
            "class that encapsulates locators and interactions."
        ),
    },
    {
        "question": "What are the recommended P95 response time thresholds for APIs?",
        "ground_truth": (
            "P95 response time should be under 500ms for read operations and "
            "under 1000ms for write operations."
        ),
    },
    {
        "question": "How should flaky tests be managed in a test suite?",
        "ground_truth": (
            "Flaky tests should be tracked with a quarantine system. Move them to a "
            "separate suite, investigate root causes, and fix within a sprint. Common "
            "causes include race conditions, shared state, and environment instability."
        ),
    },
    {
        "question": "What test levels should a web application have?",
        "ground_truth": (
            "A web application should have unit testing, integration testing, and "
            "end-to-end testing. Unit tests verify individual functions, integration "
            "tests verify components working together, and E2E tests verify complete "
            "user workflows."
        ),
    },
    {
        "question": "What status code should a POST request return on success?",
        "ground_truth": (
            "A POST request that creates a new resource should return 201 Created "
            "with a Location header."
        ),
    },
]


def build_evaluation_dataset():
    """Run all test questions through the RAG pipeline and collect results."""
    print("Building vector store...")
    vector_store = build_vector_store()
    chain, _ = build_rag_chain(vector_store)

    questions = []
    answers = []
    contexts = []
    ground_truths = []

    print(f"Running {len(TEST_QUESTIONS)} test questions through the pipeline...\n")

    for item in TEST_QUESTIONS:
        q = item["question"]
        print(f"  Q: {q}")

        answer, retrieved_contexts = query(q, chain=chain, vector_store=vector_store)
        print(f"  A: {answer[:100]}...\n")

        questions.append(q)
        answers.append(answer)
        contexts.append(retrieved_contexts)
        ground_truths.append(item["ground_truth"])

    return Dataset.from_dict(
        {
            "question": questions,
            "answer": answers,
            "contexts": contexts,
            "ground_truth": ground_truths,
        }
    )


def run_evaluation():
    """Evaluate the RAG pipeline using RAGAS metrics."""
    dataset = build_evaluation_dataset()

    print("=" * 60)
    print("Running RAGAS evaluation...")
    print("=" * 60)

    # Wrap Ollama and embeddings for RAGAS (all local, no API keys)
    # timeout=300 gives Ollama enough time for the longer evaluation prompts
    llm = LangchainLLMWrapper(ChatOllama(
        model="llama3.1",
        temperature=0,
        timeout=600,
    ))
    embeddings = LangchainEmbeddingsWrapper(
        HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    )

    # Configure metrics
    metrics = [
        LLMContextPrecisionWithoutReference(),
        Faithfulness(),
        ResponseRelevancy(),
    ]

    # batch_size=1 prevents parallel LLM calls that overwhelm local Ollama
    results = evaluate(
        dataset=dataset,
        metrics=metrics,
        llm=llm,
        embeddings=embeddings,
        batch_size=1,
    )

    print("\n" + "=" * 60)
    print("RAGAS EVALUATION RESULTS")
    print("=" * 60)
    print(f"\n{results}\n")

    # Print per-question breakdown
    df = results.to_pandas()
    print("\nPer-question breakdown:")
    print("-" * 60)

    # Find the metric columns (exclude input/output data columns)
    metric_cols = [
        col for col in df.columns
        if col not in ("question", "answer", "contexts", "ground_truth",
                        "user_input", "response", "retrieved_contexts",
                        "reference")
    ]

    for i, row in df.iterrows():
        # Try multiple possible column names for the question
        q = row.get("user_input") or row.get("question") or f"Question {i+1}"
        print(f"\nQ: {q}")
        for col in metric_cols:
            val = row[col]
            if isinstance(val, float):
                print(f"  {col}: {val:.3f}")
            else:
                print(f"  {col}: {val}")

    return results


if __name__ == "__main__":
    run_evaluation()

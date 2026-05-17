"""
Test: Answer Relevancy

Does the LLM's response actually address the question asked?

Real-world scenario: A company has an AI assistant that answers employee questions.
QA needs to verify the responses are relevant — not off-topic or evasive.
"""

import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric

from conftest import generate_response


# --- Test Data ---
# Each tuple: (input_question, system_prompt)
# The LLM generates the actual_output at runtime — we're testing REAL responses.

TEST_CASES = [
    (
        "What are the benefits of automated testing over manual testing?",
        "You are a QA engineering assistant. Give concise, practical answers.",
    ),
    (
        "Explain the difference between load testing and stress testing.",
        "You are a QA engineering assistant. Give concise, practical answers.",
    ),
    (
        "How do you handle flaky tests in a CI/CD pipeline?",
        "You are a QA engineering assistant. Give concise, practical answers.",
    ),
    (
        "What is contract testing and when should you use it?",
        "You are a QA engineering assistant. Give concise, practical answers.",
    ),
]


@pytest.mark.parametrize("input_question,system_prompt", TEST_CASES)
def test_answer_relevancy(input_question, system_prompt, ollama_model):
    """Verify the LLM's answer is relevant to the question asked."""
    actual_output = generate_response(input_question, system_prompt)

    test_case = LLMTestCase(
        input=input_question,
        actual_output=actual_output,
    )

    metric = AnswerRelevancyMetric(
        threshold=0.5,
        model=ollama_model,
    )

    assert_test(test_case, [metric])

"""
Test: Faithfulness

Is the LLM's answer grounded in the provided context, or is it hallucinating?

Real-world scenario: A company has a customer support chatbot that answers questions
using product documentation. QA needs to verify the bot doesn't make up information
that isn't in the source material.

Note: This is similar to what RAGAS tests, but here we test it as isolated unit tests
with DeepEval's pytest integration — no RAG pipeline needed. We provide the context
directly, simulating what a retriever would return.
"""

import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import FaithfulnessMetric

from conftest import generate_response


# --- Test Data ---
# Each tuple: (question, context, system_prompt)
# Context simulates what a retriever or knowledge base would provide.

TEST_CASES = [
    (
        "What is your return policy for electronics?",
        [
            "Electronics can be returned within 30 days of purchase with original receipt. "
            "Items must be in original packaging and unused condition. Opened software and "
            "digital downloads are non-refundable. Restocking fee of 15% applies to all "
            "electronics returns."
        ],
        "You are a customer support assistant. Answer based only on the provided context.",
    ),
    (
        "How do I reset my password?",
        [
            "To reset your password, go to the login page and click 'Forgot Password'. "
            "Enter your registered email address. You will receive a reset link within "
            "5 minutes. The link expires after 24 hours. If you don't receive the email, "
            "check your spam folder or contact support at help@example.com."
        ],
        "You are a customer support assistant. Answer based only on the provided context.",
    ),
    (
        "What shipping options are available?",
        [
            "We offer three shipping options: Standard (5-7 business days, free for orders "
            "over $50), Express (2-3 business days, $9.99), and Next Day ($19.99, order by "
            "2pm EST). All orders include tracking. We ship to all 50 US states. "
            "International shipping is not currently available."
        ],
        "You are a customer support assistant. Answer based only on the provided context.",
    ),
]


@pytest.mark.parametrize("input_question,context,system_prompt", TEST_CASES)
def test_faithfulness(input_question, context, system_prompt, ollama_model):
    """Verify the LLM's answer is grounded in the provided context."""
    # Build a prompt that includes context, simulating a RAG response
    full_prompt = f"""Context: {context[0]}

Question: {input_question}"""

    actual_output = generate_response(full_prompt, system_prompt)

    test_case = LLMTestCase(
        input=input_question,
        actual_output=actual_output,
        retrieval_context=context,
    )

    metric = FaithfulnessMetric(
        threshold=0.7,
        model=ollama_model,
    )

    assert_test(test_case, [metric])

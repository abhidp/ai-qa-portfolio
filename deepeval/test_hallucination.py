"""
Test: Hallucination

Is the LLM making up facts that contradict the provided context?

Real-world scenario: An AI assistant summarizes meeting notes or documents.
QA needs to verify the summary doesn't introduce facts that weren't in the original.
This is critical in finance, healthcare, and legal — hallucinated numbers or
policies can cause real damage.

Key difference from Faithfulness:
  - Faithfulness: "Is the answer supported by the context?"
  - Hallucination: "Does the answer contradict the context?"
  An answer can be unfaithful (adds info beyond context) without hallucinating
  (contradicting context). Hallucination is the more severe failure.
"""

import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import HallucinationMetric

from conftest import generate_response


# --- Test Data ---
# Each tuple: (task_prompt, context, system_prompt)
# Context is the source of truth. We check if the LLM contradicts it.

TEST_CASES = [
    (
        "Summarize this product information.",
        [
            "The XR-500 wireless headphones feature 40-hour battery life, active noise "
            "cancellation, and Bluetooth 5.3. They weigh 250 grams and come in black and "
            "navy blue. Retail price is $199.99. They are NOT water resistant. The warranty "
            "covers 1 year from date of purchase."
        ],
        "You are a product information assistant. Summarize accurately.",
    ),
    (
        "Summarize this company policy.",
        [
            "Employees are entitled to 20 days of paid time off per year. PTO does not "
            "carry over to the next calendar year. Sick leave is separate and provides "
            "10 days per year. Employees must give 2 weeks notice for planned PTO of "
            "3 or more consecutive days. PTO requests are approved by direct managers."
        ],
        "You are an HR assistant. Summarize accurately.",
    ),
    (
        "Summarize this incident report.",
        [
            "On March 5, 2026, the payment processing service experienced a 47-minute "
            "outage from 2:15 PM to 3:02 PM EST. Root cause was a failed database "
            "migration that locked the transactions table. 1,247 transactions were "
            "affected. No data was lost. The fix involved rolling back the migration "
            "and replaying queued transactions. A post-mortem is scheduled for March 7."
        ],
        "You are a technical assistant. Summarize accurately.",
    ),
]


@pytest.mark.parametrize("task_prompt,context,system_prompt", TEST_CASES)
def test_hallucination(task_prompt, context, system_prompt, ollama_model):
    """Verify the LLM doesn't hallucinate facts that contradict the source."""
    full_prompt = f"""Source material: {context[0]}

Task: {task_prompt}"""

    actual_output = generate_response(full_prompt, system_prompt)

    test_case = LLMTestCase(
        input=task_prompt,
        actual_output=actual_output,
        context=context,
    )

    metric = HallucinationMetric(
        threshold=0.5,
        model=ollama_model,
    )

    assert_test(test_case, [metric])

"""
Shared fixtures for DeepEval test suite.

Provides:
  - Ollama model instance (reused across all tests)
  - Helper to generate LLM responses
"""

import pytest
from deepeval.models import OllamaModel
from ollama import chat


OLLAMA_MODEL = "llama3.1"


@pytest.fixture(scope="session")
def ollama_model():
    """DeepEval model wrapper for Ollama — used as the judge LLM."""
    return OllamaModel(
        model=OLLAMA_MODEL,
        base_url="http://localhost:11434",
        temperature=0,
    )


def generate_response(prompt: str, system_prompt: str = "") -> str:
    """Call Ollama directly to get an LLM response for testing."""
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    response = chat(model=OLLAMA_MODEL, messages=messages)
    return response.message.content

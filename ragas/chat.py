"""
Interactive chat with the RAG pipeline.

Ask questions and see:
  1. Which document chunks were retrieved (what the LLM sees as context)
  2. The LLM's answer based on that context

This lets you manually verify that the pipeline is working correctly
by comparing the answer against the actual docs in /docs.

Usage:
    python chat.py
"""

from rag_pipeline import build_rag_chain, build_vector_store, query


def main():
    print("Loading RAG pipeline...")
    vector_store = build_vector_store()
    chain, _ = build_rag_chain(vector_store)

    print("\n" + "=" * 60)
    print("RAG Pipeline Chat — ask questions about the QA docs")
    print("Type 'quit' to exit")
    print("=" * 60)

    while True:
        print()
        question = input("You: ").strip()
        if not question or question.lower() in ("quit", "exit", "q"):
            print("Bye!")
            break

        answer, contexts = query(question, chain=chain, vector_store=vector_store)

        # Show what chunks were retrieved (what the LLM based its answer on)
        print("\n--- Retrieved Context (what the LLM sees) ---")
        for i, ctx in enumerate(contexts, 1):
            print(f"\n  Chunk {i}:")
            # Indent each line for readability
            for line in ctx.strip().split("\n"):
                print(f"    {line}")

        # Show the answer
        print(f"\n--- Answer ---\n{answer}")


if __name__ == "__main__":
    main()

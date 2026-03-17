"""
Minimal RAG pipeline using LangChain + ChromaDB + Ollama (local LLM).

This module loads documents from the /docs folder, chunks them,
stores embeddings in a local ChromaDB vector store, and answers
questions using a local Llama 3.1 model via Ollama.

No API keys required — everything runs locally.
"""

from pathlib import Path

from langchain_ollama import ChatOllama
from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# --- Configuration ---
DOCS_DIR = Path(__file__).parent / "docs"
CHROMA_DIR = Path(__file__).parent / "chroma_db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Free, local, fast
OLLAMA_MODEL = "llama3.1"             # Free, local via Ollama
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50


def build_vector_store(force_rebuild: bool = False) -> Chroma:
    """Load documents, chunk them, and store embeddings in ChromaDB."""
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    # Return existing store if it exists and we're not forcing a rebuild
    if CHROMA_DIR.exists() and not force_rebuild:
        return Chroma(
            persist_directory=str(CHROMA_DIR),
            embedding_function=embeddings,
        )

    # Load all .md files from the docs directory
    loader = DirectoryLoader(
        str(DOCS_DIR),
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    documents = loader.load()
    print(f"Loaded {len(documents)} documents from {DOCS_DIR}")

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks")

    # Create and persist vector store
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR),
    )
    print(f"Vector store created at {CHROMA_DIR}")
    return vector_store


def build_rag_chain(vector_store: Chroma):
    """Build a retrieval-augmented generation chain with Ollama (local LLM)."""
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3},
    )

    prompt = ChatPromptTemplate.from_template(
        """Answer the question based only on the following context.
If the context does not contain enough information, say so clearly.

Context:
{context}

Question: {question}

Answer:"""
    )

    llm = ChatOllama(model=OLLAMA_MODEL, temperature=0)

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain, retriever


def query(question: str, chain=None, vector_store=None):
    """Run a question through the RAG pipeline. Returns answer and retrieved contexts."""
    if vector_store is None:
        vector_store = build_vector_store()
    if chain is None:
        chain, retriever = build_rag_chain(vector_store)
    else:
        retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    # Get the answer
    answer = chain.invoke(question)

    # Get the retrieved documents (for RAGAS evaluation)
    retrieved_docs = retriever.invoke(question)
    contexts = [doc.page_content for doc in retrieved_docs]

    return answer, contexts


if __name__ == "__main__":
    print("Building vector store...")
    vs = build_vector_store(force_rebuild=True)

    print("\n--- RAG Pipeline Ready ---\n")

    test_questions = [
        "What is the Page Object Model and why should I use it?",
        "What are the recommended P95 response time thresholds for API testing?",
        "How should flaky tests be managed?",
    ]

    chain, _ = build_rag_chain(vs)
    for q in test_questions:
        print(f"Q: {q}")
        answer, contexts = query(q, chain=chain, vector_store=vs)
        print(f"A: {answer}\n")

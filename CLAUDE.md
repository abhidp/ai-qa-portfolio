# AI QA Portfolio

## PROJECT OVERVIEW

This is an AI QA learning portfolio built by a Senior QA Automation Engineer (18+ years of experience) to upskill in LLM evaluation, RAG pipeline testing, and AI-powered application quality assurance.

The portfolio demonstrates practical, interview-ready skills across the full AI testing lifecycle — from evaluating LLM outputs with metrics-based frameworks, to performance testing LLM APIs, to end-to-end testing of AI chat interfaces.

Each phase is a standalone, working project with its own test suite, documentation, and CI/CD integration.

---

## COMPLETED: Phase 2 — RAG Pipeline Testing with RAGAS

- [x] Build a minimal RAG pipeline using LangChain + ChromaDB (local, free)
- [x] Load real documents into the knowledge base (QA documentation or personal notes)
- [x] Run RAGAS evaluation metrics: context_precision, faithfulness, answer_relevancy
- [x] Understand the difference between context precision and answer faithfulness
- [x] Write a clear README in /ragas explaining the pipeline and how to run it
- [x] Interactive chat.py for manual verification
- [x] Commit working milestone

---

## TECH STACK

| Category | Tools |
|---|---|
| Languages | Python, TypeScript |
| LLM APIs | Ollama (local), Anthropic (Claude), OpenAI |
| LLM Evaluation | DeepEval, RAGAS |
| RAG Pipeline | LangChain, ChromaDB |
| E2E Testing | Playwright + TypeScript, Playwright MCP Server |
| Performance | K6 |
| CI/CD | GitHub Actions, Docker |
| Cloud | AWS Lambda, S3, DynamoDB, CloudWatch |
| Orchestration | Kubernetes |
| Secrets | .env + python-dotenv |

---

## LEARNING PHASES

### Phase 0 — Foundation

- Python refresher (functions, lists, dicts, classes)
- OpenAI/Anthropic API basics — calling an API, handling responses
- Understanding what a RAG pipeline is conceptually
- Setting up .env for secrets management
- Folder structure: /deepeval /ragas /playwright-ai /k6-llm /capstone

### Phase 1 — LLM Evaluation with DeepEval

- Install deepeval, connect to Anthropic API
- Write test cases with AnswerRelevancyMetric, FaithfulnessMetric, HallucinationMetric
- Goal: 3-4 metrics running against real Claude API responses
- Wire into GitHub Actions so tests run on every push
- **Deliverable:** /deepeval folder with test suite + GHA workflow

### Phase 2 — RAG Pipeline Testing with RAGAS

- Build a minimal RAG pipeline using LangChain + ChromaDB (local, free)
- Use any real documents as the knowledge base (e.g. QA documentation, personal notes)
- Run RAGAS evaluation metrics: context_precision, faithfulness, answer_relevancy
- Understand the difference between context precision and answer faithfulness
- **Deliverable:** /ragas folder with working RAG pipeline + RAGAS evaluation script + README

### Phase 3 — Playwright + MCP AI Testing

- Test an AI chat UI end-to-end with Playwright + TypeScript
- Handle non-deterministic LLM output with pattern matching and semantic assertions
- Write tests using the Playwright MCP server as part of the workflow
- **Deliverable:** /playwright-ai folder with test suite

### Phase 4 — K6 Performance Testing for LLMs

- Load test an LLM API endpoint with K6
- Measure P95/P99 latency, tokens per second, set pass/fail thresholds
- Pipe results to AWS CloudWatch
- **Deliverable:** /k6-llm folder with scripts + CloudWatch dashboard config

### Phase 5 — CI/CD Pipeline for AI Tests

- GitHub Actions pipeline: DeepEval on push, RAGAS nightly, K6 on schedule
- Docker for consistent environments
- Post results to a dashboard, Slack alerts on failure
- **Deliverable:** .github/workflows/ with full pipeline

### Phase 6 — Capstone: Full AI QA Framework

- Fictional company "Acme AI Assistant" — a RAG-powered support chatbot
- Demonstrates all phases working together in one repo
- Film a 5-minute Loom demo walkthrough
- **Deliverable:** /capstone folder + top-level README with demo link

---

## CONVENTIONS

- Python files use snake_case
- All secrets via .env + python-dotenv, never hardcoded
- Each phase folder must have its own README.md
- Commit after each working milestone, not at the end of the day

---

## PORTFOLIO GOAL

The end goal is a GitHub repo + demo video that can be shown and talked through in QA engineering interviews at senior/lead level, specifically targeting companies building AI-powered products.

This portfolio should demonstrate:
- Hands-on ability to evaluate LLM quality with real metrics
- Understanding of RAG pipelines and how to test them
- Performance testing methodology applied to AI systems
- CI/CD maturity with automated AI test pipelines
- Clear communication through documentation and a walkthrough demo

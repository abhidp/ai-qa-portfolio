---
name: project_trading_calculator_chatbot
description: Plan to build a RAG chatbot for the Trading Notional Volume Calculator Flask app — makes Phase 2 interview-ready with real product docs
type: project
---

User has a separate project: Trading Notional Volume Calculator (Flask app, deployed on Vercel).
Repo: github.com/abhidp/trading-notional-volume-calculator

Plan: Build a RAG-powered help chatbot for this app as the interview-ready Phase 2 demo.

**Knowledge base docs to create (mostly from existing README):**
- supported_platforms.md — MT5, cTrader, file formats, export steps
- calculation_formulas.md — Notional formulas by instrument type, with worked examples
- fx_rates.md — How FX rates work, API vs cached vs fallback
- date_filtering.md — Date range, last N days, this month
- troubleshooting.md — Common issues, unsupported instruments

**Integration approach:**
- Reuse the rag_pipeline.py framework from Phase 2
- Embed query() into a Flask /chat route
- Add chat widget to the frontend
- Run RAGAS evaluation against trading-specific questions

**Why:** Transforms Phase 2 from a tutorial exercise into a real product feature. Interview pitch: "I added an AI chatbot to a production Flask app and evaluated it with RAGAS."

**How to apply:** When user is ready to make Phase 2 interview-ready, use this plan. Docs come from the existing README content, restructured into focused files.

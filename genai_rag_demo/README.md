# GenAI / RAG / Agentic AI Portfolio Demo

A compact, provider-agnostic demo that complements the forecasting/MLOps pipeline with practical Generative-AI concepts relevant to enterprise AI roles.

## What it demonstrates

- Retrieval-Augmented Generation (RAG) flow: retrieve -> build grounded prompt -> answer
- Tool/function routing for simple agentic workflows
- Groundedness and hallucination-risk checks
- Structured evaluation of retrieval quality and answer support
- Separation between orchestration logic and any external LLM provider
- Testable Python components that can later be connected to Azure OpenAI, OpenAI, or another provider

## Why it is provider-agnostic

The demo intentionally does not claim production ownership of any commercial LLM or cloud service. It focuses on the engineering concepts that transfer across providers: retrieval, prompt construction, tool selection, evaluation, guardrails, and observability.

## Files

- `rag_agent.py` - retrieval, prompt construction, tool routing, and grounded-answer helper
- `evaluate.py` - retrieval precision and simple groundedness / hallucination-risk metrics
- `tests/test_rag_agent.py` - regression tests for retrieval and routing

## Example use cases

- Ask questions over forecasting/MLOps documentation
- Route a request to a forecasting-status or model-metrics tool
- Reject unsupported answers when retrieved context is insufficient

## Enterprise mapping

The same architecture can be implemented with Azure AI Search + Azure OpenAI / Azure AI Foundry, with identity, secrets, monitoring, and governance added around the core workflow. This repository demonstrates the application logic only; it does **not** claim prior production ownership of Azure infrastructure.

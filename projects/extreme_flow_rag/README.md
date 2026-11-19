# Extreme-Flow RAG Assistant | Generative AI + LLM + Sensor Analytics

A **runnable portfolio project** connecting extreme-flow event analysis to Retrieval-Augmented Generation (RAG). The subject is motivated by **CONNECT / CONNECT+** experience, but all records are **synthetic** and are not research project data.

**Stack:** Python · FastAPI · scikit-learn TF-IDF · optional OpenAI Responses API · pytest.

## Features

1. Calculates maximum flow, peak date and illustrative threshold-exceedance counts from CSV sensor records.
2. Indexes domain notes and calculated station statistics for top-k TF-IDF retrieval.
3. Uses retrieved context for a source-grounded LLM prompt when `OPENAI_API_KEY` is configured. Otherwise, returns sources in **retrieval-only mode**; it never mislabels excerpts as an LLM answer.
4. Exposes `GET /health`, `GET /events`, `POST /ask` and interactive `/docs`.
5. Includes offline tests for event calculations, retrieval, safeguards and API validation.

## Reproduce in five minutes

From `projects/extreme_flow_rag` in the repository (Python 3.11+):

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
pytest -q
uvicorn app:app --reload
```

Open `http://127.0.0.1:8000/docs`, or call:

```bash
curl http://127.0.0.1:8000/events
curl -X POST http://127.0.0.1:8000/ask \
  -H 'Content-Type: application/json' \
  -d '{"question":"What is the maximum flow at ALMOUROL_DEMO?"}'
```

To enable an **actual LLM call**, set `OPENAI_API_KEY` as an environment variable and optionally `OPENAI_MODEL`. Do not commit credentials. Without a key, `/ask` returns `mode: retrieval_only`, `answer: null`, and retrieved source excerpts.

## Architecture

`Synthetic station CSV → deterministic peak statistics → sourced evidence → TF-IDF top-k retrieval → grounded prompt → optional LLM → response + citations`

Question-specific records and document excerpts are available under `sources`. The LLM is instructed to cite `[S1]`, `[S2]`, etc. but output should still be reviewed for factual fidelity.

## Validation and honest scope

Run `pytest -q` for five offline tests. The synthetic ALMOUROL_DEMO maximum is **240.0 m3/s**, calculated from the included CSV. The **180 m3/s threshold is illustrative only**, not a real flood-risk threshold. This is **not** a trained forecasting model, a flood-alert service, a live deployment, or evidence of an operating CONNECT/CONNECT+ RAG system. TF-IDF is lexical, not embedding-based semantic retrieval; real-world deployment needs validated feeds, calibrated thresholds, security, privacy controls, prompt-injection tests and retrieval/answer evaluation.

**CV-ready description:** *Built a prototype extreme-flow RAG assistant using synthetic sensor data, deterministic peak-event analytics, TF-IDF retrieval, an optional LLM API, and tested FastAPI endpoints.*

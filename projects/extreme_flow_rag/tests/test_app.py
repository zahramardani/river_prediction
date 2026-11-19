"""Fast offline tests: never call a paid LLM API."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fastapi.testclient import TestClient
from app import app, peak_summary, retrieve

client = TestClient(app)

def test_peak_summary_is_computed_from_csv():
    summary = {s["station"]: s for s in peak_summary()}
    assert summary["ALMOUROL_DEMO"]["max_flow_m3_s"] == 240.0
    assert summary["ALMOUROL_DEMO"]["above_demo_threshold_180_m3_s"] == 2
    assert summary["COIMBRA_DEMO"]["peak_date"] == "2026-01-04"

def test_retrieval_finds_synthetic_flow_source():
    hits = retrieve("ALMOUROL_DEMO maximum flow", top_k=3)
    assert any("ALMOUROL_DEMO" in p["source"] for p in hits)

def test_no_key_means_retrieval_only(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    response = client.post("/ask", json={"question": "What is the maximum flow for ALMOUROL_DEMO?"})
    assert response.status_code == 200
    body = response.json()
    assert body["mode"] == "retrieval_only"
    assert body["answer"] is None
    assert body["sources"]

def test_unsupported_question_does_not_fabricate(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    response = client.post("/ask", json={"question": "quasarbanana jellyforce"})
    assert response.json()["mode"] == "no_evidence"
    assert response.json()["answer"] is None

def test_events_endpoint_and_validation():
    response = client.get("/events")
    assert response.status_code == 200
    assert response.json()["dataset"] == "synthetic"
    assert client.post("/ask", json={"question": "hi"}).status_code == 422

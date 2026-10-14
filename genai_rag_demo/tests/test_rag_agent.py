from genai_rag_demo.rag_agent import SimpleRetriever, build_grounded_prompt, route_tool


def test_retrieval_returns_relevant_chunk():
    docs = [
        "Forecasting evaluation uses MAE and RMSE.",
        "Monitoring detects drift and recommends retraining.",
    ]
    chunks = SimpleRetriever(docs).retrieve("How do you detect drift?", top_k=1)
    assert "drift" in chunks[0].text.lower()


def test_prompt_requires_grounded_answer():
    chunks = SimpleRetriever(["The API uses FastAPI."]).retrieve("Which API framework is used?", top_k=1)
    prompt = build_grounded_prompt("Which API framework is used?", chunks)
    assert "Use only the supplied context" in prompt
    assert "FastAPI" in prompt


def test_tool_router_selects_monitoring():
    tools = {"monitoring": lambda: "ok", "metrics": lambda: "ok"}
    assert route_tool("Should we retrain because of drift?", tools) == "monitoring"

"""Small provider-agnostic RAG + tool-routing demo for portfolio/interview use."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Iterable, List, Sequence

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass(frozen=True)
class RetrievedChunk:
    text: str
    score: float


class SimpleRetriever:
    """Tiny TF-IDF retriever used to demonstrate the RAG control flow."""

    def __init__(self, documents: Sequence[str]):
        if not documents:
            raise ValueError("documents must not be empty")
        self.documents = list(documents)
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.matrix = self.vectorizer.fit_transform(self.documents)

    def retrieve(self, query: str, top_k: int = 3) -> List[RetrievedChunk]:
        if top_k < 1:
            raise ValueError("top_k must be >= 1")
        query_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vec, self.matrix)[0]
        ranking = scores.argsort()[::-1][:top_k]
        return [RetrievedChunk(self.documents[i], float(scores[i])) for i in ranking]


def build_grounded_prompt(question: str, chunks: Iterable[RetrievedChunk]) -> str:
    """Build a prompt that explicitly constrains answers to retrieved evidence."""
    context = "\n\n".join(f"[Context] {c.text}" for c in chunks)
    return (
        "You are a grounded assistant. Use only the supplied context. "
        "If the context is insufficient, say that you do not have enough evidence.\n\n"
        f"{context}\n\nQuestion: {question}\nAnswer:"
    )


Tool = Callable[..., str]


def route_tool(user_request: str, tools: Dict[str, Tool]) -> str | None:
    """Simple deterministic tool router illustrating function/tool selection."""
    text = user_request.lower()
    intents = {
        "metrics": ("metric", "rmse", "mae", "accuracy", "score"),
        "forecast_status": ("forecast", "prediction", "horizon", "status"),
        "monitoring": ("drift", "monitor", "retrain", "missing"),
    }
    for tool_name, keywords in intents.items():
        if tool_name in tools and any(keyword in text for keyword in keywords):
            return tool_name
    return None


def groundedness_score(answer: str, retrieved_chunks: Sequence[RetrievedChunk]) -> float:
    """Heuristic lexical support score for quick hallucination-risk checks."""
    answer_tokens = {t.strip(".,:;!?()[]{}\"'").lower() for t in answer.split() if len(t) > 3}
    if not answer_tokens:
        return 0.0
    context_tokens = {
        t.strip(".,:;!?()[]{}\"'").lower()
        for chunk in retrieved_chunks
        for t in chunk.text.split()
        if len(t) > 3
    }
    return len(answer_tokens & context_tokens) / len(answer_tokens)


def should_block_answer(answer: str, chunks: Sequence[RetrievedChunk], min_score: float = 0.35) -> bool:
    """Guardrail: block an answer when retrieved evidence does not support it enough."""
    if not chunks or max((c.score for c in chunks), default=0.0) <= 0.0:
        return True
    return groundedness_score(answer, chunks) < min_score


if __name__ == "__main__":
    docs = [
        "The forecasting service exposes inference through FastAPI and is packaged with Docker.",
        "Model quality is evaluated with MAE, RMSE, R2 and a persistence baseline.",
        "Monitoring checks missing inputs, drift, rolling error and retraining recommendations.",
    ]
    retriever = SimpleRetriever(docs)
    question = "How is the forecasting model monitored?"
    chunks = retriever.retrieve(question, top_k=2)
    print(build_grounded_prompt(question, chunks))

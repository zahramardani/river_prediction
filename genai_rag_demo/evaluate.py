"""Evaluation helpers for the GenAI/RAG portfolio demo."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .rag_agent import RetrievedChunk, groundedness_score


@dataclass(frozen=True)
class RagEvaluation:
    retrieval_hit: bool
    top_score: float
    groundedness: float
    blocked: bool


def evaluate_case(
    expected_keyword: str,
    answer: str,
    chunks: Sequence[RetrievedChunk],
    groundedness_threshold: float = 0.35,
) -> RagEvaluation:
    """Evaluate retrieval relevance and whether the answer is grounded enough."""
    keyword = expected_keyword.lower()
    retrieval_hit = any(keyword in chunk.text.lower() for chunk in chunks)
    top_score = max((chunk.score for chunk in chunks), default=0.0)
    groundedness = groundedness_score(answer, chunks)
    blocked = top_score <= 0.0 or groundedness < groundedness_threshold
    return RagEvaluation(
        retrieval_hit=retrieval_hit,
        top_score=top_score,
        groundedness=groundedness,
        blocked=blocked,
    )

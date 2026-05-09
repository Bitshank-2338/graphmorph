"""
Lightweight intent classifier - used as deterministic fallback when
the OpenAI agent is unavailable, and as a sanity check on LLM output.
"""
from typing import Literal

QueryType = Literal[
    "risk_matrix",
    "relationship_explorer",
    "skill_gap_grid",
    "cluster_explorer",
    "simulation_workspace",
    "generative",
]

KEYWORDS = {
    "risk_matrix": [
        "bottleneck",
        "risk",
        "central",
        "depend",
        "critical",
        "single point",
        "key person",
        "influence",
    ],
    "skill_gap_grid": [
        "skill",
        "capability",
        "expertise",
        "gap",
        "coverage",
        "missing",
        "talent",
    ],
    "relationship_explorer": [
        "path",
        "connect",
        "between",
        "relationship",
        "shortest",
        "traverse",
        "explore",
    ],
    "cluster_explorer": ["cluster", "group", "community", "segment", "similar", "team"],
    "simulation_workspace": [
        "what if",
        "simulate",
        "leave",
        "remove",
        "scenario",
        "impact",
        "happens if",
    ],
}


def detect_query_type(query: str) -> QueryType:
    q = query.lower()
    scores: dict[str, int] = {}
    for query_type, keywords in KEYWORDS.items():
        scores[query_type] = sum(1 for keyword in keywords if keyword in q)
    best = max(scores, key=lambda key: scores[key])
    return best if scores[best] > 0 else "relationship_explorer"  # type: ignore

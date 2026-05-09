"""
Cypher templates per query type.
Designed to work against the heuristic schema produced by graph_transformer.py.
"""
from typing import Optional


CYPHER_TEMPLATES = {
    "risk_matrix": """
        MATCH (n:Person)-[r]-(m)
        WITH n, count(DISTINCT m) AS connections
        RETURN n.id AS id, n.label AS label, connections
        ORDER BY connections DESC
        LIMIT 12
    """,

    "skill_gap_grid": """
        MATCH (s:Skill)<-[:HAS_SKILL]-(p:Person)
        WITH s.label AS skill, count(DISTINCT p) AS headcount
        RETURN skill, headcount
        ORDER BY headcount DESC
        LIMIT 20
    """,

    "relationship_explorer": """
        MATCH (a)-[r]->(b)
        RETURN a.id AS source_id, a.label AS source_label, a.type AS source_type,
               b.id AS target_id, b.label AS target_label, b.type AS target_type,
               type(r) AS rel
        LIMIT 80
    """,

    "cluster_explorer": """
        MATCH (d:Department)<-[:BELONGS_TO]-(p:Person)
        WITH d.label AS cluster, collect(p.label) AS members
        RETURN cluster, members, size(members) AS size
        ORDER BY size DESC
    """,

    "simulation_workspace": """
        MATCH (n:Person)-[r]-(m)
        WITH n, count(DISTINCT m) AS connections
        RETURN n.id AS id, n.label AS label, connections
        ORDER BY connections DESC
        LIMIT 20
    """,
}


def generate_cypher(query_type: str, override: Optional[str] = None) -> str:
    if override:
        return override.strip()
    return CYPHER_TEMPLATES.get(query_type, CYPHER_TEMPLATES["relationship_explorer"]).strip()

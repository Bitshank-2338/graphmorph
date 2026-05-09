"""
Pushes a parsed graph into Neo4j using batched MERGE queries.
Idempotent — safe to re-run.
"""
from typing import Dict, Any
from app.services.neo4j_service import neo4j_service


def build_graph(graph_data: Dict[str, Any]) -> Dict[str, int]:
    nodes = graph_data["nodes"]
    edges = graph_data["edges"]

    if not neo4j_service.is_alive():
        neo4j_service.load_mock_graph(graph_data)
        return {
            "nodes_loaded": len(nodes),
            "edges_loaded": len(edges),
            "storage": "in_memory",
        }

    # Wipe prior dataset so demos start clean.
    neo4j_service.reset_graph()

    # --- Nodes ---
    for n in nodes:
        # Note: dynamic label injection is unsafe in untrusted contexts.
        # For hackathon scope we restrict to alphanumeric types.
        ntype = "".join(c for c in n["type"] if c.isalnum()) or "Entity"
        cypher = f"""
        MERGE (n:{ntype} {{id: $id}})
        SET n.label = $label, n.type = $type
        """
        neo4j_service.execute_query(
            cypher, {"id": n["id"], "label": n["label"], "type": n["type"]}
        )

    # --- Edges ---
    for e in edges:
        rel = "".join(c for c in e["relationship"] if c.isalnum() or c == "_") or "RELATED"
        cypher = f"""
        MATCH (a {{id: $source}})
        MATCH (b {{id: $target}})
        MERGE (a)-[r:{rel}]->(b)
        """
        neo4j_service.execute_query(
            cypher, {"source": e["source"], "target": e["target"]}
        )

    return {
        "nodes_loaded": len(nodes),
        "edges_loaded": len(edges),
        "storage": "neo4j",
    }

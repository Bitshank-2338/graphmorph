"""
Shapes raw Cypher results into the UISchema dict the frontend renders.
Each query_type maps to a different transformation.
"""
from typing import Dict, Any, List


def _risk_band(connections: int, max_conn: int) -> str:
    if max_conn == 0:
        return "low"
    pct = connections / max_conn
    if pct >= 0.85:
        return "critical"
    if pct >= 0.6:
        return "high"
    if pct >= 0.35:
        return "medium"
    return "low"


def generate_default_ui(graph_data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "ui_type": "relationship_explorer",
        "title": "Runtime Relationship Explorer",
        "subtitle": (
            f"{graph_data['stats'].get('node_count', 0)} nodes · "
            f"{graph_data['stats'].get('edge_count', 0)} edges"
        ),
        "nodes": graph_data.get("reactflow_nodes", []),
        "edges": graph_data.get("reactflow_edges", []),
    }


def generate_ui(query_type: str, query: str, raw: List[Dict[str, Any]]) -> Dict[str, Any]:
    if query_type == "risk_matrix":
        max_conn = max((r.get("connections", 0) for r in raw), default=1)
        nodes = [
            {
                "id": r.get("label") or r.get("id") or "?",
                "label": r.get("label") or r.get("id") or "?",
                "risk": _risk_band(r.get("connections", 0), max_conn),
                "connections": r.get("connections", 0),
                "metric": round(r.get("connections", 0) / max_conn, 2) if max_conn else 0,
            }
            for r in raw
        ]
        return {
            "ui_type": "risk_matrix",
            "title": "Organizational Bottlenecks",
            "subtitle": f"Top {len(nodes)} highest-centrality nodes",
            "nodes": nodes,
            "insights": _risk_insights(nodes),
        }

    if query_type == "skill_gap_grid":
        if raw:
            max_head = max((r.get("headcount", 0) for r in raw), default=1)
            skills = [
                {
                    "name": r.get("skill", "?"),
                    "headcount": r.get("headcount", 0),
                    "coverage": round(100 * r.get("headcount", 0) / max_head, 1),
                }
                for r in raw
            ]
        else:
            skills = []
        return {
            "ui_type": "skill_gap_grid",
            "title": "Skill Coverage Analysis",
            "subtitle": f"{len(skills)} distinct skills detected",
            "skills": skills,
            "insights": _skill_insights(skills),
        }

    if query_type == "relationship_explorer":
        nodes_map: Dict[str, Dict[str, Any]] = {}
        edges: List[Dict[str, Any]] = []
        for i, r in enumerate(raw):
            sid, tid = r.get("source_id"), r.get("target_id")
            if sid and sid not in nodes_map:
                nodes_map[sid] = {
                    "id": sid,
                    "data": {"label": r.get("source_label"), "type": r.get("source_type")},
                    "position": {"x": (i % 10) * 120, "y": (i // 10) * 120},
                }
            if tid and tid not in nodes_map:
                nodes_map[tid] = {
                    "id": tid,
                    "data": {"label": r.get("target_label"), "type": r.get("target_type")},
                    "position": {"x": (i % 10) * 120 + 60, "y": (i // 10) * 120 + 200},
                }
            if sid and tid:
                edges.append({
                    "id": f"e-{i}",
                    "source": sid,
                    "target": tid,
                    "label": r.get("rel"),
                    "animated": True,
                })
        return {
            "ui_type": "relationship_explorer",
            "title": "Relationship Explorer",
            "subtitle": f"{len(nodes_map)} nodes · {len(edges)} edges",
            "nodes": list(nodes_map.values()),
            "edges": edges,
        }

    if query_type == "cluster_explorer":
        return {
            "ui_type": "cluster_explorer",
            "title": "Cluster Explorer",
            "subtitle": f"{len(raw)} clusters detected",
            "nodes": [
                {"id": r["cluster"], "label": r["cluster"],
                 "members": r.get("members", []), "size": r.get("size", 0)}
                for r in raw
            ],
        }

    if query_type == "simulation_workspace":
        max_conn = max((r.get("connections", 0) for r in raw), default=1)
        return {
            "ui_type": "simulation_workspace",
            "title": "Impact Simulation",
            "subtitle": f"What-if propagation across {len(raw)} candidate nodes",
            "nodes": [
                {
                    "id": r.get("label") or r.get("id"),
                    "connections": r.get("connections", 0),
                    "impact": round(r.get("connections", 0) / max_conn, 2),
                }
                for r in raw
            ],
        }

    # Fallback
    return generate_default_ui({"reactflow_nodes": [], "reactflow_edges": [],
                                "stats": {"node_count": 0, "edge_count": 0}})


def _risk_insights(nodes: List[Dict[str, Any]]) -> List[str]:
    if not nodes:
        return ["No bottlenecks detected — graph is well-distributed."]
    top = nodes[0]
    crits = [n for n in nodes if n["risk"] in ("critical", "high")]
    out = [f"{top['label']} is the highest-risk bottleneck "
           f"({top['connections']} direct connections)."]
    if len(crits) > 1:
        out.append(f"{len(crits)} nodes carry critical/high dependency load.")
    return out


def _skill_insights(skills: List[Dict[str, Any]]) -> List[str]:
    if not skills:
        return ["No skill data found in this dataset."]
    weakest = skills[-1]
    out = [f"Lowest coverage: '{weakest['name']}' "
           f"({weakest['headcount']} people)."]
    rare = [s for s in skills if s["headcount"] <= 1]
    if rare:
        out.append(f"{len(rare)} skill(s) held by a single person — bus-factor risk.")
    return out

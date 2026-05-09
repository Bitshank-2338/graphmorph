"""
Heuristic CSV → graph transformer.
Detects entity columns (Customer/Product, Employee/Department/Skills)
and produces nodes + edges + a ReactFlow-ready layout.

Far from perfect — but it adapts to the two demo datasets without config.
"""
from typing import Dict, Any, List
import math
import uuid
import pandas as pd


# Columns that look like entities; first match per category wins.
ENTITY_HINTS = {
    "person": ["employee", "name", "person", "user"],
    "department": ["department", "team", "dept"],
    "skill": ["skill", "skills", "expertise"],
    "role": ["role", "title", "position"],
    "customer": ["customer", "client", "account"],
    "product": ["product", "item", "sku"],
    "category": ["category", "segment"],
    "region": ["region", "country", "city"],
}


def _match_col(df: pd.DataFrame, hints: List[str]) -> str | None:
    cols_lower = {c.lower(): c for c in df.columns}
    for h in hints:
        for lc, original in cols_lower.items():
            if h in lc:
                return original
    return None


def _radial_position(idx: int, total: int, radius: float) -> Dict[str, float]:
    if total <= 0:
        return {"x": 0, "y": 0}
    angle = (2 * math.pi * idx) / max(total, 1)
    return {"x": radius * math.cos(angle), "y": radius * math.sin(angle)}


def transform_to_graph(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Returns:
      {
        "nodes": [...neo4j-shaped...],
        "edges": [...neo4j-shaped...],
        "reactflow_nodes": [...],
        "reactflow_edges": [...],
        "stats": {"node_count": n, "edge_count": m, "entity_types": [...]},
      }
    """
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []
    rf_nodes: List[Dict[str, Any]] = []
    rf_edges: List[Dict[str, Any]] = []
    seen: Dict[str, str] = {}  # label -> id (de-dup)

    def upsert(label: str, ntype: str) -> str:
        key = f"{ntype}::{label}"
        if key in seen:
            return seen[key]
        nid = str(uuid.uuid4())
        seen[key] = nid
        nodes.append({"id": nid, "label": label, "type": ntype})
        return nid

    detected = {k: _match_col(df, v) for k, v in ENTITY_HINTS.items()}
    detected = {k: v for k, v in detected.items() if v is not None}

    # ---- Strategy 1: Employee collaboration dataset ----
    if "person" in detected:
        person_col = detected["person"]
        dept_col = detected.get("department")
        skill_col = detected.get("skill")
        collab_col = next(
            (c for c in df.columns if "collab" in c.lower() or "works_with" in c.lower()),
            None,
        )

        for _, row in df.iterrows():
            person = str(row[person_col]).strip()
            if not person or person == "nan":
                continue
            pid = upsert(person, "Person")

            if dept_col and pd.notna(row[dept_col]):
                did = upsert(str(row[dept_col]).strip(), "Department")
                edges.append({"source": pid, "target": did, "relationship": "BELONGS_TO"})

            if skill_col and pd.notna(row[skill_col]):
                for sk in str(row[skill_col]).split(","):
                    sk = sk.strip()
                    if sk:
                        sid = upsert(sk, "Skill")
                        edges.append({"source": pid, "target": sid, "relationship": "HAS_SKILL"})

            if collab_col and pd.notna(row[collab_col]):
                for co in str(row[collab_col]).split(","):
                    co = co.strip()
                    if co:
                        # Treat as another Person (may be ID, may be name)
                        cid = upsert(co, "Person")
                        edges.append({"source": pid, "target": cid, "relationship": "WORKS_WITH"})

    # ---- Strategy 2: Customer/Product dataset (Superstore) ----
    elif "customer" in detected and "product" in detected:
        for _, row in df.iterrows():
            cust = str(row[detected["customer"]]).strip()
            prod = str(row[detected["product"]]).strip()
            if not cust or not prod:
                continue
            cid = upsert(cust, "Customer")
            pid = upsert(prod, "Product")
            edges.append({"source": cid, "target": pid, "relationship": "PURCHASED"})
            if "category" in detected:
                cat = str(row[detected["category"]]).strip()
                catid = upsert(cat, "Category")
                edges.append({"source": pid, "target": catid, "relationship": "IN_CATEGORY"})
            if "region" in detected:
                reg = str(row[detected["region"]]).strip()
                rid = upsert(reg, "Region")
                edges.append({"source": cid, "target": rid, "relationship": "IN_REGION"})

    # ---- Fallback: first column = entity, rest = attributes ----
    else:
        if df.empty:
            return {"nodes": [], "edges": [], "reactflow_nodes": [], "reactflow_edges": [], "stats": {}}
        primary_col = df.columns[0]
        for _, row in df.iterrows():
            primary = str(row[primary_col]).strip()
            if not primary:
                continue
            pid = upsert(primary, "Entity")
            for col in df.columns[1:]:
                val = row[col]
                if pd.isna(val):
                    continue
                aid = upsert(str(val).strip(), col)
                edges.append({"source": pid, "target": aid, "relationship": col.upper()})

    # ---- ReactFlow layout (radial by type) ----
    grouped: Dict[str, List[str]] = {}
    for n in nodes:
        grouped.setdefault(n["type"], []).append(n["id"])

    type_radii: Dict[str, float] = {}
    base_r = 250
    for i, t in enumerate(grouped):
        type_radii[t] = base_r + i * 200

    type_centers: Dict[str, Dict[str, float]] = {}
    n_types = max(len(grouped), 1)
    for i, t in enumerate(grouped):
        type_centers[t] = _radial_position(i, n_types, 600)

    for n in nodes:
        center = type_centers[n["type"]]
        siblings = grouped[n["type"]]
        idx = siblings.index(n["id"])
        offset = _radial_position(idx, len(siblings), 150)
        rf_nodes.append({
            "id": n["id"],
            "data": {"label": n["label"], "type": n["type"]},
            "position": {
                "x": center["x"] + offset["x"],
                "y": center["y"] + offset["y"],
            },
            "type": "default",
        })

    for e in edges:
        rf_edges.append({
            "id": str(uuid.uuid4()),
            "source": e["source"],
            "target": e["target"],
            "label": e["relationship"],
            "animated": False,
        })

    return {
        "nodes": nodes,
        "edges": edges,
        "reactflow_nodes": rf_nodes,
        "reactflow_edges": rf_edges,
        "stats": {
            "node_count": len(nodes),
            "edge_count": len(edges),
            "entity_types": list(grouped.keys()),
        },
    }

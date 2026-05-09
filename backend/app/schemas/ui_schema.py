"""
Hybrid UI schema. Two modes:
  1) template  — ui_type names a known component (risk_matrix, relationship_explorer, ...)
  2) generative — ui_type == 'generative', and `tree` holds a recursive primitive tree
                  the frontend's GenerativeRenderer interprets.
"""
from typing import List, Dict, Any, Optional, Literal, Union
from pydantic import BaseModel, Field


# ---- Generative primitives ----
class Primitive(BaseModel):
    """Recursive primitive node. Frontend whitelists `kind`."""
    kind: str = Field(
        ...,
        description="One of: container, grid, card, heading, text, "
                    "metric, badge, heatmap_cell, list, divider, slider, "
                    "graph, button",
    )
    props: Dict[str, Any] = Field(default_factory=dict)
    children: Optional[List["Primitive"]] = None


Primitive.model_rebuild()


# ---- Template payloads (typed for safety) ----
class RiskNode(BaseModel):
    id: str
    label: Optional[str] = None
    risk: Literal["low", "medium", "high", "critical"] = "medium"
    connections: int = 0
    metric: Optional[float] = None


class SkillCoverage(BaseModel):
    name: str
    coverage: float
    headcount: int = 0


class GraphNode(BaseModel):
    id: str
    data: Dict[str, Any]
    position: Dict[str, float] = Field(default_factory=lambda: {"x": 0, "y": 0})
    type: Optional[str] = None


class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    label: Optional[str] = None
    animated: bool = False


# ---- The schema ----
class UISchema(BaseModel):
    ui_type: str = Field(..., description="risk_matrix | relationship_explorer | "
                                         "skill_gap_grid | cluster_explorer | "
                                         "simulation_workspace | generative")
    title: str = "Runtime Workspace"
    subtitle: Optional[str] = None

    # Template-specific payloads (each renderer reads what it needs)
    nodes: Optional[List[Dict[str, Any]]] = None
    edges: Optional[List[Dict[str, Any]]] = None
    skills: Optional[List[Dict[str, Any]]] = None
    metrics: Optional[List[Dict[str, Any]]] = None
    insights: Optional[List[str]] = None

    # Generative tree (only when ui_type == 'generative')
    tree: Optional[Primitive] = None

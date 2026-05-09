from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    query: str = Field(..., description="Natural language question from user")
    context: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional prior workspace state, selected nodes, etc.",
    )


class QueryResponse(BaseModel):
    query_type: str
    cypher_query: str
    reasoning: list[str]
    raw_result: list[Dict[str, Any]]
    ui_schema: Dict[str, Any]

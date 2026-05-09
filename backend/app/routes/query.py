from fastapi import APIRouter

from app.schemas.query_schema import QueryRequest
from app.services.ai_agent import process_query

router = APIRouter()


@router.post("/query")
def query_agent(req: QueryRequest):
    return process_query(req.query)

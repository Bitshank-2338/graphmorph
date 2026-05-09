"""
GraphMorph agent - OpenAI-powered.

Pipeline:
  user query
    -> classify intent (OpenAI, with deterministic fallback)
    -> if simple template intent: use Cypher template + UI shaper
    -> if complex / "build me a custom view": ask OpenAI for a generative tree
    -> execute Cypher
    -> return reasoning stream + UI schema
"""
import json
import os
import re
from typing import Any, Dict, List, Tuple

from app.services.cypher_generator import generate_cypher
from app.services.neo4j_service import neo4j_service
from app.services.reasoning_engine import detect_query_type
from app.services.ui_generator import generate_ui

try:
    from openai import OpenAI

    _OPENAI_OK = True
except ImportError:
    _OPENAI_OK = False


_API_KEY = os.getenv("OPENAI_API_KEY")
_MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
_client = OpenAI(api_key=_API_KEY) if _OPENAI_OK and _API_KEY else None


def _load_prompt(name: str) -> str:
    path = os.path.join(os.path.dirname(__file__), "..", "prompts", name)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""


SYSTEM_PROMPT = _load_prompt("system_prompt.txt")
UI_GEN_PROMPT = _load_prompt("ui_generation_prompt.txt")


VALID_TYPES = {
    "risk_matrix",
    "relationship_explorer",
    "skill_gap_grid",
    "cluster_explorer",
    "simulation_workspace",
    "generative",
}


def _extract_json(text: str) -> Dict[str, Any] | None:
    """Pull a JSON object out of model text, tolerating fenced output."""
    if not text:
        return None
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    candidate = fenced.group(1) if fenced else text
    start = candidate.find("{")
    end = candidate.rfind("}")
    if start < 0 or end < 0:
        return None
    try:
        return json.loads(candidate[start : end + 1])
    except json.JSONDecodeError:
        return None


def _generate_json(prompt: str) -> Dict[str, Any] | None:
    """Call OpenAI and parse a JSON object from the response."""
    if not _client:
        return None

    response = _client.chat.completions.create(
        model=_MODEL_NAME,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT or "You are a JSON-only assistant.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    text = response.choices[0].message.content or ""
    return _extract_json(text)


def classify_intent(query: str) -> Tuple[str, List[str]]:
    """
    Return (query_type, reasoning_steps).
    Tries OpenAI first; falls back to keyword classifier.
    """
    reasoning: List[str] = []
    fallback = detect_query_type(query)

    if not _client:
        reasoning.append("LLM unavailable - using keyword classifier.")
        reasoning.append(f"Detected query type: {fallback}")
        return fallback, reasoning

    prompt = f"""{SYSTEM_PROMPT}

Classify the user query into ONE of these UI types:
- risk_matrix         (centrality, bottlenecks, key people, dependencies)
- relationship_explorer (paths, connections, traversal, "between X and Y")
- skill_gap_grid      (skills, capabilities, coverage, missing expertise)
- cluster_explorer    (communities, groupings, segments, teams)
- simulation_workspace (what-if, removal impact, scenarios)
- generative          (custom unusual layout the templates can't express)

Return STRICT JSON only:
{{"query_type": "<one_of_above>", "rationale": "<one short sentence>"}}

User query: {query!r}
"""
    try:
        parsed = _generate_json(prompt)
        if parsed and parsed.get("query_type") in VALID_TYPES:
            query_type = parsed["query_type"]
            reasoning.append(f"OpenAI classified intent -> {query_type}")
            if parsed.get("rationale"):
                reasoning.append(f"Rationale: {parsed['rationale']}")
            return query_type, reasoning
        reasoning.append("OpenAI returned malformed classification; falling back.")
    except Exception as e:
        reasoning.append(f"OpenAI call failed ({e.__class__.__name__}); falling back.")

    reasoning.append(f"Keyword classifier -> {fallback}")
    return fallback, reasoning


def generate_generative_tree(
    query: str, raw: List[Dict[str, Any]]
) -> Dict[str, Any] | None:
    """Ask OpenAI to emit a primitive tree for highly custom layouts."""
    if not _client:
        return None

    sample = raw[:8]
    prompt = f"""{UI_GEN_PROMPT}

User query: {query!r}
Cypher result sample (max 8 rows): {json.dumps(sample)}

Return STRICT JSON for a UISchema with ui_type="generative" and a `tree`
of primitive nodes. Allowed `kind` values:
container, grid, card, heading, text, metric, badge, heatmap_cell,
list, divider, slider, graph, button.

Format:
{{
  "ui_type": "generative",
  "title": "<short title>",
  "subtitle": "<one line>",
  "tree": {{
    "kind": "container",
    "props": {{...}},
    "children": [...]
  }}
}}
"""
    try:
        parsed = _generate_json(prompt)
        if parsed and parsed.get("ui_type") == "generative" and "tree" in parsed:
            return parsed
    except Exception as e:
        print(f"[agent] generative tree failed: {e}")
    return None


def process_query(query: str) -> Dict[str, Any]:
    reasoning: List[str] = [f"Received query: {query!r}"]

    query_type, cls_steps = classify_intent(query)
    reasoning.extend(cls_steps)

    cypher = generate_cypher(query_type)
    reasoning.append(f"Generated Cypher template for '{query_type}'")

    raw_result: List[Dict[str, Any]] = []
    try:
        raw_result = neo4j_service.execute_query(cypher)
        reasoning.append(f"Executed query -> {len(raw_result)} rows")
    except Exception as e:
        reasoning.append(f"Cypher execution failed: {e}")

    if query_type == "generative":
        tree_schema = generate_generative_tree(query, raw_result)
        if tree_schema:
            reasoning.append("Assembled generative UI tree")
            ui_schema = tree_schema
        else:
            reasoning.append("Generative tree unavailable; falling back to template")
            ui_schema = generate_ui("relationship_explorer", query, raw_result)
    else:
        ui_schema = generate_ui(query_type, query, raw_result)
        reasoning.append(f"Assembled {ui_schema['ui_type']} interface")

    return {
        "query_type": query_type,
        "cypher_query": cypher,
        "reasoning": reasoning,
        "raw_result": raw_result,
        "ui_schema": ui_schema,
    }

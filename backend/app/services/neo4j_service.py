"""
Neo4j driver wrapper with an in-memory fallback.

When Aura is unreachable, uploads still become the active runtime graph so
the demo can query the user's latest CSV instead of canned rows.
"""
import os
from collections import Counter, defaultdict
from typing import Any, Dict, List, Optional

from neo4j import Driver, GraphDatabase
from neo4j.exceptions import AuthError, ServiceUnavailable


class Neo4jService:
    def __init__(self) -> None:
        self.uri = os.getenv("NEO4J_URI")
        self.user = os.getenv("NEO4J_USERNAME", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD")
        self._driver: Optional[Driver] = None
        self._mock_store: Dict[str, Any] = {"nodes": [], "edges": []}
        self._connect()

    def _connect(self) -> None:
        if not self.uri or not self.password:
            print("[neo4j] No credentials - running in in-memory mode.")
            return
        try:
            self._driver = GraphDatabase.driver(
                self.uri, auth=(self.user, self.password)
            )
        except Exception as e:
            print(f"[neo4j] Driver init failed: {e}")
            self._driver = None

    def verify(self) -> bool:
        if not self._driver:
            return False
        try:
            self._driver.verify_connectivity()
            return True
        except (ServiceUnavailable, AuthError) as e:
            print(f"[neo4j] verify failed: {e}")
            return False

    def is_alive(self) -> bool:
        return self.verify() if self._driver else False

    def execute_query(
        self, query: str, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        if not self._driver:
            return self._mock_execute(query, params or {})
        try:
            with self._driver.session() as session:
                result = session.run(query, params or {})
                return [record.data() for record in result]
        except (ServiceUnavailable, AuthError) as e:
            print(f"[neo4j] query failed, using in-memory graph: {e}")
            return self._mock_execute(query, params or {})

    def reset_graph(self) -> None:
        if not self._driver:
            self._mock_store = {"nodes": [], "edges": []}
            return
        try:
            self.execute_query("MATCH (n) DETACH DELETE n")
        except Exception as e:
            print(f"[neo4j] reset failed, using in-memory graph: {e}")
            self._mock_store = {"nodes": [], "edges": []}

    def load_mock_graph(self, graph_data: Dict[str, Any]) -> None:
        self._mock_store = {
            "nodes": graph_data.get("nodes", []),
            "edges": graph_data.get("edges", []),
        }

    def close(self) -> None:
        if self._driver:
            self._driver.close()

    def _mock_execute(
        self, query: str, params: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        q = query.lower()
        nodes = self._mock_store.get("nodes", [])
        edges = self._mock_store.get("edges", [])
        by_id = {node["id"]: node for node in nodes}

        if "merge" in q or "create" in q or "detach delete" in q:
            return []

        if "match (a)-[r]->(b)" in q:
            return [
                {
                    "source_id": edge["source"],
                    "source_label": by_id.get(edge["source"], {}).get("label"),
                    "source_type": by_id.get(edge["source"], {}).get("type"),
                    "target_id": edge["target"],
                    "target_label": by_id.get(edge["target"], {}).get("label"),
                    "target_type": by_id.get(edge["target"], {}).get("type"),
                    "rel": edge["relationship"],
                }
                for edge in edges
                if edge["source"] in by_id and edge["target"] in by_id
            ][:80]

        if "s:skill" in q and "has_skill" in q:
            skill_people: Dict[str, set[str]] = defaultdict(set)
            for edge in edges:
                source = by_id.get(edge["source"], {})
                target = by_id.get(edge["target"], {})
                if (
                    edge["relationship"] == "HAS_SKILL"
                    and source.get("type") == "Person"
                    and target.get("type") == "Skill"
                ):
                    skill_people[target["label"]].add(source["id"])
            return [
                {"skill": skill, "headcount": len(people)}
                for skill, people in sorted(
                    skill_people.items(), key=lambda item: len(item[1]), reverse=True
                )
            ][:20]

        if "d:department" in q and "belongs_to" in q:
            dept_people: Dict[str, list[str]] = defaultdict(list)
            for edge in edges:
                source = by_id.get(edge["source"], {})
                target = by_id.get(edge["target"], {})
                if (
                    edge["relationship"] == "BELONGS_TO"
                    and source.get("type") == "Person"
                    and target.get("type") == "Department"
                ):
                    dept_people[target["label"]].append(source["label"])
            return [
                {"cluster": dept, "members": members, "size": len(members)}
                for dept, members in sorted(
                    dept_people.items(), key=lambda item: len(item[1]), reverse=True
                )
            ]

        if "n:person" in q and "count(distinct m)" in q:
            neighbors: Dict[str, set[str]] = defaultdict(set)
            for edge in edges:
                source = by_id.get(edge["source"], {})
                target = by_id.get(edge["target"], {})
                if source.get("type") == "Person":
                    neighbors[source["id"]].add(edge["target"])
                if target.get("type") == "Person":
                    neighbors[target["id"]].add(edge["source"])
            counts = Counter({node_id: len(linked) for node_id, linked in neighbors.items()})
            return [
                {
                    "id": node_id,
                    "label": by_id[node_id]["label"],
                    "connections": count,
                }
                for node_id, count in counts.most_common(20)
                if by_id.get(node_id, {}).get("type") == "Person"
            ]

        return []


neo4j_service = Neo4jService()

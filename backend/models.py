"""
Core knowledge graph data models.

Entities are nodes in the graph with types and properties.
Relations are directed edges between entities with types and properties.
"""

import json
import uuid
from dataclasses import dataclass, field
from typing import Any


def new_uuid() -> str:
    """Generate a new UUID string."""
    return str(uuid.uuid4())


def serialize_json(obj: Any) -> str:
    """Serialize object to JSON string."""
    return json.dumps(obj, ensure_ascii=False)


def deserialize_json(text: str) -> Any:
    """Deserialize JSON string to object."""
    return json.loads(text)


@dataclass
class Entity:
    """
    An entity in the knowledge graph.

    Entities represent things that exist: concepts, resources, people, collections, etc.
    Each entity has:
    - Unique identifier
    - One or more type labels (e.g., ["Concept"], ["Resource", "Video"])
    - Arbitrary properties as key-value pairs
    """

    id: str
    types: list[str]
    properties: dict[str, Any] = field(default_factory=dict)

    def has_type(self, type_name: str) -> bool:
        """Check if entity has a specific type."""
        return type_name in self.types

    def to_dict(self) -> dict[str, Any]:
        """Convert entity to dictionary for API responses."""
        return {
            "id": self.id,
            "types": self.types,
            "properties": self.properties
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Entity":
        """Create entity from dictionary."""
        return cls(
            id=data["id"],
            types=data["types"],
            properties=data.get("properties", {})
        )


@dataclass
class Relation:
    """
    A directed, typed relation between two entities.

    Relations represent connections in the knowledge graph.
    Each relation has:
    - Unique identifier
    - Source entity (from_entity)
    - Target entity (to_entity)
    - Relation type (semantic predicate like "EXEMPLIFIES", "REQUIRES")
    - Optional properties (metadata like strength, rationale, timestamp)
    """

    id: str
    from_entity: str
    to_entity: str
    relation_type: str
    properties: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert relation to dictionary for API responses."""
        return {
            "id": self.id,
            "from_entity": self.from_entity,
            "to_entity": self.to_entity,
            "relation_type": self.relation_type,
            "properties": self.properties
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Relation":
        """Create relation from dictionary."""
        return cls(
            id=data["id"],
            from_entity=data["from_entity"],
            to_entity=data["to_entity"],
            relation_type=data["relation_type"],
            properties=data.get("properties", {})
        )

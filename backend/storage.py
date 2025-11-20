"""
Knowledge graph storage using SQLite with aiosqlite.

Direct SQL implementation without ORM - simple, fast, and transparent.
"""

import aiosqlite
from typing import Optional
from .models import Entity, Relation, new_uuid, serialize_json, deserialize_json


class KnowledgeGraph:
    """
    Knowledge graph storage using SQLite.

    Stores entities and relations with JSON properties.
    Provides async CRUD operations and graph traversal.
    """

    def __init__(self, db_path: str = "connections.db"):
        """Initialize knowledge graph with database path."""
        self.db_path = db_path
        self.conn: Optional[aiosqlite.Connection] = None

    async def connect(self):
        """Open database connection and initialize schema."""
        self.conn = await aiosqlite.connect(self.db_path)
        self.conn.row_factory = aiosqlite.Row
        await self.conn.execute("PRAGMA foreign_keys = ON")
        await self._init_schema()

    async def close(self):
        """Close database connection."""
        if self.conn:
            await self.conn.close()

    async def _init_schema(self):
        """Create tables if they don't exist."""
        await self.conn.execute("""
            CREATE TABLE IF NOT EXISTS entities (
                id TEXT PRIMARY KEY,
                types TEXT NOT NULL,
                properties TEXT NOT NULL
            )
        """)
        await self.conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_entity_types ON entities(types)
        """)

        await self.conn.execute("""
            CREATE TABLE IF NOT EXISTS relations (
                id TEXT PRIMARY KEY,
                from_entity TEXT NOT NULL,
                to_entity TEXT NOT NULL,
                relation_type TEXT NOT NULL,
                properties TEXT NOT NULL,
                FOREIGN KEY (from_entity) REFERENCES entities(id) ON DELETE CASCADE,
                FOREIGN KEY (to_entity) REFERENCES entities(id) ON DELETE CASCADE
            )
        """)
        await self.conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_relation_from ON relations(from_entity, relation_type)
        """)
        await self.conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_relation_to ON relations(to_entity, relation_type)
        """)
        await self.conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_relation_type ON relations(relation_type)
        """)
        await self.conn.commit()

    # Entity operations

    async def create_entity(self, entity: Entity) -> Entity:
        """Create a new entity."""
        if not entity.id:
            entity.id = new_uuid()

        await self.conn.execute(
            "INSERT INTO entities (id, types, properties) VALUES (?, ?, ?)",
            (entity.id, serialize_json(entity.types), serialize_json(entity.properties))
        )
        await self.conn.commit()
        return entity

    async def get_entity(self, entity_id: str) -> Optional[Entity]:
        """Get entity by ID."""
        async with self.conn.execute(
            "SELECT id, types, properties FROM entities WHERE id = ?",
            (entity_id,)
        ) as cursor:
            row = await cursor.fetchone()
            if not row:
                return None

            return Entity(
                id=row["id"],
                types=deserialize_json(row["types"]),
                properties=deserialize_json(row["properties"])
            )

    async def update_entity(self, entity: Entity) -> Entity:
        """Update an existing entity."""
        result = await self.conn.execute(
            "UPDATE entities SET types = ?, properties = ? WHERE id = ?",
            (serialize_json(entity.types), serialize_json(entity.properties), entity.id)
        )
        await self.conn.commit()

        if result.rowcount == 0:
            raise ValueError(f"Entity {entity.id} not found")

        return entity

    async def delete_entity(self, entity_id: str) -> bool:
        """Delete an entity."""
        result = await self.conn.execute(
            "DELETE FROM entities WHERE id = ?",
            (entity_id,)
        )
        await self.conn.commit()
        return result.rowcount > 0

    async def list_entities(
        self,
        types: Optional[list[str]] = None,
        limit: int = 100,
        offset: int = 0
    ) -> list[Entity]:
        """List entities with optional type filtering and pagination."""
        if types:
            # Filter by types using JSON LIKE queries
            type_conditions = " OR ".join(["types LIKE ?"] * len(types))
            query = f"""
                SELECT id, types, properties FROM entities
                WHERE {type_conditions}
                LIMIT ? OFFSET ?
            """
            params = [f'%"{t}"%' for t in types] + [limit, offset]
        else:
            query = "SELECT id, types, properties FROM entities LIMIT ? OFFSET ?"
            params = [limit, offset]

        entities = []
        async with self.conn.execute(query, params) as cursor:
            async for row in cursor:
                entities.append(Entity(
                    id=row["id"],
                    types=deserialize_json(row["types"]),
                    properties=deserialize_json(row["properties"])
                ))

        return entities

    # Relation operations

    async def create_relation(self, relation: Relation) -> Relation:
        """Create a new relation."""
        if not relation.id:
            relation.id = new_uuid()

        # Validate that both entities exist
        from_exists = await self.get_entity(relation.from_entity)
        to_exists = await self.get_entity(relation.to_entity)

        if not from_exists:
            raise ValueError(f"Source entity {relation.from_entity} not found")
        if not to_exists:
            raise ValueError(f"Target entity {relation.to_entity} not found")

        await self.conn.execute(
            """INSERT INTO relations
               (id, from_entity, to_entity, relation_type, properties)
               VALUES (?, ?, ?, ?, ?)""",
            (relation.id, relation.from_entity, relation.to_entity,
             relation.relation_type, serialize_json(relation.properties))
        )
        await self.conn.commit()
        return relation

    async def get_relation(self, relation_id: str) -> Optional[Relation]:
        """Get relation by ID."""
        async with self.conn.execute(
            """SELECT id, from_entity, to_entity, relation_type, properties
               FROM relations WHERE id = ?""",
            (relation_id,)
        ) as cursor:
            row = await cursor.fetchone()
            if not row:
                return None

            return Relation(
                id=row["id"],
                from_entity=row["from_entity"],
                to_entity=row["to_entity"],
                relation_type=row["relation_type"],
                properties=deserialize_json(row["properties"])
            )

    async def delete_relation(self, relation_id: str) -> bool:
        """Delete a relation."""
        result = await self.conn.execute(
            "DELETE FROM relations WHERE id = ?",
            (relation_id,)
        )
        await self.conn.commit()
        return result.rowcount > 0

    async def get_relations_from(
        self,
        entity_id: str,
        relation_type: Optional[str] = None
    ) -> list[Relation]:
        """Get all outgoing relations from an entity."""
        if relation_type:
            query = """SELECT id, from_entity, to_entity, relation_type, properties
                       FROM relations
                       WHERE from_entity = ? AND relation_type = ?"""
            params = (entity_id, relation_type)
        else:
            query = """SELECT id, from_entity, to_entity, relation_type, properties
                       FROM relations WHERE from_entity = ?"""
            params = (entity_id,)

        relations = []
        async with self.conn.execute(query, params) as cursor:
            async for row in cursor:
                relations.append(Relation(
                    id=row["id"],
                    from_entity=row["from_entity"],
                    to_entity=row["to_entity"],
                    relation_type=row["relation_type"],
                    properties=deserialize_json(row["properties"])
                ))

        return relations

    async def get_relations_to(
        self,
        entity_id: str,
        relation_type: Optional[str] = None
    ) -> list[Relation]:
        """Get all incoming relations to an entity."""
        if relation_type:
            query = """SELECT id, from_entity, to_entity, relation_type, properties
                       FROM relations
                       WHERE to_entity = ? AND relation_type = ?"""
            params = (entity_id, relation_type)
        else:
            query = """SELECT id, from_entity, to_entity, relation_type, properties
                       FROM relations WHERE to_entity = ?"""
            params = (entity_id,)

        relations = []
        async with self.conn.execute(query, params) as cursor:
            async for row in cursor:
                relations.append(Relation(
                    id=row["id"],
                    from_entity=row["from_entity"],
                    to_entity=row["to_entity"],
                    relation_type=row["relation_type"],
                    properties=deserialize_json(row["properties"])
                ))

        return relations

    async def get_relations_between(self, from_id: str, to_id: str) -> list[Relation]:
        """Get all relations connecting two entities."""
        relations = []
        async with self.conn.execute(
            """SELECT id, from_entity, to_entity, relation_type, properties
               FROM relations
               WHERE from_entity = ? AND to_entity = ?""",
            (from_id, to_id)
        ) as cursor:
            async for row in cursor:
                relations.append(Relation(
                    id=row["id"],
                    from_entity=row["from_entity"],
                    to_entity=row["to_entity"],
                    relation_type=row["relation_type"],
                    properties=deserialize_json(row["properties"])
                ))

        return relations

    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()

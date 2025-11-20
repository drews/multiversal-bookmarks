"""
Bootstrap the knowledge graph with foundational meta-entities.

Creates entities that define the core types themselves:
- EntityType entities (Concept, Resource, Person, Collection, etc.)
- RelationType entities (EXEMPLIFIES, REQUIRES, DEFINES, etc.)

This makes the schema self-documenting and evolvable within the graph.
"""

import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.storage import KnowledgeGraph
from backend.models import Entity, Relation, new_uuid


async def bootstrap():
    """Bootstrap foundational entities."""
    async with KnowledgeGraph() as kg:
        print("🌱 Bootstrapping knowledge graph...\n")

        # Check if already bootstrapped
        existing = await kg.list_entities(types=["EntityType"], limit=1)
        if existing:
            print("⚠️  Already bootstrapped. Use reset_db.sh to start fresh.\n")
            return

        # Create EntityType entities
        print("📦 Creating EntityType entities...")

        entity_types = [
            {
                "name": "Concept",
                "definition": "Abstract idea, topic, skill, or method to be learned or taught",
                "properties": ["name", "definition", "scope", "aliases", "disambiguation", "maturity"],
                "examples": ["Python Async Programming", "RESTful API Design", "Database Normalization"]
            },
            {
                "name": "Resource",
                "definition": "Concrete artifact (URL, book, video, tool) that provides information",
                "properties": ["url", "title", "description", "content_type", "author", "published_at", "authority_score"],
                "examples": ["FastAPI documentation", "YouTube tutorial", "Academic paper PDF"]
            },
            {
                "name": "Person",
                "definition": "Contributor, author, or educator in the knowledge graph",
                "properties": ["name", "identifier", "bio", "expertise"],
                "examples": ["Faculty member", "Student", "External author"]
            },
            {
                "name": "Collection",
                "definition": "Curated grouping of concepts and resources with specific purpose",
                "properties": ["name", "description", "collection_type", "created_by"],
                "examples": ["Learning path", "Reading list", "Course materials"]
            },
            {
                "name": "Tag",
                "definition": "Lightweight metadata label for categorization",
                "properties": ["name", "type", "color"],
                "examples": ["beginner", "video", "python", "advanced"]
            },
            {
                "name": "EntityType",
                "definition": "Meta-entity defining what types of entities exist in the knowledge graph",
                "properties": ["name", "definition", "properties", "examples"],
                "examples": ["Concept", "Resource", "Person"]
            },
            {
                "name": "RelationType",
                "definition": "Meta-entity defining what types of semantic relations exist",
                "properties": ["name", "definition", "domain", "range", "properties"],
                "examples": ["EXEMPLIFIES", "REQUIRES", "IS_A"]
            }
        ]

        entity_type_ids = {}
        for et in entity_types:
            entity = Entity(
                id=new_uuid(),
                types=["EntityType"],
                properties=et
            )
            created = await kg.create_entity(entity)
            entity_type_ids[et["name"]] = created.id
            print(f"  ✓ {et['name']}")

        print(f"\n📊 Created {len(entity_types)} EntityType entities\n")

        # Create RelationType entities
        print("🔗 Creating RelationType entities...")

        relation_types = [
            {
                "name": "EXEMPLIFIES",
                "definition": "Resource provides concrete example of Concept",
                "domain": "Resource",
                "range": "Concept",
                "properties": ["strength", "rationale"],
                "inverse": "HAS_EXAMPLE"
            },
            {
                "name": "EXPLAINS",
                "definition": "Resource teaches or explains Concept",
                "domain": "Resource",
                "range": "Concept",
                "properties": ["depth", "target_audience"],
                "inverse": "EXPLAINED_BY"
            },
            {
                "name": "DEFINES",
                "definition": "Resource authoritatively defines Concept",
                "domain": "Resource",
                "range": "Concept",
                "properties": ["authority_level"],
                "inverse": "DEFINED_BY"
            },
            {
                "name": "SPECIFIES",
                "definition": "Resource is formal specification of Concept",
                "domain": "Resource",
                "range": "Concept",
                "properties": ["spec_type"],
                "inverse": "SPECIFIED_BY"
            },
            {
                "name": "CRITIQUES",
                "definition": "Resource critiques or challenges Concept",
                "domain": "Resource",
                "range": "Concept",
                "properties": ["critique_type"],
                "inverse": "CRITIQUED_BY"
            },
            {
                "name": "IMPLEMENTS",
                "definition": "Resource is working implementation of Concept",
                "domain": "Resource",
                "range": "Concept",
                "properties": ["language", "completeness"],
                "inverse": "IMPLEMENTED_BY"
            },
            {
                "name": "REQUIRES",
                "definition": "Concept requires understanding of another Concept as prerequisite",
                "domain": "Concept",
                "range": "Concept",
                "properties": ["difficulty_jump", "optional"],
                "inverse": "PREREQUISITE_FOR"
            },
            {
                "name": "IS_A",
                "definition": "Concept is a type/subclass of another Concept",
                "domain": "Concept",
                "range": "Concept",
                "properties": [],
                "inverse": "HAS_SUBTYPE"
            },
            {
                "name": "PART_OF",
                "definition": "Concept is component/aspect of another Concept",
                "domain": "Concept",
                "range": "Concept",
                "properties": [],
                "inverse": "HAS_PART"
            },
            {
                "name": "RELATED_TO",
                "definition": "Concept is loosely associated with another Concept",
                "domain": "Concept",
                "range": "Concept",
                "properties": ["strength", "nature"],
                "inverse": "RELATED_TO"
            },
            {
                "name": "ALTERNATIVE_TO",
                "definition": "Concept is different approach to same problem as another Concept",
                "domain": "Concept",
                "range": "Concept",
                "properties": ["tradeoffs"],
                "inverse": "ALTERNATIVE_TO"
            },
            {
                "name": "SUPERSEDES",
                "definition": "Concept replaces or updates another Concept (temporal evolution)",
                "domain": "Concept",
                "range": "Concept",
                "properties": ["migration_guide"],
                "inverse": "SUPERSEDED_BY"
            },
            {
                "name": "CONTRIBUTED_BY",
                "definition": "Entity or Relation was contributed by Person",
                "domain": "Entity | Relation",
                "range": "Person",
                "properties": ["contributed_at", "rationale"],
                "inverse": "CONTRIBUTED"
            },
            {
                "name": "VERIFIED_BY",
                "definition": "Assertion verified by Person",
                "domain": "Relation",
                "range": "Person",
                "properties": ["verified_at", "confidence"],
                "inverse": "VERIFIED"
            },
            {
                "name": "CONTAINS",
                "definition": "Collection contains Entity",
                "domain": "Collection",
                "range": "Entity",
                "properties": ["position", "annotation"],
                "inverse": "CONTAINED_IN"
            },
            {
                "name": "TAGGED_WITH",
                "definition": "Entity is tagged with Tag for categorization",
                "domain": "Entity",
                "range": "Tag",
                "properties": [],
                "inverse": "TAGS"
            },
            {
                "name": "INSTANCE_OF",
                "definition": "Entity is instance of EntityType",
                "domain": "Entity",
                "range": "EntityType",
                "properties": [],
                "inverse": "HAS_INSTANCE"
            },
            {
                "name": "TYPE_OF",
                "definition": "Relation is instance of RelationType",
                "domain": "Relation",
                "range": "RelationType",
                "properties": [],
                "inverse": "TYPES_RELATION"
            }
        ]

        relation_type_ids = {}
        for rt in relation_types:
            entity = Entity(
                id=new_uuid(),
                types=["RelationType"],
                properties=rt
            )
            created = await kg.create_entity(entity)
            relation_type_ids[rt["name"]] = created.id
            print(f"  ✓ {rt['name']}")

        print(f"\n🔗 Created {len(relation_types)} RelationType entities\n")

        # Create meta-relations: EntityTypes are instances of EntityType
        print("🔄 Creating meta-relations...")

        for type_name, type_id in entity_type_ids.items():
            relation = Relation(
                id=new_uuid(),
                from_entity=type_id,
                to_entity=entity_type_ids["EntityType"],
                relation_type="INSTANCE_OF",
                properties={}
            )
            await kg.create_relation(relation)
            print(f"  ✓ {type_name} INSTANCE_OF EntityType")

        # RelationTypes are instances of RelationType
        for type_name, type_id in relation_type_ids.items():
            relation = Relation(
                id=new_uuid(),
                from_entity=type_id,
                to_entity=entity_type_ids["RelationType"],
                relation_type="INSTANCE_OF",
                properties={}
            )
            await kg.create_relation(relation)
            print(f"  ✓ {type_name} INSTANCE_OF RelationType")

        print("\n✨ Bootstrap complete!\n")
        print("📊 Summary:")
        print(f"  - {len(entity_types)} EntityType entities")
        print(f"  - {len(relation_types)} RelationType entities")
        print(f"  - {len(entity_type_ids) + len(relation_type_ids)} meta-relations")
        print("\n🌐 View at http://localhost:8000\n")


if __name__ == "__main__":
    asyncio.run(bootstrap())

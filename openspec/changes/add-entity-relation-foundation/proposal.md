# Proposal: Add Entity-Relation Foundation

**Change ID:** `add-entity-relation-foundation`
**Type:** New Capability
**Status:** Proposed
**Author:** drewby
**Date:** 2024-11-19

## Why

Establish the foundational knowledge graph primitives (entities and relations) that will support all knowledge organization features. This is the bedrock upon which concepts, resources, connections, and discovery will be built.

Following semantic web and property graph best practices, we need a flexible model that:
- Treats everything meaningful as an entity with identity
- Models connections as typed, directed relations
- Supports rich metadata on both entities and relations
- Remains storage-agnostic (can map to SQL, graph DB, triple store)

## What Changes

### Core Abstractions

**Entity Model:**
```python
Entity:
  - id: UUID (stable identifier)
  - types: Set[str] (can have multiple labels: ["Concept"], ["Resource", "Video"])
  - properties: Dict[str, Any] (attributes as key-value pairs)
```

**Relation Model:**
```python
Relation:
  - id: UUID (optional, for referencing relations)
  - from_entity: UUID
  - to_entity: UUID
  - relation_type: str (semantic predicate)
  - properties: Dict[str, Any] (metadata about the relation)
```

### Key Principles

1. **Everything is an entity** - Concepts, resources, people, collections, tags
2. **Connections are typed relations** - Not just foreign keys, but semantic predicates
3. **Properties vs Relations** - Properties are literals, relations connect entities
4. **Flexible schema** - New entity types and relation types can be added without migration
5. **Storage agnostic** - Model maps to any backend (SQL, Neo4j, RDF)

### Initial Implementation

Simple Python data classes that can be persisted to SQLite:
- `entities` table with id, types (JSON array), properties (JSON object)
- `relations` table with id, from_entity, to_entity, relation_type, properties (JSON)

## Impact

### Affected Specs
- `specs/knowledge-organization/spec.md` - Adds foundational data model requirements

### Affected Code
- New: `backend/models.py` - Entity and Relation data classes
- New: `backend/storage.py` - Abstract storage interface
- New: `backend/sqlite_storage.py` - SQLite implementation of storage

### Benefits

✅ **Flexible schema evolution** - Add new entity/relation types without breaking changes
✅ **Rich semantics** - Relations have meaning beyond foreign keys
✅ **Provenance-ready** - Can attach metadata to any relation
✅ **Query-friendly** - Graph traversal patterns work naturally
✅ **Future-proof** - Can swap storage backends or add inference layer

### Risks

**Low Risk:**
- Well-established pattern from Neo4j, Wikidata, RDF
- Simple to implement in SQLite initially
- Can optimize later without changing model

## Next Steps

1. Get approval for this foundational approach
2. Implement core Entity and Relation classes
3. Create SQLite storage adapter
4. Add basic CRUD operations
5. Validate with simple CLI or web interface

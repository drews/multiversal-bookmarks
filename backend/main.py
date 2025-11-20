"""
FastAPI application for the Connections knowledge graph.

REST API for entities and relations with automatic OpenAPI docs.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import Optional
from contextlib import asynccontextmanager

from .storage import KnowledgeGraph
from .models import Entity, Relation, new_uuid


# Global knowledge graph instance
kg: Optional[KnowledgeGraph] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage knowledge graph lifecycle."""
    global kg
    kg = KnowledgeGraph()
    await kg.connect()
    print("✓ Knowledge graph connected")
    yield
    await kg.close()
    print("✓ Knowledge graph closed")


# Create FastAPI app
app = FastAPI(
    title="Connections API",
    description="Knowledge graph for themultiverse.school",
    version="0.1.0",
    lifespan=lifespan
)

# Enable CORS for all origins (development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_kg() -> KnowledgeGraph:
    """Dependency injection for knowledge graph."""
    if kg is None:
        raise HTTPException(status_code=500, detail="Knowledge graph not initialized")
    return kg


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


# Entity endpoints

@app.post("/api/entities", status_code=201)
async def create_entity(
    types: list[str],
    properties: dict = {}
):
    """Create a new entity."""
    entity = Entity(
        id=new_uuid(),
        types=types,
        properties=properties
    )
    created = await get_kg().create_entity(entity)
    return created.to_dict()


@app.get("/api/entities/{entity_id}")
async def get_entity(entity_id: str):
    """Get entity by ID."""
    entity = await get_kg().get_entity(entity_id)
    if not entity:
        raise HTTPException(status_code=404, detail=f"Entity {entity_id} not found")
    return entity.to_dict()


@app.get("/api/entities")
async def list_entities(
    types: Optional[list[str]] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """List entities with optional type filtering and pagination."""
    entities = await get_kg().list_entities(types=types, limit=limit, offset=offset)
    return {
        "entities": [e.to_dict() for e in entities],
        "count": len(entities),
        "limit": limit,
        "offset": offset
    }


@app.put("/api/entities/{entity_id}")
async def update_entity(
    entity_id: str,
    types: list[str],
    properties: dict = {}
):
    """Update an entity."""
    entity = Entity(id=entity_id, types=types, properties=properties)
    try:
        updated = await get_kg().update_entity(entity)
        return updated.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.delete("/api/entities/{entity_id}", status_code=204)
async def delete_entity(entity_id: str):
    """Delete an entity."""
    deleted = await get_kg().delete_entity(entity_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Entity {entity_id} not found")


# Relation endpoints

@app.post("/api/relations", status_code=201)
async def create_relation(
    from_entity: str,
    to_entity: str,
    relation_type: str,
    properties: dict = {}
):
    """Create a new relation."""
    relation = Relation(
        id=new_uuid(),
        from_entity=from_entity,
        to_entity=to_entity,
        relation_type=relation_type,
        properties=properties
    )
    try:
        created = await get_kg().create_relation(relation)
        return created.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/relations/{relation_id}")
async def get_relation(relation_id: str):
    """Get relation by ID."""
    relation = await get_kg().get_relation(relation_id)
    if not relation:
        raise HTTPException(status_code=404, detail=f"Relation {relation_id} not found")
    return relation.to_dict()


@app.delete("/api/relations/{relation_id}", status_code=204)
async def delete_relation(relation_id: str):
    """Delete a relation."""
    deleted = await get_kg().delete_relation(relation_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Relation {relation_id} not found")


@app.get("/api/entities/{entity_id}/relations/outgoing")
async def get_outgoing_relations(
    entity_id: str,
    relation_type: Optional[str] = None
):
    """Get all outgoing relations from an entity."""
    relations = await get_kg().get_relations_from(entity_id, relation_type)
    return {
        "entity_id": entity_id,
        "direction": "outgoing",
        "relation_type": relation_type,
        "relations": [r.to_dict() for r in relations],
        "count": len(relations)
    }


@app.get("/api/entities/{entity_id}/relations/incoming")
async def get_incoming_relations(
    entity_id: str,
    relation_type: Optional[str] = None
):
    """Get all incoming relations to an entity."""
    relations = await get_kg().get_relations_to(entity_id, relation_type)
    return {
        "entity_id": entity_id,
        "direction": "incoming",
        "relation_type": relation_type,
        "relations": [r.to_dict() for r in relations],
        "count": len(relations)
    }


# Serve static files
try:
    app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
except RuntimeError:
    # Frontend directory doesn't exist yet
    @app.get("/")
    async def root():
        return {"message": "Frontend not yet available. API docs at /docs"}

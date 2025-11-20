# Tasks: Add Entity-Relation Foundation

**Change ID:** `add-entity-relation-foundation`

## Implementation Checklist

### Phase 1: Project Setup with uv

- [ ] Initialize Python project:
  - [ ] `uv init` - Create pyproject.toml
  - [ ] Configure Python 3.11+ requirement
  - [ ] Add project metadata (name, description, authors)

- [ ] Add dependencies:
  - [ ] `uv add fastapi`
  - [ ] `uv add "uvicorn[standard]"`
  - [ ] `uv add aiosqlite`
  - [ ] `uv add httpx` (for future metadata extraction)
  - [ ] `uv add beautifulsoup4` (for future metadata extraction)

- [ ] Create `.python-version` file:
  - [ ] Specify `3.11` for uv to use

### Phase 2: Core Data Models

- [ ] Create `backend/models.py`:
  - [ ] `Entity` dataclass:
    - [ ] `id: str` (UUID as string)
    - [ ] `types: list[str]` (entity labels)
    - [ ] `properties: dict[str, Any]` (flexible attributes)
    - [ ] Helper: `has_type(type_name: str) -> bool`
  - [ ] `Relation` dataclass:
    - [ ] `id: str` (UUID as string)
    - [ ] `from_entity: str` (source UUID)
    - [ ] `to_entity: str` (target UUID)
    - [ ] `relation_type: str` (semantic predicate)
    - [ ] `properties: dict[str, Any]` (relation metadata)
  - [ ] Utility functions:
    - [ ] `new_uuid() -> str` (generate UUID string)
    - [ ] `serialize_json(obj) -> str` (JSON encoder)
    - [ ] `deserialize_json(text) -> Any` (JSON decoder)

### Phase 3: Storage Layer (Direct aiosqlite)

- [ ] Create `backend/storage.py`:
  - [ ] `KnowledgeGraph` class with async context manager
  - [ ] `__init__(db_path: str)` constructor
  - [ ] `async connect()` - open aiosqlite connection
  - [ ] `async close()` - close connection gracefully
  - [ ] `async _init_schema()` - create tables if not exist:
    ```sql
    CREATE TABLE IF NOT EXISTS entities (
      id TEXT PRIMARY KEY,
      types TEXT NOT NULL,  -- JSON array
      properties TEXT NOT NULL  -- JSON object
    );
    CREATE INDEX IF NOT EXISTS idx_entity_types ON entities(types);

    CREATE TABLE IF NOT EXISTS relations (
      id TEXT PRIMARY KEY,
      from_entity TEXT NOT NULL,
      to_entity TEXT NOT NULL,
      relation_type TEXT NOT NULL,
      properties TEXT NOT NULL,  -- JSON object
      FOREIGN KEY (from_entity) REFERENCES entities(id) ON DELETE CASCADE,
      FOREIGN KEY (to_entity) REFERENCES entities(id) ON DELETE CASCADE
    );
    CREATE INDEX IF NOT EXISTS idx_relation_from ON relations(from_entity, relation_type);
    CREATE INDEX IF NOT EXISTS idx_relation_to ON relations(to_entity, relation_type);
    CREATE INDEX IF NOT EXISTS idx_relation_type ON relations(relation_type);
    ```

- [ ] Entity operations:
  - [ ] `async create_entity(entity: Entity) -> Entity`
  - [ ] `async get_entity(entity_id: str) -> Entity | None`
  - [ ] `async update_entity(entity: Entity) -> Entity`
  - [ ] `async delete_entity(entity_id: str) -> bool`
  - [ ] `async list_entities(types: list[str] | None = None, limit: int = 100, offset: int = 0) -> list[Entity]`

- [ ] Relation operations:
  - [ ] `async create_relation(relation: Relation) -> Relation`
  - [ ] `async get_relation(relation_id: str) -> Relation | None`
  - [ ] `async delete_relation(relation_id: str) -> bool`
  - [ ] `async get_relations_from(entity_id: str, relation_type: str | None = None) -> list[Relation]`
  - [ ] `async get_relations_to(entity_id: str, relation_type: str | None = None) -> list[Relation]`
  - [ ] `async get_relations_between(from_id: str, to_id: str) -> list[Relation]`

### Phase 4: FastAPI Application

- [ ] Create `backend/main.py`:
  - [ ] FastAPI app initialization
  - [ ] CORS middleware (allow all origins for now)
  - [ ] Startup event: Initialize KnowledgeGraph
  - [ ] Shutdown event: Close KnowledgeGraph
  - [ ] Dependency injection: `get_kg() -> KnowledgeGraph`

- [ ] Entity endpoints:
  - [ ] `POST /api/entities` - Create entity
  - [ ] `GET /api/entities/{id}` - Get entity by ID
  - [ ] `GET /api/entities` - List entities (with query params: types, limit, offset)
  - [ ] `PUT /api/entities/{id}` - Update entity
  - [ ] `DELETE /api/entities/{id}` - Delete entity

- [ ] Relation endpoints:
  - [ ] `POST /api/relations` - Create relation
  - [ ] `GET /api/relations/{id}` - Get relation by ID
  - [ ] `DELETE /api/relations/{id}` - Delete relation
  - [ ] `GET /api/entities/{id}/relations/outgoing` - Get outgoing relations
  - [ ] `GET /api/entities/{id}/relations/incoming` - Get incoming relations

- [ ] Health check:
  - [ ] `GET /health` - Return {"status": "ok"}

- [ ] Serve static files:
  - [ ] Mount `frontend/` directory
  - [ ] `GET /` returns `index.html`

### Phase 5: Simple Web UI for Testing

- [ ] Create `frontend/index.html`:
  - [ ] Basic HTML structure with Tailwind CSS CDN
  - [ ] Sections:
    - [ ] Create Entity form (types as comma-separated, properties as JSON)
    - [ ] List Entities (with type filter dropdown)
    - [ ] Create Relation form (entity selectors, relation type, properties)
    - [ ] View Entity detail (shows entity + incoming/outgoing relations)

- [ ] Create `frontend/app.js`:
  - [ ] Fetch API wrappers for all endpoints
  - [ ] Create entity: POST with form data
  - [ ] List entities: GET with filters, render as cards
  - [ ] Create relation: POST with entity dropdowns
  - [ ] View entity: GET entity + relations, render as simple graph
  - [ ] Delete operations with confirmation dialogs

### Phase 6: Development Scripts

- [ ] Create `scripts/dev.sh`:
  ```bash
  #!/bin/bash
  uv run uvicorn backend.main:app --reload --port 8000
  ```

- [ ] Create `scripts/reset_db.sh`:
  ```bash
  #!/bin/bash
  rm -f connections.db
  echo "Database reset. Restart server to reinitialize."
  ```

- [ ] Make scripts executable:
  - [ ] `chmod +x scripts/*.sh`

### Phase 7: Testing & Validation

- [ ] Manual testing via web UI:
  - [ ] Create several entities with different types
  - [ ] Create relations between them
  - [ ] Verify type filtering works
  - [ ] Delete entity and verify cascade deletion of relations
  - [ ] Update entity properties

- [ ] API testing with FastAPI docs:
  - [ ] Visit `http://localhost:8000/docs`
  - [ ] Test all endpoints via Swagger UI
  - [ ] Verify request/response schemas
  - [ ] Test error cases (404, 422 validation errors)

### Phase 8: Documentation

- [ ] Update `README.md`:
  ```markdown
  # Connections - Knowledge Graph for themultiverse.school

  ## Quick Start

  ### Prerequisites
  - Python 3.11+
  - uv (install: `curl -LsSf https://astral.sh/uv/install.sh | sh`)

  ### Setup
  ```bash
  # Install dependencies
  uv sync

  # Run development server
  ./scripts/dev.sh
  # or
  uv run uvicorn backend.main:app --reload
  ```

  ### Access
  - Web UI: http://localhost:8000
  - API Docs: http://localhost:8000/docs
  - API: http://localhost:8000/api/*

  ## Architecture
  - **Backend**: FastAPI + aiosqlite (no ORM)
  - **Storage**: SQLite with JSON properties
  - **Frontend**: Vanilla JS + Tailwind CSS
  - **Model**: Entity-Relation knowledge graph
  ```

- [ ] Create `.gitignore`:
  ```
  # Python
  __pycache__/
  *.py[cod]
  .python-version

  # uv
  .venv/
  uv.lock

  # Database
  *.db
  *.db-journal

  # IDE
  .vscode/
  .idea/

  # OS
  .DS_Store
  ```

## Acceptance Criteria

- ✅ Project uses `uv` for dependency management (no pip, no requirements.txt)
- ✅ `uv sync` installs all dependencies
- ✅ `uv run` starts server without manual venv activation
- ✅ No SQLAlchemy or ORM dependencies
- ✅ Direct aiosqlite usage with plain SQL
- ✅ FastAPI provides automatic OpenAPI docs at `/docs`
- ✅ Can create/read/update/delete entities via API
- ✅ Can create/traverse relations via API
- ✅ Simple web UI allows visual testing
- ✅ All data persists in SQLite database
- ✅ Foreign key cascades work correctly
- ✅ Type filtering works for entities

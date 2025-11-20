# Tasks: Add Concept and Resource Entities

**Change ID:** `add-concept-resource-entities`

## Implementation Checklist

- [x] Add Concept endpoints to `backend/main.py`:
  - [x] `POST /api/concepts` - Create concept (wraps create_entity with type="Concept")
  - [x] `GET /api/concepts` - List concepts (wraps list_entities with types=["Concept"])
  - [x] `GET /api/concepts/{id}` - Get concept (wraps get_entity)
  - [x] Validate required properties: name, definition
  - [x] Return 422 if missing required properties

- [x] Add Resource endpoints to `backend/main.py`:
  - [x] `POST /api/resources` - Create resource (wraps create_entity with type="Resource")
  - [x] `GET /api/resources` - List resources (wraps list_entities with types=["Resource"])
  - [x] `GET /api/resources/{id}` - Get resource (wraps get_entity)
  - [x] Validate required properties: url, title
  - [x] Enforce unique URLs (check before creating)
  - [x] Return 422 if missing required properties
  - [x] Return 409 if URL already exists

- [x] Update `frontend/index.html`:
  - [x] Add "Create Concept" section with form (name, definition, scope, aliases)
  - [x] Add "Browse Concepts" section showing concept cards
  - [x] Add "Create Resource" section with form (url, title, description, content_type)
  - [x] Add "Browse Resources" section showing resource cards

- [x] Update `frontend/app.js`:
  - [x] `createConcept()` - POST to /api/concepts
  - [x] `listConcepts()` - GET from /api/concepts, render cards
  - [x] `createResource()` - POST to /api/resources
  - [x] `listResources()` - GET from /api/resources, render cards with links

- [x] Testing via web UI:
  - [x] Create several concepts with various properties
  - [x] Create several resources with URLs
  - [x] Verify concepts and resources are listed separately
  - [x] Verify URL uniqueness is enforced for resources
  - [x] Verify required field validation works

## Acceptance Criteria

- ✅ Can create concepts via dedicated endpoint
- ✅ Can create resources via dedicated endpoint
- ✅ Concepts and resources can be listed separately
- ✅ URL uniqueness is enforced
- ✅ Required properties are validated
- ✅ Web UI has dedicated forms for each type

# Proposal: Add Concept and Resource Entities

**Change ID:** `add-concept-resource-entities`
**Type:** New Capability
**Status:** Proposed
**Author:** drewby
**Date:** 2024-11-19
**Depends On:** `add-entity-relation-foundation`

## Why

Implement the two core entity types that form the basis of the knowledge graph: Concepts (abstract ideas) and Resources (concrete URLs). This enables users to start capturing and organizing knowledge.

## What Changes

### New Entity Types

**Concept Entity:**
- Type label: `"Concept"`
- Required properties: `name`, `definition`
- Optional properties: `scope`, `aliases`, `disambiguation`, `maturity`

**Resource Entity:**
- Type label: `"Resource"`
- Required properties: `url`, `title`
- Optional properties: `description`, `content_type`, `author`, `published_at`, `authority_score`

### API Endpoints

Add convenience endpoints built on top of the entity foundation:
- `POST /api/concepts` - Create concept
- `GET /api/concepts` - List concepts
- `GET /api/concepts/{id}` - Get concept details
- `POST /api/resources` - Create resource
- `GET /api/resources` - List resources
- `GET /api/resources/{id}` - Get resource details

These are thin wrappers around the generic entity endpoints but provide type safety and convenience.

## Impact

### Affected Specs
- `specs/knowledge-organization/spec.md` - Implements "Capture Concepts" and "Save Resources" requirements

### Affected Code
- `backend/main.py` - Add concept and resource endpoints
- `frontend/` - Update UI to have dedicated forms for concepts and resources

## Next Steps

1. Get approval
2. Implement concept/resource endpoints in FastAPI
3. Update web UI with dedicated sections
4. Validate via web interface

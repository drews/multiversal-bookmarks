# Proposal: Add Provenance Tracking

**Change ID:** `add-provenance-tracking`
**Type:** New Capability
**Status:** Proposed
**Depends On:** `add-semantic-relations`

## Why
Track who contributed each concept, resource, and connection, with timestamps. Enables attribution and quality verification.

## What Changes
- Add Person entity type
- Add CONTRIBUTED_BY relations from entities/relations to Person
- Add created_at timestamps to all entities and relations
- Update UI to show contributors and timestamps

## Impact
Implements "Track Contributions" and "Verify Knowledge Quality" requirements from knowledge-organization spec.

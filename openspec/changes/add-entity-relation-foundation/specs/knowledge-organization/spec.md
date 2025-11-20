# Delta: Knowledge Organization (Entity-Relation Foundation)

## ADDED Requirements

### Requirement: Entity Storage
The system SHALL store entities with unique identifiers, types, and properties.

#### Scenario: Create entity with types and properties
- **WHEN** system creates entity with id, types, and properties
- **THEN** entity is stored persistently
- **AND** entity is retrievable by unique identifier

#### Scenario: Support multiple entity types
- **WHEN** entity is created with multiple type labels (e.g., ["Resource", "Video"])
- **THEN** system stores all types
- **AND** entity matches queries for any of its types

#### Scenario: Store flexible properties
- **WHEN** entity includes arbitrary properties as key-value pairs
- **THEN** system stores properties as JSON
- **AND** properties are retrievable exactly as stored
- **AND** nested objects and arrays are supported

### Requirement: Relation Storage
The system SHALL store directed, typed relations between entities with optional properties.

#### Scenario: Create relation between entities
- **WHEN** relation is created from entity A to entity B with relation type
- **THEN** system stores the directed connection
- **AND** relation is retrievable by unique identifier

#### Scenario: Attach properties to relations
- **WHEN** relation includes metadata properties (strength, rationale, timestamp)
- **THEN** system stores relation properties as JSON
- **AND** properties are retrievable with the relation

#### Scenario: Enforce referential integrity
- **WHEN** attempting to create relation referencing non-existent entity
- **THEN** system rejects the operation
- **AND** returns error indicating missing entity

#### Scenario: Cascade deletion
- **WHEN** entity is deleted
- **THEN** system automatically deletes all relations to and from that entity
- **AND** no orphaned relations remain

### Requirement: Entity Retrieval
The system SHALL provide efficient access to entities by ID and type.

#### Scenario: Get entity by ID
- **WHEN** requesting entity by unique identifier
- **THEN** system returns entity with all types and properties
- **AND** returns null/404 if entity does not exist

#### Scenario: List entities by type
- **WHEN** querying for entities with specific type
- **THEN** system returns all entities having that type
- **AND** supports multiple type filters (OR logic)

#### Scenario: Paginate entity lists
- **WHEN** listing entities with limit and offset
- **THEN** system returns requested page of results
- **AND** provides total count for pagination UI

### Requirement: Relation Traversal
The system SHALL enable navigation of the knowledge graph via relations.

#### Scenario: Get outgoing relations
- **WHEN** requesting relations from an entity
- **THEN** system returns all relations where entity is source
- **AND** optionally filters by relation type

#### Scenario: Get incoming relations
- **WHEN** requesting relations to an entity
- **THEN** system returns all relations where entity is target
- **AND** optionally filters by relation type

#### Scenario: Get relations between entities
- **WHEN** querying for relations connecting two specific entities
- **THEN** system returns all relations from A to B
- **AND** includes relation types and properties

### Requirement: Data Persistence
The system SHALL persist all entities and relations durably to SQLite database.

#### Scenario: Survive restarts
- **WHEN** system restarts
- **THEN** all previously created entities and relations are available
- **AND** no data is lost

#### Scenario: Transaction safety
- **WHEN** operation fails partway through
- **THEN** system rolls back changes
- **AND** maintains data consistency

### Requirement: Type Flexibility
The system SHALL allow adding new entity types and relation types without schema migration.

#### Scenario: Introduce new entity type
- **WHEN** creating entity with previously unused type
- **THEN** system accepts the new type
- **AND** no database migration is required

#### Scenario: Introduce new relation type
- **WHEN** creating relation with previously unused type
- **THEN** system accepts the new relation type
- **AND** no database migration is required

#### Scenario: Add properties dynamically
- **WHEN** entity includes new property keys not seen before
- **THEN** system stores the properties
- **AND** no schema update is required

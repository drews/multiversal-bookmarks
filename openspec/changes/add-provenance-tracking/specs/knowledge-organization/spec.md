# Delta: Knowledge Organization (Provenance Tracking)

## ADDED Requirements

### Requirement: Person Entity Type
The system SHALL support Person entities representing contributors.

#### Scenario: Create person
- **WHEN** system creates person with name and identifier
- **THEN** person is stored as Entity with type "Person"
- **AND** can be referenced in provenance relations

### Requirement: Contribution Attribution
The system SHALL track who created each entity and relation.

#### Scenario: Record contributor
- **WHEN** entity or relation is created
- **THEN** system creates CONTRIBUTED_BY relation to Person
- **AND** stores created_at timestamp in properties

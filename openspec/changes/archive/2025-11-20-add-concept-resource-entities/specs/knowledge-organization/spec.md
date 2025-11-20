# Delta: Knowledge Organization (Concept and Resource Entities)

## ADDED Requirements

### Requirement: Concept Entity Type
The system SHALL support Concept entities with name, definition, and metadata.

#### Scenario: Create concept with required properties
- **WHEN** user creates concept with name and definition
- **THEN** system stores concept as Entity with type "Concept"
- **AND** name and definition are in properties
- **AND** unique ID is generated

#### Scenario: Add scope to concept
- **WHEN** user specifies scope (e.g., "programming/python/async")
- **THEN** system stores scope in properties
- **AND** scope enables hierarchical browsing

#### Scenario: Add aliases to concept
- **WHEN** user provides alternative names for concept
- **THEN** system stores aliases as array in properties
- **AND** concept is searchable by any alias

### Requirement: Resource Entity Type
The system SHALL support Resource entities with URL, title, and metadata.

#### Scenario: Create resource with URL and title
- **WHEN** user creates resource with URL and title
- **THEN** system stores resource as Entity with type "Resource"
- **AND** url and title are in properties
- **AND** unique ID is generated

#### Scenario: Enforce unique URLs
- **WHEN** user attempts to create resource with existing URL
- **THEN** system rejects creation
- **AND** returns error with existing resource ID

#### Scenario: Store resource content type
- **WHEN** user specifies content_type (article, video, tutorial, specification, tool, book)
- **THEN** system stores content_type in properties
- **AND** resources can be filtered by content_type

#### Scenario: Store resource author and publication date
- **WHEN** user provides author and published_at
- **THEN** system stores in properties
- **AND** resources can be sorted by publication date

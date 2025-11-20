# Delta: Knowledge Organization (Semantic Relations)

## ADDED Requirements

### Requirement: Typed Relations Between Entities
The system SHALL support creating semantic relations with predefined types.

#### Scenario: Create EXEMPLIFIES relation
- **WHEN** user connects resource to concept with EXEMPLIFIES type
- **THEN** system creates relation with type "EXEMPLIFIES"
- **AND** relation indicates resource is example of concept

#### Scenario: Create REQUIRES relation for prerequisites
- **WHEN** user marks Concept A as requiring Concept B
- **THEN** system creates REQUIRES relation from A to B
- **AND** prerequisite chain is navigable

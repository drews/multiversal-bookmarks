# Spec Delta: Knowledge Organization - Automatic Metadata Extraction

## ADDED Requirements

### Requirement: Automatic Metadata Extraction
Users SHALL be able to preview and automatically extract metadata from resource URLs before saving.

#### Scenario: Preview metadata before saving
- **WHEN** user submits URL for preview
- **THEN** system fetches URL content
- **AND** extracts title, description, author, type, favicon, and image
- **AND** returns extracted metadata for user review
- **AND** does NOT create resource until user confirms

#### Scenario: Automatic metadata extraction on resource creation
- **WHEN** user creates resource with URL but without title
- **THEN** system automatically fetches URL content
- **AND** extracts metadata using Open Graph tags (priority 1)
- **AND** falls back to Twitter Card tags if Open Graph unavailable
- **AND** falls back to standard HTML meta tags if neither available
- **AND** extracts favicon and converts relative URLs to absolute
- **AND** detects content type (article, video, tutorial, specification, tool, book)
- **AND** completes extraction within 5 seconds or times out
- **AND** saves resource with extracted metadata

#### Scenario: Metadata extraction failure handling
- **WHEN** metadata extraction fails (timeout, network error, parse error)
- **THEN** system returns partial metadata (hostname, URL)
- **AND** allows user to manually enter missing fields
- **AND** does NOT block resource creation
- **AND** logs extraction failure for debugging

#### Scenario: Manual override of extracted metadata
- **WHEN** user provides explicit values for title, description, or other fields
- **THEN** system uses user-provided values
- **AND** does NOT override with extracted metadata
- **AND** respects user's judgment over automatic extraction

#### Scenario: Favicon resolution
- **WHEN** resource HTML contains relative favicon path
- **THEN** system converts to absolute URL using resource domain
- **WHEN** no favicon found in HTML
- **THEN** system tries Google Favicon API as fallback
- **AND** uses generic icon if all methods fail

#### Scenario: Content type detection
- **WHEN** extracting metadata
- **THEN** system analyzes URL patterns and meta tags
- **AND** detects: video (YouTube, Vimeo), docs (readthedocs, /docs/ paths), tutorials (contains "tutorial" or "guide"), tools (GitHub repos, interactive sites), books (ISBN, publisher tags), specifications (W3C, RFC, /spec/ paths)
- **AND** defaults to "article" if detection inconclusive


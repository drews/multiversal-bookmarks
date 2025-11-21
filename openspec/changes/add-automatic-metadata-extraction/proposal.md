# Proposal: Add Automatic Metadata Extraction

**Change ID:** `add-automatic-metadata-extraction`
**Type:** New Capability
**Status:** Proposed
**Author:** drewby
**Date:** 2024-11-20
**Depends On:** `add-concept-resource-entities`

## Why

**Problem:** Creating resources currently requires manually entering title, description, author, etc. This high activation energy discourages building out the knowledge graph.

**Solution:** Automatically extract metadata from URLs using Open Graph, Twitter Cards, and standard HTML meta tags. Users paste a URL and get a pre-filled form they can review and submit.

**Impact:**
- Reduces time to add resource from ~60 seconds to ~5 seconds
- Enables rapid knowledge graph population
- Sets foundation for future AI-suggested concept connections
- Aligns with existing spec requirement: "system automatically extracts metadata"

## What Changes

### New Module: Metadata Extraction

**backend/metadata.py:**
- `async extract_metadata(url: str) -> dict` - Main extraction function
- HTTP fetch with 5-second timeout (httpx)
- HTML parsing (BeautifulSoup4)
- Extraction strategy (priority order):
  1. Open Graph tags (`og:title`, `og:description`, `og:image`, `og:type`)
  2. Twitter Card tags (`twitter:title`, `twitter:description`, `twitter:image`)
  3. Standard HTML meta tags and `<title>`
- Content type detection (article, video, tutorial, specification, tool, book)
- Favicon resolution (relative → absolute, Google Favicon API fallback)
- Graceful error handling (returns partial data on failure)

### API Enhancement

**backend/main.py:**
- `POST /api/resources/from-url` - New endpoint
  - Takes only `url` parameter
  - Calls `extract_metadata(url)`
  - Returns extracted metadata for user review
  - Does NOT create resource (preview only)
- Modify `POST /api/resources`:
  - Add optional `auto_extract: bool = True` parameter
  - If URL provided without title and auto_extract=True, extract automatically
  - User can override any extracted field

### Frontend Enhancement

**frontend/:**
- "Quick Add from URL" form (single input + button)
- Extracts metadata and pre-fills main resource form
- Shows loading state during extraction
- Displays extraction errors gracefully
- Allows manual override of all fields

## Impact

### Affected Specs
- `specs/knowledge-organization/spec.md` - Implements existing "automatically extracts metadata" requirement

### Affected Code
- New: `backend/metadata.py` - Metadata extraction logic
- Modified: `backend/main.py` - Add `/api/resources/from-url` endpoint
- Modified: `frontend/` - Add quick URL form and auto-fill logic

### Benefits

✅ **Massive time savings** - 60s → 5s per resource
✅ **Lower barrier to entry** - Just paste URL and click
✅ **Better data quality** - Extracted from authoritative source
✅ **Foundation for AI** - Enables future concept suggestion based on content
✅ **Spec compliance** - Implements existing requirement

### Risks

**Low Risk:**
- Well-established pattern (used in Node.js version previously)
- httpx and BeautifulSoup4 are battle-tested
- Graceful degradation on extraction failure
- User can always override

**Considerations:**
- External URL fetching adds latency (mitigated by timeout)
- Some sites block scrapers (fallback to manual entry)
- Rate limiting from target sites (not an issue at current scale)

## Next Steps

1. Get approval
2. Implement metadata extraction module
3. Add API endpoint for preview
4. Update frontend with quick-add form
5. Test with various URL types
6. Future: Use extracted content for AI concept suggestions

# Tasks: Add Automatic Metadata Extraction

**Change ID:** `add-automatic-metadata-extraction`

## Implementation Checklist

### 1. Create Metadata Extraction Module
- [ ] Create `backend/metadata.py`
- [ ] Implement `async extract_metadata(url: str) -> dict`
- [ ] Add HTTP fetch with httpx (5-second timeout)
- [ ] Add HTML parsing with BeautifulSoup4
- [ ] Implement extraction strategy (Open Graph → Twitter Cards → Standard HTML)
- [ ] Add content type detection logic
- [ ] Add favicon resolution (relative → absolute, Google Favicon API fallback)
- [ ] Add graceful error handling (return partial data on failure)
- [ ] Add basic unit tests for extraction logic

### 2. Add API Endpoint for Preview
- [ ] Add `POST /api/resources/from-url` endpoint in `backend/main.py`
- [ ] Accept only `url` parameter
- [ ] Call `extract_metadata(url)` function
- [ ] Return extracted metadata for user review
- [ ] Ensure endpoint does NOT create resource (preview only)
- [ ] Add error handling for fetch failures

### 3. Enhance Resource Creation Endpoint
- [ ] Modify `POST /api/resources` in `backend/main.py`
- [ ] Add optional `auto_extract: bool = True` parameter
- [ ] If URL provided without title and auto_extract=True, call `extract_metadata()`
- [ ] Allow user to override any extracted field
- [ ] Preserve existing manual entry flow

### 4. Update Frontend
- [ ] Add "Quick Add from URL" form section to `frontend/index.html`
- [ ] Create single URL input + "Extract Metadata" button
- [ ] Add JavaScript handler in `frontend/app.js` to call `/api/resources/from-url`
- [ ] Show loading state during extraction
- [ ] Pre-fill main resource form with extracted metadata
- [ ] Display extraction errors gracefully (with fallback to manual entry)
- [ ] Ensure all fields remain editable for manual override

### 5. Testing
- [ ] Test extraction with various URL types:
  - [ ] Article with Open Graph tags
  - [ ] Video with Twitter Card tags
  - [ ] Documentation site with standard HTML meta
  - [ ] Plain HTML page without meta tags
  - [ ] URL that times out (5s limit)
  - [ ] Invalid URL (404, DNS failure)
- [ ] Verify favicon resolution works for relative paths
- [ ] Test manual override of extracted fields
- [ ] Verify existing manual entry flow still works

### 6. Documentation
- [ ] Update `CLAUDE.md` with metadata extraction details
- [ ] Add example of metadata extraction API usage
- [ ] Document extraction strategy and fallback behavior

## Dependencies

**Python packages** (add to pyproject.toml):
- httpx (already added)
- beautifulsoup4 (already added)

**No breaking changes** - this is a pure enhancement that preserves existing functionality.

## Success Criteria

- [ ] User can paste URL and get pre-filled resource form in < 10 seconds
- [ ] Extraction works for at least 80% of common educational URLs
- [ ] Extraction failures degrade gracefully to manual entry
- [ ] All extracted fields can be manually overridden
- [ ] Time to add resource reduced from ~60s to ~5s for successful extractions

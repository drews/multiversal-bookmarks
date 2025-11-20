# Project Context

## Purpose
Collaborative bookmarking system for themultiverse.school community. Faculty, students, and admin share educational resources to build collective knowledge. Features include metadata extraction, tagging, collections, and search.

## Tech Stack
- **Backend**: Python 3.11+ with FastAPI
- **Database**: SQLite3 with async (aiosqlite) abstraction
- **Frontend**: Vanilla JavaScript with Tailwind CSS
- **Metadata Extraction**: httpx + BeautifulSoup4 for URL parsing
- **Development**: uvicorn with --reload for hot-reload
- **Deployment**: Docker with docker-compose

## Project Conventions

### Code Style
- Python 3.11+ with type hints for clarity
- Async/await patterns for I/O operations
- RESTful API design with `/api/*` prefix
- Single-file implementations until proven insufficient
- Prefer boring, proven patterns over complexity
- Follow PEP 8 style guide

### Architecture Patterns
- Three-layer architecture: FastAPI → Database Layer → SQLite
- Database abstraction class wrapping aiosqlite for async API
- Metadata service fetches and parses URL data on bookmark creation
- Foreign key cascades handle cleanup (DELETE bookmark removes associations)
- Single persistent database connection with graceful shutdown
- FastAPI automatic OpenAPI documentation at `/docs`

### Testing Strategy
- Currently minimal testing infrastructure
- Manual testing via API endpoints
- Health checks via `/api/bookmarks` endpoint (Docker)

### Git Workflow
- Direct commits to main branch
- Commit messages without AI attribution
- Feature development in place (no branching strategy currently)

## Domain Context
- **Community**: themultiverse.school faculty, students, and admin
- **Resource types**: Video, docs, tutorial, tool, article, website
- **Metadata sources**: Open Graph, Twitter Cards, standard HTML meta tags
- **Favicon resolution**: Relative to absolute URL conversion with Google Favicon API fallback

## Important Constraints
- SQLite suitable for small-to-medium usage
- No authentication implemented (not yet exposed publicly)
- CORS enabled for all origins
- 5-second timeout on metadata extraction
- Consider PostgreSQL migration for high concurrency scenarios

## External Dependencies
- Google Favicon API (fallback for favicon resolution)
- URL metadata extraction depends on target sites being accessible
- Optional Traefik integration for campus-quest-infra deployment

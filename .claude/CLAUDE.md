# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
Collaborative bookmarking system for themultiverse.school community. Faculty, students, and admin share resources to build collective knowledge.

## Development Commands

### Running the Application
```bash
npm install          # Install dependencies
npm start           # Start production server (port 3000)
npm run dev         # Start development server with nodemon
```

### Docker Deployment
```bash
docker-compose up -d                    # Start containerized service
docker-compose logs -f                  # View logs
docker-compose down                     # Stop service
docker build -t multiversal-bookmarks . # Build image manually
```

The container exposes port 3000 and persists data via volume mounts (`./bookmarks.db` and `./data`).

## Tech Stack
- **Backend**: Express.js with SQLite3
- **Frontend**: Vanilla JavaScript + Tailwind CSS
- **Metadata Extraction**: node-fetch + cheerio
- **Development**: nodemon for hot-reload

## Architecture

### Request Flow
```
Client → Express API → Database Layer → SQLite
                    ↓
              Metadata Service (for new bookmarks)
```

### Core Modules

**backend/server.js**
- Express app with REST API endpoints
- Routes: `/api/bookmarks`, `/api/tags`, `/api/collections`, `/api/search`
- Serves static frontend from `/frontend`
- Port 3000 default (configurable via `PORT` env var)

**backend/database.js**
- Database abstraction class wrapping sqlite3
- Promise-based async API
- Automatic schema initialization on first run
- All methods return promises (use `await` or `.then()`)

**backend/metadata.js**
- `extractMetadata(url)` - Fetches and parses URL metadata
- Extracts: title, description, favicon, image, type
- 5-second timeout, falls back to hostname on failure
- Uses Open Graph, Twitter Card, and standard HTML meta tags

### Database Schema

Five tables with foreign key relationships:

```sql
bookmarks: id, url (UNIQUE), title, description, favicon, image,
           type, added_by, created_at

tags: id, name (UNIQUE), color

bookmark_tags: bookmark_id, tag_id (junction table)

collections: id, name, description, created_by, created_at

collection_bookmarks: collection_id, bookmark_id, position (junction table)
```

**Important**: SQLite foreign keys cascade on DELETE. Deleting a bookmark removes its tag and collection associations automatically.

### API Endpoints

**Bookmarks**
- `GET /api/bookmarks` - List all with tags
- `GET /api/bookmarks/:id` - Single bookmark with tags
- `POST /api/bookmarks` - Create (auto-extracts metadata from URL)
- `DELETE /api/bookmarks/:id` - Delete bookmark
- `GET /api/search?q=query` - Search by title/description/URL/tags

**Tags**
- `GET /api/tags` - List all tags with usage counts
- `POST /api/bookmarks/:id/tags` - Add tag to bookmark

**Collections**
- `GET /api/collections` - List all with bookmark counts
- `GET /api/collections/:id` - Single collection
- `GET /api/collections/:id/bookmarks` - Bookmarks in collection
- `POST /api/collections` - Create collection
- `POST /api/collections/:id/bookmarks` - Add bookmark to collection

### Frontend Structure

**frontend/index.html**
- Single-page UI with Tailwind CSS
- Main sections: bookmark grid, search, tags, collections

**frontend/app.js**
- Vanilla JavaScript client
- Fetches data from Express API
- Dynamic DOM manipulation

## Claude Code Features

### Slash Commands (`.claude/commands/`)
- `/bookmark` - Add bookmark with AI metadata extraction
- `/find` - Semantic search across bookmarks
- `/curate` - Create themed collections

### Agents (`.claude/agents/`)
- `bookmark-curator` - Autonomous curation and organization

### Skills (`.claude/skills/`)
- `extract-metadata` - Fetch URL metadata
- `detect-duplicates` - Find similar bookmarks
- `suggest-tags` - AI-powered categorization
- `build-collection` - Collection templates

### Plugins (`.claude/plugins/`)
- `resource-curator` - Reusable bookmark utilities

## Key Implementation Details

### Adding a Bookmark
1. Client POSTs `{url, added_by}` to `/api/bookmarks`
2. Server calls `extractMetadata(url)` (5s timeout)
3. Metadata saved to database with auto-generated ID
4. Optional tags added via bookmark_tags junction
5. Returns complete bookmark object with tags

### Metadata Extraction Strategy
- Prioritizes Open Graph (`og:title`, `og:description`, `og:image`)
- Falls back to Twitter Cards, then standard HTML tags
- Favicon resolution: relative URLs converted to absolute
- Type detection: URL patterns + content analysis (video, docs, tutorial, tool, article, website)
- Google Favicon API used as ultimate fallback

### Search Implementation
Basic SQL LIKE query across:
- bookmark.title
- bookmark.description
- bookmark.url
- tag.name

Results grouped by bookmark ID with tags concatenated.

### Database Connection
- Single persistent connection created in Database constructor
- Graceful shutdown on SIGINT closes connection
- Database file: `bookmarks.db` in project root (or custom path)

## Deployment Notes

**Docker**
- Health check: HTTP GET `/api/bookmarks` every 30s
- Volumes: Mount `./bookmarks.db` for data persistence
- Optional Traefik labels commented in docker-compose.yml for campus-quest-infra integration

**Production Considerations**
- SQLite suitable for small-to-medium usage
- Consider PostgreSQL for high concurrency
- No authentication implemented - add before exposing publicly
- CORS enabled for all origins

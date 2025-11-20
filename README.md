# Connections - Knowledge Graph

**Connect ideas. Build understanding. Share knowledge.**

A knowledge graph system for [themultiverse.school](http://themultiverse.school) to capture, organize, and connect educational resources and concepts using semantic relationships.

## 🎯 The Problem

Every day, faculty, students, and admin discover valuable resources:
- 📖 Documentation that finally makes sense
- 🎥 That perfect tutorial video
- 🛠️ Tools that boost productivity
- 📝 Articles worth sharing

But then what? Browser bookmarks? Discord links? Lost forever?

## 💡 The Solution

**Entity-Relation knowledge graph** where concepts and resources are semantically connected:
- 🎯 **Entities**: Concepts (abstract ideas), Resources (URLs), People (contributors)
- 🔗 **Relations**: Typed connections (EXEMPLIFIES, REQUIRES, DEFINES, etc.)
- 📊 **Properties**: Flexible JSON attributes on entities and relations
- 🔍 **Graph Traversal**: Navigate connections to discover knowledge

## 🏗️ Architecture

**Entity-Relation Model:**
- **Entities**: Nodes with types and flexible properties
- **Relations**: Typed, directed edges with metadata
- **Storage**: SQLite with JSON (no ORM, direct aiosqlite)
- **API**: FastAPI with automatic OpenAPI docs

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+**
- **uv** - Fast Python package manager

Install uv:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Installation

```bash
# Install dependencies (creates .venv automatically)
uv sync
```

### Run Development Server

```bash
# Start with auto-reload
./scripts/dev.sh

# Or manually:
uv run uvicorn backend.main:app --reload --port 8000
```

### Access

- **Web UI**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **API**: http://localhost:8000/api/*

## 📁 Project Structure

```
connections/
├── backend/
│   ├── models.py      # Entity and Relation data classes
│   ├── storage.py     # KnowledgeGraph (SQLite storage)
│   └── main.py        # FastAPI application
├── frontend/
│   ├── index.html     # Web UI
│   └── app.js         # Client-side logic
├── scripts/
│   ├── dev.sh         # Development server
│   └── reset_db.sh    # Reset database
├── openspec/          # OpenSpec documentation
├── pyproject.toml     # Project configuration
└── README.md
```

## 🎓 For Multiverse School

**Faculty**: Define concepts and connect to best resources
**Students**: Discover learning paths through concept relationships
**Admin**: Organize knowledge with semantic connections
**Everyone**: Build a shared understanding through linked ideas

## 🔧 Tech Stack

- **Backend**: Python 3.11+ with FastAPI
- **Database**: SQLite3 with aiosqlite (async, no ORM)
- **Frontend**: Vanilla JavaScript + Tailwind CSS
- **Package Manager**: uv (modern, fast)
- **Development**: uvicorn with hot-reload

## 📚 Design Principles

- **No ORM**: Direct SQL for transparency
- **Flexible schema**: JSON properties, no migrations needed
- **Type hints**: Modern Python with dataclasses
- **Simple first**: Single-file implementations until proven insufficient
- **Storage agnostic**: Easy to swap backends

## 🚀 Next Steps

See `openspec/changes/` for planned enhancements:
- Concept and Resource entity types
- Semantic relations (EXEMPLIFIES, REQUIRES, etc.)
- Provenance tracking
- Search and discovery

Built with ❤️ for collaborative learning through connected knowledge

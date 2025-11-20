#!/bin/bash
# Reset database (delete and reinitialize)

echo "⚠️  Resetting database..."
rm -f connections.db
echo "✓ Database deleted"
echo "Restart server to reinitialize schema"

// Connections Knowledge Graph - Frontend Application

const API_BASE = '/api';

// Utilities
function showMessage(elementId, message, isError = false) {
    const el = document.getElementById(elementId);
    el.innerHTML = `
        <div class="p-4 rounded-md ${isError ? 'bg-red-50 text-red-800' : 'bg-green-50 text-green-800'}">
            ${message}
        </div>
    `;
    setTimeout(() => { el.innerHTML = ''; }, 5000);
}

function formatJSON(obj) {
    return JSON.stringify(obj, null, 2);
}

// Create Concept
document.getElementById('createConceptForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const name = document.getElementById('conceptName').value.trim();
    const definition = document.getElementById('conceptDefinition').value.trim();
    const scope = document.getElementById('conceptScope').value.trim();
    const aliasesInput = document.getElementById('conceptAliases').value.trim();

    if (!name || !definition) {
        showMessage('conceptResult', 'Name and definition are required', true);
        return;
    }

    const body = { name, definition };
    if (scope) body.scope = scope;
    if (aliasesInput) {
        body.aliases = aliasesInput.split(',').map(a => a.trim()).filter(a => a);
    }

    try {
        const response = await fetch(`${API_BASE}/concepts`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to create concept');
        }

        const concept = await response.json();
        showMessage('conceptResult', `
            <strong>Concept created!</strong><br>
            <span class="text-sm">${concept.properties.name}</span><br>
            <button onclick="copyToClipboard('${concept.id}')" class="mt-2 text-xs bg-gray-200 px-2 py-1 rounded">
                Copy ID
            </button>
        `);

        // Clear form
        document.getElementById('conceptName').value = '';
        document.getElementById('conceptDefinition').value = '';
        document.getElementById('conceptScope').value = '';
        document.getElementById('conceptAliases').value = '';

        loadEntities();
    } catch (err) {
        showMessage('conceptResult', err.message, true);
    }
});

// Create Resource
document.getElementById('createResourceForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const url = document.getElementById('resourceUrl').value.trim();
    const title = document.getElementById('resourceTitle').value.trim();
    const description = document.getElementById('resourceDescription').value.trim();
    const content_type = document.getElementById('resourceContentType').value;
    const author = document.getElementById('resourceAuthor').value.trim();
    const published_at = document.getElementById('resourcePublishedAt').value;

    if (!url || !title) {
        showMessage('resourceResult', 'URL and title are required', true);
        return;
    }

    const body = { url, title };
    if (description) body.description = description;
    if (content_type) body.content_type = content_type;
    if (author) body.author = author;
    if (published_at) body.published_at = published_at;

    try {
        const response = await fetch(`${API_BASE}/resources`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to create resource');
        }

        const resource = await response.json();
        showMessage('resourceResult', `
            <strong>Resource created!</strong><br>
            <a href="${resource.properties.url}" target="_blank" class="text-sm text-blue-600 hover:underline">
                ${resource.properties.title}
            </a><br>
            <button onclick="copyToClipboard('${resource.id}')" class="mt-2 text-xs bg-gray-200 px-2 py-1 rounded">
                Copy ID
            </button>
        `);

        // Clear form
        document.getElementById('resourceUrl').value = '';
        document.getElementById('resourceTitle').value = '';
        document.getElementById('resourceDescription').value = '';
        document.getElementById('resourceContentType').value = '';
        document.getElementById('resourceAuthor').value = '';
        document.getElementById('resourcePublishedAt').value = '';

        loadEntities();
    } catch (err) {
        showMessage('resourceResult', err.message, true);
    }
});

// Create Entity
document.getElementById('createEntityForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const typesInput = document.getElementById('entityTypes').value.trim();
    const propertiesInput = document.getElementById('entityProperties').value.trim();

    const types = typesInput.split(',').map(t => t.trim()).filter(t => t);

    if (types.length === 0) {
        showMessage('entityResult', 'Please enter at least one type', true);
        return;
    }

    let properties = {};
    if (propertiesInput) {
        try {
            properties = JSON.parse(propertiesInput);
        } catch (err) {
            showMessage('entityResult', `Invalid JSON: ${err.message}`, true);
            return;
        }
    }

    try {
        const response = await fetch(`${API_BASE}/entities`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ types, properties })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to create entity');
        }

        const entity = await response.json();
        showMessage('entityResult', `
            <strong>Entity created!</strong><br>
            <span class="text-sm">ID: ${entity.id}</span><br>
            <button onclick="copyToClipboard('${entity.id}')" class="mt-2 text-xs bg-gray-200 px-2 py-1 rounded">
                Copy ID
            </button>
        `);

        // Clear form and reload entities
        document.getElementById('entityTypes').value = '';
        document.getElementById('entityProperties').value = '';
        loadEntities();
    } catch (err) {
        showMessage('entityResult', err.message, true);
    }
});

// Load and display entities
async function loadEntities() {
    const filterInput = document.getElementById('filterTypes').value.trim();
    const types = filterInput ? filterInput.split(',').map(t => t.trim()).filter(t => t) : null;

    try {
        const params = new URLSearchParams();
        if (types && types.length > 0) {
            types.forEach(t => params.append('types', t));
        }

        const response = await fetch(`${API_BASE}/entities?${params}`);
        const data = await response.json();

        const list = document.getElementById('entitiesList');

        if (data.entities.length === 0) {
            list.innerHTML = '<p class="text-gray-500 text-sm col-span-2">No entities found</p>';
            return;
        }

        list.innerHTML = data.entities.map(entity => `
            <div class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer"
                 onclick="viewEntity('${entity.id}')">
                <div class="flex gap-2 mb-2">
                    ${entity.types.map(type => `
                        <span class="text-xs px-2 py-1 bg-blue-100 text-blue-800 rounded">
                            ${type}
                        </span>
                    `).join('')}
                </div>
                <div class="text-sm text-gray-600 font-mono">
                    ${entity.id.substring(0, 8)}...
                </div>
                ${Object.keys(entity.properties).length > 0 ? `
                    <div class="mt-2 text-sm">
                        ${Object.entries(entity.properties).slice(0, 2).map(([k, v]) => `
                            <div class="text-gray-700">
                                <span class="font-medium">${k}:</span>
                                ${typeof v === 'string' ? v.substring(0, 50) : JSON.stringify(v)}
                            </div>
                        `).join('')}
                    </div>
                ` : ''}
            </div>
        `).join('');
    } catch (err) {
        document.getElementById('entitiesList').innerHTML = `
            <p class="text-red-500 text-sm col-span-2">Error loading entities: ${err.message}</p>
        `;
    }
}

// View entity details
async function viewEntity(entityId) {
    try {
        const [entityResponse, outgoingResponse, incomingResponse] = await Promise.all([
            fetch(`${API_BASE}/entities/${entityId}`),
            fetch(`${API_BASE}/entities/${entityId}/relations/outgoing`),
            fetch(`${API_BASE}/entities/${entityId}/relations/incoming`)
        ]);

        const entity = await entityResponse.json();
        const outgoing = await outgoingResponse.json();
        const incoming = await incomingResponse.json();

        const detailsSection = document.getElementById('entityDetails');
        const detailsContent = document.getElementById('entityDetailsContent');

        detailsContent.innerHTML = `
            <div class="space-y-4">
                <div>
                    <h3 class="font-medium text-gray-700 mb-2">Types</h3>
                    <div class="flex gap-2">
                        ${entity.types.map(type => `
                            <span class="px-3 py-1 bg-blue-100 text-blue-800 rounded">
                                ${type}
                            </span>
                        `).join('')}
                    </div>
                </div>

                <div>
                    <h3 class="font-medium text-gray-700 mb-2">ID</h3>
                    <code class="text-sm bg-gray-100 px-2 py-1 rounded">${entity.id}</code>
                    <button onclick="copyToClipboard('${entity.id}')" class="ml-2 text-xs bg-gray-200 px-2 py-1 rounded">
                        Copy
                    </button>
                </div>

                <div>
                    <h3 class="font-medium text-gray-700 mb-2">Properties</h3>
                    <pre class="bg-gray-50 p-3 rounded text-sm overflow-auto">${formatJSON(entity.properties)}</pre>
                </div>

                <div>
                    <h3 class="font-medium text-gray-700 mb-2">Outgoing Relations (${outgoing.count})</h3>
                    ${outgoing.count > 0 ? `
                        <div class="space-y-2">
                            ${outgoing.relations.map(rel => `
                                <div class="border border-gray-200 rounded p-2 text-sm">
                                    <div class="font-medium text-green-700">${rel.relation_type}</div>
                                    <div class="text-gray-600">→ ${rel.to_entity.substring(0, 8)}...</div>
                                    ${Object.keys(rel.properties).length > 0 ? `
                                        <div class="text-xs text-gray-500 mt-1">
                                            ${formatJSON(rel.properties)}
                                        </div>
                                    ` : ''}
                                </div>
                            `).join('')}
                        </div>
                    ` : '<p class="text-gray-500 text-sm">None</p>'}
                </div>

                <div>
                    <h3 class="font-medium text-gray-700 mb-2">Incoming Relations (${incoming.count})</h3>
                    ${incoming.count > 0 ? `
                        <div class="space-y-2">
                            ${incoming.relations.map(rel => `
                                <div class="border border-gray-200 rounded p-2 text-sm">
                                    <div class="font-medium text-purple-700">${rel.relation_type}</div>
                                    <div class="text-gray-600">← ${rel.from_entity.substring(0, 8)}...</div>
                                    ${Object.keys(rel.properties).length > 0 ? `
                                        <div class="text-xs text-gray-500 mt-1">
                                            ${formatJSON(rel.properties)}
                                        </div>
                                    ` : ''}
                                </div>
                            `).join('')}
                        </div>
                    ` : '<p class="text-gray-500 text-sm">None</p>'}
                </div>

                <div class="pt-4 border-t">
                    <button
                        onclick="deleteEntity('${entity.id}')"
                        class="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 text-sm"
                    >
                        Delete Entity
                    </button>
                </div>
            </div>
        `;

        detailsSection.classList.remove('hidden');
        detailsSection.scrollIntoView({ behavior: 'smooth' });
    } catch (err) {
        alert(`Error loading entity: ${err.message}`);
    }
}

function closeEntityDetails() {
    document.getElementById('entityDetails').classList.add('hidden');
}

// Delete entity
async function deleteEntity(entityId) {
    if (!confirm('Delete this entity? All relations will also be deleted.')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/entities/${entityId}`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            throw new Error('Failed to delete entity');
        }

        closeEntityDetails();
        loadEntities();
    } catch (err) {
        alert(`Error deleting entity: ${err.message}`);
    }
}

// Create Relation
document.getElementById('createRelationForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const fromEntity = document.getElementById('fromEntity').value.trim();
    const toEntity = document.getElementById('toEntity').value.trim();
    const relationType = document.getElementById('relationType').value.trim();
    const propertiesInput = document.getElementById('relationProperties').value.trim();

    if (!fromEntity || !toEntity || !relationType) {
        showMessage('relationResult', 'Please fill in all required fields', true);
        return;
    }

    let properties = {};
    if (propertiesInput) {
        try {
            properties = JSON.parse(propertiesInput);
        } catch (err) {
            showMessage('relationResult', `Invalid JSON: ${err.message}`, true);
            return;
        }
    }

    try {
        const response = await fetch(`${API_BASE}/relations`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                from_entity: fromEntity,
                to_entity: toEntity,
                relation_type: relationType,
                properties
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to create relation');
        }

        const relation = await response.json();
        showMessage('relationResult', `
            <strong>Relation created!</strong><br>
            <span class="text-sm">${relation.relation_type}</span>
        `);

        // Clear form
        document.getElementById('fromEntity').value = '';
        document.getElementById('toEntity').value = '';
        document.getElementById('relationType').value = '';
        document.getElementById('relationProperties').value = '';
    } catch (err) {
        showMessage('relationResult', err.message, true);
    }
});

// Utility functions
function copyToClipboard(text) {
    navigator.clipboard.writeText(text);
    alert('Copied to clipboard!');
}

// Load entities on page load
loadEntities();

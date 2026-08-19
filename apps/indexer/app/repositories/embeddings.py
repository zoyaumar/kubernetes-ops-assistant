"""Document embeddings repository.

Handles inserting embedding vectors into document_embeddings (pgvector).

Idempotency
-----------
document_embeddings has a PRIMARY KEY on document_id, so re-embedding
the same document with the same model is idempotent via ON CONFLICT DO NOTHING.

Model versioning
----------------
If the embedding model changes, do NOT silently overwrite old vectors.
The 'model' column allows coexistence of multiple model versions.
Run a migration + re-index job when changing models.
"""

from __future__ import annotations

# TODO(week-4): implement

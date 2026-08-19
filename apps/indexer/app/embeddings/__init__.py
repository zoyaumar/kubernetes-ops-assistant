"""
Embedding provider abstraction.

The Provider Protocol defines the interface; LocalProvider implements it
using sentence-transformers on CPU.

The embedding dimension is not hard-coded. EMBEDDING_DIM must match the
chosen model. If the model changes, run a new Alembic migration to alter
the vector column dimension before regenerating embeddings.
"""

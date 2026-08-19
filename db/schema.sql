-- Kubernetes Ops Assistant — PostgreSQL schema
--
-- Reference & documentation file.
-- Actual migrations managed by Alembic (apps/indexer/alembic/).

CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- ─── users ─────────────────────────────────────────────────────────────────────────
CREATE TABLE users (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email       TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ─── clusters ────────────────────────────────────────────────────────────────────
CREATE TABLE clusters (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        TEXT NOT NULL,
    environment TEXT NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_seen_at TIMESTAMPTZ
);

-- ─── resources ───────────────────────────────────────────────────────────────────
CREATE TABLE resources (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cluster_id    UUID NOT NULL REFERENCES clusters(id) ON DELETE CASCADE,
    uid           TEXT NOT NULL,
    resource_type TEXT NOT NULL,
    namespace     TEXT,
    name          TEXT NOT NULL,
    node_name     TEXT,
    labels        JSONB,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at    TIMESTAMPTZ NOT NULL DEFAULT now(),

    UNIQUE(cluster_id, uid)
);

-- ─── cluster_events ──────────────────────────────────────────────────────────────
CREATE TABLE cluster_events (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cluster_id     UUID NOT NULL REFERENCES clusters(id) ON DELETE CASCADE,
    resource_id    UUID REFERENCES resources(id) ON DELETE SET NULL,
    event_uid      TEXT NOT NULL,
    event_type     TEXT NOT NULL,
    reason         TEXT,
    severity       TEXT,
    namespace      TEXT,
    resource_type  TEXT,
    resource_name  TEXT,
    container_name TEXT,
    message        TEXT NOT NULL,
    occurred_at    TIMESTAMPTZ NOT NULL,
    received_at    TIMESTAMPTZ NOT NULL,
    metadata       JSONB,

    UNIQUE(cluster_id, event_uid)
);

CREATE INDEX idx_cluster_events_occurred_at ON cluster_events(cluster_id, occurred_at DESC);
CREATE INDEX idx_cluster_events_namespace ON cluster_events(cluster_id, namespace);
CREATE INDEX idx_cluster_events_severity ON cluster_events(cluster_id, severity);

-- ─── documents ─────────────────────────────────────────────────────────────────────
CREATE TABLE documents (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cluster_id  UUID NOT NULL REFERENCES clusters(id) ON DELETE CASCADE,
    source_type TEXT NOT NULL,
    source_id   UUID,
    content     TEXT NOT NULL,
    metadata    JSONB NOT NULL DEFAULT '{}',
    occurred_at TIMESTAMPTZ,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_documents_cluster_time ON documents(cluster_id, occurred_at DESC);

-- ─── document_embeddings ────────────────────────────────────────────────────────────
CREATE TABLE document_embeddings (
    document_id UUID PRIMARY KEY REFERENCES documents(id) ON DELETE CASCADE,
    embedding   VECTOR(384) NOT NULL,
    model       TEXT NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_doc_embeddings_ivfflat
    ON document_embeddings
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);

-- ─── conversations ────────────────────────────────────────────────────────────────
CREATE TABLE conversations (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    cluster_id  UUID REFERENCES clusters(id) ON DELETE SET NULL,
    title       TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ─── messages ───────────────────────────────────────────────────────────────────────
CREATE TABLE messages (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id  UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role             TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content          TEXT NOT NULL,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ─── message_citations ─────────────────────────────────────────────────────────────
CREATE TABLE message_citations (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    message_id  UUID NOT NULL REFERENCES messages(id) ON DELETE CASCADE,
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    rank        INT NOT NULL,
    score       DOUBLE PRECISION,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

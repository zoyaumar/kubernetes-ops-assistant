# Architectural Decision Records (ADRs) — Consolidated Log

> This document consolidates all core architectural and technical decisions made for the **Kubernetes Ops Assistant** project. Each record captures the context, decision, rationale, trade-offs, and consequences.

---

## Index of Decisions

1. [ADR-001: Local Kubernetes Environment (`kind`)](#adr-001-local-kubernetes-environment-kind)
2. [ADR-002: Message Streaming Broker (NATS JetStream over Kafka)](#adr-002-message-streaming-broker-nats-jetstream-over-kafka)
3. [ADR-003: Delivery Model (At-Least-Once + Idempotent Consumers)](#adr-003-delivery-model-at-least-once--idempotent-consumers)
4. [ADR-004: Unified Persistence & Vector Store (PostgreSQL + pgvector)](#adr-004-unified-persistence--vector-store-postgresql--pgvector)
5. [ADR-005: LLM Vendor Abstraction Layer (`LLMProvider`)](#adr-005-llm-vendor-abstraction-layer-llmprovider)
6. [ADR-006: Hybrid Retrieval Engine (SQL Filters + Vector Cosine Search)](#adr-006-hybrid-retrieval-engine-sql-filters--vector-cosine-search)
7. [ADR-007: Local CPU Embedding Generation (`all-MiniLM-L6-v2`)](#adr-007-local-cpu-embedding-generation-all-minilm-l6-v2)
8. [ADR-008: Grounded RAG Response Policy & Anti-Hallucination Guardrails](#adr-008-grounded-rag-response-policy--anti-hallucination-guardrails)
9. [ADR-009: Event-Driven Autoscaling Strategy (KEDA NATS Lag Scaler)](#adr-009-event-driven-autoscaling-strategy-keda-nats-lag-scaler)
10. [ADR-010: Microservice Boundaries & Technology Stack Division](#adr-010-microservice-boundaries--technology-stack-division)
11. [ADR-011: Security & Kubernetes Least-Privilege RBAC Model](#adr-011-security--kubernetes-least-privilege-rbac-model)

---

## ADR-001: Local Kubernetes Environment (`kind`)

* **Status**: Accepted
* **Date**: 2026-08-19

### Context
The system requires a local Kubernetes environment for development, automated integration testing, and live portfolio demonstrations. The environment must run inside standard developer environments (macOS/Windows/Linux with Docker Desktop) at $0 cost and consume <1GB RAM.

### Decision
Use **`kind` (Kubernetes in Docker)** as the primary local cluster provider.

### Rationale
* **Low Footprint**: Single-node kind clusters run as a single Docker container, consuming ~500MB RAM compared to multi-gigabyte virtual machine setups (e.g. Minikube with hypervisors).
* **Hermetic & Scriptable**: `kind create cluster` enables rapid, reproducible cluster bootstrap via shell scripts (`scripts/kind-up.sh`).
* **CI/CD Compatibility**: Kind runs natively inside standard GitHub Actions Ubuntu runners without special hardware configuration.

### Consequences
* Kubernetes `LoadBalancer` services are not natively provisioned; local access relies on `kubectl port-forward` or NodePorts.
* Cluster destruction (`kind delete cluster`) removes local container volumes; persistent state relies on database seed scripts for environment reset.

---

## ADR-002: Message Streaming Broker (NATS JetStream over Kafka)

* **Status**: Accepted
* **Date**: 2026-08-19

### Context
The Watcher service captures high-frequency Kubernetes API events and pod logs, requiring a durable, stream-oriented broker to buffer and publish messages to downstream indexer workers.

### Decision
Use **NATS JetStream** instead of Apache Kafka or Redis Streams.

### Rationale
* **Resource Efficiency**: NATS compiles to a single static binary (~15MB container image, <30MB RAM idle). Apache Kafka requires JVM runtime overhead and ZooKeeper/KRaft cluster coordination consuming 1GB+ RAM.
* **JetStream Capabilities**: Provides at-least-once message persistence, stream replay, subject wildcards (`k8s.events.*`), explicit consumer acknowledgements, and dead-letter queue (DLQ) support out of the box.
* **Native Scaler Integration**: KEDA maintains a native `nats-jetstream` scalar trigger based on unacknowledged stream lag.

### Consequences
* JetStream stream parameters (retention windows, max bytes) must be declared on stream initialization (`K8S_EVENTS`).

---

## ADR-003: Delivery Model (At-Least-Once + Idempotent Consumers)

* **Status**: Accepted
* **Date**: 2026-08-19

### Context
Distributed processing over NATS JetStream can suffer transient network disconnects or consumer worker restarts, leading to redelivered messages.

### Decision
Adopt an **at-least-once delivery** model coupled with **idempotent database insertion**, explicitly avoiding complex distributed exactly-once transactions (2PC).

### Implementation
1. **Stable Event Identifiers**: Watcher assigns a stable `event_uid` derived from the underlying Kubernetes resource/event `metadata.uid` (not a transient consumer timestamp).
2. **Database Constraints**: `cluster_events` table enforces a composite unique constraint: `UNIQUE(cluster_id, event_uid)`.
3. **Upsert Semantics**: Indexer inserts use PostgreSQL `ON CONFLICT (cluster_id, event_uid) DO NOTHING`.
4. **Post-Commit ACK**: Consumer ACKs the JetStream message *only after* the PostgreSQL transaction commits successfully. If the indexer crashes post-write but pre-ACK, redelivery safely hits the unique constraint without side-effects.

```text
Message Redelivery ──► Indexer Process ──► DB INSERT (ON CONFLICT DO NOTHING) ──► NATS ACK
```

---

## ADR-004: Unified Persistence & Vector Store (PostgreSQL + pgvector)

* **Status**: Accepted
* **Date**: 2026-08-19

### Context
Retrieval Augmented Generation (RAG) applications typically require two data stores: a relational database for application state/metadata and a specialized vector database (Pinecone, Qdrant, Milvus) for semantic embeddings.

### Decision
Use **PostgreSQL 16 with the `pgvector` extension** as the single unified data store for relational records and vector embeddings.

### Rationale
* **Transactional Consistency**: Relational facts (`cluster_events`, `documents`) and vector embeddings (`document_embeddings`) can be inserted within a single atomic SQL transaction.
* **Unified Query Execution**: Allows hybrid SQL queries combining metadata filters (`namespace`, `severity`, `occurred_at BETWEEN ...`) and cosine vector similarity (`embedding <=> query_vector`) in a single query execution plan.
* **Operational Simplicity**: $0 cost, zero cloud dependencies, and unified backup/migration via Alembic and standard PostgreSQL tooling.

### Consequences
* The vector dimension (`VECTOR(384)`) is tied to the selected embedding model and specified during schema migration. Changing embedding models requires an Alembic schema migration.

---

## ADR-005: LLM Vendor Abstraction Layer (`LLMProvider`)

* **Status**: Accepted
* **Date**: 2026-08-19

### Context
Directly embedding vendor-specific SDK calls (e.g. OpenAI SDK) throughout the API layer creates vendor lock-in, complicates rate-limit handling, and prevents offline unit testing without paid API keys.

### Decision
Encapsulate all LLM interaction behind an internal TypeScript interface:

```typescript
export interface LLMMessage {
  role: 'system' | 'user' | 'assistant';
  content: string;
}

export interface LLMResponse {
  content: string;
  usage: { promptTokens: number; completionTokens: number; totalTokens: number; };
}

export interface LLMProvider {
  readonly name: string;
  chat(messages: LLMMessage[], maxTokens?: number): Promise<LLMResponse>;
}
```

Implementations:
* `GroqProvider`: Production/dev provider using Groq's high-speed Llama-3 inference backend.
* `MockLLMProvider`: Offline provider returning deterministic test fixtures for unit tests and retrieval evaluation scripts without network I/O or API costs.

---

## ADR-006: Hybrid Retrieval Engine (SQL Filters + Vector Cosine Search)

* **Status**: Accepted
* **Date**: 2026-08-19

### Context
Pure vector similarity search performs poorly on operational Kubernetes queries (e.g. "Why did `payments-api` crash in namespace `payments` at 02:14 AM?"). Dense vector embeddings lack exact filter enforcement for namespaces, container names, and narrow time windows.

### Decision
Implement a **hybrid retrieval strategy** combining structured metadata filtering with vector similarity search:

```text
User Question
    │
    ▼
1. Extract metadata & time window (namespace, resource_name, start/end timestamps)
    │
    ▼
2. Exec SQL Filter: Candidate subset from cluster_events & documents
    │
    ▼
3. Exec Vector Search: Top-K cosine similarity match (pgvector vector_cosine_ops)
    │
    ▼
4. Score Fusion & Reranking: Combined Score = (Vector Similarity * 0.6) + (Recency Decay * 0.2) + (Severity Weight * 0.2)
    │
    ▼
5. Inject Top-K Evidence Chunks into Prompt Builder
```

---

## ADR-007: Local CPU Embedding Generation (`all-MiniLM-L6-v2`)

* **Status**: Accepted
* **Date**: 2026-08-19

### Context
Generating document and query embeddings via external APIs (e.g. OpenAI `text-embedding-3-small`) introduces per-request network latency, rate limit risk, and ongoing API costs during continuous ingestion.

### Decision
Use a compact local CPU-bound embedding model: **`sentence-transformers/all-MiniLM-L6-v2`**.

### Key Characteristics
* **Dimensions**: 384 float vector outputs.
* **Footprint**: ~80MB disk storage, ~300MB RAM when loaded in PyTorch CPU runtime.
* **Performance**: Fast CPU inference (~10–20ms per document chunk), eliminating external HTTP round-trips.
* **Deterministic Execution**: Embeddings can be generated offline during integration testing and CI runs.

---

## ADR-008: Grounded RAG Response Policy & Anti-Hallucination Guardrails

* **Status**: Accepted
* **Date**: 2026-08-19

### Context
LLMs tend to hallucinate plausible cluster causes (e.g. fabricating missing log lines or hypothetical network errors) when evidence is sparse or absent.

### Decision
Enforce strict prompt guardrails and explicit confidence classification:
1. **System Prompt Mandate**: Instruct the model that retrieved `EVIDENCE` is the sole source of truth. Any factual claim must cite a valid evidence index (e.g. `[1]`, `[2]`).
2. **Explicit Distinction**: Hypotheses or inferences must be explicitly labeled as inferences (e.g. *"Inferred cause: container limits suggest OOM..."*).
3. **Insufficient Evidence Fallback**: If retrieved evidence score is below minimum threshold or contains zero relevant records, the system must return `confidence: "insufficient"` and state: *"Insufficient evidence to determine root cause."*

---

## ADR-009: Event-Driven Autoscaling Strategy (KEDA NATS Lag Scaler)

* **Status**: Accepted
* **Date**: 2026-08-19

### Context
During cluster incidents (e.g. cascading pod crash loops), Kubernetes emits high volumes of warning events. Standard CPU/Memory Horizontal Pod Autoscalers (HPA) scale reactively only after container CPU/memory usage rises, leading to message processing backlog.

### Decision
Use **KEDA (Kubernetes Event-driven Autoscaling)** with a **`nats-jetstream` scalar trigger** monitoring stream lag.

### Configuration Target
* **Target Spec**: `k8s/keda/indexer-scaledobject.yaml`
* **Scale Target**: `Deployment/indexer`
* **Metrics Source**: NATS JetStream HTTP monitoring endpoint (`:8222`)
* **Threshold**: Scale up indexer worker replicas when pending unacknowledged message lag exceeds 100 messages per replica (bounded between 1 and 5 replicas).

---

## ADR-010: Microservice Boundaries & Technology Stack Division

* **Status**: Accepted
* **Date**: 2026-08-19

### Context
Structuring the portfolio codebase into clean service boundaries with appropriate language selections for each domain.

### Decision
Structure as a monorepo containing **three primary microservices**:

| Service | Language / Stack | Responsibility |
| :--- | :--- | :--- |
| **`apps/watcher`** | Python 3.12 / `kubernetes-client`, `nats-py` | Event watcher: low-overhead async loops monitoring K8s API streams and publishing normalized `ClusterEvent` JSON envelopes. |
| **`apps/indexer`** | Python 3.12 / `sentence-transformers`, `asyncpg`, `sqlalchemy` | Ingestion processor: CPU-intensive text chunking, local vector embedding, and idempotent PostgreSQL/pgvector persistence. |
| **`apps/api`** | TypeScript / Node 20, Fastify, `postgres`, `groq-sdk` | User API: Fastify server handling auth, schema validation (Zod), conversation state, and hybrid RAG orchestration. |
| **`frontend`** | TypeScript / React 18, Vite, Vanilla CSS | UI Dashboard: Interactive incident chat, evidence timeline visualizer, and event log browser. |

---

## ADR-011: Security & Kubernetes Least-Privilege RBAC Model

* **Status**: Accepted
* **Date**: 2026-08-19

### Context
The Watcher service runs inside the Kubernetes cluster and requires access to cluster events, pods, deployments, and logs without exposing sensitive cluster credentials or granting excessive administrative privileges.

### Decision
Implement strict least-privilege Kubernetes RBAC and authentication controls:

### Watcher ServiceAccount (`k8s/base/rbac.yaml`)
* **Dedicated ServiceAccount**: `k8s-ops-watcher` in namespace `k8s-ops`.
* **ClusterRole Permissions**: Read-Only access (`get`, `list`, `watch`) restricted to `pods`, `pods/log`, `events`, `nodes`, `deployments`, `replicasets`.
* **Denied Verbs**: Explicitly denies `create`, `update`, `patch`, `delete`, and `exec`.

### API & User Security
* Passwords stored using bcrypt (cost factor ≥ 12).
* Stateless authentication via short-lived JWT access tokens (`@fastify/jwt`).
* Secrets (DB credentials, Groq API keys, JWT secret) passed via environment variables / Kubernetes `Secret` manifests, never committed to git.

# Kubernetes Ops Assistant — System Architecture & Technology Stack

> An event-driven, Kubernetes-native RAG system that continuously ingests Kubernetes events/logs, indexes them for hybrid retrieval, and uses an LLM to explain failures and answer operational questions with grounded evidence.

---

## 1. System Overview

Kubernetes Ops Assistant consists of **three primary application microservices** and **five supporting infrastructure components**:

```text
                                 ┌─────────────────────┐
                                 │    React / Vite UI  │
                                 │     (TypeScript)    │
                                 └──────────┬──────────┘
                                            │
                                      HTTPS / JSON
                                            │
                                            ▼
                                 ┌─────────────────────┐
                                 │  Node / Fastify API │
                                 │  + RAG Orchestrator │
                                 └──────────┬──────────┘
                                            │
                           ┌────────────────┼────────────────┐
                           │                │                │
                           ▼                ▼                ▼
                      SQL filters      vector search     conversations
                           │                │                │
                           └────────────────┼────────────────┘
                                            ▼
                                   ┌────────────────┐
                                   │ PostgreSQL 16  │
                                   │  + pgvector    │
                                   └────────────────┘

 Kubernetes API
       │
       ▼
┌───────────────┐      ┌──────────────┐      ┌────────────────┐
│ K8s Watcher   │─────►│ NATS         │─────►│ Python Indexer │
│ Python/asyncio│      │ JetStream    │      │ + Embeddings   │
└───────────────┘      └──────────────┘      └────────────────┘
                                                  │
                                                  ▼
                                           PostgreSQL + pgvector

                         Observability
               ┌─────────────────────────────┐
               │ Prometheus + Grafana        │
               │ OpenTelemetry Collector     │
               └─────────────────────────────┘

                         Autoscaling
               ┌─────────────────────────────┐
               │ KEDA (NATS backlog metric)  │
               │ → scales indexer workers    │
               └─────────────────────────────┘
```

---

## 2. Technology Stack & Decision Rationale

### 2.1 Services & Frameworks

| Component | Tech Stack | Responsibility & Justification |
| :--- | :--- | :--- |
| **Watcher** | Python 3.12, `kubernetes`, `nats-py`, `pydantic`, `structlog` | Connects to Kubernetes API using async watch loops. Normalizes Pod, Event, Deployment, and Log streams into canonical `ClusterEvent` envelopes and publishes to NATS JetStream. |
| **Indexer** | Python 3.12, `sentence-transformers`, `asyncpg`, `sqlalchemy`, `alembic` | Consumes NATS events via durable JetStream subscriptions. Performs sliding-window chunking, generates local 384-d embeddings (`all-MiniLM-L6-v2`), and executes idempotent PostgreSQL/pgvector writes. |
| **API & RAG** | Node 20, TypeScript, Fastify, `@fastify/jwt`, `postgres`, `groq-sdk`, `zod` | Provides JWT authentication, cluster query routes, conversation state, and hybrid RAG orchestration (combining SQL filters + cosine vector similarity + Groq LLM reasoning). |
| **Frontend** | React 18, TypeScript, Vite, Vanilla CSS | Single Page Application (SPA) providing incident investigation chat, evidence visualizer, timeline viewer, and cluster event stream inspection. |

### 2.2 Infrastructure & Middleware

* **Local Cluster Orchestration**: `kind` (Kubernetes in Docker). Provides lightweight, reproducible single-node/multi-node Kubernetes development without cloud costs.
* **Event Stream / Broker**: `NATS JetStream`. Chosen over Kafka for minimal memory footprint (~15MB vs ~1GB+), built-in JetStream persistence, simple subject wildcarding (`k8s.events.*`), and easy KEDA metric integration.
* **Persistence & Vector Storage**: `PostgreSQL 16` + `pgvector`. Eliminates vector DB synchronization issues by storing structured facts (`cluster_events`, `resources`) and semantic vector embeddings (`document_embeddings`) in a single ACID-compliant transactional database.
* **Autoscaling**: `KEDA` (Kubernetes Event-driven Autoscaling). Monitors NATS pending message lag and dynamically scales the indexer deployment from 1 to 5 replicas during event bursts.
* **Observability**: Prometheus (metrics), Grafana (dashboards), OpenTelemetry Collector (OTLP gRPC/HTTP distributed tracing).

---

## 3. Data Pipelines & Flow Mechanics

### 3.1 Ingestion & Indexing Pipeline (Async / Event-Driven)

```text
1. Kubernetes Resource Event / Log
   ↓ Watcher captures via K8s Watch API (watch_pods, watch_events, etc.)
2. Canonical Normalization (ClusterEvent Pydantic envelope)
   ↓ Idempotency key: cluster_id + source + source_event_uid
3. Publish to NATS JetStream (subject: k8s.events.*)
   ↓ Stream: K8S_EVENTS (durable storage, at-least-once)
4. Indexer JetStream Consumer (consumer: INDEXER)
   ↓ Explicit ack after successful DB transaction
5. Chunking & Local Embedding
   ↓ sentence-transformers/all-MiniLM-L6-v2 (CPU execution)
6. PostgreSQL Transaction:
   ├── INSERT INTO cluster_events ON CONFLICT (cluster_id, event_uid) DO NOTHING
   ├── INSERT INTO documents (...)
   └── INSERT INTO document_embeddings (document_id, embedding, model)
```

### 3.2 Query & RAG Retrieval Pipeline (Synchronous / Interactive)

```text
1. User asks question: "Why did payments-api crash last night?"
   ↓ POST /api/v1/conversations/:id/messages
2. Intent & Time Extraction
   ↓ Extract target namespace ("payments"), resource ("payments-api"), time range
3. Hybrid Retrieval:
   ├── SQL Query: Exact match on cluster_id, namespace, severity, occurred_at window
   └── pgvector Query: Top-K cosine similarity on embedded query string
4. Merge, Deduplicate, & Score Reranking
   ↓ Combine similarity score + recency decay + Warning severity boost
5. Grounded Prompt Construction
   ↓ System prompt strictly mandates answering ONLY from provided EVIDENCE [1], [2]
6. Groq LLM Synthesis (Llama-3 8b)
   ↓ Returns structured answer, confidence rating, timeline, and citation IDs
```

---

## 4. Reliability & Edge Case Handling

1. **At-Least-Once Delivery & Idempotency**:
   * Consumer acks NATS messages *only after* DB transaction commit.
   * Duplicate events hit DB unique constraint `(cluster_id, event_uid)` and execute `ON CONFLICT DO NOTHING`, safely ignoring redeliveries.
2. **Dead Letter Queue (DLQ)**:
   * Messages exceeding `MAX_ATTEMPTS` (4 retries) or failing validation are routed to NATS subject `k8s.dlq` with failure metadata.
3. **Provider Abstraction**:
   * LLM calls are hidden behind the `LLMProvider` interface (`GroqProvider`, `MockLLMProvider`), allowing zero-cost unit/eval testing and provider hot-swapping.
4. **Rate Limit Resilience**:
   * Exponential backoff and jitter on LLM `429` rate limits.
5. **No Evidence Fallback**:
   * If retrieved documents score below threshold, system returns `confidence: "insufficient"` and states "Insufficient evidence to determine root cause" rather than hallucinating cluster state.

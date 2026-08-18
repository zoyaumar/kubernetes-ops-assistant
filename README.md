# Kubernetes Ops Assistant

> 🚧 **Work in Progress**

An event-driven, Kubernetes-native RAG system that monitors a Kubernetes cluster and answers natural-language questions about incidents, failures, and cluster activity using grounded evidence.

### Example

> **Why did `payments-api` crash last night?**

The system collects Kubernetes events and logs, indexes them, retrieves relevant evidence, and uses an LLM to explain what happened with citations.

---

## Architecture

```text
                         ┌──────────────┐
                         │   React UI   │
                         └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │ Node/TS API  │
                         │    + RAG     │
                         └──────┬───────┘
                                │
                       ┌────────┴─────────┐
                       ▼                  ▼
                Structured search   Vector search
                       │                  │
                       └────────┬─────────┘
                                ▼
                       ┌─────────────────┐
                       │   PostgreSQL    │
                       │   + pgvector    │
                       └─────────────────┘


 Kubernetes API
       │
       ▼
┌─────────────┐     ┌─────────────┐     ┌──────────────┐
│   Watcher   │────►│    NATS     │────►│   Indexer    │
│   Python    │     │  JetStream  │     │    Python    │
└─────────────┘     └─────────────┘     └──────────────┘
```

Local development runs on a lightweight **kind** Kubernetes cluster.

---

## Stack

* **Kubernetes:** kind
* **Backend:** Python + Node.js/TypeScript
* **Messaging:** NATS JetStream
* **Database:** PostgreSQL + pgvector
* **LLM:** Groq (free tier)
* **Embeddings:** Local open-source model
* **Autoscaling:** KEDA
* **Observability:** Prometheus + Grafana + OpenTelemetry
* **Frontend:** React
* **CI/CD:** GitHub Actions
* **Containers:** Docker

Designed to be fully usable with open-source/local infrastructure and free-tier services.

---

## Key Design Decisions

### At-least-once delivery

Use **at-least-once delivery + idempotent consumers** rather than relying on exactly-once semantics.

```text
NATS → Indexer → PostgreSQL → ACK
              ↓
           failure
              ↓
          redelivery
              ↓
       duplicate ignored
```

Stable event IDs and database uniqueness constraints make duplicate processing safe.

### Hybrid RAG

Combine multiple retrieval strategies:

```text
Structured filters
        +
Time filtering
        +
Vector similarity
        +
Ranking
```

### Provider abstraction

LLM calls use a provider interface so Groq can be replaced without changing the rest of the system.

### Least-privilege RBAC

The Kubernetes watcher uses a dedicated read-only ServiceAccount rather than `cluster-admin`.

### KEDA autoscaling

The indexer scales based on the NATS message backlog.

---

## Status

### 🚧 Work in Progress

* [ ] kind + project setup
* [ ] Kubernetes watcher
* [ ] NATS JetStream pipeline
* [ ] PostgreSQL + pgvector
* [ ] Embedding/indexing pipeline
* [ ] Node/TS RAG API
* [ ] Groq integration
* [ ] React chat UI
* [ ] RBAC + authentication
* [ ] Idempotency + retries + DLQ
* [ ] KEDA autoscaling
* [ ] Prometheus/Grafana/OpenTelemetry
* [ ] Unit/integration/E2E tests
* [ ] RAG evaluation
* [ ] GitHub Actions CI/CD

---

## Repository Structure

```text
apps/
├── watcher/       # Kubernetes events/logs → NATS
├── indexer/       # NATS → PostgreSQL + embeddings
└── api/           # Auth + retrieval + RAG + LLM

frontend/          # React UI
db/                # PostgreSQL schema/migrations
k8s/               # Kubernetes manifests
evals/             # RAG evaluation
docs/              # Architecture + ADRs
scripts/           # Local/demo scripts
```

---

## Local Development

### Prerequisites

* Docker
* kubectl
* kind
* Python
* Node.js

### Start

```bash
git clone https://github.com/your-org/k8s-ops-assistant.git
cd k8s-ops-assistant

make kind-up
make bootstrap
```

Configure the environment:

```env
GROQ_API_KEY=...
```

---

## Demo Goal

Create controlled failures such as:

```text
OOMKilled
CrashLoopBackOff
ImagePullBackOff
FailedScheduling
Failed deployment rollout
```

Then ask the assistant why the incident occurred and receive a grounded explanation backed by cluster evidence.

---

## License

MIT

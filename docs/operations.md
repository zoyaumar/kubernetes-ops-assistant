# Operations & Local Development Guide

## Prerequisites

1. **Docker Desktop**: Version 4.x+
2. **kind**: `kind --version` (v0.20+)
3. **kubectl**: `kubectl version --client`
4. **uv**: Fast Python package installer (`pip install uv`)
5. **Node.js**: v20+ & npm

---

## Getting Started (Local Setup)

1. **Environment Config**:
   ```bash
   cp .env.example .env
   # Set GROQ_API_KEY and JWT_SECRET in .env
   ```

2. **Bootstrap Cluster & Infrastructure**:
   ```bash
   make kind-up       # Spawns single-node kind cluster
   make bootstrap     # Applies namespace, RBAC, NATS, Postgres, and App manifests
   make db-migrate    # Runs Alembic migrations
   ```

3. **Port Forwarding Services**:
   ```bash
   bash scripts/port-forward.sh
   ```
   * React UI: http://localhost:5173
   * Node/TS API: http://localhost:3000
   * NATS Monitoring: http://localhost:8222
   * Grafana Dashboard: http://localhost:3001 (admin/admin)

4. **Seeding & Demo Scenarios**:
   ```bash
   make seed-cluster       # Deploys synthetic workload (payments-api)
   make generate-failure   # Triggers memory pressure & OOMKill
   ```

---

## Maintenance Commands

* **Run All Tests**: `make test`
* **Run Retrieval Evaluation**: `make eval-retrieval`
* **Reset Database**: `make db-reset`
* **Teardown Environment**: `make kind-down`

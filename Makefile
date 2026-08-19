# Kubernetes Ops Assistant — Makefile
#
# Targets are organized by lifecycle phase:
#   cluster   — kind cluster management
#   infra     — NATS / Postgres in-cluster
#   apps      — build and deploy application services
#   dev       — local development helpers
#   db        — database migrations and resets
#   test      — run test suites
#   eval      — RAG evaluation
#   obs       — observability (port-forwards)
#   clean     — teardown

.PHONY: help kind-up kind-down bootstrap build \
        db-migrate db-reset db-seed \
        test test-unit test-integration test-e2e \
        eval-retrieval eval-generation \
        port-forward-api port-forward-grafana port-forward-nats \
        seed-cluster generate-failure smoke-test \
        lint fmt clean

# ─── Defaults ──────────────────────────────────────────────────────────────────
CLUSTER_NAME ?= k8s-ops-assistant
NAMESPACE     ?= k8s-ops

# ─── Help ──────────────────────────────────────────────────────────────────────
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-28s\033[0m %s\n", $$1, $$2}'

# ─── Cluster ───────────────────────────────────────────────────────────────────
kind-up: ## Create the kind cluster
	@bash scripts/kind-up.sh

kind-down: ## Destroy the kind cluster
	@bash scripts/kind-down.sh

bootstrap: ## Apply base k8s manifests (namespace, RBAC, infra, apps)
	# TODO: apply k8s/base manifests in dependency order
	kubectl apply -f k8s/base/namespace.yaml
	kubectl apply -f k8s/base/serviceaccounts.yaml
	kubectl apply -f k8s/base/rbac.yaml
	kubectl apply -f k8s/base/nats.yaml
	kubectl apply -f k8s/base/postgres.yaml
	kubectl apply -f k8s/base/watcher.yaml
	kubectl apply -f k8s/base/indexer.yaml
	kubectl apply -f k8s/base/api.yaml
	kubectl apply -f k8s/base/frontend.yaml
	kubectl apply -f k8s/base/services.yaml

# ─── Database ──────────────────────────────────────────────────────────────────
db-migrate: ## Run Alembic migrations
	# TODO: wire to indexer pyproject.toml alembic entry
	cd apps/indexer && uv run alembic upgrade head

db-reset: ## Drop and recreate the database schema (DESTRUCTIVE)
	# TODO: implement reset via psql + alembic
	@echo "WARNING: this will drop all data in $(POSTGRES_DB)"
	@read -p "Are you sure? [y/N] " ans && [ $${ans:-N} = y ]
	cd apps/indexer && uv run alembic downgrade base && uv run alembic upgrade head

db-seed: ## Seed with synthetic Kubernetes events for local testing
	@bash scripts/seed-cluster.sh

# ─── Build ─────────────────────────────────────────────────────────────────────
build: ## Build all Docker images
	docker build -t watcher:dev apps/watcher
	docker build -t indexer:dev apps/indexer
	docker build -t api:dev apps/api
	docker build -t frontend:dev frontend

# ─── Tests ─────────────────────────────────────────────────────────────────────
test: test-unit test-integration ## Run unit + integration tests

test-unit: ## Run unit tests (pytest + vitest)
	cd apps/watcher && uv run pytest tests/unit -v
	cd apps/indexer && uv run pytest tests/unit -v
	cd apps/api && npm run test:unit

test-integration: ## Run integration tests (requires local Postgres + NATS)
	cd apps/watcher && uv run pytest tests/integration -v
	cd apps/indexer && uv run pytest tests/integration -v
	cd apps/api && npm run test:integration

test-e2e: ## Run Playwright E2E tests
	cd frontend && npx playwright test

# ─── RAG Evaluation ────────────────────────────────────────────────────────────
eval-retrieval: ## Evaluate retrieval quality (Recall@K, Precision@K, MRR)
	cd evals && uv run python retrieval/evaluate.py

eval-generation: ## Evaluate LLM answer quality (citation correctness, faithfulness)
	cd evals && uv run python generation/evaluate.py

# ─── Lint / Format ─────────────────────────────────────────────────────────────
lint: ## Lint all services
	cd apps/watcher && uv run ruff check app tests
	cd apps/indexer && uv run ruff check app tests
	cd apps/api && npm run lint
	cd frontend && npm run lint

fmt: ## Auto-format all services
	cd apps/watcher && uv run ruff format app tests
	cd apps/indexer && uv run ruff format app tests
	cd apps/api && npm run fmt
	cd frontend && npm run fmt

# ─── Observability port-forwards ───────────────────────────────────────────────
port-forward-api: ## Forward API service to localhost:3000
	kubectl port-forward -n $(NAMESPACE) svc/api 3000:3000

port-forward-grafana: ## Forward Grafana to localhost:3001
	kubectl port-forward -n $(NAMESPACE) svc/grafana 3001:3000

port-forward-nats: ## Forward NATS to localhost:4222
	kubectl port-forward -n $(NAMESPACE) svc/nats 4222:4222

# ─── Demo helpers ──────────────────────────────────────────────────────────────
seed-cluster: ## Deploy synthetic workloads for demo
	@bash scripts/seed-cluster.sh

generate-failure: ## Trigger an OOMKilled / CrashLoopBackOff scenario
	@bash scripts/generate-failure.sh

smoke-test: ## Basic end-to-end smoke test against the live cluster
	@bash scripts/smoke-test.sh

# ─── Vector search shortcut ────────────────────────────────────────────────────
search: ## Run a standalone retrieval query. Usage: make search QUERY="why did payments-api crash?"
	# TODO: implement standalone retrieval script in scripts/search.py
	cd apps/indexer && uv run python -m app.search "$(QUERY)"

# ─── Clean ─────────────────────────────────────────────────────────────────────
clean: ## Remove local build artefacts
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf apps/api/dist frontend/dist

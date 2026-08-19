# Troubleshooting Guide

## Common Issues & Diagnoses

### 1. Watcher fails to connect to Kubernetes API
* **Symptoms**: Watcher pod crashes or logs `Forbidden` errors.
* **Diagnosis**: Check if RBAC ServiceAccount is bound.
* **Fix**:
  ```bash
  kubectl auth can-i list pods -n default --as=system:serviceaccount:k8s-ops:k8s-ops-watcher
  kubectl apply -f k8s/base/rbac.yaml
  ```

### 2. Indexer unable to process NATS stream
* **Symptoms**: NATS backlog growing (`nats stream info K8S_EVENTS`), zero documents in Postgres.
* **Diagnosis**: Check DB connection string and vector extension initialization.
* **Fix**:
  ```bash
  kubectl logs -n k8s-ops deploy/indexer
  kubectl exec -n k8s-ops deploy/postgres -- psql -U k8s_ops -d k8s_ops -c "\dx"
  ```

### 3. LLM Rate Limit (`429 Too Many Requests`)
* **Symptoms**: API returns `LLMRateLimitError`.
* **Fix**: Check `GROQ_API_KEY` quota or switch provider to `mock` for local dev tests in `.env`:
  ```ini
  LLM_PROVIDER=mock
  ```

### 4. KEDA ScaledObject Not Scaling Indexer
* **Symptoms**: Replicas stay at 1 even when 1,000 events are queued.
* **Diagnosis**: Check KEDA CRD status and NATS monitoring endpoint (`:8222`).
* **Fix**:
  ```bash
  kubectl get scaledobject -n k8s-ops
  kubectl describe scaledobject indexer-scaledobject -n k8s-ops
  ```

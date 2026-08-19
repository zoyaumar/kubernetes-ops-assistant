"""Kubernetes Ops Assistant — Indexer / Processor service.

Responsibilities
----------------
* Subscribe to NATS JetStream stream K8S_EVENTS with durable consumer INDEXER.
* Use at-least-once delivery with explicit acknowledgement.
* Normalize, validate, and deduplicate incoming ClusterEvent envelopes.
* Chunk long log content into embeddable units.
* Generate embeddings using a local sentence-transformers model.
* Persist structured data to PostgreSQL (cluster_events, documents, resources).
* Persist embeddings to pgvector (document_embeddings).
* Route failed messages to the DLQ after bounded retries.
* Expose /health and /metrics endpoints.
"""

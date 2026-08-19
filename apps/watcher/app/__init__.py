"""Kubernetes Ops Assistant — Watcher service.

Responsibilities
----------------
* Connect to the Kubernetes API using in-cluster config (or kubeconfig for local dev).
* Watch Pods, Events, Deployments, and collect Pod logs.
* Normalize every Kubernetes signal into the canonical ClusterEvent envelope.
* Publish envelopes to NATS JetStream (subject: k8s.events.*)
  with at-least-once delivery semantics.
* Expose /health and /ready HTTP endpoints for Kubernetes probes.
* Expose Prometheus metrics at /metrics.
"""

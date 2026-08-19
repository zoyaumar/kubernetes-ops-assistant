"""Health and metrics HTTP server for the indexer.

Endpoints
---------
GET /health  — liveness
GET /ready   — readiness: requires DB connection and embedding model loaded
GET /metrics — Prometheus
"""

from __future__ import annotations

# TODO(week-7): implement (mirror of watcher/app/health.py)

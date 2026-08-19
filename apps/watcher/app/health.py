"""Lightweight HTTP health server for Kubernetes liveness and readiness probes.

Endpoints
---------
GET /health  — liveness:  returns 200 if the process is running.
GET /ready   — readiness: returns 200 only when NATS is connected and
               at least one watcher loop is active.
GET /metrics — Prometheus metrics (delegated to prometheus_client).
"""

from __future__ import annotations

# TODO(week-2): implement aiohttp-based health server
# Suggested structure:
#
#   async def health_handler(request) -> web.Response: ...
#   async def ready_handler(request, nats_client, watcher_tasks) -> web.Response: ...
#   async def metrics_handler(request) -> web.Response: ...
#
#   async def start_health_server(port: int, ...) -> web.AppRunner: ...

"""Watcher service entry point.

Starts all watcher coroutines concurrently and handles graceful shutdown.

Shutdown sequence
-----------------
1. Receive SIGTERM / SIGINT.
2. Cancel watcher tasks.
3. Flush buffered NATS messages (bounded buffer).
4. Close NATS connection.
5. Stop health/metrics HTTP server.
"""

from __future__ import annotations

import asyncio
import signal
import sys

import structlog

from app.config import Settings
from app.logging import configure_logging

log = structlog.get_logger(__name__)


async def main() -> None:
    """Bootstrap and run the watcher service."""
    settings = Settings()  # Loaded from environment / .env
    configure_logging(settings.log_level)

    log.info("watcher.starting", cluster_id=settings.cluster_id)

    # TODO(week-2): initialise NATS publisher
    # TODO(week-2): initialise Kubernetes client
    # TODO(week-2): start health HTTP server (aiohttp)
    # TODO(week-2): start pod watcher coroutine
    # TODO(week-2): start event watcher coroutine
    # TODO(week-2): start deployment watcher coroutine
    # TODO(week-2): start log ingestion coroutine
    # TODO(week-7): start Prometheus metrics server
    # TODO(week-7): initialise OpenTelemetry tracer

    # Placeholder: keep the process alive until cancelled
    stop_event = asyncio.Event()

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, stop_event.set)

    await stop_event.wait()
    log.info("watcher.stopping")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)

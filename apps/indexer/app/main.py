"""Indexer service entry point.

Lifecycle
---------
1. Load settings from environment.
2. Set up structured logging + OTel.
3. Connect to PostgreSQL (verify schema is migrated).
4. Load embedding model (cached in container filesystem).
5. Connect to NATS and subscribe to JetStream consumer.
6. Start consuming messages (concurrent workers bounded by settings).
7. Handle SIGTERM gracefully — finish in-flight messages before exiting.
"""

from __future__ import annotations

import asyncio
import signal
import sys

import structlog

from app.config import Settings

log = structlog.get_logger(__name__)


async def main() -> None:
    """Bootstrap and run the indexer service."""
    settings = Settings()

    # TODO(week-3): configure logging
    # TODO(week-3): initialise OTel tracer
    # TODO(week-3): connect to PostgreSQL (asyncpg pool)
    # TODO(week-4): load embedding model (sentence-transformers)
    # TODO(week-3): connect to NATS JetStream
    # TODO(week-3): start consumer workers (asyncio.gather with semaphore)
    # TODO(week-7): start health + metrics HTTP server

    log.info("indexer.starting")

    stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, stop_event.set)

    await stop_event.wait()
    log.info("indexer.stopping")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)

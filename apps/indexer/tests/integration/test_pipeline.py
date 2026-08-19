"""Integration test: full message pipeline.

Tests
-----
* Publish a synthetic ClusterEvent to NATS.
* Assert the event appears in cluster_events table.
* Assert a document record is created.
* Publish the same event again (duplicate).
* Assert only one record in cluster_events (idempotency).
"""

import pytest

# TODO(week-3): implement once NATS consumer and repositories are wired up


@pytest.mark.skip(reason="requires NATS + PostgreSQL — implement in week 3")
async def test_end_to_end_pipeline() -> None:
    pass


@pytest.mark.skip(reason="requires PostgreSQL — implement in week 3")
async def test_duplicate_event_is_idempotent() -> None:
    pass

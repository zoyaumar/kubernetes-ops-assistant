"""Cluster events repository.

Handles idempotent insertion of cluster_events, resources, and the
associated documents row.

Idempotency
-----------
All inserts use ON CONFLICT DO NOTHING keyed on (cluster_id, event_uid).
A duplicate event results in a no-op at the DB level; the consumer
can safely ack the NATS message.
"""

from __future__ import annotations

# TODO(week-3): implement
# Suggested interface:
#
# class EventRepository:
#     def __init__(self, session: AsyncSession) -> None: ...
#
#     async def upsert_cluster(self, cluster_id: str, name: str) -> UUID: ...
#
#     async def upsert_resource(self, ...) -> UUID: ...
#
#     async def insert_event(
#         self,
#         cluster_id: UUID,
#         event: NormalizedEvent,
#     ) -> UUID | None:
#         """Returns the new event UUID, or None if duplicate."""
#
#     async def insert_document(
#         self,
#         cluster_id: UUID,
#         event_id: UUID | None,
#         content: str,
#         metadata: dict,
#         occurred_at: datetime,
#     ) -> UUID: ...

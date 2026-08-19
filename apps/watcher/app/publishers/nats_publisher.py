"""NATS JetStream publisher.

Responsibilities
----------------
* Publish ClusterEvent envelopes to NATS subjects.
* Reconnect to NATS with exponential backoff if the connection drops.
* Buffer at most NATS_BUFFER_MAX events in memory while disconnected.
  If the buffer is full, drop the event and increment `nats_buffer_overflow_total`.
* Serialize events to JSON before publishing.

Reliability note
----------------
The watcher is a producer, not a consumer. It does not use acks.
At-least-once delivery is guaranteed by the JetStream stream on the
consumer (indexer) side, not here.
"""

from __future__ import annotations

# TODO(week-2): implement
# Suggested interface:
#
# class NatsPublisher:
#     def __init__(self, settings: Settings) -> None: ...
#     async def connect(self) -> None: ...
#     async def publish(self, event: ClusterEvent, subject: str) -> None: ...
#     async def close(self) -> None: ...

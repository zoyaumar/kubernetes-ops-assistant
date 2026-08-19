"""Dead Letter Queue (DLQ) handler.

A message is sent to the DLQ when:
* It fails processing after max_attempts retries.
* It fails schema validation (malformed event).

DLQ NATS subject: k8s.dlq

The DLQ message preserves:
* Original payload
* Failure reason
* Attempt count
* Timestamp of first and last attempt

DLQ inspection
--------------
The API exposes:
  GET  /api/v1/dead-letters
  POST /api/v1/dead-letters/:id/retry

See the API routes for the operator-facing interface.
"""

from __future__ import annotations

# TODO(week-3): implement
# Suggested interface:
#
# class DLQHandler:
#     def __init__(self, nats_publisher: NatsPublisher, dlq_subject: str) -> None: ...
#
#     async def send_to_dlq(
#         self,
#         original_payload: bytes,
#         reason: str,
#         attempt_count: int,
#     ) -> None: ...

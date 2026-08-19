"""NATS JetStream durable consumer.

Design
------
* Uses push-based JetStream subscription with explicit ack.
* At-least-once delivery: a message is redelivered if ack is not received.
* Bounded concurrency: asyncio.Semaphore(settings.worker_concurrency).
* Retry tracking: attempt count is stored in message headers.
  After max_attempts, the message is acked (to remove from stream) and
  published to the DLQ.

Acknowledgement contract
------------------------
A message is acked ONLY after the DB transaction commits successfully.
If the indexer crashes after writing but before acking, NATS will
redeliver the message. The idempotency check in the repository layer
will detect the duplicate and skip re-insertion safely.
"""

from __future__ import annotations

# TODO(week-3): implement
# Suggested interface:
#
# class NatsConsumer:
#     def __init__(self, settings: Settings, processor: MessageProcessor) -> None: ...
#     async def connect(self) -> None: ...
#     async def start(self) -> None:
#         # subscribe to JetStream, process messages with semaphore
#     async def _handle_message(self, msg: nats.aio.client.Msg) -> None:
#         async with self._semaphore:
#             await self._processor.process(msg)
#     async def close(self) -> None: ...

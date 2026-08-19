"""Pod lifecycle watcher.

Watches Pod events across configured namespaces and emits ClusterEvent
envelopes for:
* Pod phase transitions (Pending → Running → Succeeded / Failed)
* Container status changes (OOMKilled, CrashLoopBackOff, Error, etc.)
* Restart count changes
* Termination reasons

NATS subject: k8s.events.pod
"""

from __future__ import annotations

# TODO(week-2): implement
# Outline:
#
# async def watch_pods(
#     k8s: KubernetesClient,
#     publisher: NatsPublisher,
#     settings: Settings,
# ) -> None:
#     """Infinite loop — reconnects on error with exponential backoff."""
#     while True:
#         try:
#             async for event in k8s.core().list_pod_for_all_namespaces(watch=True):
#                 envelope = _normalize(event, settings.cluster_id)
#                 await publisher.publish(envelope, subject="k8s.events.pod")
#         except Exception as exc:
#             log.warning("pod_watcher.error", exc=exc)
#             await asyncio.sleep(backoff)

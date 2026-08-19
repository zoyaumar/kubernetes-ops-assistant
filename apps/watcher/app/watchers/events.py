"""Kubernetes Event watcher.

Watches the core Events API (v1.Event) and emits ClusterEvent envelopes for:
* Warning events (OOMKilled, BackOff, Failed, FailedScheduling, etc.)
* Normal events for baseline context

NATS subjects:
  k8s.events.warning  — for type=Warning events
  k8s.events.normal   — for type=Normal events

Idempotency key: cluster_id + kubernetes + event.metadata.uid
"""

from __future__ import annotations

# TODO(week-2): implement

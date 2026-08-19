"""Deployment watcher.

Watches Deployment resources and emits ClusterEvent envelopes for:
* Replica count changes (scale up/down)
* Rollout transitions (Progressing, Available, Degraded)
* Image version changes
* Generation bumps (new rollout initiated)

NATS subject: k8s.events.deployment
"""

from __future__ import annotations

# TODO(week-2): implement

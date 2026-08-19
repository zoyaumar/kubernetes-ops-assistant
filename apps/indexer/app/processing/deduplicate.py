"""Idempotency / deduplication logic.

Strategy
--------
The cluster_events table has a UNIQUE constraint on (cluster_id, event_uid).
On INSERT conflict we use ON CONFLICT DO NOTHING (PostgreSQL upsert).

The idempotency key is derived as:
    cluster_id + source + source_event_uid

Where source_event_uid is the Kubernetes object UID, NOT a generated ULID.
The ULID in the envelope is the NATS message ID; the source_event_uid is
the stable key used for deduplication.

Design note
-----------
Do not use the envelope event_id as the only idempotency key.
The watcher could restart and generate a new ULID for the same
underlying Kubernetes event. Use the Kubernetes UID instead.
"""

from __future__ import annotations

# TODO(week-3): implement
# Suggested helper:
#
# def build_idempotency_key(cluster_id: str, source: str, uid: str) -> str:
#     """Returns a stable key for duplicate detection."""
#     return f"{cluster_id}::{source}::{uid}"

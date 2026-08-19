"""Canonical ClusterEvent envelope — the single wire format for all NATS messages.

Every watcher (pods, events, deployments, logs) normalizes its Kubernetes
source into this schema before publishing to NATS.

The indexer on the other side deserializes from this same schema.

Idempotency
-----------
The `event_uid` field is the STABLE idempotency key. It is derived from
the underlying Kubernetes object UID (not regenerated each time).

This prevents the watcher from re-inserting an event it has already published
if the stream replays or if the watcher restarts.

Schema versioning
-----------------
`schema_version` allows the indexer to handle migration gracefully if
the envelope shape changes. Start at 1.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ResourceIdentity(BaseModel):
    """Identifies the Kubernetes resource that generated the event."""

    uid: str = Field(description="Kubernetes object metadata.uid")
    kind: str = Field(description="e.g. Pod, Deployment, Node")
    namespace: str | None = Field(default=None)
    name: str
    container: str | None = Field(default=None, description="Set for container-level events")


class ClusterEvent(BaseModel):
    """Canonical event envelope published to NATS.

    All fields except `payload` are indexed in PostgreSQL for structured
    filtering. `payload` is stored in the metadata JSONB column and used
    to build the searchable document for pgvector.
    """

    # Globally unique event identifier (ULID recommended for sortability)
    event_id: str = Field(description="Stable, unique event ID (ULID)")

    # Incremented when this schema changes — consumers can branch on this
    schema_version: int = Field(default=1)

    cluster_id: str = Field(description="Must match clusters.name in the DB")
    source: str = Field(default="kubernetes", description="Origin system")

    # Hierarchical event type — determines NATS subject routing
    # Examples: pod.event, pod.log, deployment.event, node.event
    event_type: str

    occurred_at: datetime = Field(description="When the event happened in the cluster")
    received_at: datetime = Field(description="When the watcher received the event")

    resource: ResourceIdentity

    # Raw payload — varies by event_type; stored as JSONB
    payload: dict[str, Any] = Field(default_factory=dict)

    # Optional human-readable summary (used as the primary text for embedding)
    message: str | None = Field(default=None)

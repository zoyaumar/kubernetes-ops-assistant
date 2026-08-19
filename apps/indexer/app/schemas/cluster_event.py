"""ClusterEvent schema — deserialization side (indexer).

This is the same canonical envelope as apps/watcher/app/schemas/cluster_event.py.

TODO(week-1): Once the packages/event-schema shared package is set up,
both watcher and indexer should import from there instead of maintaining
two copies. For the initial scaffold, duplicating is acceptable.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ResourceIdentity(BaseModel):
    uid: str
    kind: str
    namespace: str | None = None
    name: str
    container: str | None = None


class ClusterEvent(BaseModel):
    event_id: str
    schema_version: int = 1
    cluster_id: str
    source: str = "kubernetes"
    event_type: str
    occurred_at: datetime
    received_at: datetime
    resource: ResourceIdentity
    payload: dict[str, Any] = Field(default_factory=dict)
    message: str | None = None

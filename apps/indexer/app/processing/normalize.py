"""Event normalization.

Converts a raw ClusterEvent envelope from NATS into domain objects
suitable for database insertion.

Normalization rules
-------------------
* Validate the envelope against ClusterEvent schema.
* Reject (DLQ) if schema_version is unsupported.
* Derive the document.content text from the event message + payload fields.
  This text is what gets embedded and indexed for semantic search.
* Map event_type to event_type_enum values used in the DB.
* Extract severity from Kubernetes event type (Warning / Normal).
"""

from __future__ import annotations

# TODO(week-3): implement

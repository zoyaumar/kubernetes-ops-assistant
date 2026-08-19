"""Unit tests for the ClusterEvent schema.

Tests
-----
* Schema validation accepts a valid envelope.
* Schema rejects missing required fields.
* Schema version defaults to 1.
* event_uid is required (idempotency key).
"""

import pytest
from pydantic import ValidationError

from app.schemas.cluster_event import ClusterEvent, ResourceIdentity


# TODO(week-2): expand these stubs into real tests

def test_cluster_event_requires_event_id() -> None:
    """ClusterEvent must have a stable event_id."""
    with pytest.raises(ValidationError):
        ClusterEvent.model_validate({})  # type: ignore[arg-type]


def test_cluster_event_schema_version_defaults_to_1() -> None:
    """schema_version defaults to 1 if not provided."""
    # TODO: build a minimal valid ClusterEvent and assert schema_version == 1
    pass

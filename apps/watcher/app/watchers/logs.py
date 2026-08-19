"""Pod log ingestion.

Polls application container logs for configured namespaces.

Constraints (to avoid storage explosion)
-----------------------------------------
* Application containers only (no sidecar/infrastructure containers by default).
* Chunked at LOG_MAX_BYTES_PER_CHUNK bytes.
* Only LOG_LOOKBACK_SECONDS of history on startup.
* Rate-limited per pod.
* Only namespaces in LOG_NAMESPACES.

NATS subject: k8s.events (source_type: pod_log)

Do NOT tail logs infinitely without bounds — this can fill storage quickly.
"""

from __future__ import annotations

# TODO(week-2): implement

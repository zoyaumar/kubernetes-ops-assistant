"""Watcher service configuration.

All settings are loaded from environment variables (or .env file via pydantic-settings).
See .env.example at the repo root for reference values.
"""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration for the watcher service."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Cluster identity — must match the cluster_id in the DB so that all
    # services reference the same cluster record.
    cluster_id: str = Field(default="local-kind", alias="CLUSTER_ID")

    # NATS connection
    nats_url: str = Field(default="nats://localhost:4222", alias="NATS_URL")
    nats_stream_name: str = Field(default="K8S_EVENTS", alias="NATS_STREAM_NAME")
    nats_dlq_subject: str = Field(default="k8s.dlq", alias="NATS_DLQ_SUBJECT")

    # In-memory publish buffer cap.
    # If NATS is unavailable the watcher will hold at most this many events
    # before dropping (and recording a metric). Do NOT allow unbounded growth.
    nats_buffer_max: int = Field(default=500, alias="NATS_BUFFER_MAX")

    # Log ingestion controls — logs are noisy; constrain carefully.
    log_namespaces: list[str] = Field(
        default=["default", "payments", "k8s-ops"],
        alias="LOG_NAMESPACES",
    )
    log_max_bytes_per_chunk: int = Field(
        default=8192,  # 8 KiB per chunk
        alias="LOG_MAX_BYTES_PER_CHUNK",
    )
    log_lookback_seconds: int = Field(
        default=300,  # 5 minutes on startup
        alias="LOG_LOOKBACK_SECONDS",
    )

    # Health / metrics HTTP server
    health_port: int = Field(default=8080, alias="HEALTH_PORT")

    # Observability
    log_level: str = Field(default="info", alias="LOG_LEVEL")
    otel_endpoint: str = Field(
        default="http://localhost:4318",
        alias="OTEL_EXPORTER_OTLP_ENDPOINT",
    )

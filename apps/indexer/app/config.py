"""Indexer service configuration."""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration for the indexer service."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    cluster_id: str = Field(default="local-kind", alias="CLUSTER_ID")

    # NATS
    nats_url: str = Field(default="nats://localhost:4222", alias="NATS_URL")
    nats_stream_name: str = Field(default="K8S_EVENTS", alias="NATS_STREAM_NAME")
    nats_consumer_name: str = Field(default="INDEXER", alias="NATS_CONSUMER_NAME")
    nats_dlq_subject: str = Field(default="k8s.dlq", alias="NATS_DLQ_SUBJECT")

    # How many messages to process concurrently.
    # KEDA will scale replicas; within each replica limit concurrency here.
    worker_concurrency: int = Field(default=5, alias="WORKER_CONCURRENCY")

    # Max processing attempts before routing to DLQ
    max_attempts: int = Field(default=4, alias="MAX_ATTEMPTS")

    # PostgreSQL
    postgres_dsn: str = Field(
        default="postgresql+asyncpg://k8s_ops:changeme@localhost:5432/k8s_ops",
        alias="POSTGRES_DSN",
    )

    # Embedding model
    # IMPORTANT: the DB schema (document_embeddings.embedding dimension) must match.
    # After choosing a model, run a migration to set the correct VECTOR(...) dimension.
    embedding_model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        alias="EMBEDDING_MODEL",
    )
    # Dimension MUST match embedding_model output. Do not hard-code.
    embedding_dim: int = Field(default=384, alias="EMBEDDING_DIM")

    # Chunking
    chunk_max_chars: int = Field(default=2000, alias="CHUNK_MAX_CHARS")
    chunk_overlap_chars: int = Field(default=200, alias="CHUNK_OVERLAP_CHARS")

    # Observability
    log_level: str = Field(default="info", alias="LOG_LEVEL")
    otel_endpoint: str = Field(
        default="http://localhost:4318",
        alias="OTEL_EXPORTER_OTLP_ENDPOINT",
    )
    health_port: int = Field(default=8081, alias="HEALTH_PORT")

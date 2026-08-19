"""Structured logging configuration using structlog.

All services emit JSON logs so that:
* Kubernetes log aggregators (Loki, Fluentd, etc.) can parse them.
* OpenTelemetry trace/span IDs can be injected automatically.
* request_id and event_id fields are propagated via contextvars.
"""

from __future__ import annotations

import logging
import sys

import structlog


def configure_logging(level: str = "info") -> None:
    """Set up structlog with JSON output and stdlib integration.

    Args:
        level: Log level string (debug, info, warning, error).
    """
    log_level = getattr(logging, level.upper(), logging.INFO)

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            # TODO(week-7): inject OTel trace_id / span_id here
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        logger_factory=structlog.PrintLoggerFactory(sys.stdout),
        cache_logger_on_first_use=True,
    )

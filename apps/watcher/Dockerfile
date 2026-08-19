# syntax=docker/dockerfile:1
# ─── Watcher service Dockerfile ───────────────────────────────────────────────
# Uses uv for fast, deterministic dependency installation.
# Runs as a non-root user for security.

FROM python:3.12-slim AS base

# Install uv
RUN pip install --no-cache-dir uv

WORKDIR /app

# Copy dependency manifests first (layer cache optimisation)
COPY pyproject.toml .

# Install production dependencies only
RUN uv sync --no-dev

# Copy application source
COPY app/ app/

# Run as non-root
RUN useradd -m -u 1001 watcher
USER watcher

# Health probe port
EXPOSE 8080

# TODO(week-2): replace with a proper entrypoint once main.py is implemented
CMD ["uv", "run", "python", "-m", "app.main"]

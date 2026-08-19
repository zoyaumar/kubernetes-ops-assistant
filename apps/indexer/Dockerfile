# syntax=docker/dockerfile:1
# ─── Indexer service Dockerfile ───────────────────────────────────────────────
#
# NOTE: The sentence-transformers model is downloaded at first run and cached.
# For production images, bake the model into the image during build to avoid
# network calls at runtime:
#
#   RUN python -c "from sentence_transformers import SentenceTransformer; \
#       SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"
#
# This adds ~80MB to the image but removes the startup download.

FROM python:3.12-slim AS base

# Install uv
RUN pip install --no-cache-dir uv

WORKDIR /app

COPY pyproject.toml .

# CPU-only torch (avoids pulling 2+ GB GPU wheels)
# TODO: add --extra-index-url https://download.pytorch.org/whl/cpu if needed
RUN uv sync --no-dev

COPY app/ app/

RUN useradd -m -u 1001 indexer
USER indexer

EXPOSE 8081

CMD ["uv", "run", "python", "-m", "app.main"]

"""Text chunking for long log entries.

Motivation
----------
Embedding models have a fixed token limit (e.g. all-MiniLM-L6-v2: 256 tokens).
Log entries can be much longer. Chunking splits them into overlapping windows
so that each chunk fits within the model's context window.

Strategy
--------
* Character-based splitting with overlap.
* Each chunk becomes its own document record with the same source_id.
* Chunk metadata includes: chunk_index, total_chunks, source_type, source_id.

Config
------
See Settings.chunk_max_chars and Settings.chunk_overlap_chars.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Chunk:
    """A single text chunk with position metadata."""

    content: str
    chunk_index: int
    total_chunks: int
    source_id: str
    source_type: str


def chunk_text(
    text: str,
    source_id: str,
    source_type: str,
    max_chars: int = 2000,
    overlap_chars: int = 200,
) -> list[Chunk]:
    """Split `text` into overlapping chunks.

    Args:
        text: Input text to chunk.
        source_id: ID of the originating document/event.
        source_type: e.g. 'pod_log', 'cluster_event'.
        max_chars: Maximum characters per chunk.
        overlap_chars: Characters to repeat between adjacent chunks.

    Returns:
        List of Chunk objects (at least one, even for short inputs).
    """
    # TODO(week-4): implement sliding window chunking
    raise NotImplementedError

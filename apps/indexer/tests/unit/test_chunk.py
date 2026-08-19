"""Unit tests for the chunking module.

Tests
-----
* Short text produces one chunk.
* Long text produces multiple overlapping chunks.
* Overlap characters appear in adjacent chunks.
* Each chunk carries correct chunk_index and total_chunks.
"""

import pytest

from app.processing.chunk import Chunk, chunk_text


# TODO(week-4): un-skip once chunk_text is implemented

@pytest.mark.skip(reason="chunk_text not yet implemented")
def test_short_text_produces_one_chunk() -> None:
    chunks = chunk_text("hello world", "src-1", "pod_log")
    assert len(chunks) == 1
    assert chunks[0].chunk_index == 0
    assert chunks[0].total_chunks == 1


@pytest.mark.skip(reason="chunk_text not yet implemented")
def test_long_text_produces_multiple_chunks() -> None:
    text = "x" * 5000
    chunks = chunk_text(text, "src-1", "pod_log", max_chars=2000, overlap_chars=200)
    assert len(chunks) > 1
    # Last chunk must end where the text ends
    assert "".join(c.content for c in chunks[-1:]).endswith("x")

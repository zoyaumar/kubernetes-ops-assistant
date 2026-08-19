"""Embedding provider Protocol definition.

Any class that implements this Protocol can be used as an embedding backend.
This allows tests to use a stub instead of loading the real model.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class EmbeddingProvider(Protocol):
    """Interface for embedding backends.

    Implementations must be async-capable because embedding a batch
    of texts may involve I/O (remote API) or blocking CPU work
    (run_in_executor for local models).
    """

    model_name: str
    dimensions: int

    async def embed(self, texts: list[str]) -> list[list[float]]:
        """Embed a batch of texts.

        Args:
            texts: Non-empty list of strings to embed.

        Returns:
            List of float vectors, one per input text.
            Each vector has length == self.dimensions.
        """
        ...

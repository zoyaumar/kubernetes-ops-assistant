"""Local CPU embedding provider using sentence-transformers.

Model selection
---------------
Default: sentence-transformers/all-MiniLM-L6-v2
  - 384 dimensions
  - ~80 MB disk
  - Fast on CPU
  - Good quality for retrieval tasks

The model is downloaded once and cached. Set HF_HOME or
TRANSFORMERS_CACHE env var to control cache location.

Thread safety
-------------
SentenceTransformer.encode() is blocking. We run it in a thread pool
executor to avoid blocking the asyncio event loop.
"""

from __future__ import annotations

import asyncio
from concurrent.futures import ThreadPoolExecutor


class LocalEmbeddingProvider:
    """sentence-transformers embedding provider."""

    def __init__(self, model_name: str, dimensions: int) -> None:
        self.model_name = model_name
        self.dimensions = dimensions
        self._model = None  # Lazy-loaded on first use
        self._executor = ThreadPoolExecutor(max_workers=1)

    def _load_model(self) -> None:
        """Download/load the model (blocking — run once at startup)."""
        # TODO(week-4): from sentence_transformers import SentenceTransformer
        # self._model = SentenceTransformer(self.model_name)
        raise NotImplementedError

    async def embed(self, texts: list[str]) -> list[list[float]]:
        """Embed texts in a thread pool to avoid blocking the event loop."""
        # TODO(week-4): implement
        # loop = asyncio.get_running_loop()
        # result = await loop.run_in_executor(
        #     self._executor,
        #     lambda: self._model.encode(texts, convert_to_numpy=True).tolist(),
        # )
        # return result
        raise NotImplementedError

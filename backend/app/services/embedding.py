import hashlib
from functools import lru_cache
from typing import List

import numpy as np

from app.core.config import settings


class LocalEmbeddingClient:
    """Deterministic hash-based embedding for offline environments."""

    def __init__(self, dimensions: int = 128, seed: int = 13):
        self.dimensions = dimensions
        self.seed = seed

    def embed(self, text: str) -> List[float]:
        tokens = text.split()
        if not tokens:
            return [0.0] * self.dimensions
        vector = np.zeros(self.dimensions, dtype=np.float32)
        for token in tokens:
            digest = hashlib.sha256(f"{self.seed}:{token}".encode("utf-8")).digest()
            idx = digest[0] % self.dimensions
            sign = 1 if digest[1] % 2 == 0 else -1
            weight = (digest[2] / 255.0) + 0.5
            vector[idx] += sign * weight
        norm = np.linalg.norm(vector)
        if norm:
            vector /= norm
        return vector.astype(np.float32).tolist()


@lru_cache(maxsize=1)
def get_embedding_client() -> LocalEmbeddingClient:
    # Placeholder for future provider selection (OpenAI, etc.)
    return LocalEmbeddingClient(dimensions=settings.embedding_dimensions)


def embed_text(text: str) -> List[float]:
    client = get_embedding_client()
    return client.embed(text)


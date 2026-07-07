import os
import time
import requests
import numpy as np


class EmbeddingModel:
    """
    Generates embeddings via the Hugging Face Inference API instead of
    running sentence-transformers/torch locally — keeps memory usage low
    enough for Render's free tier.
    """

    API_URL = (
        "https://router.huggingface.co/hf-inference/models/"
        "sentence-transformers/all-MiniLM-L6-v2/pipeline/feature-extraction"
    )

    def __init__(self):
        self.token = os.getenv("HF_API_TOKEN")
        if not self.token:
            raise RuntimeError(
                "HF_API_TOKEN environment variable is not set. "
                "Get a free token at https://huggingface.co/settings/tokens"
            )
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def _query(self, payload, max_retries=5):
        for attempt in range(max_retries):
            response = requests.post(
                self.API_URL, headers=self.headers, json=payload, timeout=30
            )

            if response.status_code == 200:
                return response.json()

            # Model is cold-starting on HF's side — wait and retry.
            if response.status_code == 503:
                time.sleep(3)
                continue

            raise RuntimeError(
                f"HF Inference API error {response.status_code}: {response.text}"
            )

        raise RuntimeError("HF Inference API did not respond after retries.")

    def embed_documents(self, chunks):
        result = self._query({"inputs": chunks})
        return np.array(result)

    def embed_query(self, question):
        result = self._query({"inputs": question})
        return np.array(result)
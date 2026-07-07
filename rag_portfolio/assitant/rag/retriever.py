import numpy as np


class Retriever:

    def __init__(self, vector_store, embedder):
        self.vector_store = vector_store
        self.embedder = embedder

    def retrieve(self, question, k=3):

        # Load FAISS index and chunks
        index, chunks = self.vector_store.load_index()

        # Convert question to embedding
        query_embedding = self.embedder.embed_query(question)

        query_embedding = np.array(
            [query_embedding],
            dtype="float32"
        )

        # Search
        distances, indices = index.search(query_embedding, k)

        results = []

        for idx in indices[0]:

            if idx != -1:
                results.append(chunks[idx])

        return results
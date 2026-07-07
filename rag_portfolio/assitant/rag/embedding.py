from sentence_transformers import SentenceTransformer


class EmbeddingModel:

    def __init__(self):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def embed_documents(self, chunks):

        embeddings = self.model.encode(
            chunks,
            convert_to_numpy=True
        )

        return embeddings

    def embed_query(self, question):

        embedding = self.model.encode(
            question,
            convert_to_numpy=True
        )

        return embedding
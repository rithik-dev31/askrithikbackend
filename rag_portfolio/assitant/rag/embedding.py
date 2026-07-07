from sentence_transformers import SentenceTransformer


class EmbeddingModel:

    def __init__(self):
        self.model = None

    def get_model(self):
        if self.model is None:
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
        return self.model

    def embed_documents(self, chunks):
        return self.get_model().encode(chunks, convert_to_numpy=True)

    def embed_query(self, question):
        return self.get_model().encode(question, convert_to_numpy=True)
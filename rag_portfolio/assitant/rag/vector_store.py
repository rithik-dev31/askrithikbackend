import faiss
import numpy as np
import pickle
from pathlib import Path


class VectorStore:

    def __init__(self):

        self.base_path = Path(__file__).resolve().parent.parent

        self.index_path = self.base_path / "faiss_index" / "index.faiss"

        self.metadata_path = self.base_path / "faiss_index" / "metadata.pkl"

    def build_index(self, embeddings, chunks):

        dimension = embeddings.shape[1]

        index = faiss.IndexFlatL2(dimension)

        index.add(np.array(embeddings, dtype="float32"))

        faiss.write_index(index, str(self.index_path))

        with open(self.metadata_path, "wb") as file:
            pickle.dump(chunks, file)

        print("✅ FAISS Index Saved Successfully")

    def load_index(self):

        index = faiss.read_index(str(self.index_path))

        with open(self.metadata_path, "rb") as file:
            chunks = pickle.load(file)

        return index, chunks
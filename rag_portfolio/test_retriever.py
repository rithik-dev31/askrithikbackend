from assitant.rag.embedding import EmbeddingModel
from assitant.rag.vector_store import VectorStore
from assitant.rag.retriever import Retriever

embedder = EmbeddingModel()
vector_store = VectorStore()

retriever = Retriever(
    vector_store,
    embedder
)

question = input("Ask: ")

results = retriever.retrieve(question)

print("\nRetrieved Chunks:\n")

for i, chunk in enumerate(results, start=1):

    print("=" * 80)
    print(f"Result {i}")
    print("=" * 80)

    print(chunk)
    print()
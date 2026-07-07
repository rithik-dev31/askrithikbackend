from assitant.rag.loader import DocumentLoader
from assitant.rag.splitter import TextSplitter
from assitant.rag.embedding import EmbeddingModel
from assitant.rag.vector_store import VectorStore

loader = DocumentLoader()
splitter = TextSplitter()
embedder = EmbeddingModel()
vector_store = VectorStore()

text = loader.load_documents()

chunks = splitter.split_text(text)

embeddings = embedder.embed_documents(chunks)

vector_store.build_index(
    embeddings,
    chunks
)

print("Total Chunks:", len(chunks))


# from assitant.rag.loader import DocumentLoader
# from assitant.rag.splitter import TextSplitter

# loader = DocumentLoader()
# splitter = TextSplitter()

# # Load both resume.pdf and knowledge.txt
# text = loader.load_documents()

# # Split into chunks
# chunks = splitter.split_text(text)

# print(f"\nTotal Chunks: {len(chunks)}\n")

# for i, chunk in enumerate(chunks, start=1):
#     print("=" * 80)
#     print(f"CHUNK {i}")
#     print("=" * 80)
#     print(chunk)
#     print("\n")
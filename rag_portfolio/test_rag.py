from assitant.rag.embedding import EmbeddingModel
from assitant.rag.vector_store import VectorStore
from assitant.rag.retriever import Retriever
from assitant.rag.prompt_builder import PromptBuilder
from assitant.rag.llm import LLM

embedder = EmbeddingModel()
vector_store = VectorStore()

retriever = Retriever(vector_store, embedder)
prompt_builder = PromptBuilder()
llm = LLM()

question = input("Ask: ")

# Retrieve relevant chunks
contexts = retriever.retrieve(question)

# Build prompt
prompt = prompt_builder.build(question, contexts)

# Generate answer
answer = llm.generate(prompt)

print("\n")
print(answer)
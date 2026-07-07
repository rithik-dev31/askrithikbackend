from .embedding import EmbeddingModel
from .vector_store import VectorStore
from .retriever import Retriever
from .prompt_builder import PromptBuilder
from .llm import LLM


class RAGPipeline:

    def __init__(self):

        self.embedder = EmbeddingModel()

        self.vector_store = VectorStore()

        self.retriever = Retriever(
            self.vector_store,
            self.embedder
        )

        self.prompt_builder = PromptBuilder()

        self.llm = LLM()

    def ask(self, question):

        # Retrieve relevant chunks
        contexts = self.retriever.retrieve(question)

        # Build prompt
        prompt = self.prompt_builder.build(
            question,
            contexts
        )

        # Generate response
        answer,usage = self.llm.generate(prompt)

        return answer,usage
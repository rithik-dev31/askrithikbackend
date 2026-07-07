from .embedding import EmbeddingModel
from .vector_store import VectorStore
from .retriever import Retriever
from .prompt_builder import PromptBuilder
from .llm import LLM


class RAGPipeline:

    def __init__(self):
        self.embedder = None
        self.vector_store = None
        self.retriever = None
        self.prompt_builder = None
        self.llm = None

    def initialize(self):
        if self.embedder is None:
            self.embedder = EmbeddingModel()

        if self.vector_store is None:
            self.vector_store = VectorStore()

        if self.retriever is None:
            self.retriever = Retriever(
                self.vector_store,
                self.embedder
            )

        if self.prompt_builder is None:
            self.prompt_builder = PromptBuilder()

        if self.llm is None:
            self.llm = LLM()

    def ask(self, question):

        # Initialize components only when needed
        self.initialize()

        # Retrieve relevant chunks
        contexts = self.retriever.retrieve(question)

        # Build prompt
        prompt = self.prompt_builder.build(
            question,
            contexts
        )

        # Generate response
        answer, usage = self.llm.generate(prompt)

        return answer, usage
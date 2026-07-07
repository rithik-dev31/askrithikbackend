from assitant.rag.llm import LLM

llm = LLM()

answer = llm.generate(
    "Who are you?"
)

print(answer)
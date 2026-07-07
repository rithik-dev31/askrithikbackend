import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class LLM:

    def __init__(self):

        self.client = OpenAI(
            api_key=os.getenv("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        )

        self.model = "openai/gpt-oss-20b"

    def generate(self, prompt):

        response = self.client.responses.create(
            model=self.model,
            input=prompt
        )

        usage = getattr(response, "usage", None)


        input_tokens = getattr(usage, "input_tokens", 0) if usage else 0
        output_tokens = getattr(usage, "output_tokens", 0) if usage else 0
        total_tokens = getattr(usage, "total_tokens", 0) if usage else 0

        return response.output_text, {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
        }
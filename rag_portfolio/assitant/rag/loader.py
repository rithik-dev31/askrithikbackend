import fitz
from pathlib import Path


class DocumentLoader:

    def __init__(self):
        self.base_path = Path(__file__).resolve().parent.parent

    def load_resume(self):

        pdf_path = self.base_path / "data" / "resume.pdf"

        document = fitz.open(pdf_path)

        text = ""

        for page in document:
            text += page.get_text()

        document.close()

        return text

    def load_links(self):

        file_path = self.base_path / "data" / "knowledge.txt"

        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    def load_documents(self):

        resume_text = self.load_resume()

        links_text = self.load_links()

        return resume_text + "\n\n" + links_text
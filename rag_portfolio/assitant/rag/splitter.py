from langchain_text_splitters import RecursiveCharacterTextSplitter


class TextSplitter:

    def __init__(self):

        self.recursive_splitter = RecursiveCharacterTextSplitter(
            chunk_size=700,
            chunk_overlap=100,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ]
        )

        self.section_headers = [
            "Profile",
            "Education",
            "Technical Skills",
            "Projects",
            "Experience",
            "Certifications",
            "Achievements"
        ]

    def split_text(self, text):

        lines = text.splitlines()

        chunks = []

        current_section = None
        buffer = []

        i = 0

        while i < len(lines):

            line = lines[i].strip()

            # ---------- New Section ----------
            if line in self.section_headers:

                if buffer:
                    chunks.extend(self._process_section(current_section, buffer))

                current_section = line
                buffer = []

            else:
                buffer.append(line)

            i += 1

        if buffer:
            chunks.extend(self._process_section(current_section, buffer))

        return chunks

    def _process_section(self, header, lines):

    # Handle content before the first section (contact details)
        if header is None:
            header = "Profile"

        if header == "Projects":
            return self._split_projects(lines)

        text = header + "\n" + "\n".join(lines)

        if len(text) > 700:
            return self.recursive_splitter.split_text(text)

        return [text]

    def _split_projects(self, lines):

        chunks = []

        current_project = []

        for line in lines:

            line = line.strip()

            # Project title line
            if "|" in line and "GitHub" in line:

                if current_project:

                    text = "\n".join(current_project)

                    if len(text) > 700:
                        chunks.extend(
                            self.recursive_splitter.split_text(text)
                        )
                    else:
                        chunks.append(text)

                current_project = [line]

            else:

                current_project.append(line)

        if current_project:

            text = "\n".join(current_project)

            if len(text) > 700:
                chunks.extend(
                    self.recursive_splitter.split_text(text)
                )
            else:
                chunks.append(text)

        return chunks
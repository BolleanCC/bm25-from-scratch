# Chunk by section
import re


def chunk_by_section(document_text):
    pattern = r"\n## "
    return re.split(pattern, document_text)

text = "Introduction\n## Section 1\nHello\n## Section 2\nWorld"

chunks = chunk_by_section(text)

print(chunks)  
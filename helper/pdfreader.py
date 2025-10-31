import fitz  # PyMuPDF
import re

def read_pdf(file_path: str, output_path: str) -> str:
    """
    Reads a PDF, cleans extra spaces and newlines,
    and writes the cleaned text to a .txt file.
    """
    doc = fitz.open(file_path)
    text = ""

    for page_num, page in enumerate(doc, start=1):
        page_content = page.get_text("text")

        # Step 1: collapse multiple spaces into one
        page_content = re.sub(r"[ ]+", " ", page_content)

        # Step 2: collapse 3+ newlines into 2 (keep paragraph separation)
        page_content = re.sub(r"\n{3,}", "\n\n", page_content)

        # Step 3: strip spaces around each line
        page_content = "\n".join(line.strip() for line in page_content.splitlines())

        # Step 4: remove accidental empty lines around page marker
        page_content = re.sub(r"\n*\Z", "", page_content)  # strip trailing newlines

        # Append cleaned page content with separator
        text += page_content

    # Final cleanup: collapse multiple empty lines globally
    text = re.sub(r"\n{3,}", "\n\n", text)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"{file_path} converted to cleaned text at {output_path}")
    return text

if __name__ == "__main__":
    file_path = "./documents/demo-FRD.pdf"
    output_path = "./uploades/pdf-text.txt"
    #Example
    read_pdf(file_path, output_path)

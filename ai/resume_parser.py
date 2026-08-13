import fitz  # PyMuPDF


def extract_text(pdf_path):
    """
    Extract all text from a PDF file.

    Args:
        pdf_path (str): Path to the uploaded PDF.

    Returns:
        str: Extracted text from the PDF.
    """

    text = ""

    try:
        document = fitz.open(pdf_path)

        for page in document:
            page_text = page.get_text()

            if page_text:
                text += page_text + "\n"

        document.close()

    except Exception as e:
        raise Exception(f"Error reading PDF: {e}")

    return text.strip()


if __name__ == "__main__":

    pdf_path = input("Enter PDF path: ")

    resume_text = extract_text(pdf_path)

    print("\n=========== EXTRACTED TEXT ===========\n")

    print(resume_text)
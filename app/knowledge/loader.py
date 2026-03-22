from pathlib import Path
from typing import List

from pypdf import PdfReader

from app.services.rag import DocumentForIndex

PROJECT_ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE_DIR = PROJECT_ROOT / "data" / "knowledge"


def load_documents_for_rag() -> List[DocumentForIndex]:
    documents: List[DocumentForIndex] = []

    # Load all PDF files
    for pdf_file in KNOWLEDGE_DIR.glob("*.pdf"):
        try:
            reader = PdfReader(pdf_file)
            texts = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    texts.append(text.strip())

            pdf_text = "\n\n".join(texts)
            documents.append(
                {
                    "id": pdf_file.stem,
                    "text": pdf_text,
                    "source": pdf_file.name,
                    "metadata": {"type": "pdf", "filename": pdf_file.name},
                }
            )
        except Exception as e:
            print(f"Error loading PDF {pdf_file.name}: {e}")

    # Load all TXT files
    for txt_file in KNOWLEDGE_DIR.glob("*.txt"):
        try:
            txt_content = txt_file.read_text(encoding="utf-8")
            documents.append(
                {
                    "id": txt_file.stem,
                    "text": txt_content,
                    "source": txt_file.name,
                    "metadata": {"type": "txt", "filename": txt_file.name},
                }
            )
        except Exception as e:
            print(f"Error loading TXT {txt_file.name}: {e}")

    return documents

import pypdfium2 as pdfium
import pdfplumber
import pytesseract

from pipelines.ingestion.models import ExtractedPage


async def extract_pdf(file_path: str):

    pdf = pdfium.PdfDocument(file_path)

    pages = []

    # =========================
    # Text extraction + OCR
    # =========================

    for i in range(len(pdf)):

        page = pdf[i]

        textpage = page.get_textpage()

        text = textpage.get_text_range()

        used_ocr = False

        # OCR fallback for scanned PDFs
        if len(text.strip()) < 50:

            bitmap = page.render()

            pil_image = bitmap.to_pil()

            text = pytesseract.image_to_string(
                pil_image,
                config="--psm 6"
            )

            used_ocr = True

        pages.append(
            ExtractedPage(
                page_number=i + 1,
                content=text,
                content_type="text",
                metadata={
                    "source": "pdf",
                    "ocr_used": used_ocr
                }
            )
        )

    # =========================
    # Table extraction
    # =========================

    with pdfplumber.open(file_path) as pdf_tables:

        for page_num, page in enumerate(pdf_tables.pages):

            tables = page.extract_tables()

            for table in tables:

                rows = []

                for row in table:

                    cleaned = [
                        str(cell) if cell else ""
                        for cell in row
                    ]

                    rows.append(" | ".join(cleaned))

                table_text = "\n".join(rows)

                pages.append(
                    ExtractedPage(
                        page_number=page_num + 1,
                        content=table_text,
                        content_type="table",
                        metadata={
                            "source": "pdf_table"
                        }
                    )
                )

    return pages


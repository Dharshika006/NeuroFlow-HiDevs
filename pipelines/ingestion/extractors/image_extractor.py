from PIL import Image
import pytesseract

from pipelines.ingestion.models import ExtractedPage


async def extract_image(file_path: str):

    image = Image.open(file_path)

    image.thumbnail((1024, 1024))

    text = pytesseract.image_to_string(image)

    content = f"""
Image OCR Content:

{text}
"""

    return [
        ExtractedPage(
            page_number=1,
            content=content,
            content_type="image",
            metadata={
                "source": "image"
            }
        )
    ]
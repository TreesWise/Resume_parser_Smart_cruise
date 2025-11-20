# import base64
# import fitz
# import os
# from app_logging import logger

# def convert_to_base64(file_path):
#     ext = os.path.splitext(file_path)[-1].lower()
#     images_b64 = []

#     if ext == ".pdf":
#         doc = fitz.open(file_path)
#         for page in doc:
#             pix = page.get_pixmap(dpi=100)
#             b64 = base64.b64encode(pix.tobytes("png")).decode("utf-8")
#             images_b64.append(b64)
#     elif ext in [".jpg", ".jpeg", ".png"]:
#         with open(file_path, "rb") as f:
#             b64 = base64.b64encode(f.read()).decode("utf-8")
#             images_b64.append(b64)
#     else:
#         raise ValueError("Unsupported file format.")
#     print("Image converted.............................................")
#     return images_b64




import base64
import fitz
import os
from app_logging import logger

def convert_to_base64(file_path, dpi=100, max_pages=10):
    """
    Convert PDF or image file to Base64-encoded image(s).

    Returns:
        List[str]: Base64-encoded images
    """
    ext = os.path.splitext(file_path)[-1].lower()
    images_b64 = []

    try:
        if ext == ".pdf":
            with fitz.open(file_path) as doc:
                if len(doc) > max_pages:
                    logger.warning(f"PDF '{file_path}' has {len(doc)} pages. Converting only the first {max_pages}.")
                for i, page in enumerate(doc[:max_pages]):
                    pix = page.get_pixmap(dpi=dpi)
                    b64 = base64.b64encode(pix.tobytes("png")).decode("utf-8")
                    images_b64.append(b64)

        elif ext in [".jpg", ".jpeg", ".png"]:
            with open(file_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
                images_b64.append(b64)

        else:
            raise ValueError(f"Unsupported file format: {ext}")

        logger.info(f"File '{file_path}' converted to base64 ({len(images_b64)} image(s)).")

    except Exception as e:
        logger.error(f"Error converting file '{file_path}' to base64: {e}")
        raise

    return images_b64

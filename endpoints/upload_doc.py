import os
import json
import shutil
import tempfile
from fastapi.responses import JSONResponse
from country_mapping import country_mapping
from res_services.convert_docx_to_pdf import convert_docx_to_pdf
from doc_services.process_document_to_json import process_document_to_json
from automate_functions.load_map_dict_from_blob import load_mapping_dict_from_blob
from datetime import datetime
from doc_openai_functions.doc_json_extraction import get_default_json
from app_logging import logger
mapping_dict = load_mapping_dict_from_blob()


def replace_docnames(data: list, mapping: dict) -> list:
    """
    Replace 'docName' values in the JSON data based on a mapping dictionary.
    Ensures standardized document naming and adds uploadedDate if missing.
    """
    # Build reverse lookup for fast mapping
    reverse_map = {}
    for standard_name, variants in mapping.items():
        for v in variants:
            if isinstance(v, str):
                reverse_map[v.strip().lower()] = standard_name

    for item in data:
        doc_name = item.get("docName", "")
        if isinstance(doc_name, str):
            key = doc_name.strip().lower()
            if key  in reverse_map:
                item["docName"] = reverse_map[key]

        # Ensure uploadedDate exists
        if not item.get("uploadedDate"):
            item["uploadedDate"] = datetime.now().strftime("%d-%m-%Y")

    return data


async def process_document_upload(file, doctype: str):
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in [".pdf", ".jpg", ".jpeg", ".png", ".docx"]:
        logger.warning(f"Invalid file type received: {file_ext}")
        return JSONResponse({"error": "Only PDF, DOCX, or image files allowed."}, status_code=400)

    temp_file_path = None
    try:
        if file_ext == ".docx":
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_file:
                shutil.copyfileobj(file.file, temp_file)
                temp_file_path = temp_file.name

            pdf_path = await convert_docx_to_pdf(temp_file_path)
            logger.debug(f"DOCX successfully converted to PDF: {pdf_path}")
            result = process_document_to_json(pdf_path)
            logger.info("Document successfully processed into JSON.")

        else:
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
                shutil.copyfileobj(file.file, temp_file)
                temp_file_path = temp_file.name
                logger.debug(f"Temporary file saved at {temp_file_path}")

            result = process_document_to_json(temp_file_path)
            logger.info("Document successfully processed into JSON.")

        if isinstance(result, str):
            result = json.loads(result)
            
        # Apply mappings
        logger.info("Loading mapping dictionary from blob storage.")
        mapping_dict_from_blob = load_mapping_dict_from_blob()
        result = replace_docnames(result, mapping_dict_from_blob)

        for i, item in enumerate(result):
            doc_name = str(item.get("docName", "")).strip().lower()
            doc_number = str(item.get("DocNumber", "")).strip().lower()

            if doc_name in ["", "null", None] and doc_number in ["", "null", None]:
                # ✅ Replace entire entry with default JSON
                result[i] = get_default_json()
                
        for item in result:
            original_country = item.get("issuedCountry", "").strip().lower()
            for key, value in country_mapping.items():
                if key.strip().lower() == original_country:
                    item["issuedCountry"] = value
                    break
        logger.info(f"process_document_upload completed successfully for {file.filename}")
        return JSONResponse(content=result, media_type="application/json")

    except Exception as e:
        logger.exception(f"Error occurred while processing {file.filename}: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)

    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
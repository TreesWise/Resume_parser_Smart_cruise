import json
from doc_services.convert_to_base64 import convert_to_base64
from doc_openai_functions.doc_json_extraction import extract_json, get_default_json
from app_logging import logger

def postprocess_json(raw_json):
    if not isinstance(raw_json, str):
        return raw_json  # Nothing to do

    try:
        json_objects = raw_json.split('}\n{')
        if json_objects:
            json_objects[0] += '}'
            json_objects[-1] = '{' + json_objects[-1]
        results = [json.loads(obj) for obj in json_objects]
    except json.JSONDecodeError:
        return raw_json  # or return [] if you'd rather fail silently

    formatted = []
    for obj in results:
        known_fields = {
            "docType": obj.get("docType", "null").strip(),
            "docName": obj.get("docName", "").strip(),
            "DocNumber": obj.get("DocNumber", "").strip(),
            "uploadedDate": obj.get("uploadedDate", "Not Available"),
            "issuedCountry": obj.get("issuedCountry", "").strip(),
            
            "IssuedPlace": obj.get("IssuedPlace", "").strip(),
            
            "issueDate": obj.get("issueDate", "").strip(),
            "expDate": obj.get("expDate", "Not Available").strip(),
            "isNationalDoc": obj.get("isNationalDoc", "No").strip(),
        }

        extra_fields = {
            k: v for k, v in obj.items()
            if k not in known_fields and k not in known_fields.keys()
        }

        if extra_fields:
            known_fields["metadata"] = extra_fields

        formatted.append(known_fields)

    return formatted


# def process_document_to_json(file_path):
#     images_b64 = convert_to_base64(file_path)
    
#     raw_json = extract_json(images_b64)

#     # If it's a string, try parsing
#     if isinstance(raw_json, str):
#         try:
#             # Try to parse as proper JSON list
#             raw_json = json.loads(raw_json)
#         except json.JSONDecodeError:
#             # If it's not valid JSON, try fallback string splitting logic
#             return postprocess_json(raw_json)

#     # If it's already a list, return it as-is
#     if isinstance(raw_json, list) and raw_json:
#         return raw_json

#     # If it's something else, return safely
#     return [get_default_json()]


def process_document_to_json(file_path):
    logger.info(f"Starting process_document_to_json for file: {file_path}")

    try:
        images_b64 = convert_to_base64(file_path)
        logger.info("File successfully converted to base64.")
    except Exception as e:
        logger.exception(f"Error converting file to base64: {e}")
        return [get_default_json()]

    try:
        raw_json = extract_json(images_b64)
        logger.info("extract_json completed successfully.")
    except Exception as e:
        logger.exception(f"Error extracting JSON from document: {e}")
        return [get_default_json()]

    # If it's a string, try parsing
    if isinstance(raw_json, str):
        logger.debug("raw_json is a string. Attempting to parse JSON.")
        try:
            raw_json = json.loads(raw_json)
            logger.info("raw_json successfully parsed into JSON.")
        except json.JSONDecodeError as e:
            logger.warning(f"JSON decoding failed: {e}. Using postprocess_json as fallback.")
            return postprocess_json(raw_json)

    # If it's already a list, return it as-is
    if isinstance(raw_json, list) and raw_json:
        logger.info(f"Returning valid JSON list with {len(raw_json)} entries.")
        return raw_json

    # If it's something else or empty, return default
    logger.warning("Unexpected or empty JSON format detected. Returning default JSON.")
    return [get_default_json()]
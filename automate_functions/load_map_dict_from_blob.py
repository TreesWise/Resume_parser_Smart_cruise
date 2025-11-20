import ast
import re
import os
from azure.storage.blob import BlobServiceClient

AZURE_CONNECTION_STRING=os.getenv("AZURE_STORAGE_CONNECTION_STRING")
AZURE_CONTAINER_NAME= os.getenv("AZURE_BLOB_CONTAINER_NAME")
AZURE_SQL_CONNECTION_STRING=os.getenv("AZURE_SQL_CONNECTION_STRING")
MAPPING_BLOB_NAME = os.getenv("MAPPING_BLOB_NAME")

DOCUMENTPARSER_AZURE_BLOB_CONTAINER_NAME=os.getenv("container_name2")


_mapping_cache = {"etag": None, "data": {}}
def _parse_mapping_dict_py(file_text: str) -> dict:
    """
    Expects a Python file that contains:
        mapping_dict = { ... }
    Returns the dict safely using ast.literal_eval.
    """
    m = re.search(r"mapping_dict\s*=\s*(\{.*\})\s*\Z", file_text, flags=re.DOTALL)
    if not m:
        # Fallback: split once
        parts = file_text.split("=", 1)
        if len(parts) == 2:
            return ast.literal_eval(parts[1].strip())
        return {}
    return ast.literal_eval(m.group(1))

def load_mapping_dict_from_blob(force: bool = False) -> dict:
    """
    Download dict_file.py from Azure Blob and return the mapping dict.
    Uses an ETag-based cache to avoid unnecessary downloads.
    """
    try:
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
        blob_client = blob_service_client.get_blob_client(container=AZURE_CONTAINER_NAME, blob=MAPPING_BLOB_NAME)

        props = blob_client.get_blob_properties()
        if (not force) and _mapping_cache["etag"] == props.etag and _mapping_cache["data"]:
            return _mapping_cache["data"]

        content_bytes = blob_client.download_blob().readall()
        content_text = content_bytes.decode("utf-8", errors="replace")
        data = _parse_mapping_dict_py(content_text)
        _mapping_cache["etag"] = props.etag
        _mapping_cache["data"] = data
        
        # print("data---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------", data)
        return data
    except Exception as e:
        # Graceful fallback: keep last good cache if present
        if _mapping_cache["data"]:
            return _mapping_cache["data"]
        print(f"[WARN] load_mapping_dict_from_blob failed: {e}. Using empty mapping.", flush=True)
        return {}



def document_parser_load_mapping_dict_from_blob(force: bool = False) -> dict:
    """
    Download dict_file.py from Azure Blob and return the mapping dict.
    Uses an ETag-based cache to avoid unnecessary downloads.
    """
    try:
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
        blob_client = blob_service_client.get_blob_client(container=DOCUMENTPARSER_AZURE_BLOB_CONTAINER_NAME, blob=MAPPING_BLOB_NAME)

        props = blob_client.get_blob_properties()
        if (not force) and _mapping_cache["etag"] == props.etag and _mapping_cache["data"]:
            return _mapping_cache["data"]

        content_bytes = blob_client.download_blob().readall()
        content_text = content_bytes.decode("utf-8", errors="replace")
        data = _parse_mapping_dict_py(content_text)
        _mapping_cache["etag"] = props.etag
        _mapping_cache["data"] = data
        
        # print("data---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------", data)
        return data
    except Exception as e:
        # Graceful fallback: keep last good cache if present
        if _mapping_cache["data"]:
            return _mapping_cache["data"]
        print(f"[WARN] load_mapping_dict_from_blob failed: {e}. Using empty mapping.", flush=True)
        return {}
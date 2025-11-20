from azure.storage.blob import BlobServiceClient
import os
from app_logging import logger

AZURE_CONNECTION_STRING=os.getenv("AZURE_STORAGE_CONNECTION_STRING")
AZURE_CONTAINER_NAME= os.getenv("AZURE_BLOB_CONTAINER_NAME")
DOCUMENTPARSER_AZURE_BLOB_CONTAINER_NAME=os.getenv("container_name2")


def get_latest_replied_blob_name():
    print("[TASK] get_latest_replied_blob_name START", flush=True)
    try:
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)

        blobs = list(container_client.list_blobs(name_starts_with="verification_documents_replied_"))
        replied_blobs = sorted(
            [b for b in blobs if b.name.endswith(".xlsx")],
            key=lambda b: b.last_modified,
            reverse=True
        )

        if not replied_blobs:
            raise Exception("No replied verification documents found in blob storage.")

        latest = replied_blobs[0].name
        print(f"[TASK] Latest replied blob: {latest}", flush=True)
        return latest
    finally:
        print("[TASK] get_latest_replied_blob_name END", flush=True)
        


def document_parser_get_latest_replied_blob_name():
    print("[TASK] get_latest_replied_blob_name START", flush=True)
    try:
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(DOCUMENTPARSER_AZURE_BLOB_CONTAINER_NAME)

        blobs = list(container_client.list_blobs(name_starts_with="verification_documents_replied_"))
        replied_blobs = sorted(
            [b for b in blobs if b.name.endswith(".xlsx")],
            key=lambda b: b.last_modified,
            reverse=True
        )

        if not replied_blobs:
            raise Exception("No replied verification documents found in blob storage.")

        latest = replied_blobs[0].name
        print(f"[TASK] Latest replied blob: {latest}", flush=True)
        return latest
    finally:
        print("[TASK] get_latest_replied_blob_name END", flush=True)

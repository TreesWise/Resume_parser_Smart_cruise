from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import os
from app_logging import logger

load_dotenv()
AZURE_CONNECTION_STRING=os.getenv("AZURE_STORAGE_CONNECTION_STRING")

def download_dict_file_from_blob(container_name, blob_name, download_path):
    try:
        # Get the Azure Blob Service Client
        # connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)

        # Get the container client
        container_client = blob_service_client.get_container_client(container_name)

        # Download the blob (dict_file.py) to the specified path
        blob_client = container_client.get_blob_client(blob_name)
        with open(download_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())

        print(f"[INFO] dict_file.py downloaded successfully from Blob storage to {download_path}")

    except Exception as e:
        print(f"[ERROR] Failed to download dict_file.py from Blob: {e}")




# def document_parser_download_dict_file_from_blob(container_name, blob_name, download_path):
#     try:
#         # Get the Azure Blob Service Client
#         # connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
#         blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)

#         # Get the container client
#         container_client = blob_service_client.get_container_client(container_name)

#         # Download the blob (dict_file.py) to the specified path
#         blob_client = container_client.get_blob_client(blob_name)
#         with open(download_path, "wb") as download_file:
#             download_file.write(blob_client.download_blob().readall())

#         print(f"[INFO] dict_file.py downloaded successfully from Blob storage to {download_path}")

#     except Exception as e:
#         print(f"[ERROR] Failed to download dict_file.py from Blob: {e}")

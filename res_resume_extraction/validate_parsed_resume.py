from azure.storage.blob import BlobServiceClient
from app_logging import logger
import os

def upload_to_blob_storage(file_path, container_name, connection_string):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=os.path.basename(file_path))
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
        logger.info("File %s successfully uploaded to %s.", file_path, container_name)
    except Exception as e:
        logger.error("Error uploading file to Blob Storage: %s", e, exc_info=True)
        
        
def validate_parsed_resume(extracted_info, file_path, confidence_threshold=0.8, container_name=None, connection_string=None):
    
    container_name = os.getenv("container_name")
    connection_string = os.getenv("connection_string")
    errors = []   
    logger.info("Confidence score----------------------------------------------: %s", extracted_info.get("confidence", 1))
    if extracted_info.get("confidence", 1) < confidence_threshold:
        errors.append("Low confidence score")
        
        # Upload file for retrainingl
        if container_name and connection_string:
            upload_to_blob_storage(file_path, container_name, connection_string)
    
    return errors if errors else ["Resume parsed successfully."]
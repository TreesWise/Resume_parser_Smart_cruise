from sqlalchemy import text, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
from datetime import datetime
import os
from app_logging import logger

load_dotenv()
AZURE_CONNECTION_STRING=os.getenv("AZURE_STORAGE_CONNECTION_STRING")

Base = declarative_base()

class TempDocument(Base):
    __tablename__ = 'temp_table'
    id = Column(Integer, primary_key=True, autoincrement=True)
    unidentified_doc_name = Column(String, nullable=False)
    mapped_doc_name = Column(String, nullable=False)
    status = Column(String, default='pending')
    CreatedDate = Column(DateTime, default=datetime.now)

class MasterDocument(Base):
    __tablename__ = 'Master_unidentified_doc_Table'
    id = Column(Integer, primary_key=True, autoincrement=True)
    unidentified_doc_name = Column(String, nullable=False)
    mapped_doc_name = Column(String, nullable=False)
    uploaded_date = Column(DateTime, default=datetime.now)
    status = Column(String, default='pending')

def upload_dict_file_to_blob(file_path, container_name, blob_name):
    try:
        # Get the Azure Blob Service Client
        # connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)

        # Get the container client
        container_client = blob_service_client.get_container_client(container_name)

        # Upload the file to the container
        with open(file_path, "rb") as data:
            container_client.upload_blob(name=blob_name, data=data, overwrite=True)

        print(f"[INFO] dict_file.py uploaded successfully to Blob storage as {blob_name}")

    except Exception as e:
        print(f"[ERROR] Failed to upload dict_file.py to Blob: {e}")
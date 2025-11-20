
from sqlalchemy import text, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from azure.storage.blob import BlobServiceClient
from datetime import datetime
import os
from db import get_db_engine
import pandas as pd
import io
from app_logging import logger

AZURE_CONNECTION_STRING=os.getenv("AZURE_STORAGE_CONNECTION_STRING")
AZURE_CONTAINER_NAME= os.getenv("AZURE_BLOB_CONTAINER_NAME")
DOCUMENTPARSER_AZURE_BLOB_CONTAINER_NAME=os.getenv("container_name2")



# Base = declarative_base()

# class TempDocument(Base):
#     __tablename__ = 'temp_table'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     unidentified_doc_name = Column(String, nullable=False)
#     mapped_doc_name = Column(String, nullable=False)
#     status = Column(String, default='pending')
#     CreatedDate = Column(DateTime, default=datetime.now)

# class MasterDocument(Base):
#     __tablename__ = 'Master_unidentified_doc_Table'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     unidentified_doc_name = Column(String, nullable=False)
#     mapped_doc_name = Column(String, nullable=False)
#     uploaded_date = Column(DateTime, default=datetime.now)
#     status = Column(String, default='pending')


def insert_data_from_blob(blob_name: str):
    print(f"[TASK] insert_data_from_blob START ({blob_name})", flush=True)
    try:
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)

        blob_data = blob_service_client.get_blob_client(container=AZURE_CONTAINER_NAME, blob=blob_name)\
            .download_blob().readall()
        df = pd.read_excel(io.BytesIO(blob_data))
        print(f"[TASK] Read {len(df)} rows from replied Excel; columns={list(df.columns)}", flush=True)

        engine = get_db_engine()
        inserted = 0
        with engine.begin() as conn:
            for _, row in df.iterrows():

                
                existing = conn.execute(text("""
                    SELECT 1 FROM Master_unidentified_doc_Table 
                    where unidentified_doc_name = :unidentified_doc_name 
                    AND mapped_doc_name = :mapped_doc_name
                """), {
                    "unidentified_doc_name": row['unidentified_doc_name'],
                    "mapped_doc_name": row['mapped_doc_name']
                }).fetchone()

                if not existing:
                    conn.execute(text("""
                        INSERT INTO Master_unidentified_doc_Table
                        (unidentified_doc_name, mapped_doc_name, uploaded_date, status)
                        VALUES ( :unidentified_doc_name, :mapped_doc_name, :uploaded_date, :status)
                    """), {
                        "unidentified_doc_name": row['unidentified_doc_name'],
                        "mapped_doc_name": row['mapped_doc_name'],
                        "uploaded_date": row['CreatedDate'],
                        "status": row['status']
                    })
                    inserted += 1

        print(f"[TASK] Inserted {inserted} new rows into Master_unidentified_doc_Table", flush=True)
    except Exception as e:
        print(f"[TASK] Insertion from blob failed: {e}", flush=True)
    finally:
        print("[TASK] insert_data_from_blob END", flush=True)
        
        

def documentparser_insert_data_from_blob(blob_name: str):
    print(f"[TASK] insert_data_from_blob START ({blob_name})", flush=True)
    try:
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)

        blob_data = blob_service_client.get_blob_client(container=DOCUMENTPARSER_AZURE_BLOB_CONTAINER_NAME, blob=blob_name)\
            .download_blob().readall()
        df = pd.read_excel(io.BytesIO(blob_data))
        print(f"[TASK] Read {len(df)} rows from replied Excel; columns={list(df.columns)}", flush=True)

    
        engine = get_db_engine()
        inserted = 0
        with engine.begin() as conn:
            for _, row in df.iterrows():

                
                existing = conn.execute(text("""
                    
                    SELECT 1 FROM Document_parser_master_unidentified_doc_Table 
                    where unidentified_doc_name = :unidentified_doc_name 
                    AND mapped_doc_name = :mapped_doc_name
                """), {
                    "unidentified_doc_name": row['unidentified_doc_name'],
                    "mapped_doc_name": row['mapped_doc_name']
                }).fetchone()

                if not existing:
                    conn.execute(text("""
                        INSERT INTO Document_parser_master_unidentified_doc_Table
                        (unidentified_doc_name, mapped_doc_name, uploaded_date, status)
                        VALUES ( :unidentified_doc_name, :mapped_doc_name, :uploaded_date, :status)
                    """), {
                        "unidentified_doc_name": row['unidentified_doc_name'],
                        "mapped_doc_name": row['mapped_doc_name'],
                        "uploaded_date": row['CreatedDate'],
                        "status": row['status']
                    })
                    inserted += 1

        print(f"[TASK] Inserted {inserted} new rows into Master_unidentified_doc_Table", flush=True)
    except Exception as e:
        print(f"[TASK] Insertion from blob failed: {e}", flush=True)
    finally:
        print("[TASK] insert_data_from_blob END", flush=True)
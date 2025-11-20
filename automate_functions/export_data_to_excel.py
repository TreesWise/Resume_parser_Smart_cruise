from sqlalchemy import text, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from db import get_db_engine
from dotenv import load_dotenv
import os
from azure.core.exceptions import ResourceExistsError
import io
from app_logging import logger
import pandas as pd

load_dotenv()

# Base = declarative_base()


AZURE_CONNECTION_STRING=os.getenv("AZURE_STORAGE_CONNECTION_STRING")
AZURE_CONTAINER_NAME= os.getenv("AZURE_BLOB_CONTAINER_NAME")
AZURE_SQL_CONNECTION_STRING=os.getenv("AZURE_SQL_CONNECTION_STRING")

AZURE_CONTAINER_NAME2=os.getenv("container_name2")



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


def export_data_to_excel():
    print("[TASK] export_data_to_excel START", flush=True)
    try:

        engine = get_db_engine()
        with engine.begin() as conn:
            
            result = conn.execute(text("""
                SELECT * FROM temp_table
                WHERE LTRIM(RTRIM(status)) = 'pending'
                AND CONVERT(date, CreatedDate) < CONVERT(date, GETDATE())
            """))

            data = result.fetchall()
            
            print("data----------------------------------------------------------------------------------------", data)
            print(f"[TASK] Fetched {len(data)} rows", flush=True)
            if not data:
                print("[TASK] Nothing to export. Returning.", flush=True)
                return

            df = pd.DataFrame(data, columns=result.keys())
            print(f"[TASK] DataFrame shape = {df.shape}", flush=True)

            excel_buffer = io.BytesIO()
            df.to_excel(excel_buffer, index=False)
            excel_buffer.seek(0)
            print("[TASK] Exported data to Excel (in-memory)", flush=True)

            blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)

            container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)
            try:
                container_client.create_container()
                print(f"[BLOB] Created container '{AZURE_CONTAINER_NAME}'", flush=True)
            except ResourceExistsError:
                pass

            blob_name = f"verification_documents_exported_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            blob_client = blob_service_client.get_blob_client(container=AZURE_CONTAINER_NAME, blob=blob_name)
            blob_client.upload_blob(excel_buffer, overwrite=True)
            print(f"[TASK] Uploaded Excel to blob: {blob_name}", flush=True)

            with engine.begin() as conn2:
                conn2.execute(text("""
                    UPDATE temp_table
                    SET status='exported'
                    WHERE LTRIM(RTRIM(status)) = 'pending'
                    AND CONVERT(date, CreatedDate) < CONVERT(date, GETDATE())
                """))

                print("[TASK] Updated rows to 'exported'", flush=True)
                conn2.execute(text("""
                    DELETE FROM temp_table
                    WHERE LTRIM(RTRIM(status)) = 'exported'
                    AND CONVERT(date, CreatedDate) < CONVERT(date, GETDATE())
                """))
                # conn2.execute(text("DELETE FROM temp_table WHERE TRIM(status) = 'exported'"))
                print("[TASK] Deleted exported rows", flush=True)

    except Exception as e:
        print(f"[TASK] Export Error: {e}", flush=True)
    finally:
        print("[TASK] export_data_to_excel END", flush=True)



def export_document_paser_data_to_excel():
    print("[TASK] export_data_to_excel START", flush=True)
    try:

        engine = get_db_engine()
        with engine.begin() as conn:
            
            result = conn.execute(text("""
                  SELECT * FROM Document_parser_temp_table
                WHERE LTRIM(RTRIM(status)) = 'pending'
                AND CONVERT(date, CreatedDate) < CONVERT(date, GETDATE())

            """))

            data = result.fetchall()
            
            print("data----------------------------------------------------------------------------------------", data)
            print(f"[TASK] Fetched {len(data)} rows", flush=True)
            if not data:
                print("[TASK] Nothing to export. Returning.", flush=True)
                return

            df = pd.DataFrame(data, columns=result.keys())
            print(f"[TASK] DataFrame shape = {df.shape}", flush=True)

            excel_buffer = io.BytesIO()
            df.to_excel(excel_buffer, index=False)
            excel_buffer.seek(0)
            print("[TASK] Exported data to Excel (in-memory)", flush=True)

            blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)

            container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME2)
            try:
                container_client.create_container()
                print(f"[BLOB] Created container '{AZURE_CONTAINER_NAME2}'", flush=True)
            except ResourceExistsError:
                pass

            blob_name = f"verification_documents_exported_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            blob_client = blob_service_client.get_blob_client(container=AZURE_CONTAINER_NAME2, blob=blob_name)
            blob_client.upload_blob(excel_buffer, overwrite=True)
            print(f"[TASK] Uploaded Excel to blob: {blob_name}", flush=True)

            with engine.begin() as conn2:
                conn2.execute(text("""
                    UPDATE Document_parser_temp_table
                    SET status='exported'
                    WHERE LTRIM(RTRIM(status)) = 'pending'
                    AND CONVERT(date, CreatedDate) < CONVERT(date, GETDATE())
                """))

                print("[TASK] Updated rows to 'exported'", flush=True)
                conn2.execute(text("""
                    DELETE FROM Document_parser_temp_table
                    WHERE LTRIM(RTRIM(status)) = 'exported'
                    AND CONVERT(date, CreatedDate) < CONVERT(date, GETDATE())
                """))
                # conn2.execute(text("DELETE FROM temp_table WHERE TRIM(status) = 'exported'"))
                print("[TASK] Deleted exported rows", flush=True)

    except Exception as e:
        print(f"[TASK] Export Error: {e}", flush=True)
    finally:
        print("[TASK] export_data_to_excel END", flush=True)

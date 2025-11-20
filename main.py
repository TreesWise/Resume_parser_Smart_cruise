from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Security, Depends,Body
from fastapi.security.api_key import APIKeyHeader
from datetime import datetime
import os
from datetime import datetime
from sqlalchemy import text
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pytz
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd
from typing import List, Dict
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, text, Column, Integer, String, DateTime, inspect
from fastapi.responses import JSONResponse

from automate_functions.init_database import init_db
from automate_functions.scheduler import start_scheduler_guarded
from endpoints.upload import process_resume_upload
from endpoints.upload_doc import process_document_upload
from endpoints.insert_temp_doc import process_insert_temp_documents,process_insert_document_parser_temp_documents
from app_logging import logger
from db import get_db_engine
from models import TempDocument, MasterDocument, Base,DocumentParserTempTable


load_dotenv()
app = FastAPI(title="Resume Parser API", version="1.0")
# app = FastAPI(
#     title="Resume Parser API",
#     version="1.0",
#     docs_url="/docs",
#     prefix="/birp-bsm",
#     openapi_prefix="/birp-bsm",
#     )


API_KEY = os.getenv("your_secure_api_key")
API_KEY_NAME = os.getenv("api_key_name")
endpoint = os.getenv("endpoint")
key = os.getenv("key")
model_id = os.getenv("model_id")
container_name = os.getenv("container_name")
connection_string = os.getenv("connection_string")
AZURE_CONNECTION_STRING=os.getenv("AZURE_STORAGE_CONNECTION_STRING")
AZURE_CONTAINER_NAME= os.getenv("AZURE_BLOB_CONTAINER_NAME")
AZURE_SQL_CONNECTION_STRING=os.getenv("AZURE_SQL_CONNECTION_STRING")
MAPPING_BLOB_NAME = os.getenv("MAPPING_BLOB_NAME")

SCHED_TZ = pytz.timezone("Asia/Kolkata")
scheduler = AsyncIOScheduler(timezone=SCHED_TZ)

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


api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False) 

def verify_api_key(api_key: str = Security(api_key_header)):
    """Validate API Key"""
    if not api_key or api_key != API_KEY:
        raise HTTPException(status_code=403, detail=" Invalid API Key")
    return api_key
 
# upload resume endpoint
@app.post("/upload/")
async def upload_file(
    api_key: str = Depends(verify_api_key),  
    file: UploadFile = File(...),
    entity: str = Form("")
):
    return await process_resume_upload(file, entity, endpoint, key, model_id, container_name, connection_string)

# Endpoint for uploading the document
@app.post("/upload-document/")
async def upload_file(api_key: str = Depends(verify_api_key), file: UploadFile = File(...), Doctype: str = Form("")):
    return await process_document_upload(file, Doctype)

# endpoint for inserting unidentified documents
@app.post("/insert-temp-documents/")
def insert_temp_documents(
    api_key: str = Depends(verify_api_key),
    mappings: List[Dict[str, str]] = Body(...),
):
    return process_insert_temp_documents(mappings)





@app.post("/insert-document_parser_temp-documents/")
def insert_temp_documents(
    api_key: str = Depends(verify_api_key),
    mappings: List[Dict[str, str]] = Body(...),
):
    return process_insert_document_parser_temp_documents(mappings)








@app.get("/view-temp-documents/")
def view_temp_documents(api_key: str = Depends(verify_api_key)):
    print("[API] /view-temp-documents called", flush=True)
    try:
        # print(f"[SANITY] DB path (view) = {sqlite_db_path}", flush=True)
        engine = get_db_engine()
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()

        result = session.query(TempDocument).all()
        print(f"[API] Retrieved {len(result)} rows from local_temp_table", flush=True)

        data = [{
            "id": record.id,
            "unidentified_doc_name": record.unidentified_doc_name, 
            "mapped_doc_name": record.mapped_doc_name,
            "status": record.status, 
            "CreatedDate": record.CreatedDate.strftime('%Y-%m-%d %H:%M:%S') if record.CreatedDate else None
        } for record in result]

        return JSONResponse(content={"data": data})
    except Exception as e:
        print(f"[API] view-temp-documents failed: {e}", flush=True)
        return {"error": f"Failed to fetch data: {str(e)}"}




@app.get("/view_document_parser_temp_documents/")
def view_document_parser_temp_documents(api_key: str = Depends(verify_api_key)):
    print("[API] /view-temp-documents called", flush=True)
    try:
        # print(f"[SANITY] DB path (view) = {sqlite_db_path}", flush=True)
        engine = get_db_engine()
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()

        result = session.query(DocumentParserTempTable).all()
        print(f"[API] Retrieved {len(result)} rows from local_temp_table", flush=True)

        data = [{
            "id": record.id,
            "unidentified_doc_name": record.unidentified_doc_name, 
            "mapped_doc_name": record.mapped_doc_name,
            "status": record.status, 
            "CreatedDate": record.CreatedDate.strftime('%Y-%m-%d %H:%M:%S') if record.CreatedDate else None
        } for record in result]

        return JSONResponse(content={"data": data})
    except Exception as e:
        print(f"[API] view-temp-documents failed: {e}", flush=True)
        return {"error": f"Failed to fetch data: {str(e)}"}
    



#Scheduler 
@app.on_event("startup")
async def on_startup():
    print("current_date:", datetime.now().strftime("%d-%m-%Y"), flush=True)
    init_db()
    start_scheduler_guarded()

@app.on_event("shutdown")
async def shutdown_scheduler():
    try:
        scheduler.shutdown(wait=False)
        print("[SCHEDULER] APScheduler stopped", flush=True)
    except Exception:
        pass
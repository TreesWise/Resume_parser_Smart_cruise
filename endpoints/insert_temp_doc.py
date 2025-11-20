import pandas as pd
from datetime import datetime
from fastapi.responses import JSONResponse
from typing import List, Dict

from automate_functions.pandas_to_sql import pandas_to_sql_fast
from db import get_db_engine
from app_logging import logger

def process_insert_temp_documents(mappings: List[Dict[str, str]]):
    try:
        # Validate input
        if not mappings or not isinstance(mappings[0], dict):
            return JSONResponse(
                {"error": "Invalid format. Expected a dictionary inside a list."},
                status_code=400
            )

        # Prepare dataframe
        df = pd.DataFrame([{
            "unidentified_doc_name": (item.get("unidentified_doc_name") or "").strip().lower(),
            "mapped_doc_name": (item.get("mapped_doc_name") or "").strip().lower()
        } for item in mappings])

        # Add metadata
        df['status'] = 'pending'
        df['CreatedDate'] = datetime.utcnow()   # always store UTC

        # Insert into database
        engine = get_db_engine()
        pandas_to_sql_fast(df, 'temp_table', engine)

        return {"message": f"{len(df)} document(s) inserted as pending."}

    except Exception as e:
        logger.error("Insertion failed: %s", e, exc_info=True)
        return JSONResponse(
            {"error": f"Insertion failed: {str(e)}"},
            status_code=500
        )




def process_insert_document_parser_temp_documents(mappings: List[Dict[str, str]]):
    try:
        # Validate input
        if not mappings or not isinstance(mappings[0], dict):
            return JSONResponse(
                {"error": "Invalid format. Expected a dictionary inside a list."},
                status_code=400
            )

        # Prepare dataframe
        df = pd.DataFrame([{
            "unidentified_doc_name": (item.get("unidentified_doc_name") or "").strip().lower(),
            "mapped_doc_name": (item.get("mapped_doc_name") or "").strip().lower()
        } for item in mappings])

        # Add metadata
        df['status'] = 'pending'
        df['CreatedDate'] = datetime.utcnow()   # always store UTC

        # Insert into database
        engine = get_db_engine()
        pandas_to_sql_fast(df, 'Document_parser_temp_table', engine)

        return {"message": f"{len(df)} document(s) inserted as pending."}

    except Exception as e:
        logger.error("Insertion failed: %s", e, exc_info=True)
        return JSONResponse(
            {"error": f"Insertion failed: {str(e)}"},
            status_code=500
        )
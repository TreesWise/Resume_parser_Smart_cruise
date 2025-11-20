# from sqlalchemy import text, Column, Integer, String, DateTime
# from sqlalchemy.ext.declarative import declarative_base
# from datetime import datetime
# from db import get_db_engine
# from app_logging import logger

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

# def init_db():
#     """
#     Initialize Azure SQL database
#     """
#     try:
#         engine = get_db_engine()
        
#         # Test connection first
#         with engine.connect() as conn:
#             conn.execute(text("SELECT 1"))
#             print("[DB] Azure SQL connection test successful", flush=True)
        
#         # Create tables if they don't exist
#         Base.metadata.create_all(bind=engine, checkfirst=True)
#         print("[DB] Azure SQL tables initialized", flush=True)
        
#     except Exception as e:
#         print(f"[DB] Initialization failed: {e}", flush=True)
#         # Re-raise the exception to prevent app startup if DB is critical
#         raise






from models import Base
from db import get_db_engine
from sqlalchemy import text

def init_db():
    
    try:
        engine = get_db_engine()

        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        Base.metadata.create_all(bind=engine, checkfirst=True)
        print("[DB] Azure SQL tables initialized", flush=True)
    
    except Exception as e:
        print(f"[DB] Initialization failed: {e}", flush=True)
        # Re-raise the exception to prevent app startup if DB is critical
        raise
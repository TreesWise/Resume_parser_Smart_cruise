from sqlalchemy import text, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from db import get_db_engine
from app_logging import logger

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


def fetch_mapped_documents():
    engine = get_db_engine()
    with engine.begin() as conn:
        result = conn.execute(text("""
            SELECT unidentified_doc_name, mapped_doc_name
            FROM Master_unidentified_doc_Table
            WHERE status = 'pending' OR status = 'exported'
        """))
        return result.fetchall()


def document_parser_fetch_mapped_documents():
    engine = get_db_engine()
    with engine.begin() as conn:
        result = conn.execute(text("""
            SELECT unidentified_doc_name, mapped_doc_name
            FROM Document_parser_master_unidentified_doc_Table
            WHERE status = 'pending' OR status = 'exported'
        """))
        return result.fetchall()
    

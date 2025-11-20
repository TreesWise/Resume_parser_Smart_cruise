from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

Base = declarative_base()

class TempDocument(Base):
    __tablename__ = "temp_table"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    unidentified_doc_name = Column(String, nullable=False)
    mapped_doc_name = Column(String, nullable=False)
    status = Column(String, default="pending")
    CreatedDate = Column(DateTime, default=datetime.now)

class MasterDocument(Base):
    __tablename__ = "Master_unidentified_doc_Table"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    unidentified_doc_name = Column(String, nullable=False)
    mapped_doc_name = Column(String, nullable=False)
    uploaded_date = Column(DateTime, default=datetime.now)
    status = Column(String, default="pending")


class DocumentParserTempTable(Base):
    __tablename__ = "Document_parser_temp_table"

    id = Column(Integer, primary_key=True, autoincrement=True)
    unidentified_doc_name = Column(String, nullable=False)
    mapped_doc_name = Column(String, nullable=False)
    status = Column(String, default="pending")
    CreatedDate = Column(DateTime, default=datetime.now)


# 4. NEW parser master unidentified table
class DocumentParserMasterUnidentified(Base):
    __tablename__ = "Document_parser_master_unidentified_doc_Table"

    id = Column(Integer, primary_key=True, autoincrement=True)
    unidentified_doc_name = Column(String, nullable=False)
    mapped_doc_name = Column(String, nullable=False)
    uploaded_date = Column(DateTime, default=datetime.now)
    status = Column(String, default="pending")
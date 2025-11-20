# from sqlalchemy import text, Column, Integer, String, DateTime
# from sqlalchemy.ext.declarative import declarative_base
# from datetime import datetime
# from app_logging import logger
# import pandas as pd

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

# def pandas_to_sql_fast(df: pd.DataFrame, table_name: str, engine):
#     # Use raw_connection to ensure pyodbc cursor available for fast_executemany
#     conn = engine.raw_connection()
#     cursor = conn.cursor()
#     try:
#         try:
#             cursor.fast_executemany = True
#         except Exception:
#             pass
#         # Use pandas to_sql that uses the SQLAlchemy engine; commit using raw connection
#         df.to_sql(table_name, con=engine, if_exists='append', index=False, method=None)
#         conn.commit()
#     finally:
#         try:
#             cursor.close()
#             conn.close()
#         except Exception:
#             pass






from sqlalchemy import text, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from app_logging import logger
import pandas as pd

from models import TempDocument, MasterDocument


def pandas_to_sql_fast(df: pd.DataFrame, table_name: str, engine):
    # Use raw_connection to ensure pyodbc cursor available for fast_executemany
    conn = engine.raw_connection()
    cursor = conn.cursor()
    try:
        try:
            cursor.fast_executemany = True
        except Exception:
            pass
        # Use pandas to_sql that uses the SQLAlchemy engine; commit using raw connection
        df.to_sql(table_name, con=engine, if_exists='append', index=False, method=None)
        conn.commit()
    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass
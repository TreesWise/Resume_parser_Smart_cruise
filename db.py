import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

AZURE_SQL_USER= os.getenv("AZURE_SQL_USER")
AZURE_SQL_PASSWORD= os.getenv("AZURE_SQL_PASSWORD")
AZURE_SQL_SERVER=os.getenv("AZURE_SQL_SERVER")
AZURE_SQL_DB=os.getenv("AZURE_SQL_DB")
AZURE_SQL_DRIVER=os.getenv("AZURE_SQL_DRIVER")

import urllib.parse
def get_db_engine():
    user = AZURE_SQL_USER
    password = AZURE_SQL_PASSWORD
    server = AZURE_SQL_SERVER
    database = AZURE_SQL_DB
    driver = AZURE_SQL_DRIVER
    # Encode credentials
    password_enc = urllib.parse.quote_plus(password)
    driver_enc = urllib.parse.quote_plus(driver)

    # Create SQLAlchemy engine
    engine_url = f"mssql+pyodbc://{user}:{password_enc}@{server}/{database}?driver={driver_enc}&Encrypt=yes&TrustServerCertificate=no"
    engine = create_engine(engine_url, pool_pre_ping=True)
    
    return engine
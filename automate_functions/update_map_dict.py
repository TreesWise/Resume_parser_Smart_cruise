from sqlalchemy import text, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from automate_functions.fetch_mapped_doc import fetch_mapped_documents,document_parser_fetch_mapped_documents
from automate_functions.download_dict_from_blob import download_dict_file_from_blob
# document_parser_download_dict_file_from_blob
from automate_functions.upload_dict_to_blob import upload_dict_file_to_blob
import ast
import os
from dotenv import load_dotenv
from app_logging import logger

load_dotenv()
AZURE_CONTAINER_NAME=os.getenv("AZURE_BLOB_CONTAINER_NAME")

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


# Function to escape newlines, quotes, and special characters properly
def escape_value(value):
    value = value.replace("\n", "\\n")
    value = value.replace('"', '\\"')
    return value


# def update_mapping_dict():
#     rows = fetch_mapped_documents()

#     mapping_dict = {}

#     try:
#         # Step 1: Download the current dict_file.py from Blob storage
#         download_dict_file_from_blob(AZURE_CONTAINER_NAME, 'dict_file.py', 'dict_file_local.py')
        
#         # Step 2: Load the downloaded dict file locally
#         with open('dict_file_local.py', 'r', encoding='utf-8') as f:
#             content = f.read()
#             if content.strip():  # Ensure the file isn't empty
#                 mapping_dict = ast.literal_eval(content.split('=', 1)[1].strip())

#     except FileNotFoundError:
#         logger.info("dict_file.py not found, starting fresh.")

#     # Helper: track lowercase->actual key for case-insensitive merge
#     normalized_keys = {k.lower(): k for k in mapping_dict.keys()}

#     # Step 3: Loop through rows and update mapping_dict
#     for row in rows:
#         unidentified_name = row[0]  # from DB
#         mapped_name = row[1]        # from DB
#         # unidentified_name = row["unidentified_doc_name"]
#         # mapped_name = row["mapped_doc_name"]

#         mapped_name_lower = mapped_name.lower()

#         if mapped_name_lower in normalized_keys:
#             # Use the first stored capitalization
#             actual_key = normalized_keys[mapped_name_lower]
#         else:
#             # New key → remember original capitalization
#             actual_key = mapped_name
#             normalized_keys[mapped_name_lower] = actual_key
#             mapping_dict[actual_key] = []

#         # Add unidentified if not already present
#         if unidentified_name not in mapping_dict[actual_key]:
#             mapping_dict[actual_key].append(unidentified_name)

#     # Step 4: Write the updated mapping_dict to file
#     with open('dict_file_updated.py', 'w', encoding='utf-8') as f:
#         f.write("mapping_dict = {\n")
#         for key, values in mapping_dict.items():
#             key = escape_value(key)
#             escaped_values = [f'"{escape_value(v)}"' for v in values]
#             f.write(f'    "{key}": [{", ".join(escaped_values)}],\n')
#         f.write("}\n")

#     # Step 5: Upload the updated dict_file.py back to Blob storage
#     upload_dict_file_to_blob('dict_file_updated.py', AZURE_CONTAINER_NAME, 'dict_file.py')

#     logger.info("dict_file.py updated and uploaded to Blob storage.")




def update_mapping_dict():
    # Combine rows from both fetch functions
    rows = []
    rows.extend(fetch_mapped_documents())
    rows.extend(document_parser_fetch_mapped_documents())

    mapping_dict = {}

    try:
        # Step 1: Download the current dict_file.py from Blob storage
        download_dict_file_from_blob(AZURE_CONTAINER_NAME, 'dict_file.py', 'dict_file_local.py')
        
        # Step 2: Load the downloaded dict file locally
        with open('dict_file_local.py', 'r', encoding='utf-8') as f:
            content = f.read()
            if content.strip():  # Ensure file isn't empty
                mapping_dict = ast.literal_eval(content.split('=', 1)[1].strip())

    except FileNotFoundError:
        logger.info("dict_file.py not found, starting fresh.")

    # Helper: track lowercase->actual key for case-insensitive merge
    normalized_keys = {k.lower(): k for k in mapping_dict.keys()}

    # Step 3: Loop through rows and update mapping_dict
    for row in rows:
        unidentified_name = row[0]  # from DB
        mapped_name = row[1]        # from DB

        mapped_name_lower = mapped_name.lower()

        if mapped_name_lower in normalized_keys:
            # Use the existing capitalization
            actual_key = normalized_keys[mapped_name_lower]
        else:
            # New key → store with original capitalization
            actual_key = mapped_name
            normalized_keys[mapped_name_lower] = actual_key
            mapping_dict[actual_key] = []

        # Add unidentified if not already present
        if unidentified_name not in mapping_dict[actual_key]:
            mapping_dict[actual_key].append(unidentified_name)

    # Step 4: Write updated mapping_dict to file
    with open('dict_file_updated.py', 'w', encoding='utf-8') as f:
        f.write("mapping_dict = {\n")
        for key, values in mapping_dict.items():
            key = escape_value(key)
            escaped_values = [f'"{escape_value(v)}"' for v in values]
            f.write(f'    "{key}": [{", ".join(escaped_values)}],\n')
        f.write("}\n")

    # Step 5: Upload updated file back to Blob storage
    upload_dict_file_to_blob('dict_file_updated.py', AZURE_CONTAINER_NAME, 'dict_file.py')

    logger.info("dict_file.py updated and uploaded to Blob storage.")



# def document_parser_update_mapping_dict():
#     rows = document_parser_fetch_mapped_documents()

#     mapping_dict = {}

#     try:
#         # Step 1: Download the current dict_file.py from Blob storage
#         document_parser_download_dict_file_from_blob(DOCUMENTPARSER_AZURE_BLOB_CONTAINER_NAME, 'dict_file.py', 'dict_file_local.py')
        
#         # Step 2: Load the downloaded dict file locally
#         with open('dict_file_local.py', 'r', encoding='utf-8') as f:
#             content = f.read()
#             if content.strip():  # Ensure the file isn't empty
#                 mapping_dict = ast.literal_eval(content.split('=', 1)[1].strip())

#     except FileNotFoundError:
#         logger.info("dict_file.py not found, starting fresh.")

#     # Helper: track lowercase->actual key for case-insensitive merge
#     normalized_keys = {k.lower(): k for k in mapping_dict.keys()}

#     # Step 3: Loop through rows and update mapping_dict
#     for row in rows:
#         unidentified_name = row[0]  # from DB
#         mapped_name = row[1]        # from DB
#         # unidentified_name = row["unidentified_doc_name"]
#         # mapped_name = row["mapped_doc_name"]

#         mapped_name_lower = mapped_name.lower()

#         if mapped_name_lower in normalized_keys:
#             # Use the first stored capitalization
#             actual_key = normalized_keys[mapped_name_lower]
#         else:
#             # New key → remember original capitalization
#             actual_key = mapped_name
#             normalized_keys[mapped_name_lower] = actual_key
#             mapping_dict[actual_key] = []

#         # Add unidentified if not already present
#         if unidentified_name not in mapping_dict[actual_key]:
#             mapping_dict[actual_key].append(unidentified_name)

#     # Step 4: Write the updated mapping_dict to file
#     with open('dict_file_updated.py', 'w', encoding='utf-8') as f:
#         f.write("mapping_dict = {\n")
#         for key, values in mapping_dict.items():
#             key = escape_value(key)
#             escaped_values = [f'"{escape_value(v)}"' for v in values]
#             f.write(f'    "{key}": [{", ".join(escaped_values)}],\n')
#         f.write("}\n")

#     # Step 5: Upload the updated dict_file.py back to Blob storage
#     upload_dict_file_to_blob('dict_file_updated.py', DOCUMENTPARSER_AZURE_BLOB_CONTAINER_NAME, 'dict_file.py')

#     logger.info("dict_file.py updated and uploaded to Blob storage.")

from automate_functions.export_data_to_excel import export_data_to_excel,export_document_paser_data_to_excel
from automate_functions.get_latest_replied_blob import get_latest_replied_blob_name,document_parser_get_latest_replied_blob_name
from automate_functions.insert_data_from_blob import insert_data_from_blob,documentparser_insert_data_from_blob
from automate_functions.update_map_dict import update_mapping_dict
# document_parser_update_mapping_dict
from app_logging import logger

def run_both_tasks():
    logger.info("[JOB] run_both_tasks START")
    try:
        export_data_to_excel()
        latest_blob = get_latest_replied_blob_name()
        insert_data_from_blob(latest_blob)
        update_mapping_dict()
        
        
        export_document_paser_data_to_excel()
        latest_blob=document_parser_get_latest_replied_blob_name()
        documentparser_insert_data_from_blob(latest_blob)
        # document_parser_update_mapping_dict()
        update_mapping_dict()


        
        
        
        
    except Exception:
        logger.exception("[JOB] run_both_tasks failed")
    finally:
        logger.info("[JOB] run_both_tasks END")
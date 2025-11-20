from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from azure.core.credentials import AzureKeyCredential
from app_logging import logger

def extract_resume_info(endpoint, key, model_id, path_to_sample_documents):
    document_intelligence_client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    
    with open(path_to_sample_documents, "rb") as f:
        poller = document_intelligence_client.begin_analyze_document(model_id=model_id, body=f)
    result: AnalyzeResult = poller.result()

    extracted_info = {}
    tables = []
    
    if result.documents:
        for idx, document in enumerate(result.documents):
            extracted_info["doc_type"] = document.doc_type
            extracted_info["confidence"] = document.confidence
            extracted_info["model_id"] = result.model_id
            
            if document.fields:
                extracted_info["fields"] = {}
                for name, field in document.fields.items():
                    field_value = field.get("valueString") if field.get("valueString") else field.content
                    extracted_info["fields"][name] = field_value
            
            # Extract table information
            for field_name, field_value in document.fields.items():
                if field_value.type == "array" and field_value.value_array:
                    col_names = []
                    sample_obj = field_value.value_array[0]
                    if "valueObject" in sample_obj:
                        col_names = list(sample_obj["valueObject"].keys())
                    
                    table_rows = []
                    for obj in field_value.value_array:
                        if "valueObject" in obj:
                            value_obj = obj["valueObject"]
                            row_data = [value_obj[col].get("content", None) for col in col_names]
                            table_rows.append(row_data)
                    
                    tables.append({"table_name": field_name, "columns": col_names, "rows": table_rows})
    
    extracted_info["tables"] = tables
    return extracted_info

import os
import shutil
import tempfile
import asyncio
from datetime import datetime
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from res_services.convert_docx_to_pdf import convert_docx_to_pdf
from res_resume_extraction.extract_resume_info import extract_resume_info
from res_openai_functions.basic_openai import basic_openai
from res_openai_functions.certificate_openai import certificate_openai
from res_openai_functions.experience_openai import experience_openai
from res_services.clean_vessel_name import clean_vessel_names
from res_variables.var import basic_details_order, certificate_table_order, experience_table_order
from res_services.reorder_basicdetails_table import reorder_basic_details_table
from res_services.reorder_certificate_table import reorder_certificate_table
from res_services.reorder_experience_table import reorder_experience_table
from res_resume_extraction.validate_parsed_resume import validate_parsed_resume
from res_services.replace_certificates import replace_values
from res_services.replace_rank import replace_rank
from res_services.replace_country import replace_country
from res_services.reposition_fields import reposition_fields
from country_mapping import country_mapping
from rank_map_dict import rank_mapping
from app_logging import logger
from automate_functions.load_map_dict_from_blob import load_mapping_dict_from_blob


async def process_resume_upload(file, entity, endpoint, key, model_id, container_name, connection_string):
    temp_file_path = None
    try:
        # Extract file extension
        suffix = os.path.splitext(file.filename)[-1].lower()
        if suffix not in [".pdf", ".docx"]:
            raise HTTPException(status_code=400, detail="Only PDF and Word documents are allowed")

        # Generate custom filename with timestamp
        timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        temp_file_path = os.path.join(tempfile.gettempdir(), f"{timestamp}{suffix}")

        # Write the uploaded file to the custom temp path
        with open(temp_file_path, "wb") as temp_file:
            shutil.copyfileobj(file.file, temp_file)

        # Handle .docx conversion if needed
        if suffix == ".docx":
            temp_file_path = await convert_docx_to_pdf(temp_file_path)

        # Extract JSON from document
        extracted_info = extract_resume_info(endpoint, key, model_id, temp_file_path)

        fields_only = extracted_info["fields"]
        tables = extracted_info.get('tables', [])
        certificate_table, experience_table = None, None

        for table in tables:
            if table.get('table_name') == 'certificate_table':
                certificate_table = table
            elif table.get('table_name') == 'experience_table':
                experience_table = table

        # Run async tasks
        basic_out, cert_out, expe_out = await asyncio.gather(
            asyncio.to_thread(basic_openai, fields_only),
            asyncio.to_thread(certificate_openai, certificate_table),
            asyncio.to_thread(experience_openai, experience_table),
        )

        # Merge outputs
        basic_details_merge = basic_out['basic_details']
        certificate_table_merge = cert_out['certificate_table']

        # Inject gender logic
        if basic_details_merge and len(basic_details_merge) > 1:
            header = basic_details_merge[0]
            values = basic_details_merge[1]
            gender_index = None
            for keyy, value in header.items():
                if value.lower() == "gender":
                    gender_index = keyy
                    break
            if gender_index is not None:
                gender_value = str(values.get(gender_index, "")).strip().lower()
                if gender_value not in ["male", "female"]:
                    values[gender_index] = "Male"
                else:
                    values[gender_index] = gender_value.capitalize()

        experience_table_merge = clean_vessel_names(expe_out['experience_table'])
        reordered_basic = reorder_basic_details_table(basic_details_merge)
        reordered_certificates = reorder_certificate_table(certificate_table_merge)
        reordered_experience = reorder_experience_table(experience_table_merge)

        final_output = {
            "status": "success",
            "data": {
                "basic_details": reordered_basic,
                "experience_table": reordered_experience,
                "certificate_table": reordered_certificates
            },
            "utc_time_stamp": datetime.utcnow().strftime("%d/%m/%Y, %H:%M:%S")
        }

        validation_errors = validate_parsed_resume(extracted_info, temp_file_path, 0.8, container_name, connection_string)
        logger.info("Validation result: %s", validation_errors)

        # Mappings
        current_mapping_dict = load_mapping_dict_from_blob() 
        course_map = replace_values(final_output, current_mapping_dict)
        rank_map = replace_rank(course_map, rank_mapping)
        rank_map = replace_country(rank_map, country_mapping)

        # Apply country replacement
        rank_map['data']['basic_details'] = replace_country(rank_map['data']['basic_details'], country_mapping)
        rank_map['data']['certificate_table'] = replace_country(rank_map['data']['certificate_table'], country_mapping)

        # Reorder fields
        basic_details = reposition_fields(rank_map['data']['basic_details'], basic_details_order) if rank_map['data']['basic_details'] else []
        experience_table = reposition_fields(rank_map['data']['experience_table'], experience_table_order) if rank_map['data']['experience_table'] else []
        certificate_table = reposition_fields(rank_map['data']['certificate_table'], certificate_table_order) if rank_map['data']['certificate_table'] else []

        rank_map['data']['basic_details'] = basic_details
        rank_map['data']['experience_table'] = experience_table
        rank_map['data']['certificate_table'] = certificate_table

        # Filter invalid experience rows
        if experience_table:
            filtered_experience = [experience_table[0]]
            max_allowed_nulls = 8
            for row in experience_table[1:]:
                if isinstance(row, dict):
                    null_count = sum(1 for v in row.values() if v is None)
                    if null_count < max_allowed_nulls:
                        filtered_experience.append(row)
            rank_map['data']['experience_table'] = filtered_experience
            logger.info("Filtered experience_table: %s", filtered_experience)

        return rank_map

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        logger.error("Unexpected error in process_resume_upload: %s", e, exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": "An unexpected error occurred during resume processing.",
                "detail": str(e)
            }
        )

    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            logger.debug("Temporary file removed: %s", temp_file_path)

import re
from app_logging import logger

def clean_vessel_names(experience_table):
    if not experience_table or len(experience_table) < 2:
        return experience_table
 
    # Identify the header index for "VesselName"
    header = experience_table[0]
    vessel_name_index = None
    for key, value in header.items():
        if value.lower() == "vesselname":
            vessel_name_index = key
            break
 
    if vessel_name_index is None:
        return experience_table  # Skip if "VesselName" not found
 
    # Updated pattern includes hyphens after prefix
    prefix_pattern = r'^(M[\s./\\]?[V|T][\s.\-]*)'
 
    # Clean each row
    for row in experience_table[1:]:
        vessel_name = row.get(vessel_name_index, "")
        if vessel_name:
            # Remove the prefix if it matches
            cleaned_name = re.sub(prefix_pattern, '', vessel_name, flags=re.IGNORECASE).strip()
            row[vessel_name_index] = cleaned_name
 
    return experience_table
 
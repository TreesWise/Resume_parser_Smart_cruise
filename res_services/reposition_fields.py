from app_logging import logger

def reposition_fields(table_data, desired_order):
    updated_table_data = []
    
    # Get the header row
    header = table_data[0]
    
    # Create a mapping of field names to index positions
    key_mapping = {value: key for key, value in header.items()}
    
    for row in table_data:
        reordered_row = {}

        # Ensure all specified fields are placed correctly
        for i, field in enumerate(desired_order):
            reordered_row[str(i)] = row.get(key_mapping.get(field, ""), "")

        # Add remaining fields starting at index after the last specified field
        remaining_keys = [k for k in row.keys() if k not in key_mapping.values()]
        for j, key in enumerate(remaining_keys, start=len(desired_order)):
            reordered_row[str(j)] = row.get(key, "")

        updated_table_data.append(reordered_row)

    return updated_table_data

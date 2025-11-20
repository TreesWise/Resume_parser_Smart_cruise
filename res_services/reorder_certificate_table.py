from res_variables.var import desired_cert_order
from app_logging import logger

def reorder_certificate_table(data):
    if not data:
        return []

    # Step 1: Get current header (first element is a dict with index keys)
    current_header = data[0]
    
    # Build mapping: "CertificateNo" => "0", etc.
    name_to_index = {v: k for k, v in current_header.items()}
    
    # Step 2: Build new header with desired order
    new_header = {str(i): col_name for i, col_name in enumerate(desired_cert_order)}
    
    # Step 3: Reorder all rows based on desired order
    reordered_data = [new_header]
    
    for row in data[1:]:
        new_row = {}
        for new_idx, col_name in enumerate(desired_cert_order):
            old_idx = name_to_index.get(col_name)
            new_row[str(new_idx)] = row.get(old_idx) if old_idx is not None else None
        reordered_data.append(new_row)

    return reordered_data

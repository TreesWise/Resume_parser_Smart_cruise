from app_logging import logger
from res_variables.var import  desired_basic_order

def reorder_basic_details_table(data):
            if not data:
                return []
 
            # Get current header
            current_header = data[0]
           
            # Map field name to current index
            name_to_index = {v: k for k, v in current_header.items()}
           
            # New header in desired order
            new_header = {str(i): field_name for i, field_name in enumerate(desired_basic_order)}
 
            reordered_data = [new_header]
 
            for row in data[1:]:
                new_row = {}
                for new_idx, field_name in enumerate(desired_basic_order):
                    old_idx = name_to_index.get(field_name)
                    new_row[str(new_idx)] = row.get(old_idx) if old_idx is not None else None
                reordered_data.append(new_row)
 
            return reordered_data
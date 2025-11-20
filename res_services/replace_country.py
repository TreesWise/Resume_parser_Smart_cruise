from app_logging import logger

def replace_country(data, mapping):
    if isinstance(data, dict):
        new_dict = {}
        for key, value in data.items():
            # Process both keys and values
            new_key = mapping.get(key, key) if isinstance(key, str) else key
            new_value = replace_country(value, mapping)
            new_dict[new_key] = new_value
            
            # Print if value changed (only for string values)
            if isinstance(value, str) and value != new_value:
                # print(f"Mapping country: '{value}' → '{new_value}'")
                logger.debug("Mapping country: '%s' → '%s'", value, new_value)
        return new_dict
        
    elif isinstance(data, list):
        new_list = []
        for item in data:
            new_item = replace_country(item, mapping)
            new_list.append(new_item)
        return new_list
        
    elif isinstance(data, str):
        return mapping.get(data, data)
        
    return data

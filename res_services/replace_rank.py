from app_logging import logger

def replace_rank(json_data, rank_mapping):
    # Convert rank_mapping keys to lowercase for case-insensitive replacement
    rank_mapping = {key.lower(): value for key, value in rank_mapping.items()}

    if isinstance(json_data, dict):
        return {
            key: replace_rank(value, rank_mapping) if key != "2" else  # "2" corresponds to "Position"
            rank_mapping.get(value.lower(), value) if isinstance(value, str) else value
            for key, value in json_data.items()
        }
    elif isinstance(json_data, list):
        return [replace_rank(item, rank_mapping) for item in json_data]
    return json_data
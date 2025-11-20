from app_logging import logger

# def replace_values(data, mapping):
#     if isinstance(data, dict):
#         return {mapping.get(key, key): replace_values(value, mapping) for key, value in data.items()}
#     elif isinstance(data, list):
#         return [replace_values(item, mapping) for item in data]
#     elif isinstance(data, str):
#         return mapping.get(data, data)  # Replace if found, else keep original
#     return data


# def replace_values(data, mapping):
#     # Build a reverse lookup dictionary (case-insensitive)
#     reverse_map = {}     
#     for key, variants in mapping.items():
#         for v in variants:
#             reverse_map[v.lower()] = key  # match lowercase for comparison

#     # Process certificate_table rows (skip header)
#     for row in data.get("data", {}).get("certificate_table", [])[1:]:
#         cert_name = row.get("1", "")
#         if cert_name.lower() in reverse_map:  # case-insensitive match
#             row["1"] = reverse_map[cert_name.lower()]  # replace with canonical name

#     return data



def replace_values(data, mapping):
    # Build a reverse lookup dictionary (case-insensitive)
    reverse_map = {}
    for key, variants in mapping.items():
        for v in variants:
            if isinstance(v, str):  # ensure variant is string
                reverse_map[v.strip().lower()] = key  # normalize spaces + lowercase

    # Process certificate_table rows (skip header)
    for row in data.get("data", {}).get("certificate_table", [])[1:]:
        cert_name = row.get("1", "")
        if isinstance(cert_name, str):  # only process if it's a string
            cert_key = cert_name.strip().lower()
            if cert_key in reverse_map:
                row["1"] = reverse_map[cert_key]

    return data

import json
from client import client
from app_logging import logger

def basic_openai(basic_table):

    prompt = f"""
    You are given a Python dictionary representing extracted personal information from a resume. Transform it into a JSON object with a key "basic_details", whose value is a list of two dictionaries:

    1. The first dictionary maps indexes (as string keys) from "0" to "19" to specific field names in this exact order:
    ["Name", "FirstName", "MiddleName", "LastName", "Nationality", "Gender", "Doa", "Dob", "Address1", "Address2", "Address3", "Address4", "City", "State", "Country", "ZipCode", "EmailId", "MobileNo", "AlternateNo", "Rank"]

    2. The second dictionary maps the same indexes to the actual values found in the input dictionary (or `null` if not present or value is None).

    Ensure:
    - The output is valid JSON.
    - All keys in the first and second dictionaries are stringified numbers ("0", "1", ..., "19").
    - The order of the fields is preserved exactly as described.
    - Use `null` in JSON for missing or None values, not the Python `None`.
    - Remove any escape characters (such as `\\n`, `\\t`, `\\r`, or unnecessary backslashes) from the final JSON output so that it looks clean and properly formatted.

    3. Convert all dates to DD-MM-YYYY format
    4. Replace country names in Nationality with their demonym (e.g., Russia → Russian)
    5. Normalize gender values (male → Male, female → Female)
    # The above code is outlining a set of normalization rules for the "Country" field in a dataset.
    # It specifies steps to clean and standardize the country names by removing leading labels,
    # splitting on delimiters, identifying known country names, and handling cases where multiple
    # parts are present. Additionally, it provides instructions for populating the "City" field based
    # on the normalized country values. The goal is to ensure consistent and formatted country and
    # city data in the dataset.
    6. Normalize the "Country" field:
    - Remove any leading labels or descriptors (e.g., words like "country", "residency", "city", etc.).
    - If the remaining value contains multiple parts separated by delimiters (any of `/ | , ; - : >`), split on the first delimiter.
    - Take the **country** as:
        a) the part that matches a known country name (case-insensitive), if present; otherwise
        b) the first non-empty part after trimming.
    - Trim extra spaces, collapse repeated whitespace, and title-case names (preserve accents and standard abbreviations like USA, UK, UAE).
    7. Populate the "City" field:
    - If, after applying rule 6, there is a second non-empty part from the split, assign it to **City** after trimming and normalizing spacing (title-case).
    - If no second part exists, set City to `null`.
    - If the detected country and city are identical, keep the value as Country and set City to `null`.
    8. Handle and correct location fields (City, State, Country):
    - If City is present but State or Country is missing, infer its State and Country and populate to its corresponding fields.
    - If only State is present but Country is missing, infer its Country and populate to its corresponding field.
    - If any of these fields (City, State, Country) contain misplaced values (e.g., "India" in City or "Chennai" in Country), correct and reassign them.
    - If City and State are identical, map the correct State for that City.
    - Use known city–state–country mappings (e.g., "Chennai" → "Tamil Nadu", "India") to ensure consistency.
    

    Here is the input dictionary:
    {basic_table}

    Return the final JSON as a list of dictionaries under the key "experience_table".
    """
    print("basic details------------------------------------------------------------", basic_table)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a data formatter."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0
    )
    
    

    res_json = json.loads(response.choices[0].message.content)
    return res_json
import json
from client import client
from app_logging import logger

def experience_openai(experience_table):

    prompt = f"""
    You are given a dictionary with the following structure:
    - "table_name": the name of the table.
    - "columns": a list of column names.
    - "rows": a list of lists, where each sublist represents a row corresponding to the columns.

    Your task is to convert this dictionary into a list of dictionaries with the following rules:

    1. The first dictionary should map column indices as strings ("0", "1", ..., etc.) to their corresponding column names in order.
    2. Each subsequent dictionary should represent one row of data, where:
       - Keys are column indices as strings.
       - Values are cell values from that row, matched to the correct column index.
       - If a value is missing or the row has fewer elements than the number of columns, fill the missing ones with null.
    3. If any cell contains multi-line values separated by newline characters (`\\n`), treat them as multiple rows, properly aligned.
    4. If any cell in the FromDt (index "5") or ToDt (index "6") column contains **two dates separated by a newline character (`\\n`)**, such as `"09.08.18\\n30.03.19"` or `"27.04.19\\n20.10.20"`:
        - Do NOT split this row into multiple rows.
        - Instead, split the two dates into separate values.
        - Assign the **first date** to FromDt (index "5").
        - Assign the **second date** to ToDt (index "6").
        - Keep all other data in the row unchanged.
        - This ensures the row remains one complete record with FromDt and ToDt properly filled.
    5. If any row contains mostly null values except for **one or more isolated non-null fields**, consider this row a **continuation or supplemental data** for a nearby related row:
       - The model must identify the nearest logical row missing that data.
       - Merge or assign the orphan data into that row’s appropriate field(s).
       - Remove these orphan rows from the final output after merging.
       - This applies to *any* column, such as dates, flags, places, or others.
    6. Maintain the same number of fields per row and ensure no data is lost.
    7. Preserve the original order as much as possible while maintaining data integrity.
    8. Convert all dates to DD-MM-YYYY format.
    9. Fix broken words caused by accidental spaces (e.g., 'Carri er')
    10. Do not merge or overwrite existing entries. If a new row contains only one non-null field and the rest are null, it must be treated as a separate, junk row and excluded from the final output. Do not use such rows to update or modify the previous row.
    11. DO NOT drop or skip any rows or fields in the experience_table
    12. Remove any escape characters (such as `\\n`, `\\t`, `\\r`, or unnecessary backslashes) from the final JSON output so that it looks clean and properly formatted.
    


    Here is the input dictionary:
    {experience_table}

    Return the final JSON as a list of dictionaries under the key "experience_table".
    """


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
import json
from client import client
from app_logging import logger

def certificate_openai(certificate_table):
    prompt = f"""
You are given a dictionary with the following structure:
- "table_name": the name of the table.
- "columns": a list of column names.
- "rows": a list of lists, where each sublist represents a row of data.

Your task is to transform this dictionary into a list of dictionaries under the key "certificate_table", following these rules:

1. Column Mapping  
   - The first dictionary should map column indices as strings ("0", "1", ..., "N") to their corresponding column names in order.

2. Row Transformation  
   - Each subsequent dictionary should represent one row of data.  
   - Keys = column indices as strings.  
   - Values = cell values from that row.  
   - If a value is missing or the row has fewer elements than the number of columns, fill the missing values with null.

3. **Certificate Name Handling**  
   - If a cell in the Certificate Name column contains multiple certificates separated by newline characters ("\\n"):  
     - Keep the first certificate name in the original row.  
     - The second certificate name must **not create a new duplicate row**.  
     - Instead, place it into the nearest following row’s empty Certificate Name field (index "1"), while keeping that row’s existing data unchanged.  
     - Only if no such row exists, create a new row with that certificate name.  
     - Ensure no duplication of certificate numbers, dates, or country values.

4. Date Splitting & Correction  
   - If any field contains two dates separated by "/" or "," (e.g., "17.04.2019/17.04.2024", "17.04.2019,17.04.2024"):  
     - Place the first date in the "DateOfIssue" column (index "4").  
     - Place the second date in the "DateOfExpiry" column (index "5").  
     - This applies regardless of which column originally contained the dates.
   - If "DateOfExpiry" contains two dates separated by "/" or "," (e.g., "17.04.2019/17.04.2024", "17.04.2019,17.04.2024"):
     - Place the first date in "DateOfExpiry" column of same cell(index "5").
     - Place it into the nearest following row’s empty "DateOfExpiry" (index "5"), while keeping that row’s existing data unchanged.
     - Also make sure that it doesn't create a new cell. 
    
      
      Apply this Mapping all over in the certificate_table section. 

5. Date Formatting  
   - Convert all dates into DD-MM-YYYY format.

6. Data Preservation  
   - Maintain the same number of fields per row as the number of columns.  
   - Do not drop or skip any rows or fields.  
   - Preserve the original row order.

7. Country of Issue Inference  
   - If PlaceOfIssue is provided but CountryOfIssue is missing, determine the country corresponding to the place and populate it.

8. Text Cleaning  
   - Fix broken words caused by accidental spaces (e.g., "Carri er" → "Carrier").

9. Remove any escape characters (such as `\\n`, `\\t`, `\\r`, or unnecessary backslashes) from the final JSON output so that it looks clean and properly formatted.
---

---

Here is the input dictionary:
{certificate_table}

Return the final JSON as a list of dictionaries under the key "certificate_table".
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


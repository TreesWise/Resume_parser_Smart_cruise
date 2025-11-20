# from datetime import datetime
# from client import client
# from app_logging import logger

# current_date = datetime.now().strftime("%d-%m-%Y")

# def get_default_json():
#     return {
#         "docName": "null",
#         "DocNumber": "null",
#         "uploadedDate": current_date,
#         "issuedCountry": "null",
#         "IssuedPlace": "null",
#         "issueDate": "null",
#         "expDate": "null",
#         "isNationalDoc": "null"
#     }   


# def extract_json(images_b64):
#     prompt_text = f"""You are an expert in document data extraction. Extract and translate into English only the following details in the following JSON format:

#     JSON Format:
#     {{
#     "docName": "...",              
#     "DocNumber": "...",            
#     "uploadedDate": "{current_date}",
#     "issuedCountry": "...",  
#     "IssuedPlace": "...",   
#     "issueDate": "dd-mm-yyyy",     
#     "expDate": "dd-mm-yyyy",       
#     "isNationalDoc": "Yes" or "No"   
#     }}

    
#     ### Instructions:
#     1. Extract all **valid certificates, endorsements, medical documents, and training courses** from the document and return each as a separate JSON object.
#     2.1. **For Visa documents** (i.e., if `docName` is "Visa" or contains the word "Visa"):
#     - Extract only the **Visa Control Number** or **Visa Grant Number** as the `DocNumber`.
#     - **Strictly ignore the Passport Number**, even if it appears on the same page.
#     - The `DocNumber` must never be set to a **Passport Number** in Visa documents under any condition.
#     - If **both numbers are found**, always choose the **Visa-specific number**, and discard the Passport Number.

#     ### Special Rules for IssuedPlace:
#     - **IssuedPlace** refers to the place of issue (city, port, or institution).
#     - Do not use **place of birth, residence, or home city** as `IssuedPlace`.
#     - **Never set `IssuedPlace` to `"null"`** if the country is known; use the country as a fallback if `IssuedPlace` is missing.
#     - Set `IssuedPlace` to `"null"` only if both the place and country are missing or invalid.
#     - **This rule applies to all documents**. Even if `IssuedPlace` is missing in any document, it must always fallback to the `IssuedCountry` if the country is available. Do **not apply this logic to just the first document**, but **ensure it is applied consistently to all documents in the list**.


#     ### Special Rules for DocNumber:
#     - **"DocNumber"**: Select the most relevant number based on priority:
#     1. **For Visa documents** (if `docName` is "Visa" or contains the word "Visa"): 
#         - Extract the **Visa Control Number** and use it as the `DocNumber`.
#         - **Do not** extract the **Passport Number** for Visa documents, even if both numbers are present.
#     2. **For Passport documents**: 
#         - Extract the **Passport Number** and use it as the `DocNumber`.
#     3. **Seaman's Book No.**.
#     4. **Certificate No.** / **Doc Number**.
#     5. **Strictly ignore any numbers without an explicit label indicating a document number** (e.g., "Passport Number", "Seaman's Book No.", "Certificate No.", "Doc Number", "Visa Control Number", "Visa Grant Number"). This includes numbers found in fields like "Application ID", "Serial No", "Control Number" or any unlabelled number. If no valid DocNumber with an explicit label is found, set "DocNumber" to "null".
#     6.For e-Business Visa use Applictaion id as DocNumber.
#     ### Special Rules for docName:
#     - **if the docName  is visa then check which visa also.



#     - **Do not use** "Serial No", "SL No", "Control Number", or "ID No".

    

#     ### Field Rules:
#     1. **"docName"** – Name of the certificate, endorsement, or training (e.g., "Certificate of Competency", "Advanced Fire Fighting", "Passport", "Visa").
#     2. **"DocNumber"** – Use explicit labels like “Certificate No.”, “Doc Number”, “Passport Number” etc.
#     3. **"uploadedDate"** – Use today’s date: **{current_date}**.
#     4. **"issuedCountry"** – Country where the document was issued.
#     5. **"IssuedPlace"** – City or port of issue. If only an institution name is listed (e.g., "Ministry of..."), set to **"null"**.
#     6. **"issueDate"** and **"expDate"** – Format as **dd-mm-yyyy**.
#     7. **"isNationalDoc"** – 
#     - Set to **"Yes"** only if the document is a **Passport** (i.e., `"docName"` is `"Passport"`).
#     - For **all other documents**, set it to **"No"**.

#     8. Use **"null"** for any missing fields (like DocNumber, IssuedPlace, etc.).

#     ### Extraction Guidelines:
#     - Extract valid sections of the document:
#     - Certificates, Endorsements, Health Certificates, Training Courses, Seaman’s Book, Passport.
#     - Only extract sections with valid **document numbers** and clear details.
#     - If multiple numbers or expiry dates exist, return them as separate objects.
#     - Ignore irrelevant sections like revalidations, administrative stamps, or incomplete details.
#     - If no valid information is found, return `null`.
#     - Extract all valid certificates and courses, no prioritization.
#     - **Translate content into English** where needed.

#     ### Special Case: Course Lists or Tables
#     - If training courses are listed in tables, extract each row as a separate object.
#     - Set `"DocNumber"`, `"issueDate"`, `"expDate"`, `"IssuedPlace"` to `"null"` if not available.
#     - Do not skip course entries even if embedded in other sections.

#     ### Output Format:
#     - Return a flat JSON array with no markdown, code blocks, or extra commentary.
#     - Each object must include all fields listed in the JSON format.
#     - Ensure the output is valid JSON.

#     ### Examples:
#     - Certificate of Competency (Master)
#     - Endorsement (GMDSS Radio Operator)
#     - Seafarer's Medical Certificate
#     - Seaman’s Book
#     - Passport
#     - Familiarization and Basic Safety Training
#     - Advanced Fire Fighting
#     - Medical First Aid
#     - ARPA
#     - Radar Simulator
#     - Security Awareness Training
#     """

#     prompt = [
#         {
#             "type": "text",
#             "text": prompt_text
#         },
#         *[
#             {
#                 "type": "image_url",
#                 "image_url": {
#                     "url": f"data:image/png;base64,{img}"
#                 }
#             } for img in images_b64
#         ]
#     ]

#     response = client.chat.completions.create(
#         model="gpt-4o",
#         messages=[{"role": "user", "content": prompt}]
#     )

#     content = response.choices[0].message.content.strip()
#     if content.startswith("```json"):
#         content = content.replace("```json", "").replace("```", "").strip()

#     return content



# from datetime import datetime
# from client import client
# from app_logging import logger

# current_date = datetime.now().strftime("%d-%m-%Y")

# def get_default_json():
#     return {
#         "docName": "null",
#         "DocNumber": "null",
#         "uploadedDate": current_date,
#         "issuedCountry": "null",
#         "IssuedPlace": "null",
#         "issueDate": "null",
#         "expDate": "null",
#         "isNationalDoc": "null"
#     }   


# def extract_json(images_b64):
    

#     prompt_text = f"""You are an expert in document data extraction. Extract and translate into English only the following details in the following JSON format:

#     JSON Format:
#     {{
#     "docName": "...",              
#     "DocNumber": "...",            
#     "uploadedDate": "{current_date}",
#     "issuedCountry": "...",  
#     "IssuedPlace": "...",   
#     "issueDate": "dd-mm-yyyy",     
#     "expDate": "dd-mm-yyyy",       
#     "isNationalDoc": "Yes" or "No"   
#     }}

    
#     ### Instructions:
#     1. Extract all **valid certificates, endorsements, medical documents, and training courses** from the document and return each as a separate JSON object.
#     2.1. **For Visa documents** (i.e., if `docName` is "Visa" or contains the word "Visa"):
#     - Extract only the **Visa Control Number** or **Visa Grant Number** as the `DocNumber`.
#     - **Strictly ignore the Passport Number**, even if it appears on the same page.
#     - The `DocNumber` must never be set to a **Passport Number** in Visa documents under any condition.
#     - If **both numbers are found**, always choose the **Visa-specific number**, and discard the Passport Number.

#     ### Special Rules for IssuedPlace:
#     - **IssuedPlace** refers to the place of issue (city, port, or institution).
#     - Do not use **place of birth, residence, or home city** as `IssuedPlace`.
#     - **Never set `IssuedPlace` to `"null"`** if the country is known; use the country as a fallback if `IssuedPlace` is missing.
#     - Set `IssuedPlace` to `"null"` only if both the place and country are missing or invalid.
#     - **This rule applies to all documents**. Even if `IssuedPlace` is missing in any document, it must always fallback to the `IssuedCountry` if the country is available. Do **not apply this logic to just the first document**, but **ensure it is applied consistently to all documents in the list**.


#     ### Special Rules for DocNumber:
#     - **"DocNumber"**: Select the most relevant number based on priority:
#     1. **For Visa documents** (if `docName` is "Visa" or contains the word "Visa"): 
#         - Extract the **Visa Control Number** and use it as the `DocNumber`.
#         - **Do not** extract the **Passport Number** for Visa documents, even if both numbers are present.
#     2. **For Passport documents**: 
#         - Extract the **Passport Number** and use it as the `DocNumber`.
#     3. **Seaman's Book No.**.
#     4. **Certificate No.** / **Doc Number**.
#     5. **Strictly ignore any numbers without an explicit label indicating a document number** (e.g., "Passport Number", "Seaman's Book No.", "Certificate No.", "Doc Number", "Visa Control Number", "Visa Grant Number"). This includes numbers found in fields like "Application ID", "Serial No", "Control Number" or any unlabelled number. If no valid DocNumber with an explicit label is found, set "DocNumber" to "null".
#     6.For e-Business Visa use Applictaion id as DocNumber.
    
#     ### Special Rules for docName:
#     - "docName" must exactly match an explicitly written title, heading, or labeled phrase in the document image such as:
#     "Certificate of Competency", "Endorsement", "Passport", "Visa", "Medical Certificate", "Training Course", etc.
#     - If no clear document title or name appears in the image, set "docName" = "null".
#     - Never infer, guess, or assume a document name based on surrounding words.
#     - Do not use partial or prefix words such as "Certificate", "Form", "Document","Type" or "Application" alone as the document name 
#     if they are followed by terms like "Number", "Type", "Date", "Name", etc.
#     - Example: If the text says "Certificate Number" or "Certificate Type" without an actual title (e.g., "Certificate of Competency"), 
#     treat "Certificate" as a field label, not a title → set "docName": "null".
#     - If "docName" contains the word "Visa", analyze the type (e.g., "Business Visa", "Seaman Visa", "Employment Visa") if available.
#     - **Do not use** generic field headers or control labels like "Serial No", "SL No", "Control Number", "ID No", "Form No", or "Reference No" as document names.
    

#     ### Field Rules:
#     1. **"docName"** – Name of the certificate, endorsement, or training (e.g., "Certificate of Competency", "Advanced Fire Fighting", "Passport", "Visa").
#     2. **"DocNumber"** – Use explicit labels like “Certificate No.”, “Doc Number”, “Passport Number” etc.
#     3. **"uploadedDate"** – Use today’s date: **{current_date}**.
#     4. **"issuedCountry"** – Country where the document was issued.
#     5. **"IssuedPlace"** – City or port of issue. If only an institution name is listed (e.g., "Ministry of..."), set to **"null"**.
#     6. **"issueDate"** and **"expDate"** – Format as **dd-mm-yyyy**.
#     7. **"isNationalDoc"** – 
#     - Set to **"Yes"** only if the document is a **Passport** (i.e., `"docName"` is `"Passport"`).
#     - For **all other documents**, set it to **"No"**.

#     8. Use **"null"** for any missing fields (like DocNumber, IssuedPlace, etc.).

#     ### Extraction Guidelines:
#     - Extract valid sections of the document:
#     - Certificates, Endorsements, Health Certificates, Training Courses, Seaman’s Book, Passport.
#     - Only extract sections with valid **document numbers** and clear details.
#     - If multiple numbers or expiry dates exist, return them as separate objects.
#     - Ignore irrelevant sections like revalidations, administrative stamps, or incomplete details.
#     - If no valid information is found, return `null`.
#     - Extract all valid certificates and courses, no prioritization.
#     - **Translate content into English** where needed.
    
#     ### **Critical Validation Rule:**
#     - Each document object must be returned **unless both** `"docName"` and `"DocNumber"` are missing, invalid, or `"null"`.
#     - Never invent or assume document names, if not explicitly written in the image.
#     - If **both** `"docName"` and `"DocNumber"` are missing, return exactly **one default JSON object** as follows:

#     {{
#       "docName": "null",
#       "DocNumber": "null",
#       "uploadedDate": "{current_date}",
#       "issuedCountry": "null",
#       "IssuedPlace": "null",
#       "issueDate": "null",
#       "expDate": "null",
#       "isNationalDoc": "null"
#     }}

#     - This rule applies globally to all extracted documents.
    
#     ### Special Case: Course Lists or Tables
#     - If training courses are listed in tables, extract each row as a separate object.
#     - Set `"DocNumber"`, `"issueDate"`, `"expDate"`, `"IssuedPlace"` to `"null"` if not available.
#     - Do not skip course entries even if embedded in other sections.

#     ### Output Format:
#     - Return a flat JSON array with no markdown, code blocks, or extra commentary.
#     - Each object must include all fields listed in the JSON format.
#     - Ensure the output is valid JSON.

#     ### Examples:
#     - Certificate of Competency (Master)
#     - Endorsement (GMDSS Radio Operator)
#     - Seafarer's Medical Certificate
#     - Seaman’s Book
#     - Passport
#     - Familiarization and Basic Safety Training
#     - Advanced Fire Fighting
#     - Medical First Aid
#     - ARPA
#     - Radar Simulator
#     - Security Awareness Training
#     """

#     prompt = [
#         {
#             "type": "text",
#             "text": prompt_text
#         },
#         *[
#             {
#                 "type": "image_url",
#                 "image_url": {
#                     "url": f"data:image/png;base64,{img}"
#                 }
#             } for img in images_b64
#         ]
#     ]

#     response = client.chat.completions.create(
#         model="gpt-4o",
#         messages=[{"role": "user", "content": prompt}]
#     )
#     content = response.choices[0].message.content.strip()

#     if content.startswith("```json"):
#         content = content.replace("```json", "").replace("```", "").strip()


    
#     return content




from datetime import datetime
from client import client
from app_logging import logger



def get_default_json():

    current_date = datetime.now().strftime("%d-%m-%Y")

    return {
        "docType": "null",
        "docName": "null",
        "DocNumber": "null",
        "uploadedDate": current_date,
        "issuedCountry": "null",
        "IssuedPlace": "null",
        "issueDate": "null",
        "expDate": "null",
        "isNationalDoc": "null"
    }   


def extract_json(images_b64):
    
    current_date = datetime.now().strftime("%d-%m-%Y")
    
    prompt_text = f"""You are an expert in document data extraction. Extract and translate into English only the following details in the following JSON format:

    JSON Format:
    {{
    "docType": "Travel ID" | "License" | "Training" | "Medical",
    "docName": "...",              
    "DocNumber": "...",           
    "uploadedDate": "{current_date}",
    "issuedCountry": "...",  
    "IssuedPlace": "...",   
    "issueDate": "dd-mm-yyyy",     
    "expDate": "dd-mm-yyyy",       
    "isNationalDoc": "Yes" or "No"   
    }}

    
    ### Instructions:
    1. **For Visa documents** (i.e., if `docName` is "Visa" or contains the word "Visa"):
    - Extract only the **Visa Control Number** or **Visa Grant Number** as the `DocNumber`.
    - **Strictly ignore the Passport Number**, even if it appears on the same page.
    - The `DocNumber` must never be set to a **Passport Number** in Visa documents under any condition.
    - If **both numbers are found**, always choose the **Visa-specific number**, and discard the Passport Number.

    ### Special Rules for IssuedPlace:
    - **IssuedPlace** refers to the place of issue (city, port, or institution).
    - Do not use **place of birth, residence, or home city** as `IssuedPlace`.
    - **Never set `IssuedPlace` to `"null"`** if the country is known; use the country as a fallback if `IssuedPlace` is missing.
    - Set `IssuedPlace` to `"null"` only if both the place and country are missing or invalid.
    - **This rule applies to all documents**. Even if `IssuedPlace` is missing in any document, it must always fallback to the `IssuedCountry` if the country is available. Do **not apply this logic to just the first document**, but **ensure it is applied consistently to all documents in the list**.


    ### Special Rules for DocNumber:
    - **"DocNumber"**: Select the most relevant number based on priority:
    1. **For Visa documents** (if `docName` is "Visa" or contains the word "Visa"): 
        - Extract the **Visa Control Number** and use it as the `DocNumber`.
        - **Do not** extract the **Passport Number** for Visa documents, even if both numbers are present.
    2. **For Passport documents**: 
        - Extract the **Passport Number** and use it as the `DocNumber`.
    3. **Seaman's Book No.**.
    4. **Certificate No.** / **Doc Number**.
    5. **Strictly ignore any numbers without an explicit label indicating a document number** (e.g., "Passport Number", "Seaman's Book No.", "Certificate No.", "Doc Number", "Visa Control Number", "Visa Grant Number"). This includes numbers found in fields like "Application ID", "Serial No", "Control Number" or any unlabelled number. If no valid DocNumber with an explicit label is found, set "DocNumber" to "null".
    6.For e-Business Visa use Applictaion id as DocNumber.
    
    ### Special Rules for docName:
    - "docName" must exactly match an explicitly written title, heading, or labeled phrase in the document image.
    - If no clear document title or name appears in the image, set "docName" = "null".
    - Never infer, guess, or assume a document name based on surrounding words.
    - Do not use partial or prefix words such as "Certificate", "Form", "Document","Type" or "Application" alone as the document name 
      if they are followed by terms like "Number", "Type", "Date", "Name", etc.
    - Example: If the text says "Certificate Number" or "Certificate Type" without an actual title, treat "Certificate" as a field label, not a title → set "docName": "null".
    - If "docName" contains the word "Visa", analyze the type (e.g., "Business Visa", "Seaman Visa", "Employment Visa") if available.
    - **Do not use** generic field headers or control labels like "Serial No", "SL No", "Control Number", "ID No", "Form No", or "Reference No" as document names.
    - **Do not just provide the docName as “Certificate”, “Certificate of Competency”, “Certificate of Completion”, or “Certificate of Proficiency”. The docName must clearly specify the subject or area it refers to — for example, “Certificate of Proficiency in Survival Craft”, “Certificate of Completion in Advanced Fire Fighting”, or “Certificate of Competency in Navigation”.**

    #### Additional Combination Rules:
    - **For "Certificate of Competency" and "Certificate of Receipt of Application" documents:**
        - If a **Function** is mentioned in the document, append it to the document name along with the **Level** (e.g., "Management Level", "Operational Level") and **Limitation** (e.g., "Oil Tanker", "Gas Carrier", "Near Coastal"), if available,
            in the following format:
            `"Certificate of Receipt of Application (<Function> - <Level> - <Limitation>)"`.
            `"Certificate of Competency (<Function> - <Level> - <Limitation>)"`.
        - If more than one **Function** is mentioned treat them as seperate entries with same document number.
        - Don't treat **capacity** as Document name.
        - If the function column contains any integers instead of the function name map it according to the below list:
            Function No.	Meaning	STCW Reference
            1	Navigation	STCW A-II/1, A-II/2
            2	Cargo Handling & Stowage	STCW A-II/1, A-II/2
            3	Ship Operation & Care for Persons	STCW A-II/1, A-II/2
            4	Marine Engineering	STCW A-III/1, A-III/2
            5	Electrical, Electronic & Control Engineering	STCW A-III/1, A-III/2
            6	Maintenance & Repair	STCW A-III/1, A-III/2
            7	Radio Communications (GMDSS)	STCW A-IV/2
            8	Controlling the Operation of the Ship and Care for Persons on Board
    
    - **For "Endorsement" documents:**
        - If a **Function** is mentioned in the document, append it to the document name along with the **Level** (e.g., "Management Level", "Operational Level") and **Limitation** (e.g., "Oil Tanker", "Gas Carrier", "Near Coastal"), if available, 
            in the following format:
            "Endorsement (<Function> - <Level> - <Limitation>)"
        - If more than one **Function** is mentioned treat them as seperate entries with same document number.
        - Don't treat **capacity** as Document name.
        - If the function column contains any integers instead of the function name map it according to the below list:
            Function No.	Meaning	STCW Reference
            1	Navigation	STCW A-II/1, A-II/2
            2	Cargo Handling & Stowage	STCW A-II/1, A-II/2
            3	Ship Operation & Care for Persons	STCW A-II/1, A-II/2
            4	Marine Engineering	STCW A-III/1, A-III/2
            5	Electrical, Electronic & Control Engineering	STCW A-III/1, A-III/2
            6	Maintenance & Repair	STCW A-III/1, A-III/2
            7	Radio Communications (GMDSS)	STCW A-IV/2
            8	Controlling the Operation of the Ship and Care for Persons on Board

    ### Special Rules for docType:
    - "docType" must be **one of the following values only**:
      1. "Travel ID" → for documents like **Passport**, **Visa**, **Seaman’s Book**, **CDC**.
      2. "License" → for documents like **Certificate of Competency**, **Endorsement**, **GMDSS Radio Operator**, etc.
      3. "Training" → for **training certificates**, **safety courses**, **refreshers**, or **simulator training**.
      4. "Medical" → for any **medical certificate** or **medical fitness** document.
    - Always infer "docType" based on the **document content** and **document name**.
    - If the document name does not clearly indicate a category, analyze the text for clues (e.g., words like “training”, “competency”, “medical”, “visa”, “passport”) and assign the most likely type.
    - "docType" must **never be "null"**. If unsure, choose the **closest matching type** from the list.

    ### Field Rules:
    1. **"docType"** – Must be **one of these values only**: "Travel ID", "License", "Training", or "Medical".
        - Infer from the **document content** and **document name**.
        - Never leave empty or use a value outside this list.
    2. **"docName"** – Name of the certificate, endorsement, or training.
    3. **"DocNumber"** – Use explicit labels like “Certificate No.”, “Doc Number”, “Passport Number” etc.
    4. **"uploadedDate"** – Use today’s date: **{current_date}**.
    5. **"issuedCountry"** – Country where the document was issued.
    6. **"IssuedPlace"** – City or port of issue. If only an institution name is listed (e.g., "Ministry of..."), set to **"null"**.
    7. **"issueDate"** and **"expDate"** – Format as **dd-mm-yyyy**.
    8. **"isNationalDoc"** – 
        - Set to **"Yes"** only if the document is a **Passport** (i.e., `"docName"` is `"Passport"`).
        - For **all other documents**, set it to **"No"**.
    9. Use **"null"** for any missing fields (like DocNumber, IssuedPlace, etc.).

    ### Extraction Guidelines:
    - Extract valid sections of the document:
    - Certificates, Endorsements, Health Certificates, Training Courses, Seaman’s Book, Passport.
    - Only extract sections with valid **document numbers** and clear details.
    - If multiple numbers or expiry dates exist, return them as separate objects.
    - Ignore irrelevant sections like revalidations, administrative stamps, or incomplete details.
    - If no valid information is found, return `null`.
    - Extract all valid certificates and courses, no prioritization.
    - **Translate content into English** where needed.
    
    ### **Critical Validation Rule:**
    - Each document object must be returned **unless both** `"docName"` and `"DocNumber"` are missing, invalid, or `"null"`.
    - Never invent or assume document names, if not explicitly written in the image.
    - If **both** `"docName"` and `"DocNumber"` are missing, return exactly **one default JSON object** as follows:

    {{
      "docType": "null",
      "docName": "null",
      "DocNumber": "null",
      "uploadedDate": "{current_date}",
      "issuedCountry": "null",
      "IssuedPlace": "null",
      "issueDate": "null",
      "expDate": "null",
      "isNationalDoc": "null"
    }}

    - This rule applies globally to all extracted documents.
    
    ### Special Case: Course Lists or Tables
    - If training courses are listed in tables, extract each row as a separate object.
    - Set `"DocNumber"`, `"issueDate"`, `"expDate"`, `"IssuedPlace"` to `"null"` if not available.
    - Do not skip course entries even if embedded in other sections.

    ### Output Format:
    - Return a flat JSON array with no markdown, code blocks, or extra commentary.
    - Each object must include all fields listed in the JSON format.
    - Ensure the output is valid JSON.

    ### Examples:
    - Certificate of Competency (Master)
    - Endorsement (GMDSS Radio Operator)
    - Seafarer's Medical Certificate
    - Seaman’s Book
    - Passport
    - Familiarization and Basic Safety Training
    - Advanced Fire Fighting
    - Medical First Aid
    - ARPA
    - Radar Simulator
    - Security Awareness Training
    
    ### Special strict rule:
    - Respond only with the below message, if you can't extract the content from the image.
      -**not able to extract**.
    
    """

    prompt = [
        {
            "type": "text",
            "text": prompt_text
        },
        *[
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{img}"
                }
            } for img in images_b64
        ]
    ]
    
    
    

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}]
    )
    

    
    content = response.choices[0].message.content.strip()
    
    
    
    if "not able to extract" in content.lower():
        logger.error("Model not able to extract the content from the document")
        return get_default_json()

    if content.startswith("```json"):
        content = content.replace("```json", "").replace("```", "").strip()


    
    return content





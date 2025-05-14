import os
from openai import OpenAI
from dotenv import load_dotenv
import mimetypes

# Load environment variables
load_dotenv()

# Retrieve the API key from the .env file
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)


def process_image(image_url: str, name: str) -> str:
    """
    Extract personal/account info from the image via OpenAI using a URL.
    Returns the raw assistant response.
    """
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": f"""You are a high-precision OCR assistant. An image of a legal or business document follows. Please perform the following steps exactly:

                            1. Validate each uploaded document if matches {name} category
                            - Determine whether the document is acceptable for visa processing.
                            - In the output, list each file as an object with:
                                - `"isValid"`: `true` if the document meets requirements, otherwise `false`.

                            2. Extract applicant’s personal data  
                            From the collection of provided files, pull exactly these fields (no extras):

                            - `firstName` (string)  
                            - `middleName` (string)  
                            - `lastName` (string)  
                            - `dobDay` (string, 1–31)  
                            - `dobMonth` (string, 1–12)  
                            - `dobYear` (string, four digits)  
                            - `visaDetails` (string) 
                     
                            3. Produce a single JSON response
                            - Top-level object with two keys: `"files"` and `"fields"`.
                            - `"files"`: an array of file-status objects as above.
                            - `"fields"`: an object mapping each personal-data key to its extracted value.
                            - Do **not** include any other fields or metadata.

                            4. Formatting Rules
                            - Always output valid, parseable JSON.
                            - Use double quotes around keys and string values.
                            - Do not pretty-print (no extra newlines or comments).

                            #### Example Output

                            ```
                            {
                            "files": [
                                { "isValid": true }
                            ],
                            "fields": {
                                "firstName":  "John",
                                "middleName": "Doe",
                                "lastName":   "Doe",
                                "dobDay":     "23",
                                "dobMonth":   "9",
                                "dobYear":    "1986"
                            }
                            }
                            ```
                    """},
                    {
                        "type": "input_image",
                        "image_url": image_url,
                    },
                ],
            }
        ],
    )

    # Return the result
    return response.choices[0].message.content




def process_pdf(file_path: str, name: str) -> str:
    """
    Process a PDF file via OpenAI.
    Uploads the PDF file and queries it for specific information.
    """
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type != "application/pdf":
        raise ValueError("The provided file is not a PDF.")

    try:
        # Upload the PDF file to OpenAI
        file = client.files.create(
            file=open(file_path, "rb"),
            purpose="user_data"
        )

        # Query the uploaded PDF file
        response = client.responses.create(
            model="gpt-4.1",
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_file",
                            "file_id": file.id,
                        },
                        {
                            "type": "input_text",
                            "text": f"""You are a high-precision attorney assistant. A file of a legal or business document follows. Please perform the following steps exactly:

                            1. Validate each uploaded document if matches {name} category
                            - Determine whether the document is acceptable for visa processing.
                            - In the output, list each file as an object with:
                                - `"isValid"`: `true` if the document meets requirements, otherwise `false`.

                            2. Extract applicant’s personal data  
                            From the collection of provided files, pull exactly these fields (no extras):

                            - `firstName` (string)  
                            - `middleName` (string)  
                            - `lastName` (string)  
                            - `dobDay` (string, 1–31)  
                            - `dobMonth` (string, 1–12)  
                            - `dobYear` (string, four digits)  
                            - `visaDetails` (string) 
                     
                            3. Produce a single JSON response
                            - Top-level object with two keys: `"files"` and `"fields"`.
                            - `"files"`: an array of file-status objects as above.
                            - `"fields"`: an object mapping each personal-data key to its extracted value.
                            - Do **not** include any other fields or metadata.

                            4. Formatting Rules
                            - Always output valid, parseable JSON.
                            - Use double quotes around keys and string values.
                            - Do not pretty-print (no extra newlines or comments).

                            #### Example Output

                            ```
                            {
                            "files": [
                                { "isValid": true }
                            ],
                            "fields": {
                                "firstName":  "John",
                                "middleName": "Doe",
                                "lastName":   "Doe",
                                "dobDay":     "23",
                                "dobMonth":   "9",
                                "dobYear":    "1986"
                            }
                            }
                            ```
                            """,
                    },
                    ]
                }
            ],
        )

        # Return the result
        return response.choices[0].message.content

    except Exception as e:
        raise RuntimeError(f"Error processing PDF file: {str(e)}")



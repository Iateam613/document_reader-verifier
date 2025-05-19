import os
from openai import OpenAI
from dotenv import load_dotenv
import base64

# Load environment variables
load_dotenv()

# Retrieve the API key from the .env file
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)


def encode_image(image_path: str) -> str:
    """
    Encodes an image file in Base64 format.
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def process_image(image_path: str, name: str) -> str:
    """
    Processes an image file via OpenAI.
    Encodes the image in Base64 and queries it for specific information.
    """
    try:
        # Encode the image in Base64
        base64_image = encode_image(image_path)

        # Query the OpenAI API with the encoded image
        response = client.responses.create(
            model="gpt-4.1",
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": f"""You are a high-precision assistant and an OCR that need to get data from the provided image. An image of a legal or business document follows. Please perform the following steps exactly:

                            1. Validate the uploaded document if it matches the {name} category:
                            - Determine whether the document is acceptable for visa processing.
                            - In the output, list each file as an object with:
                                - `"isValid"`: `true` if the document meets requirements, otherwise `false`.

                            2. Extract applicant’s personal data:
                            - `firstName` (string)
                            - `middleName` (string)
                            - `lastName` (string)
                            - `dobDay` (string, 1–31)
                            - `dobMonth` (string, 1–12)
                            - `dobYear` (string, four digits)
                            - `visaDetails` (string)

                            3. Produce a single JSON response:
                            - Top-level object with two keys: `"files"` and `"fields"`.
                            - `"files"`: an just a string like in the example bellow of file-status objects as above.
                            - `"fields"`: an object mapping each personal-data key to its extracted value.
                            - Do **not** include any other fields or metadata.

                            4. Formatting Rules:
                            - Always output valid, parseable JSON.
                            - Use double quotes around keys and string values.
                            - Do not pretty-print (no extra newlines or comments).
                            """
                            """
                            #### NOTE Must follow Example Output:
                            ```
                            {
                            "isValid": true,
                            "fields": {
                                "firstName": "HAPPY",
                                "middleName": "",
                                "lastName": "TRAVELER",
                                "dobDay": "1",
                                "dobMonth": "1",
                                "dobYear": "1981"
                            }
                            }
                            ```
                            """,
                        },
                        {
                            "type": "input_image",
                            "image_url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    ],
                }
            ],
        )

        # Return the result
        return response.output_text

    except Exception as e:
        raise RuntimeError(f"Error processing image file: {str(e)}")



def process_pdf(temp_file_path: str, name: str) -> str:
    """
    Process a PDF file via OpenAI.
    Uploads the PDF file and queries it for specific information.
    """
    try:
        print(f"Processing PDF file: {temp_file_path}")
        print(name)
        # Read the PDF file and encode it in base64
        with open(temp_file_path, "rb") as f:
            data = f.read()

        base64_string = base64.b64encode(data).decode("utf-8")
        #print(base64_string)

        # Query the uploaded PDF file
        response = client.responses.create(
            model="gpt-4.1",
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_file",
                            "filename": "temp_file.pdf",
                            "file_data": f"data:application/pdf;base64,{base64_string}",
                        },
                        {
                            "type": "input_text",
                            "text": f"""You are a high-precision attorney assistant. A file of a legal or business document follows. Please perform the following steps exactly:

                            1. Validate each uploaded document if it matches the {name} category:
                            - Determine whether the document is acceptable for visa processing.
                            - In the output, list each file as an object with:
                                - `"isValid"`: `true` if the document meets requirements, otherwise `false`.

                            2. Extract applicant’s personal data:
                            - `firstName` (string)
                            - `middleName` (string)
                            - `lastName` (string)
                            - `dobDay` (string, 1–31)
                            - `dobMonth` (string, 1–12)
                            - `dobYear` (string, four digits)
                            - `visaDetails` (string)

                            3. Produce a single JSON response:
                            - Top-level object with two keys: `"files"` and `"fields"`.
                            - `"files"`: an just a string like in the example bellow of file-status objects as above.
                            - `"fields"`: an object mapping each personal-data key to its extracted value.
                            - Do **not** include any other fields or metadata.

                            4. Formatting Rules:
                            - Always output valid, parseable JSON.
                            - Use double quotes around keys and string values.
                            - Do not pretty-print (no extra newlines or comments).
                            """
                            
                            """
                        
                            #### NOTE Must follow Example Output:
                            ```
                            {
                            "isValid": true,
                            "fields": {
                                "firstName": "HAPPY",
                                "middleName": "",
                                "lastName": "TRAVELER",
                                "dobDay": "1",
                                "dobMonth": "1",
                                "dobYear": "1981"
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
        return response.output_text

    except Exception as e:
        raise RuntimeError(f"Error processing PDF file: {str(e)}")



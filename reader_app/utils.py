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


def image_process_details(image_url: str) -> str:
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
                    {"type": "input_text", "text": """You are a high-precision OCR assistant. An image of a legal or business document follows. Please perform the following steps exactly:
                        1. Field Detection
                            Identify every distinct text field or label in the image (e.g., “Address,” “Date,” “Name,” etc.), even if you haven’t seen that specific document type before.
                        2. Verbatim Extraction
                            For each detected label, extract its value verbatim, preserving every character exactly as it appears, including:
                                Alphabetical letters that appear before or after numbers (e.g., “A1234” → “A1234”)
                                Punctuation, symbols, and whitespace
                                Case sensitivity (upper/lower-case)
                        3. Formatting
                            Output plain text, one line per field, in the form:
                            <Label>: <Value>
                        4. Normalization
                            Dates → convert to YYYY-MM-DD (but do not alter any surrounding letters if part of the field).
                        5. Missing Fields
                            If a detected label has no value, skip that field entirely.
                        6. No Extra Text
                            Do not include any commentary, summaries, or explanations—only the extracted fields in the specified format.
                        7. Double-Check
                            Before returning, verify that no character has been dropped or altered.
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


def image_verification(image_url: str) -> str:
    """
    Verify the document’s authenticity via OpenAI using a URL.
    Returns a brief description of the file.
    """
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Tell me what kind of file I have provided in 20 words max."},
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


def process_pdf(file_path: str, query: str) -> str:
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
                            "text": """You are a high-precision OCR assistant. An image of a legal or business document follows. Please perform the following steps exactly:
                                    1. Field Detection
                                        Identify every distinct text field or label in the image (e.g., “Address,” “Date,” “Name,” etc.), even if you haven’t seen that specific document type before.
                                    2. Verbatim Extraction
                                        For each detected label, extract its value verbatim, preserving every character exactly as it appears, including:
                                            Alphabetical letters that appear before or after numbers (e.g., “A1234” → “A1234”)
                                            Punctuation, symbols, and whitespace
                                            Case sensitivity (upper/lower-case)
                                    3. Formatting
                                        Output plain text, one line per field, in the form:
                                        <Label>: <Value>
                                    4. Normalization
                                        Dates → convert to YYYY-MM-DD (but do not alter any surrounding letters if part of the field).
                                    5. Missing Fields
                                        If a detected label has no value, skip that field entirely.
                                    6. No Extra Text
                                        Do not include any commentary, summaries, or explanations—only the extracted fields in the specified format.
                                    7. Double-Check
                                        Before returning, verify that no character has been dropped or altered.
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


def verify_pdf(file_path: str) -> str:
    """
    Verify the authenticity of a PDF file via OpenAI.
    Uploads the PDF file and queries it for verification.
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

        # Query the uploaded PDF file for verification
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
                            "text": "Tell me what kind of file I have provided in 20 words max.",
                        },
                    ]
                }
            ],
        )

        # Return the result
        return response.choices[0].message.content

    except Exception as e:
        raise RuntimeError(f"Error verifying PDF file: {str(e)}")



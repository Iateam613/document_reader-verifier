import os
import base64
import mimetypes
from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()

# Retrieve the API key from the .env file
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

def encode_image_to_base64(path: str) -> str:
    """Read a file and return its base64-encoded string."""
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

def process_details(image_path: str) -> str:
    """
    Extract personal/account info from the image via OpenAI.
    Returns the raw assistant response.
    """
    mime_type, _ = mimetypes.guess_type(image_path)
    b64 = encode_image_to_base64(image_path)

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "user",
                "content": [
                                        { "type": "text", "text": """You are a high-precision OCR assistant. An image of a legal or business document follows. Please perform the following steps exactly:
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
                    """ },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{b64}",
                        },
                    },
                ],
            }
        ],
    )

    # Return the result
    return response.choices[0].message.content

def get_verification(image_path: str) -> str:
    """
    Verify the document’s authenticity via OpenAI.
    Returns a brief description of the file.
    """
    mime_type, _ = mimetypes.guess_type(image_path)
    b64 = encode_image_to_base64(image_path)

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "user",
                "content": [
                    { "type": "text", "text": "Tell me what kind of file I have provided in 20 words max" },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{b64}",
                        },
                    },
                ],
            }
        ],
    )

    # Return the result
    return response.choices[0].message.content


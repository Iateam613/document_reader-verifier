import os
import base64
import mimetypes
from dotenv import load_dotenv
from openai import OpenAI
#from asgiref.sync import sync_to_async

load_dotenv()

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def encode_image_to_base64(path: str) -> str:
    """Read a file and return its base64-encoded string."""
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

def process_details(image_path: str) -> str:
    """Extract personal/account info from the image via OpenAI."""
    mime_type, _ = mimetypes.guess_type(image_path)
    b64 = encode_image_to_base64(image_path)

    resp = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": {"type": "text", "text": "List all the personal information , account information from the image provided no summary and additional text"},
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{mime_type};base64,{b64}"}
                    },
                ],
            }
        ],
    )

    return resp.choices[0].message.content

def get_verification(image_path: str) -> str:
    """Verify the document’s authenticity via OpenAI."""
    mime_type, _ = mimetypes.guess_type(image_path)
    b64 = encode_image_to_base64(image_path)

    resp = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Tell me what kind of file I have provided in 20 words max."},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{mime_type};base64,{b64}"}
                    },
                ],
            }
        ],
    )

    return resp.choices[0].message.content


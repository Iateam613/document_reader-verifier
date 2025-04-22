import os
import base64
import mimetypes
from dotenv import load_dotenv
from openai import OpenAI

def process_image(image_path):
    # Load environment variables from .env file
    load_dotenv()

    # Retrieve the API key from the .env file
    api_key = os.getenv("OPENAI_API_KEY")

    # Initialize the OpenAI client
    client = OpenAI(api_key=api_key)

    # Function to encode the image
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    # Determine the MIME type of the image
    mime_type, _ = mimetypes.guess_type(image_path)

    # Getting the Base64 string
    base64_image = encode_image(image_path)

    # Call the OpenAI API
    completion = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "user",
                "content": [
                    { "type": "text", "text": "Tell me what kind of file I have provided in 20 words max" },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{base64_image}",
                        },
                    },
                ],
            }
        ],
    )

    # Return the result
    return completion.choices[0].message.content

# Example usage
if __name__ == "__main__":
    image_path = r"C:\Users\USER\OneDrive\Documents\projects\Document-reader\sample-file\Resume1.png"
    verification = process_image(image_path)
    print(verification)
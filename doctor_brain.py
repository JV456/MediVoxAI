import base64
import os

from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Debug: Print loaded API key
print("Loaded API Key:", os.getenv("GROQ_API_KEY"))

# Initialize Groq client with API key
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Read and encode image
image_path = "images/acne.jpg"
try:
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
except FileNotFoundError:
    print(f"Error: Image file not found at {image_path}")
    exit(1)

# Prepare the message with image and query
query = "Is there something wrong with my face?"
model = "meta-llama/llama-4-scout-17b-16e-instruct"

messages = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": query},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{encoded_image}",
                },
            },
        ],
    }
]

try:
    # Make the API call
    chat_completion = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    print(chat_completion.choices[0].message.content)
except Exception as e:
    print(f"Error making API call: {e}")
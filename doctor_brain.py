import base64
import os

from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Read and encode image
# image_path = "images/acne.jpg"
def encode_image(image_path):
    image_file=open(image_path, "rb")
    return base64.b64encode(image_file.read()).decode("utf-8")
    
    
query = "Is there something wrong with my face?"
model = "meta-llama/llama-4-scout-17b-16e-instruct"

def analyze_image_with_query(query,model,encoded_image):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
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
        chat_completion = client.chat.completions.create(
            model=model,
            messages=messages,
        )
        return (chat_completion.choices[0].message.content)
    except Exception as e:
        print(f"Error making API call: {e}")
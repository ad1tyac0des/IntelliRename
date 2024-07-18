import os
from dotenv import load_dotenv
import requests
import base64
import json
from colorama import init, Fore

#Load Environment variables from .env
load_dotenv()
API_KEY = os.getenv('NVIDIA_API_KEY') # Get API key from environment variable

# Initialize colorama
init(autoreset=True)

def generate_image_name(image_path):
    invoke_url = "https://ai.api.nvidia.com/v1/vlm/microsoft/phi-3-vision-128k-instruct"
    
    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode()

    assert len(image_b64) < 180_0000, \
        "To upload larger images, use the assets API (see docs)"

    headers = {
        "Authorization": f"Bearer {API_KEY}", #Use API Key from environment variable
        "Accept": "application/json"
    }

    payload = {
        "messages": [
            {
                "role": "user",
                "content": f'''Analyze the image and generate a THREE-WORD name for it. Follow these rules strictly:
1. The name MUST contain EXACTLY three words.
2. Include the COLOR of the main object.
3. Include the TYPE or CATEGORY of the main object.
4. If needed, add a descriptive word to reach three words.
5. Format: [Color] [Descriptor/Type] [Object]
6. Examples: "Red Sporty Car", "Blue Floral Dress", "Green Leafy Plant"
7. Do NOT use punctuation or write sentences.
8. Respond ONLY with the three-word name.

Image: <img src="data:image/jpg;base64,{image_b64}" />'''
            }
        ],
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 1.0,
        "stream": False
    }

    def get_name():
        response = requests.post(invoke_url, headers=headers, json=payload)
        response_json = response.json()
        main_output = response_json['choices'][0]['message']['content']
        return main_output.strip()

    while True:
        name = get_name()
        words = name.split()
        
        if len(words) == 3:
            return name
        else:
            print(f"{Fore.LIGHTRED_EX}   Invalid name: {name}")
            print(f"{Fore.YELLOW}   Retrying...")

if __name__ == "__main__":
    # This block is for testing the module directly
    test_image_path = "Folder\\file.jpg"
    result = generate_image_name(test_image_path)
    print("Generated name:", result)
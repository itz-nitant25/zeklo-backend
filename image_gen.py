import os
import requests

IMAGE_API_KEY = os.getenv("IMAGE_API_KEY")
IMAGE_API_URL = "https://api.your-image-provider.com/generate"

def generate_image(prompt: str) -> str | None:
    headers = {
        "Authorization": f"Bearer {IMAGE_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": prompt,
        "size": "1024x1024"
    }

    res = requests.post(IMAGE_API_URL, json=payload, headers=headers, timeout=30)

    if res.status_code != 200:
        return None

    data = res.json()
    return data.get("image_url")

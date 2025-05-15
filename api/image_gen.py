from openai import OpenAI
import base64
from uuid import uuid4
import os
from django.conf import settings

client = OpenAI(api_key=settings.OPENAI_SECRET)


def generate_image(prompt: str) -> str:
    """Generate image using OpenAI API and return URL"""

    coin_prompt = f"{prompt}"

    result = client.images.generate(
        model="dall-e-3",
        prompt=coin_prompt,
        size="1024x1024",
        n=1,
        response_format="b64_json"
    )

    image_b64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_b64)

    # os.makedirs("static", exist_ok=True)

    image_name = f"{uuid4()}.png"
    path = f"static/{image_name}"

    with open(path, "wb") as f:
        f.write(image_bytes)

    return path
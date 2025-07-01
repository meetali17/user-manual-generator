import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("TOGETHER_API_KEY")

# Choose a model available on Together (e.g., mistralai/Mixtral-8x7B-Instruct-v0.1)
model = "mistralai/Mixtral-8x7B-Instruct-v0.1"

def generate_manual(prompt: str):
    try:
        response = requests.post(
            "https://api.together.xyz/v1/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "prompt": prompt,
                "max_tokens": 1024,
                "temperature": 0.7,
                "top_p": 0.9,
                "stop": ["</s>"]
            }
        )

        response.raise_for_status()
        result = response.json()

        # New parsing logic
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["text"].strip()
        else:
            return "❌ Error: No output text returned."

    except Exception as e:
        return f"❌ Error: {str(e)}"


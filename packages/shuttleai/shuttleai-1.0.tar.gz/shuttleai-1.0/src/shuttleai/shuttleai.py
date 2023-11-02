"""
@Author: shuttle
@Version: 0.01
@Date: 11-1-2023
"""
import httpx
from terminut import log

class ShuttleClient:
    def __init__(self, api_key):
        self.api_key = api_key 
        self.base_url = "https://api.shuttle.rip/v1"
    
    @property
    def models(self):
        try:
            url = f"{self.base_url}/models"
            response = httpx.get(url, timeout=10)
            return response.json()
        except Exception as e:
            log.error(f"[ShuttleAI] Error: {e}")

    def chat_completion(self, model, messages, stream=False, plain=False):
     try:
        url = f"{self.base_url}/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}"}

        if plain: # If plain_message is True, convert the plain message to the structured format
            messages = [{"role": "system", "content": messages}]

        data = {
            "model": model,
            "messages": messages,
            "stream": stream
        }
        response = httpx.post(url, json=data, headers=headers, timeout=60)
        return response.json()
     except Exception as e:
         log.error(f"[ShuttleAI] Error: {e}")

    def images_generations(self, model, prompt, n=1):
        try:
            url = f"{self.base_url}/v1/images/generations"
            headers = {"Authorization": f"Bearer {self.api_key}"}
            data = {
                "model": model,
                "prompt": prompt,
                "n": n
            }
            response = httpx.post(url, json=data, headers=headers)
            return response.json()
        except Exception as e:
            log.error(f"[ShuttleAI] Error: {e}")
import requests
import json
import base64
import trimesh
from io import BytesIO

class LLMClient:
    def __init__(self, api_key: str, base_url: str = "https://api.openai.com"):
        self.api_key = api_key
        self.base_url = base_url

    def query_llm(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-Title": "LLM3DPrint"
        }
        payload = {
            "model": "openai/shap-e",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a 3D printing expert. generate a stl file for a 3D model. and give me the download link."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        json_payload = json.dumps(payload)

        try:
            response = requests.post(
                f"{self.base_url}/v1/chat/completions",
                headers=headers,
                data=json_payload
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return ""

        if response.status_code != 200:
            print(f"Unexpected status code: {response.status_code}")
            print(f"Response content: {response.text}")
            return ""

        try:
            data = response.json()
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            print(f"Response content: {response.text}")
            return ""

        return {
            "message": data["choices"][0]["text"],
            "model": data["choices"][0]["model"]
        }
    
    def generate_object_llm(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-Title": "LLM3DPrint"
        }

        payload = {
            "prompt": prompt,
            "numInferenceSteps": 48
        }

        json_payload = json.dumps(payload)

        try:
            response = requests.post(
                f"{self.base_url}/api/v1/objects/generations",
                headers=headers,
                data=json_payload
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return ""
        
        if response.status_code != 200:
            print(f"Unexpected status code: {response.status_code}")
            print(f"Response content: {response.text}")
            return ""

        try:
            data = response.json()
            output = data["generations"]
            data_uri = output[0]["uri"]
            ply_data = base64.b64decode(data_uri.split(",")[1])
            mesh = trimesh.load(BytesIO(ply_data), file_type="ply")
            
            stl_data = mesh.export(file_type="stl")
            file_name = ""
            with open("output.stl", "wb") as f:
                f.write(stl_data)
                file_name = f.name

            return {
                "message": "File generated successfully",
                "file_name": file_name
            }
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            print(f"Response content: {response.text}")
            return ""

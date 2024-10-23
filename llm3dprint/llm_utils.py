import httpx
import json
import base64
import trimesh
from io import BytesIO
import os

class LLMClient:
    def __init__(self, api_key: str, base_url: str = "https://api.openai.com"):
        self.api_key = api_key
        self.base_url = base_url
        self.open_router_model = "openai/gpt-4o-mini"
        self.timeout = httpx.Timeout(60.0)  # Long timeout of 60 seconds
    
    def set_api_key(self, api_key: str):
        self.api_key = api_key
    
    def set_base_url(self, base_url: str):
        self.base_url = base_url
    
    def set_open_router_model(self, model: str):
        self.open_router_model = model

    def generate_object_openscad_based(self, messages: list) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-Title": "LLM3DPrint"
        }
        payload = {
            "model": self.open_router_model,
            "messages": messages,
        }

        print(f"Sending request: {payload}")

        try:
            response = httpx.post(
                f"{self.base_url}/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
        except httpx.RequestError as e:
            print(f"Request failed: {e}")
            return {
                "message": "Error generating Openscad code"
            }

        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e}")
            print(f"Response content: {response.text}")
            return {
                "message": "Error generating Openscad code"
            }

        try:
            data = response.json()
            print(response.text)
            print("Response data: ", data)
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            print(f"Response content: {response.text}")
            return {
                "message": "Error generating Openscad code"
            }

        openscad_code = data["choices"][0]["message"]["content"]
        new_histoy_message = data["choices"][0]["message"]
        # takeout ```openscad from the code
        openscad_code = openscad_code.replace("```openscad", "")
        openscad_code = openscad_code.replace("```", "")
        with open("temp_scad_file.scad", "w") as f:
            f.write(openscad_code)
        # generate stl file
        os.system(f"openscad -o openscad_model.stl temp_scad_file.scad")
        
        return {
            "openscad_code": openscad_code,
            "message": f"Openscad code generated successfully\n{openscad_code}",
            "new_histoy_message": new_histoy_message,
            "file_name": "openscad_model.stl"
        }
    
    def generate_object_stl_content_based(self, messages: list) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-Title": "LLM3DPrint"
        }
        payload = {
            "model": self.open_router_model,
            "messages": messages,
        }

        try:
            response = httpx.post(
                f"{self.base_url}/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
        except httpx.RequestError as e:
            print(f"Request failed: {e}")
            return {
                "message": "Error generating STL content"
            }

        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e}")
            print(f"Response content: {response.text}")
            return {
                "message": "Error generating STL content"
            }

        try:
            data = response.json()
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            print(f"Response content: {response.text}")
            return {
                "message": "Error generating STL content"
            }
        stl_content = data["choices"][0]["message"]["content"]
       
        new_histoy_message = data["choices"][0]["message"]
        with open("stl_model_output.stl", "w") as f:
            f.write(stl_content)
        return {
            "stl_content": stl_content,
            "message": f"STL content generated successfully\n{stl_content}",
            "file_name": "stl_model_output.stl",
            "new_histoy_message": new_histoy_message
        }
    
    def generate_object_llm_shape(self, prompt: str) -> dict:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-Title": "LLM3DPrint"
        }

        payload = {
            "prompt": prompt,
            "numInferenceSteps": 48
        }

        try:
            response = httpx.post(
                f"{self.base_url}/api/v1/objects/generations",
                headers=headers,
                json=payload,
                timeout=10000
            )
            response.raise_for_status()
        except httpx.RequestError as e:
            print(f"Request failed: {e}")
            print(f"Response content: {response.text}")
            return {
                "message": "Error generating file"
            }
        
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e}")
            print(f"Response content: {response.text}")
            return {
                "message": "Error generating file"
            }

        try:
            data = response.json()
            output = data["generations"]
            data_uri = output[0]["uri"]
            ply_data = base64.b64decode(data_uri.split(",")[1])
            mesh = trimesh.load(BytesIO(ply_data), file_type="ply")
            
            stl_data = mesh.export(file_type="stl")
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
            return {
                "message": "Error generating file"
            }

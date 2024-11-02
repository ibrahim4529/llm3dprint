from llm3dprint.app_setting import get_setting
import httpx
import json
import base64
import trimesh
from io import BytesIO
import os


class BaseLLMClient:
    """Base class for LLM clients
    This class will be inherited by the OLLAMAClient and OpenRouterClient
    """

    def __init__(self):
        self.timeout = httpx.Timeout(60.0)
        self.setting = get_setting()
        self.headers = {}

    def generate_object_openscad_based(self, messages: list) -> dict:
        """Generate an openscad code based on the messages
        Arguments:
            messages {list} -- List of messages following the conversation template
        Returns:
            dict -- A dictionary containing the openscad code, message and file name
        """
        pass

    def generate_object_stl_content_based(self, messages: list) -> dict:
        """Generate an STL content based on the messages
        Arguments:
            messages {list} -- List of messages following the conversation template
        Returns:
            dict -- A dictionary containing the stl content, message and file name
        """
        pass


class OLLAMAClient(BaseLLMClient):
    """Client for OLLAMA API
    This class will be used to interact with the OLLAMA API to generate
    openscad code and stl content based on the messages
    """

    def __init__(self):
        super().__init__()
        self.model = self.setting.get_value("ollama_model")
        self.base_url = f"{self.setting.get_value('ollama_api_url')}/api/chat"

    def generate_object_openscad_based(self, messages):
        headers = {
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False
        }
        try:
            response = httpx.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
        except httpx.RequestError or httpx.HTTPStatusError as e:
            print(f"Request error: {e}")
            return {
                "message": "Error generating openscad code based on the messages"
            }

        try:
            data = response.json()
            openscad_code = data["message"]["content"]
            new_histoy_message = data["message"]
            # clean the code in case it has ```openscad
            openscad_code = openscad_code.replace("```openscad", "")
            openscad_code = openscad_code.replace("```", "")

            with open("temp_scad_file.scad", "w") as f:
                f.write(openscad_code)
            # generate stl file
            os.system("openscad -o openscad_model.stl temp_scad_file.scad")

            return {
                "openscad_code": openscad_code,
                "message": f"Openscad code generated successfully\n{openscad_code}",
                "new_histoy_message": new_histoy_message,
                "file_name": "openscad_model.stl"
            }

        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return {
                "message": "Error generating openscad code based on the messages"
            }

    def generate_object_stl_content_based(self, messages: str) -> dict:
        headers = {
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False
        }

        try:
            response = httpx.post(
                self.base_url,
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
        except httpx.RequestError or httpx.HTTPStatusError as e:
            print(f"Request error: {e}")
            return {
                "message": "Error generating stl content based on the messages"
            }

        try:
            data = response.json()
            stl_content = data["message"]["content"]
            new_histoy_message = data["message"]

            with open("stl_model_output.stl", "w") as f:
                f.write(stl_content)

            return {
                "message": f"STL content generated successfully\n{stl_content}",
                "new_histoy_message": new_histoy_message,
                "file_name": "stl_model_output.stl"
            }
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return {
                "message": "Error generating stl content based on the messages"
            }


class OpenRouterClient(BaseLLMClient):
    """Client for OpenRouter API
    This class will be used to interact with the OpenRouter API to generate
    openscad code and stl content based on the messages. also generate 3d file based
    on openai shape-e model
    """

    def __init__(self):
        super().__init__()
        self.model = self.setting.get_value("openrouter_model")
        self.base_url = self.setting.get_value("llm_api_url")
        self.api_key = self.setting.get_value("llm_api_key")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-Title": "LLM3DPrint"
        }

    def generate_object_openscad_based(self, messages: list) -> dict:
        payload = {
            "model": self.model,
            "messages": messages
        }
        try:
            response = httpx.post(
                f"{self.base_url}/api/v1/chat/completions",
                headers=self.headers,
                json=payload,
            )
            response.raise_for_status()
        except httpx.RequestError as e:
            print(f"Request error: {e}")
            return {
                "message": "Failed to generating openscad code based on the messages"
            }
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e}")
            return {
                "message": "Failed to generating openscad code based on the messages"
            }

        try:
            data = response.json()
            openscad_code = data["choices"][0]["message"]["content"]
            new_histoy_message = data["choices"][0]["message"]
            # clean the code in case it has ```openscad
            openscad_code = openscad_code.replace("```openscad", "")
            openscad_code = openscad_code.replace("```", "")

            with open("temp_scad_file.scad", "w") as f:
                f.write(openscad_code)
            # generate stl file
            os.system("openscad -o openscad_model.stl temp_scad_file.scad")

            return {
                "openscad_code": openscad_code,
                "message": f"Openscad code generated successfully\n{openscad_code}",
                "new_histoy_message": new_histoy_message,
                "file_name": "openscad_model.stl"
            }
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return {
                "message": "Failed to generating openscad code based on the messages"
            }

    def generate_object_stl_content_based(self, messages):
        payload = {
            "model": self.model,
            "messages": messages,
        }

        try:
            response = httpx.post(
                f"{self.base_url}/api/v1/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
        except httpx.RequestError or httpx.HTTPStatusError as e:
            print(f"Request error: {e}")
            return {
                "message": "Failed to generating stl content based on the messages"
            }

        try:
            data = response.json()
            openscad_code = data["choices"][0]["message"]["content"]
            new_histoy_message = data["choices"][0]["message"]
            stl_content = data["choices"][0]["message"]["content"]

            new_histoy_message = data["choices"][0]["message"]
            with open("stl_model_output.stl", "w") as f:
                f.write(stl_content)

            return {
                "openscad_code": openscad_code,
                "message": f"Openscad code generated successfully\n{openscad_code}",
                "new_histoy_message": new_histoy_message,
                "file_name": "openscad_model.stl"
            }
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return {
                "message": "Failed to generating stl content based on the messages"
            }

    def generate_object_llm_shape_e_model(self, prompt):
        payload = {
            "prompt": prompt,
            "numInferenceSteps": 48
        }

        try:
            response = httpx.post(
                f"{self.base_url}/api/v1/objects/generations",
                headers=self.headers,
                json=payload,
                timeout=10000
            )
            response.raise_for_status()
        except httpx.RequestError or httpx.HTTPStatusError as e:
            print(f"Request error: {e}")
            return {
                "message": "Error generating file using shape-e model"
            }

        try:
            data = response.json()
            output = data["generations"]
            data_uri = output[0]["uri"]
            ply_data = base64.b64decode(data_uri.split(",")[1])
            mesh = trimesh.load(BytesIO(ply_data), file_type="ply")

            stl_data = mesh.export(file_type="stl")
            with open("shape_e_ouput.stl", "wb") as f:
                f.write(stl_data)
                file_name = f.name

            return {
                "message": "File generated successfully",
                "file_name": file_name
            }
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return {
                "message": "Error generating file using shape-e model"
            }

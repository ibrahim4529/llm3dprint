from PySide6.QtCore import QThread, Signal, Slot
from llm3dprint.llm_utils import LLMClient
from llm3dprint.app_setting import get_setting


class LLMThread(QThread):
    """Thread for running LLM API requests"""

    response_received = Signal(dict)
    is_loading = Signal(bool)
    hitory_openscad = [
        {
            "role": "system",
            "content": """You are machine to generate openscad code to create 3D object based on the prompt.
            return the openscad code without any other information. and make sure content is only cde qithout any prefix or suffix.
            """
        }
    ]
    hitory_stl = [
        {
            "role": "system",
            "content": """
            You are machine to generate stl file content to create 3D object based on the prompt.
            return the stl file content without any other information. and make sure content is only cde qithout any prefix or suffix.
            """
        }
    ]

    @Slot()
    def prompt_request(self, prompt: str, model: int):
        """Request LLM to generate a prompt"""
        self.model = model
        self.prompt = prompt
        self.start()

    def __init__(self, parent=None):
        super(LLMThread, self).__init__(parent)
        self.running = False
        self.finished.connect(self.stop)
        self.setting = get_setting()

    def run(self):
        api_key = self.setting.get_value("llm_api_key")
        base_url = self.setting.get_value("llm_api_url")
        self.llm_client = LLMClient(api_key, base_url)

        self.running = True
        while self.running:
            try:
                self.is_loading.emit(True)
                if self.model == 0:
                    response = self.llm_client.generate_object_llm_shape(
                        self.prompt)
                elif self.model == 1:
                    self.hitory_openscad.append({
                        "role": "user",
                        "content": self.prompt
                    })
                    response = self.llm_client.generate_object_openscad_based(
                        self.hitory_openscad)
                    # self.hitory_openscad.append(response)
                elif self.model == 2:
                    self.hitory_stl.append({
                        "role": "user",
                        "content": self.prompt
                    })
                    response = self.llm_client.generate_object_stl_content_based(
                        self.hitory_stl)
                    # self.hitory_stl.append(response)
                self.response_received.emit(response)
            except Exception as e:
                print(f"Error: {str(e)}")
                print(type(e))
                self.response_received.emit(f"Error: {str(e)}")
            finally:
                self.running = False
                self.is_loading.emit(False)

    def stop(self):
        self.running = False

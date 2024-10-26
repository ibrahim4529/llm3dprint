from PySide6.QtCore import QThread, Signal, Slot
from llm3dprint.llm_utils import OLLAMAClient, OpenRouterClient
from llm3dprint.app_setting import get_setting


class LLMThread(QThread):
    """Thread for running LLM API requests
    This approach is simpler than the one in llama_index_thread.py
    this class is just api call and emit signal to the main thread
    """

    response_received = Signal(dict)
    is_loading = Signal(bool)
    llm_client = None
    history_openscad = []
    hitory_stl = []
    

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
        self.reset_history()
    
    def init_llm_client(self):
        client_mapping = {
            0: OpenRouterClient,  # OpenRouter: Shap-e
            1: OpenRouterClient,  # OpenRouter (openscad)
            2: OpenRouterClient,  # OpenRouter (stl file content)
            3: OLLAMAClient,      # Ollama (openscad)
            4: OLLAMAClient       # Ollama (stl file content)
        }

        client_class = client_mapping.get(self.model)
        if client_class:
            self.llm_client = client_class()
        else:
            raise ValueError(f"Invalid model type: {self.model}")
        

    def run(self):
        self.init_llm_client()
        self.running = True
        print("running")
        while self.running:
            try:
                self.is_loading.emit(True)
                if self.model == 0 and isinstance (self.llm_client, OpenRouterClient): 
                    response = self.llm_client.generate_object_llm_shape_e_model(
                        self.prompt)
                elif self.model == 1 or self.model == 3 and self.llm_client is not None:
                    print(self.model)
                    print("Using openscad")
                    print(type(self.llm_client))
                    self.hitory_openscad.append({
                        "role": "user",
                        "content": self.prompt
                    })
                    response = self.llm_client.generate_object_openscad_based(
                        self.hitory_openscad)
                    print(response)
                    if response["new_histoy_message"]:
                        self.hitory_openscad.append(
                            response["new_histoy_message"])
                elif self.model == 2 or self.model == 4 and self.llm_client is not None:
                    self.hitory_stl.append({
                        "role": "user",
                        "content": self.prompt
                    })
                    response = self.llm_client.generate_object_stl_content_based(
                        self.hitory_stl)
                    if response["new_histoy_message"]:
                        self.hitory_stl.append(response["new_histoy_message"])
                self.response_received.emit(response)
            except Exception as e:
                self.response_received.emit(f"Error: {str(e)}")
            finally:
                self.running = False
                self.is_loading.emit(False)

    def stop(self):
        self.running = False

    def reset_history(self):
        self.hitory_openscad = [
            {
                "role": "system",
                "content": """You are ai agent help me to generate openscad code to create 3D object based on the prompt.
                return the openscad code without any other information, and make sure content is only code without any prefix or suffix.
                """
            }
        ]
        self.hitory_stl = [
            {
                "role": "system",
                "content": """
                You are ai agent help me to generate stl file content to create 3D object based on the prompt.
                return the stl file content without any other information, and make sure content is only code without any prefix or suffix.
                """
            }
        ]
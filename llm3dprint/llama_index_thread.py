from PySide6.QtCore import QThread, Signal, Slot
from llama_index.llms.openrouter import OpenRouter
from llama_index.core.llms import ChatMessage
from app_setting import get_setting
import os


class LlamaIndexThread(QThread):
    """Thread for running LLM API requests"""

    response_received = Signal(dict)
    setting = get_setting()
    is_loading = Signal(bool)
    messages: list[ChatMessage] = []
    

    @Slot()
    def prompt_request(self, prompt: str):
        """Start the thread with a prompt and model selected
        @TODO: implement RAG for the model to make better responses
        """
        self.prompt = prompt
        self.agent = OpenRouter(
            model=self.setting.get_value("openrouter_model"),
            api_key=self.setting.get_value("llm_api_key"),
            max_tokens=4096,
        )
        self.start()

    def __init__(self, parent=None):
        super(LlamaIndexThread, self).__init__(parent)
        self.running = False
        self.finished.connect(self.stop)
        self.reinit_message()

    def run(self):
        self.running = True
        new_prompt: ChatMessage = ChatMessage(
            role="user",
            content=self.prompt
        )
        self.messages.append(new_prompt)
        self.is_loading.emit(True)
        while self.running:
            try:
                response = self.agent.chat(self.messages)
                openscad_code = response.message.content
                # Clean mesup ```openscad code``` or any other information in the response.
                print("Response from LLM: ", response.message)
                openscad_code = openscad_code.replace("```openscad", "")
                openscad_code = openscad_code.replace("```", "")
                if openscad_code:
                    with open("temp_llama_index.scad", "w") as f:
                        f.write(openscad_code)
                    os.system("openscad temp_llama_index.scad -o temp_llama_index.stl")
                    self.response_received.emit({
                        "message": "3D Model Generate Successfully",
                        "file_name": "temp_llama_index.stl"
                    })
                self.messages.append(response.message)
            except Exception as e:
                print("Error Communicating with LLM ", e)
                self.response_received.emit({
                    "message": "Error Communicating with LLM ",
                })
            self.running = False
            self.is_loading.emit(False)
    def stop(self):
        self.running = False
    
    def reinit_message(self):
        system_message: ChatMessage = ChatMessage(
            role="system",
            content="""You are openscad master, you will help me to generate the 3D model from the prompt.
            I will give you the prompt and you will give me the openscad code.
            Make sure to use the correct syntax and format for the openscad code.
            Dont add any extra information in the code, dont add prefix or suffix to the code.
            please dont provide ```openscad code``` or any other information in the response.
            """
        )
        self.messages.append(system_message)
    
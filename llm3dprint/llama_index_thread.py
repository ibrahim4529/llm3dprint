# from PySide6.QtCore import QThread, Signal, Slot
# from llama_index.core.chat_engine.types import ChatMessage
# from llama_index.llms.ollama import Ollama
# from llama_index.llms.openrouter import OpenRouter
# from llama_index.core.tools import FunctionTool
# from llama_index.core.memory import BaseMemory

# from app_setting import get_setting

# def multify_function(a: int, b: int) -> int:
#     """Multiply two numbers together and return the result"""
#     return a * b

# def create_stl_file(content: str):
#     """This function will create an STL file from the content of the response
#     and will return the path to the file.
#     """
#     with open("output.stl", "w") as f:
#         f.write(content)
    
#     return "output.stl"
    


# class LlamaIndexThread(QThread):
#     """Thread for running LLM API requests"""

#     response_received = Signal(str)
#     setting = get_setting()
#     memory = BaseMemory.from_defaults()

#     @Slot()
#     def prompt_request(self, prompt: str, model: str = "openai/gpt-3.5-turbo"):
#         """Start the thread with a prompt and model selected"""
#         self.prompt = prompt
#         # self.model = OpenRouter(
#         #     model=model,
#         #     api_key=self.setting.get_value("llm_api_key"),
#         # )
#         self.llm = Ollama(
#             model="llama3.1",
#         )
#         self.agent = 
#         self.start()

#     def __init__(self, parent=None):
#         super(LlamaIndexThread, self).__init__(parent)
#         self.running = False
#         self.finished.connect(self.stop)

#     def run(self):
#         self.running = True
#         while self.running:
#             try:
#                 response = self.agent.chat(self.prompt)
#                 self.response_received.emit(response.__str__())
#             except Exception as e:
#                 print(f"Error: {str(e)}")
#                 print(type(e))
#                 self.response_received.emit(f"Error: {str(e)}")
#             self.running = False

#     def stop(self):
#         self.running = False
    
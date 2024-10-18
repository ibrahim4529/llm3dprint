from PySide6.QtCore import QThread, Signal, Slot
from llm_utils import LLMClient
from app_setting import get_setting


class LLMThread(QThread):
    """Thread for running LLM API requests"""

    response_received = Signal(dict)

    @Slot()
    def prompt_request(self, prompt: str):
        self.prompt = prompt
        self.start()

    def __init__(self, parent=None):
        super(LLMThread, self).__init__(parent)
        self.running = False
        self.finished.connect(self.stop)

        setting = get_setting()
        api_key = setting.get_value("llm_api_key")
        base_url = setting.get_value("llm_api_url")
        self.llm_client = LLMClient(api_key, base_url)

    def run(self):
        self.running = True
        while self.running:
            try:
                response = self.llm_client.generate_object_llm(self.prompt)
                self.response_received.emit(response)
            except Exception as e:
                print(f"Error: {str(e)}")
                print(type(e))
                self.response_received.emit(f"Error: {str(e)}")
            self.running = False

    def stop(self):
        self.running = False

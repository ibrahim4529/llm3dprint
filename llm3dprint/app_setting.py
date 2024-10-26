from PySide6.QtCore import QSettings


class AppSetting:
    """Class for application settings management
    This class will be used to manage the application settings using QSettings
    This will initialize the default values for the settings if they are not set
    or if the settings file is not found
    """

    def __init__(self):
        self.settings = QSettings(
            "llm3dprint.ini",
            QSettings.IniFormat
        )
        self.init_default_values()

    def set_value(self, key: str, value):
        self.settings.setValue(key, value)

    def get_value(self, key):
        return self.settings.value(key)

    def remove_value(self, key: str):
        self.settings.remove(key)

    def get_all_keys(self):
        return self.settings.allKeys()

    def clear_all(self):
        self.settings.clear()

    def sync(self):
        self.settings.sync()

    def is_exist(self, key: str) -> bool:
        return self.settings.contains(key)

    def init_default_values(self):
        if not self.is_exist("llm_api_key"):
            self.set_value("llm_api_key", "")
        if not self.is_exist("llm_api_url"):
            self.set_value("llm_api_url", "https://openrouter.ai")
        if not self.is_exist("openrouter_model"):
            self.set_value("openrouter_model", "openai/gpt-3.5-turbo")
        if not self.is_exist("ollama_api_url"):
            self.set_value("ollama_api_url", "http://localhost:11434")
        if not self.is_exist("ollama_model"):
            self.set_value("ollama_model", "llama3.1")
        if not self.is_exist("slicer_app_path"):
            self.set_value("slicer_app_path", "")


def get_setting():
    setting = AppSetting()
    if setting is not None:
        return setting
    else:
        return AppSetting()

from PySide6.QtCore import QSettings


class AppSetting:
    def __init__(self):
        self.settings = QSettings(
            "llm3dprint.ini",
            QSettings.IniFormat
        )

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


def get_setting():
    setting = AppSetting()
    if setting is not None:
        return setting
    else:
        return AppSetting()

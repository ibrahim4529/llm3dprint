from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QMessageBox,
)
from app_setting import get_setting


class SettingDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.resize(400, 300)  # Make the dialog larger

        self.layout = QVBoxLayout()

        # LLM API URL
        self.llm_api_url_label = QLabel("LLM API URL:")
        self.llm_api_url_input = QLineEdit()
        self.layout.addWidget(self.llm_api_url_label)
        self.layout.addWidget(self.llm_api_url_input)

        # LLM API Key
        self.llm_api_key_label = QLabel("LLM API Key:")
        self.llm_api_key_input = QLineEdit()
        self.llm_api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.llm_api_key_label)
        self.layout.addWidget(self.llm_api_key_input)

        # 3D Print Slicer App Path
        self.slicer_app_path_label = QLabel("3D Print Slicer App Path:")
        self.slicer_app_path_input = QLineEdit()
        self.slicer_app_path_button = QPushButton("Select Path")
        self.slicer_app_path_button.clicked.connect(self.select_slicer_app_path)
        self.layout.addWidget(self.slicer_app_path_label)
        self.layout.addWidget(self.slicer_app_path_input)
        self.layout.addWidget(self.slicer_app_path_button)

        # Save Button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_settings)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

        # Load existing settings
        self.load_settings()

    def select_slicer_app_path(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select 3D Print Slicer App")
        if file_path:
            self.slicer_app_path_input.setText(file_path)

    def save_settings(self):
        if not self.validate_inputs():
            return

        setting = get_setting()
        setting.set_value("llm_api_url", self.llm_api_url_input.text())
        setting.set_value("llm_api_key", self.llm_api_key_input.text())
        setting.set_value("slicer_app_path", self.slicer_app_path_input.text())
        setting.sync()
        self.accept()

    def load_settings(self):
        setting = get_setting()
        self.llm_api_url_input.setText(setting.get_value("llm_api_url") or "")
        self.llm_api_key_input.setText(setting.get_value("llm_api_key") or "")
        self.slicer_app_path_input.setText(setting.get_value("slicer_app_path") or "")

    def validate_inputs(self):
        if not self.llm_api_url_input.text().strip():
            QMessageBox.warning(self, "Input Error", "LLM API URL cannot be empty.")
            return False
        if not self.llm_api_key_input.text().strip():
            QMessageBox.warning(self, "Input Error", "LLM API Key cannot be empty.")
            return False
        if not self.slicer_app_path_input.text().strip():
            QMessageBox.warning(
                self, "Input Error", "3D Print Slicer App Path cannot be empty."
            )
            return False
        return True

    def accept(self):
        if self.validate_inputs():
            super().accept()

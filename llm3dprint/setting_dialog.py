from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QMessageBox,
)
from llm3dprint.app_setting import get_setting


class SettingDialog(QDialog):
    """Dialog for application settings
    This dialog will be used to set the application settings
    """

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

        # Ollama API URL
        self.ollama_api_url_label = QLabel("Ollama API URL:")
        self.ollama_api_url_input = QLineEdit()
        self.layout.addWidget(self.ollama_api_url_label)
        self.layout.addWidget(self.ollama_api_url_input)

        # LLM API Key
        self.llm_api_key_label = QLabel("LLM API Key:")
        self.llm_api_key_input = QLineEdit()
        self.llm_api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.llm_api_key_label)
        self.layout.addWidget(self.llm_api_key_input)

        # 3D Print Slicer App Path
        self.slicer_app_path_label = QLabel("3D Print Slicer App Path:")
        self.slicer_app_path_input = QLineEdit()
        self.slicer_app_path_button = QPushButton("Select Slicer App Path")
        self.slicer_app_path_button.clicked.connect(
            self.select_slicer_app_path)
        self.layout.addWidget(self.slicer_app_path_label)
        self.layout.addWidget(self.slicer_app_path_input)
        self.layout.addWidget(self.slicer_app_path_button)

        # Openscad App Path
        self.openscad_app_path_label = QLabel("Openscad App Path:")
        self.openscad_app_path_input = QLineEdit()
        self.openscad_app_path_button = QPushButton("Select Openscad App Path")
        self.openscad_app_path_button.clicked.connect(
            self.select_openscad_app_path)
        self.layout.addWidget(self.openscad_app_path_label)
        self.layout.addWidget(self.openscad_app_path_input)
        self.layout.addWidget(self.openscad_app_path_button)

        # Operouter Model
        self.openrouter_model_label = QLabel("Openrouter Model:")
        self.openrouter_model_input = QLineEdit()
        self.layout.addWidget(self.openrouter_model_label)
        self.layout.addWidget(self.openrouter_model_input)

        # Ollama Model
        self.ollama_model_label = QLabel("Ollama Model:")
        self.ollama_model_input = QLineEdit()
        self.layout.addWidget(self.ollama_model_label)
        self.layout.addWidget(self.ollama_model_input)

        # Save Button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_settings)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

        # Load existing settings
        self.load_settings()

    def select_slicer_app_path(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, "Select 3D Print Slicer App")
        if file_path:
            self.slicer_app_path_input.setText(file_path)

    def select_openscad_app_path(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select Openscad App")
        if file_path:
            self.openscad_app_path_input.setText(file_path)

    def save_settings(self):
        if not self.validate_inputs():
            return

        setting = get_setting()
        setting.set_value("llm_api_url", self.llm_api_url_input.text())
        setting.set_value("llm_api_key", self.llm_api_key_input.text())
        setting.set_value("slicer_app_path", self.slicer_app_path_input.text())
        setting.set_value("openscad_app_path",
                          self.openscad_app_path_input.text())
        setting.set_value("openrouter_model", self.openrouter_model_input.text())
        setting.set_value("ollama_api_url", self.ollama_api_url_input.text())

        setting.sync()
        self.accept()

    def load_settings(self):
        setting = get_setting()
        self.llm_api_url_input.setText(setting.get_value(
            "llm_api_url") or "https://openrouter.ai")
        self.llm_api_key_input.setText(setting.get_value("llm_api_key") or "")
        self.slicer_app_path_input.setText(
            setting.get_value("slicer_app_path") or "")
        self.openscad_app_path_input.setText(
            setting.get_value("openscad_app_path") or "")
        self.openrouter_model_input.setText(
            setting.get_value("openrouter_model") or "")
        self.ollama_api_url_input.setText(setting.get_value(
            "ollama_api_url") or "http://localhost:11434")
        self.ollama_model_input.setText(
            setting.get_value("ollama_model") or "llama3.1")

    def validate_inputs(self):
        if not self.llm_api_url_input.text().strip():
            QMessageBox.warning(self, "Input Error",
                                "LLM API URL cannot be empty.")
            return False
        if not self.llm_api_key_input.text().strip():
            QMessageBox.warning(self, "Input Error",
                                "LLM API Key cannot be empty.")
            return False
        if not self.slicer_app_path_input.text().strip():
            QMessageBox.warning(
                self, "Input Error", "3D Print Slicer App Path cannot be empty."
            )
            return False
        if not self.openscad_app_path_input.text().strip():
            QMessageBox.warning(
                self, "Input Error", "Openscad App Path cannot be empty."
            )
            return False
        if not self.openrouter_model_input.text().strip():
            QMessageBox.warning(
                self, "Input Error", "Operouter Model cannot be empty."
            )
            return False
        if not self.ollama_api_url_input.text().strip():
            QMessageBox.warning(
                self, "Input Error", "Ollama API URL cannot be empty."
            )
            return False
        if not self.ollama_model_input.text().strip():
            QMessageBox.warning(
                self, "Input Error", "Ollama Model cannot be empty."
            )
            return False
        return True

    def accept(self):
        if self.validate_inputs():
            super().accept()

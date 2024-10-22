from PySide6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QWidget,
    QComboBox
)
from llm3dprint.app_setting import get_setting
from llm3dprint.setting_dialog import SettingDialog
from llm3dprint.chat_history import ChatHistory
from llm3dprint.stl_viewer import STLViewer
from llm3dprint.llm_thread import LLMThread


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("LLM3DPrint")
        self.resize(800, 600)
        self.setting = get_setting()
        self.stl_viewer = STLViewer()
        self.llm_thread = LLMThread()
        self.llm_thread.response_received.connect(self.handle_llm_response)
        self.llm_thread.is_loading.connect(self.set_loading_state)
        self.restore_ui()
        self.setup_menu()
        self.setup_ui()
        self.show()

    def closeEvent(self, event):
        self.setting.set_value("geometry", self.geometry())
        self.setting.set_value("windowState", self.saveState())
        self.setting.sync()
        event.accept()

    def setup_ui(self):
        """Setup the user interface for the main window"""
        # Main layout
        main_layout = QVBoxLayout()

        # Model picker layout
        model_picker_layout = QHBoxLayout()
        self.model_picker = QComboBox()
        self.model_picker.addItems(["OpenAI: Shap-e", "OpenAI 4o (openscad)", "OpenAI 4o (stl file content)"])
        self.model_picker.currentIndexChanged.connect(self.model_picker_changed)
        model_picker_layout.addWidget(self.model_picker)


        # Top group layout
        chat_histoty_group = QVBoxLayout()
        top_group = QHBoxLayout()
        top_group.addWidget(self.stl_viewer)
        self.chat_history = ChatHistory()
        chat_histoty_group.addLayout(model_picker_layout)
        chat_histoty_group.addWidget(self.chat_history)
        top_group.addLayout(chat_histoty_group)

        # Bottom group layout
        bottom_group = QHBoxLayout()
        self.input_message = QLineEdit()
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        bottom_group.addWidget(self.input_message)
        bottom_group.addWidget(self.send_button)

        # Add top and bottom groups to main layout
        main_layout.addLayout(top_group)
        main_layout.addLayout(model_picker_layout)
        main_layout.addLayout(bottom_group)

        # Create a central widget and set the main layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def restore_ui(self):
        if self.setting.is_exist("geometry"):
            self.setGeometry(self.setting.get_value("geometry"))
        if self.setting.is_exist("windowState"):
            self.restoreState(self.setting.get_value("windowState"))
        self.setting.sync()

    def setup_menu(self):
        """Setup the menu bar for setting up the application"""
        # make menu bar native window
        self.menuBar().setNativeMenuBar(False)
        self.menu = self.menuBar().addMenu("File")
        self.menu.addAction("Exit", self.close)
        self.menu = self.menuBar().addMenu("Edit")
        self.menu.addAction("Settings", self.show_settings)
        self.menu = self.menuBar().addMenu("Help")
        self.menu.addAction("About", self.show_about)

    def show_settings(self):
        """Craete a dialog to show the settings"""
        dialog = SettingDialog()
        dialog.exec()

    def show_about(self):
        print("Show about")
        setting = get_setting()
        print(setting.get_all_keys())
        for key in setting.get_all_keys():
            print(key, setting.get_value(key))
    
    def send_message(self):
        message = self.input_message.text()
        model = self.model_picker.currentIndex()
        if message:
            self.chat_history.add_user_message(message)
            self.input_message.clear()
            self.llm_thread.prompt_request(message, model)

    def handle_llm_response(self, response):
        if isinstance(response, dict):
            self.chat_history.add_llm_message(response["message"])
            self.stl_viewer.load_stl(response["file_name"])
        else:
            self.chat_history.add_llm_message(response)

    def set_loading_state(self, is_loading):
        self.send_button.setEnabled(not is_loading)
        self.input_message.setEnabled(not is_loading)
        self.send_button.setText("Loading..." if is_loading else "Send")
        if is_loading:
            self.chat_history.add_llm_message("LLM is generating 3D model...")
    
    def model_picker_changed(self, index):
        print(f"Model picker changed: {index}")
        self.chat_history.clean_all_history()
        self.stl_viewer.clear()
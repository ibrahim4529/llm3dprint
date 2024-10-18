from PySide6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QWidget,
)
from app_setting import get_setting
from setting_dialog import SettingDialog
from chat_history import ChatHistory
from stl_viewer import STLViewer
from llm_thread import LLMThread


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("LLM3DPrint")
        self.resize(800, 600)
        self.setting = get_setting()
        self.stl_viewer = STLViewer()
        self.llm_thread = LLMThread()
        self.llm_thread.response_received.connect(self.handle_llm_response)
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
        # Top group layout
        top_group = QHBoxLayout()
        top_group.addWidget(self.stl_viewer)
        self.chat_history = ChatHistory()
        top_group.addWidget(self.chat_history)

        # Bottom group layout
        bottom_group = QHBoxLayout()
        self.input_message = QLineEdit()
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        bottom_group.addWidget(self.input_message)
        bottom_group.addWidget(self.send_button)

        # Add top and bottom groups to main layout
        main_layout.addLayout(top_group)
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
        self.menuBar().setNativeMenuBar(True)
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
        if message:
            self.chat_history.add_user_message(message)
            self.input_message.clear()
            self.llm_thread.prompt_request(message)

    def handle_llm_response(self, response):
        if isinstance(response, dict):
            self.chat_history.add_llm_message(response["message"])
            self.stl_viewer.load_stl(response["file_name"])
        else:
            self.chat_history.add_llm_message(response)
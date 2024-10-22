from PySide6.QtWidgets import QListWidget, QListWidgetItem, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

class ChatHistory(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("QListWidget { background-color: white; }")
        self.setMaximumWidth(400)
        self.setSpacing(10)

    def add_user_message(self, message):
        item = QListWidgetItem(self)
        item_widget = self.create_message_widget(message, QColor(173, 216, 230), Qt.AlignLeft)
        item.setSizeHint(item_widget.sizeHint())
        self.setItemWidget(item, item_widget)

    def add_llm_message(self, message):
        item = QListWidgetItem(self)
        item_widget = self.create_message_widget(message, QColor(144, 238, 144), Qt.AlignRight)
        item.setSizeHint(item_widget.sizeHint())
        self.setItemWidget(item, item_widget)

    def create_message_widget(self, message, color, alignment):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(5, 5, 5, 5)
        
        label = QLabel(message)
        label.setWordWrap(True)
        label.setStyleSheet(f"""
            background-color: {color.name()};
            border-radius: 10px;
            padding: 5px;
        """)
        label.setAlignment(alignment)
        
        layout.addWidget(label)
        
        if alignment == Qt.AlignLeft:
            layout.setAlignment(Qt.AlignLeft)
        else:
            layout.setAlignment(Qt.AlignRight)
        
        return widget

    def clean_all_history(self):
        self.clear()
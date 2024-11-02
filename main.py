import sys
from PySide6.QtWidgets import QApplication
from llm3dprint.main_window import MainWindow


def main():
    app = QApplication([])
    _ = MainWindow()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
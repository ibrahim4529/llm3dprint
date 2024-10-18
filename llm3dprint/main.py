import sys
from PySide6.QtWidgets import QApplication
# from app_setting import get_setting
from main_window import MainWindow


def main():
    app = QApplication([])
    _ = MainWindow()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
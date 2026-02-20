import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

APP_VERSION = "1.3.0"

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("MaFile Manager")
    app.setApplicationVersion(APP_VERSION)
    win = MainWindow(version=APP_VERSION)
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

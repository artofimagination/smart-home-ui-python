import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from gui_main import MainWindow

if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv + ["--no-sandbox"])
    window = MainWindow()

    sys.exit(app.exec_())

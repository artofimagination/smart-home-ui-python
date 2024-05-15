import sys

from PyQt5.QtWidgets import QApplication
from gui_main import MainWindow

if __name__ == "__main__":
    # --no-sandbox is only required when running in docker as root
    app = QApplication(sys.argv + ["--no-sandbox"])
    window = MainWindow()

    sys.exit(app.exec_())

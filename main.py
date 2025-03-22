import sys

from PyQt6.QtWidgets import QApplication
from MediaPlayer import MusiquePlayer

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MusiquePlayer()
    window.show()
    sys.exit(app.exec())

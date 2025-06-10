import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import CompilerUI


def main():
    app = QApplication(sys.argv)
    window = CompilerUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

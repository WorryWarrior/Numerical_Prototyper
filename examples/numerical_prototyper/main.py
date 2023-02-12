import os, sys
from qtpy.QtWidgets import QApplication
from numerical_window import NumericalWindow

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))


def main():
    app = QApplication(sys.argv)

    app.setStyle('Fusion')

    wnd = NumericalWindow()
    # wnd.nodeeditor.addNodes()
    wnd.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

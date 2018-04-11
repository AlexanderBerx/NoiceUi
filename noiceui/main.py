try:
    from PySide2 import QtWidgets
except ImportError:
    from Qt import QtWidgets
import sys
from noiceui.controller import NoiceController


def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = NoiceController()
    controller.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

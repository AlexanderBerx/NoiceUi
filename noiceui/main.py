try:
    from PySide2 import QtWidgets, QtCore
except ImportError:
    from Qt import QtWidgets, QtCore
import os
import sys
from noiceui import constants
from noiceui.controller import NoiceController


def load_resources():
    rsc_file = os.path.join(os.path.split(__file__)[0], constants.RSC_FILE)
    rsc_file = os.path.abspath(rsc_file)
    resources = QtCore.QResource()
    if not resources.registerResource(rsc_file):
        raise RuntimeError('Failed to register resources')

def main():
    app = QtWidgets.QApplication(sys.argv)
    load_resources()
    controller = NoiceController()
    controller.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

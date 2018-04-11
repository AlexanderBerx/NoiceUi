try:
    from PySide2 import QtWidgets, QtCore
except ImportError:
    from Qt import QtWidgets, QtCore

from noiceui.view import NoiceWindow


class NoiceController(QtCore.QObject):
    def __init__(self):
        super(NoiceController, self).__init__()
        self._view = NoiceWindow()
        self._connect_signals()

    def _connect_signals(self):
        self._view.signal_browse_noice_app.connect(self.browse_noice_app)

    @QtCore.Slot()
    def browse_noice_app(self):
        file_, _ = QtWidgets.QFileDialog.getOpenFileName(self._view, 'Set Noice app')
        if file_:
            self._view.set_noice_app(file_)

    def show(self):
        self._view.show()



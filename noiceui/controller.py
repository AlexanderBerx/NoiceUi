try:
    from PySide2 import QtWidgets, QtCore
except ImportError:
    from Qt import QtWidgets, QtCore

from noiceui.view import NoiceWindow
from noiceui.model import NoiceModel

class NoiceController(QtCore.QObject):
    def __init__(self):
        super(NoiceController, self).__init__()
        self._view = NoiceWindow()
        self._model = NoiceModel()

        self._connect_signals()
        self._bind_model()

    def _bind_model(self):
        self._view.set_aov_model(self._model.aov_model)
        self._view.set_input_model(self._model.input_model)

    def _connect_signals(self):
        self._view.signal_browse_noice_app.connect(self.browse_noice_app)
        self._view.signal_reset.connect(self.reset)
        self._view.signal_add_aov.connect(self.add_aov)

    @QtCore.Slot()
    def browse_noice_app(self):
        file_, _ = QtWidgets.QFileDialog.getOpenFileName(self._view, 'Set Noice app')
        if file_:
            self._view.set_noice_app(file_)

    @QtCore.Slot()
    def reset(self):
        # TODO: implement reset functionality
        pass

    @QtCore.Slot()
    def add_aov(self):
        prompt = QtWidgets.QInputDialog(self._view)
        prompt.setWindowTitle('Add AOV')
        prompt.setLabelText('AOV name:')
        prompt.setOkButtonText('Add')
        if prompt.exec_():
            self._model.add_aov(prompt.textValue())

    def show(self):
        self._view.show()


